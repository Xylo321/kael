import os
import time

from flask import request, session, Blueprint, send_from_directory, redirect, url_for, send_file

from reborn.apps import ACCOUNT_MYSQL_POOL, VIDEO_MYSQL_POOL
from reborn.db.account import User
from reborn.db.video import Video, Category
from reborn.settings.apps.account import IS_LOGIN
from reborn.settings.apps import CACHE_DIR
from reborn.settings.apps import MDFS_DOWNLOAD_URL, MDFS_API_KEY, MDFS_UPLOAD_URL, MDFS_EDIT_URL, MDFS_DELETE_URL
from reborn.utils.mdfs import download as mdfs_download, upload as mdfs_upload, edit as mdfs_edit, delete as mdfs_delete

VIDEO_VIDEO_BP = Blueprint('video_video_bp', __name__)


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'mp4'}


@VIDEO_VIDEO_BP.route('/del_video', methods=['POST'])
def del_video():
    """
    删除视频

    POST 请求form表单 {"title": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        title = request.form['title']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            video = Video(VIDEO_MYSQL_POOL)

            result = video.get_video(title, user_id)
            if result:
                category_id = result[0]['category_id']
                if 0 == mdfs_delete(MDFS_DELETE_URL, MDFS_API_KEY, user_id, category_id, title):
                    return {"data": [], "status": -1}
                return {"data": [], "status": video.delete_video(title, user_id)}
            return {"data": [], "status": -1}
        return redirect(url_for("user_bp.login"))


@VIDEO_VIDEO_BP.route('/get_video', methods=['POST', 'GET'])
def get_video():
    """
    获取单个视频

    POST 请求form表单 {"title": xxx}
        返回json 成功: {"data":
                            [{
                                "title": xxx,
                                "date": xxx,
                                "category_name": xxx,
                                "local_url": xxx,
                                "remote_url": xxx,
                                "description": xxx
                            }],
                            "status": 1
                        }
                失败: {"data": [], "status": -1}

    GET url参数 /get_video?look=xxx
        请求form表单 {"title": xxx}
        返回json 成功: {"data":
                            [{
                                "title": xxx,
                                "date": xxx,
                                "category_name": xxx,
                                "local_url": xxx,
                                "remote_url" xxx,
                                "description": xxx
                            }],
                            "status": 1
                        }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        title = request.form['title']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            video = Video(VIDEO_MYSQL_POOL)
            result = video.get_video(title, user_id)
            if result:
                title = result[0]['title']
                category_id = result[0]['category_id']
                third_user_id = user_id
                expire = 9000
                url = mdfs_download(MDFS_DOWNLOAD_URL, MDFS_API_KEY, third_user_id, category_id, title, expire)
                if url is None:
                    return {"data": [],"status": -1}
                result[0]['url'] = url
                return {"data": result, "status": 1}
            return {"data": [], "status": -1}
        return redirect(url_for("user_bp.login"))
    elif request.method == "GET":
        look = request.args.get("look")
        if look and look.strip() != "":
            user = User(ACCOUNT_MYSQL_POOL)
            vi_user_id = user.get_user_id(look)
            if vi_user_id != None:
                title = request.args.get('title')

                video = Video(VIDEO_MYSQL_POOL)
                result = video.get_video(title, vi_user_id)
                if result is not None:
                    title = result[0]['title']
                    category_id = result[0]['category_id']
                    third_user_id = vi_user_id
                    expire = 9000
                    url = mdfs_download(MDFS_DOWNLOAD_URL, MDFS_API_KEY, third_user_id, category_id, title, expire)
                    if url is None:
                        return {"data": [], "status": -1}
                    result[0]['url'] = url
                    return {"data": result, "status": 1}
        return redirect(url_for("user_bp.login"))


