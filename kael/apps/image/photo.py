import os
import time
import traceback

from flask import request, session, Blueprint, redirect, url_for
from werkzeug.utils import secure_filename

from kael.apps import ACCOUNT_MYSQL_POOL, IMAGE_MYSQL_POOL
from kael.db.account import User
from kael.db.image import Photo, Category
from kael.settings.apps import CACHE_DIR, MDFS_API_KEY, MDFS_DOWNLOAD_URL, MDFS_EDIT_URL, MDFS_UPLOAD_URL, \
    MDFS_DOWNLOAD_MANY_URL, MDFS_DELETE_URL
from kael.settings.apps.account import IS_LOGIN
from kael.utils.mdfs import download as mdfs_download, upload as mdfs_upload, download_many as mdfs_download_many, \
    edit as mdfs_edit, delete as mdfs_delete

IMAGE_PHOTO_BP = Blueprint('image_photo_bp', __name__)


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'jfif'}


@IMAGE_PHOTO_BP.route('/del_photo', methods=['POST'])
def del_photo():
    """
    删除图片

    POST 请求form表单 {"title": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        title = request.form['title']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            photo = Photo(IMAGE_MYSQL_POOL)
            result = photo.get_photo(title, user_id)
            if result:
                third_user_id = user_id
                category_id = result[0]['category_id']
                title = result[0]['title']
                date = result[0]['date']
                category_name = result[0]['category_name']
                try:
                    if 0 == mdfs_delete(MDFS_DELETE_URL, MDFS_API_KEY, third_user_id, category_id, title):
                        return {"data": [], "status": -1}
                    result = photo.delete_photo(title, user_id)
                    return {"data": [], "status": result}
                except:
                    print(traceback.format_exc())
            return {"data": [], "status": -1}
        return redirect(url_for("user_bp.login"))


@IMAGE_PHOTO_BP.route('/get_photo', methods=['POST', 'GET'])
def get_photo():
    """
    获取单个图片

    POST 请求form表单 {"title": xxx}
        返回json 成功: {"data":
                            [{
                                "title": xxx,
                                "date": xxx,
                                "category_name": xxx,
                                "url": xxx,
                            }],
                            "status": 1
                        }
                失败: {"data": [], "status": -1}

    GET url参数 /get_photo?look=xxx
        请求form表单 {"title": xxx}
        返回json 成功: {"data":
                            [{
                                "title": xxx,
                                "date": xxx,
                                "category_name": xxx,
                                "url": xxx,
                            }],
                            "status": 1
                        }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        title = request.form['title']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            photo = Photo(IMAGE_MYSQL_POOL)
            result = photo.get_photo(title, user_id)
            if result:
                third_user_id = user_id
                category_id = result[0]['category_id']
                title = result[0]['title']
                date = result[0]['date']
                category_name = result[0]['category_name']
                url = None
                try:
                    url = mdfs_download(MDFS_DOWNLOAD_URL, MDFS_API_KEY, third_user_id, category_id, title)
                except:
                    pass

                if url is None: return {"data": [], "status": -1}
                result = [{'title': title, 'date': date, 'category_name': category_name, 'url': url}]
                return {"data": result, "status": 1}
        return redirect(url_for("user_bp.login"))
    elif request.method == "GET":
        look = request.args.get("look")
        if look and look.strip() != "":
            user = User(ACCOUNT_MYSQL_POOL)
            vi_user_id = user.get_user_id(look)
            if vi_user_id != None:
                title = request.args.get('title')

                photo = Photo(IMAGE_MYSQL_POOL)
                result = photo.get_photo(title, vi_user_id)
                if result is not None:
                    third_user_id = vi_user_id
                    category_id = result[0]['category_id']
                    title = result[0]['title']
                    date = result[0]['date']
                    category_name = result[0]['category_name']
                    expire = 9000
                    url = None
                    try:
                        url = mdfs_download(MDFS_DOWNLOAD_URL, MDFS_API_KEY, third_user_id, category_id, title, expire)
                    except Exception as e:
                        print(e)
                    if url is None:
                        return {"data": [], "status": -1}
                    result = [{'title': title, 'date': date, 'category_name': category_name, 'url': url}]
                    return {"data": result, "status": 1}
                return {"data": [], "status": -1}

    return redirect(url_for("user_bp.login"))


