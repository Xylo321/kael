import os
import time

from flask import request, session, Blueprint, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

from reborn.apps import ACCOUNT_MYSQL_POOL, IMAGE_MYSQL_POOL
from reborn.db.account import User
from reborn.db.image import Photo, Category
from reborn.settings.apps.account import IS_LOGIN
from reborn.settings.apps.image import UPLOAD_FOLDER

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
                try:
                    local_url = result[0]
                    filename = UPLOAD_FOLDER + os.path.sep + local_url['local_url']
                    os.remove(filename)
                    print('删除文件成功：', filename)

                    result = photo.delete_photo(title, user_id)

                    return {
                        "data": [],
                        "status": result
                    }
                except OSError as err:
                    print(err)
                    print('删除文件失败：', filename)
            else:
                return {
                    "data": [],
                    "status": -1
                }
        else:
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
                                "local_url": xxx,
                                "remote_url": xxx
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
                                "local_url": xxx,
                                "remote_url" xxx
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
                return {
                    "data": result,
                    "status": 1
                }
            else:
                return {
                    "data": [],
                    "status": -1
                }
        else:
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
                    return {
                        "data": result,
                        "status": 1
                    }
                else:
                    return {
                        "data": [],
                        "status": -1
                    }
            else:
                return {
                    "data": [],
                    "status": -1
                }
        else:
            return {
                "data": [],
                "status": -1
            }


@IMAGE_PHOTO_BP.route('/pag_photo', methods=['POST', 'GET'])
def pag_photo():
    """
    图片分页

    GET 获取未登录用户的图片列表
        url参数 ?look=xxx
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "local_url": xxx, "remote_url": xxx, "date": xxx}],
                                "status": 1}
                失败: {"data": [], "status": -1}


    POST 获取已登录用户的图片列表
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "local_url": xxx, "remote_url": xxx, "date": xxx}]
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
                return {
                    "data": result,
                    "status": 1
                }
            else:
                return {
                    "data": [],
                    "status": -1
                }
        else:
            return {
                "data": [],
                "status": -1
            }

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
                    return {
                        "data": result,
                        "status": 1
                    }
                else:
                    return {
                        "data": [],
                        "status": -1
                    }
            else:
                return {
                    "data": [],
                    "status": -1
                }
        else:
            return {
                "data": [],
                "status": -1
            }


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
                return {
                    "data": [],
                    "status": -1
                }

            category = Category(IMAGE_MYSQL_POOL)

            if -1 == category.exist(category_name, user_id):
                return {
                    "data": [],
                    "status": -1
                }

            if 'upload_file_name' not in request.files:
                return {
                    "data": [],
                    "status": -1
                }

            file = request.files['upload_file_name']

            if file.filename == '':
                return {
                    "data": [],
                    "status": -1
                }
            filename = str(time.time()) + '_' + secure_filename(file.filename)
            if file and _allowed_file(file.filename):
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                return {
                    "data": [],
                    "status": -1
                }

            if 1 == photo.add_photo(title, category_name, filename, user_id):
                return {
                    "data": [],
                    "status": 1
                }
            return {
                "data": [],
                "status": -1
            }
        else:
            return redirect(url_for("user_bp.login"))


@IMAGE_PHOTO_BP.route('/view_photo/<filename>', methods=['GET'])
def view_photo(filename):
    if request.method == 'GET':
        return send_from_directory(UPLOAD_FOLDER, filename)


@IMAGE_PHOTO_BP.route('/update_photo', methods=['POST'])
def update_photo():
    """
    更新图片

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

            if 1 == photo.exist(new_title, user_id) and src_title != new_title or -1 == photo.exist(src_title, user_id):
                return {
                    "data": [],
                    "status": -1
                }

            category = Category(IMAGE_MYSQL_POOL)

            if -1 == category.exist(category_name, user_id):
                return {
                    "data": [],
                    "status": -1
                }

            if 'upload_file_name' not in request.files:
                return {
                    "data": [],
                    "status": -1
                }

            file = request.files['upload_file_name']

            if file.filename == '':
                # 更新图片标题，时间，分类
                result = photo.update_photo(user_id, src_title, new_title, category_name)
                return {
                    "data": [],
                    "status": result
                }
            else:
                # 删除老图片，更新标题，时间，分类，local_url，保存新图片
                img = photo.get_photo(src_title, user_id)
                local_url = img[0]['local_url']
                os.remove(UPLOAD_FOLDER + os.path.sep + local_url)

                # 保存新图片
                filename = str(time.time()) + '_' + secure_filename(file.filename)
                if file and _allowed_file(file.filename):
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    result = photo.update_photo(user_id, src_title, new_title, category_name, filename)
                    return {
                        "data": [],
                        "status": result
                    }
                else:
                    return {
                        "data": [],
                        "status": -1
                    }
        else:
            return redirect(url_for("user_bp.login"))