@VIDEO_VIDEO_BP.route('/pag_video', methods=['POST', 'GET'])
def pag_video():
    """
    视频分页

    GET 获取未登录用户的视频列表
        url参数 ?look=xxx
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "local_url": xxx, "remote_url": xxx, "date": xxx, "description": xxx}],
                                "status": 1}
                失败: {"data": [], "status": -1}


    POST 获取已登录用户的视频列表
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "local_url": xxx, "remote_url": xxx, "date": xxx, "description": xxx}]
                                "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        page = int(request.form['page'])
        category_name = request.form['category_name']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            video = Video(VIDEO_MYSQL_POOL)
            result = video.pag_video(page, category_name, user_id)
            if result is not None:
                return {"data": result, "status": 1}
        return redirect(url_for("user_bp.login"))
    elif request.method == "GET":
        look = request.args.get("look")
        if look and look.strip() != "":
            user = User(ACCOUNT_MYSQL_POOL)
            vi_user_id = user.get_user_id(look)
            if vi_user_id != None:
                page = int(request.args.get('page'))
                category_name = request.args.get('category_name')
                video = Video(VIDEO_MYSQL_POOL)
                result = video.pag_video(page, category_name, vi_user_id)

                if result is not None:
                    return {"data": result, "status": 1}
        return redirect(url_for("user_bp.login"))


@VIDEO_VIDEO_BP.route('/upload', methods=['POST'])
def upload():
    """
    增加视频

    POST 请求form表单 {"title": xxx, "category_name": xxx, "upload_file_name": xxx, "description": xxx}
         返回json 成功: {"data": [], "status": 1}
         返回json 失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        user_id = session.get(IS_LOGIN)

        if user_id != None:
            title = request.form['title']
            category_name = request.form['category_name']
            description = request.form['description']

            video = Video(VIDEO_MYSQL_POOL)
            if 1 == video.exist(title, user_id):
                return {"data": [], "status": -1}

            category = Category(VIDEO_MYSQL_POOL)
            category_id = category.get_category_id(category_name, user_id)
            if category_id is None:
                return {"data": [], "status": -1}

            if 'upload_file_name' not in request.files:
                return {"data": [], "status": -1}
            file = request.files['upload_file_name']
            if file.filename == '':
                return {"data": [], "status": -1}
            filename = str(time.time()) + '_' + file.filename
            file_extension = filename.rsplit('.', 1)
            if len(file_extension) == 2:
                file_extension = file_extension[1]
            else:
                file_extension = ''
            file_path = os.path.join(CACHE_DIR, filename)
            if file is None or not _allowed_file(file.filename):
                return {"data": [], "status": -1}
            # 心里痛苦，只能上传mp4吧，上传其它格式直接拒绝算了。flv有时候也有问题
            # if get_video_type(file_path) not in ['mp4', 'flv']: 这里mp4也有问题，mp4文件居然不能获取到
            # 开源项目有时候还真是靠不住，如果这不能控制，就只能靠用户自己去控制自己的内容了。
            #     # 有时候，客户端改变文件扩展名上传文件，我这里直接检测文件二进制里的头
            #     # try:
            #     #     if convert_mp4(file_path, file_path + '.mp4'):
            #     #         filename += '.mp4'
            #     # except:
            #     #     return {
            #     #         "data": [],
            #     #         "status": -1
            #     #     }
            #     # finally:
            #     os.remove(file_path)
            #
            #     return {
            #         "data": [],
            #         "status": -1
            #     }
            try:
                file.save(file_path)
            except:
                print('保存文件失败', file_path)
                return {"data": [], "status": -1}
            try:
                if mdfs_upload(MDFS_UPLOAD_URL, MDFS_API_KEY, user_id, category_id, title, filename, file_path) != 1:
                    return {"data": [], "status": -1}
            except:
                print('上传到mdfs失败', request.form)
                return  {"data": [], "status": -1}
            finally:
                try:
                    os.remove(file_path)
                except:
                    print('删除文件失败')
            if 1 == video.add_video(title, category_name, file_extension, description, user_id):
                return {"data": [],"status": 1}
            return {"data": [], "status": -1}
        return redirect(url_for("user_bp.login"))


@VIDEO_VIDEO_BP.route('/update_video', methods=['POST'])
def update_video():
    """
    更新视频

    POST 请求form表单 {"src_title": xxx, "new_title": xxx, "category_name": xxx, "upload_file_name": xxx， "description": xxx}
         返回json 成功: {"data": [], "status": 1}
         返回json 失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        user_id = session.get(IS_LOGIN)

        if user_id != None:
            category = Category(VIDEO_MYSQL_POOL)
            video = Video(VIDEO_MYSQL_POOL)

            src_title = request.form['src_title']
            new_title = request.form['new_title']
            category_name = request.form['category_name']
            description = request.form['description']

            ss = video.get_category_id_file_extension_by_title(src_title, user_id)
            new_category_id = category.get_category_id(category_name, user_id)
            src_third_user_id = new_third_user_id = user_id

            # 新，或者旧的分类不存在，或者新的标题存在video且新旧标题不相同，错误
            if ss is None or new_category_id is None or src_title != new_title and video.exist(new_title, user_id) == 1:
                return {"data": [],"status": -1}
            src_category_id = ss[0]['category_id']
            src_file_extension = ss[0]['file_extension']

            if 'upload_file_name' not in request.files:
                return {"data": [], "status": -1}

            file = request.files['upload_file_name']
            if file is not None and file.filename == '':
                if 0 == mdfs_edit(MDFS_EDIT_URL, MDFS_API_KEY, src_third_user_id, src_category_id, src_title, src_file_extension,
                                  new_third_user_id, new_category_id, new_title, src_file_extension):
                    return {"data": [], "status": -1}
                result = video.update_video(user_id, src_title, new_title, category_name, description, src_file_extension)
                return {"data": [], "status": result}
            else:
                filename = str(time.time()) + '_' + file.filename
                new_file_extension = filename.rsplit('.', 1)
                if len(new_file_extension) == 2:
                    new_file_extension = new_file_extension[1]
                else:
                    new_file_extension = ''

                if file and _allowed_file(file.filename):
                    file_path = os.path.sep.join([CACHE_DIR, filename])
                    try:
                        file.save(file_path)
                    except:
                        print('保存文件失败')
                        return {"data": [], "status": -1}
                    try:
                        if 0 == mdfs_edit(MDFS_EDIT_URL, MDFS_API_KEY, src_third_user_id, src_category_id, src_title, src_file_extension,
                                          new_third_user_id, new_category_id, new_title, new_file_extension, filename, file_path):
                            return {"data": [], "status": -1}
                    except:
                        print('上传mdfs失败', request.form)
                        return {"data": [], "status": -1}
                    finally:
                        try:
                            os.remove(file_path)
                        except:
                            print('删除文件失败', file_path)
                    result = video.update_video(user_id, src_title, new_title, category_name, description, new_file_extension)
                    return {"data": [], "status": result}
                return {"data": [], "status": -1}
        return redirect(url_for("user_bp.login"))