@IMAGE_PHOTO_BP.route('/pag_photo', methods=['POST', 'GET'])
def pag_photo():
    """
    图片分页

    GET 获取未登录用户的图片列表
        url参数 ?look=xxx
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "url": xxx, "date": xxx}],
                                "status": 1}
                失败: {"data": [], "status": -1}


    POST 获取已登录用户的图片列表
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "date": xxx, 'url': xxx, 'category_name': xxx}]
                                "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        page = int(request.form['page'])
        category_name = request.form['category_name']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            photo = Photo(IMAGE_MYSQL_POOL)
            result = photo.pag_photo(page, category_name, user_id)
            if result is not None:
                req_data = []
                for row in result:
                    title = row['title']
                    category_id = row['category_id']
                    req_data.append({
                        'third_user_id': user_id,
                        'category_id': category_id,
                        'title': title,
                        'expire': 9000
                    })
                res_data = mdfs_download_many(MDFS_DOWNLOAD_MANY_URL, MDFS_API_KEY, req_data)
                if res_data is None:
                    return {"data": [], "status": -1}

                response_data = []
                for row in result:
                    for res_d in res_data:
                        if row['title'] == res_d['title'] and str(row['category_id']) == str(res_d['category_id']) \
                                and str(user_id) == str(res_d['third_user_id']):
                            response_data.append({
                                'category_name': row['category_name'],
                                'url': res_d.get('url', None),
                                'title': row['title'],
                                'date': row['date']
                            })
                            break
                return {"data": response_data, "status": 1}
        return redirect(url_for("user_bp.login"))

    elif request.method == "GET":
        look = request.args.get("look")
        if look and look.strip() != "":
            user = User(ACCOUNT_MYSQL_POOL)
            vi_user_id = user.get_user_id(look)
            if vi_user_id != None:
                page = int(request.args.get('page'))
                category_name = request.args.get('category_name')
                photo = Photo(IMAGE_MYSQL_POOL)
                result = photo.pag_photo(page, category_name, vi_user_id)

                if result is not None:
                    req_data = []
                    for row in result:
                        title = row['title']
                        category_id = row['category_id']
                        req_data.append({
                            'third_user_id': vi_user_id,
                            'category_id': category_id,
                            'title': title,
                            'expire': 60
                        })
                    res_data = mdfs_download_many(MDFS_DOWNLOAD_MANY_URL, MDFS_API_KEY, req_data)
                    if res_data is None:
                        return {"data": [], "status": -1}

                    response_data = []
                    for row in result:
                        for res_d in res_data:
                            if row['title'] == res_d['title'] and str(row['category_id']) == str(res_d['category_id']) \
                                    and str(vi_user_id) == str(res_d['third_user_id']):
                                response_data.append({
                                    'category_name': row['category_name'],
                                    'url': res_d['url'],
                                    'title': row['title'],
                                    'date': row['date']
                                })
                                break
                    return {"data": response_data, "status": 1}
        return redirect(url_for("user_bp.login"))


@IMAGE_PHOTO_BP.route('/upload', methods=['POST'])
def upload():
    """
    增加图片

    POST 请求form表单 {"title": xxx, "category_name": xxx, “upload_file_name": xxx}
         返回json 成功: {"data": [], "status": 1}
         返回json 失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        user_id = session.get(IS_LOGIN)

        if user_id != None:
            title = request.form['title']
            category_name = request.form['category_name']

            photo = Photo(IMAGE_MYSQL_POOL)

            if 1 == photo.exist(title, user_id):
                return {"data": [], "status": -1}

            category = Category(IMAGE_MYSQL_POOL)

            category_id = category.get_category_id(category_name, user_id)
            if category_id is None:
                return {"data": [], "status": -1}

            if 'upload_file_name' not in request.files:
                return {"data": [], "status": -1}

            file = request.files['upload_file_name']
            if file.filename == '':
                return {"data": [], "status": -1}

            filename = str(time.time()) + '_' + secure_filename(file.filename)
            file_extension = ''
            fn_list = filename.rsplit('.', 1)
            if len(fn_list) > 1:
                file_extension = fn_list[1]

            if file and _allowed_file(file.filename):
                file_path = os.path.join(CACHE_DIR, filename)
                file.save(file_path)
                status = mdfs_upload(MDFS_UPLOAD_URL, MDFS_API_KEY, user_id, category_id, title, filename, file_path)
                if status == 0:
                    return {"data": [], "status": -1}
            else:
                return {"data": [], "status": -1}

            if 1 == photo.add_photo(title, category_name, file_extension, user_id):
                return {"data": [], "status": 1}
            return {"data": [], "status": -1}
        return redirect(url_for("user_bp.login"))


@IMAGE_PHOTO_BP.route('/update_photo', methods=['POST'])
def update_photo():
    """更新图片

    POST 请求form表单 {"src_title": xxx, "new_title": xxx, "category_name": xxx, "upload_file_name": xxx}
         返回json 成功: {"data": [], "status": 1}
         返回json 失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        user_id = session.get(IS_LOGIN)

        if user_id != None:
            src_title = request.form['src_title']
            new_title = request.form['new_title']
            category_name = request.form['category_name']

            photo = Photo(IMAGE_MYSQL_POOL)

            src_photo_id = photo.get_photo_id(src_title, user_id)
            new_photo_id = photo.get_photo_id(new_title, user_id)
            if src_photo_id != new_photo_id:
                if src_photo_id is None:
                    return {"data": [], "status": -1}

            category = Category(IMAGE_MYSQL_POOL)
            category_id = category.get_category_id(category_name, user_id)
            if category_id is None:
                return {"data": [], "status": -1}

            if 'upload_file_name' not in request.files:
                return {"data": [], "status": -1}
            file = request.files['upload_file_name']

            src_img = photo.get_photo(src_title, user_id)
            if src_img is None:
                return {"data": [], "status": 0}

            if file.filename == '':
                # 更新图片标题，时间，分类
                src_third_user_id = user_id
                src_category_id = src_img[0]['category_id']
                src_file_extension = src_img[0]['file_extension']
                new_third_user_id = user_id
                new_category_id = category_id
                new_file_extension = src_file_extension
                try:
                    if 0 == mdfs_edit(MDFS_EDIT_URL, MDFS_API_KEY, src_third_user_id, src_category_id, src_title,
                                      src_file_extension,
                                      new_third_user_id, new_category_id, new_title, new_file_extension,
                                      upload_file_name=None, upload_file_path=None):
                        return {"data": [], "status": -1}
                except:
                    print('文件在mdfs上修改失败')
                    return {"data": [], "status": -1}

                result = photo.update_photo(user_id, src_title, new_title, category_name)

                return {"data": [], "status": result}
            else:
                filename = str(time.time()) + '_' + secure_filename(file.filename)
                new_file_extension = ''
                fn_list = filename.rsplit('.', 1)
                if len(fn_list) == 2:
                    new_file_extension = fn_list[1]

                file_path = os.path.join(CACHE_DIR, filename)
                if file and _allowed_file(file.filename):
                    file.save(file_path)

                    src_third_user_id = user_id
                    src_category_id = src_img[0]['category_id']
                    src_file_extension = src_img[0]['file_extension']
                    new_third_user_id = user_id
                    new_category_id = category_id
                    try:
                        if 0 == mdfs_edit(MDFS_EDIT_URL, MDFS_API_KEY, src_third_user_id, src_category_id, src_title,
                                          src_file_extension,
                                          new_third_user_id, new_category_id, new_title, new_file_extension,
                                          upload_file_name=filename, upload_file_path=file_path):
                            return {"data": [], "status": -1}
                    except:
                        print('文件转存失败')
                        return {"data": [], "status": -1}
                    finally:
                        os.remove(file_path)

                    result = photo.update_photo(user_id, src_title, new_title, category_name)
                    return {"data": [], "status": result}
                else:
                    return {"data": [], "status": -1}
        return redirect(url_for("user_bp.login"))