import os
import time

from flask import request, session, Blueprint, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

from reborn.apps import ACCOUNT_MYSQL_POOL, VIDEO_MYSQL_POOL
from reborn.db.account import User
from reborn.db.video import Video, Category
from reborn.settings.apps.account import IS_LOGIN
from reborn.settings.apps.video import UPLOAD_FOLDER

VIDEO_VIDEO_BP = Blueprint('video_video_bp', __name__)


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'flv'}


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
                try:
                    print(result)
                    local_url = result[0]
                    filename = UPLOAD_FOLDER + os.path.sep + local_url['local_url']
                    os.remove(filename)
                    print('删除文件成功：', filename)
                except OSError as err:
                    print(err)
                    print('删除文件失败：', filename)

                result = video.delete_video(title, user_id)

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

                video = Video(VIDEO_MYSQL_POOL)
                result = video.get_video(title, vi_user_id)
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
                video = Video(VIDEO_MYSQL_POOL)
                result = video.pag_video(page, category_name, vi_user_id)

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
                return {
                    "data": [],
                    "status": -1
                }

            category = Category(VIDEO_MYSQL_POOL)

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

            if 1 == video.add_video(title, category_name, filename, description, user_id):
                return {
                    "data": [],
                    "status": 1
                }
            else:
                return {
                    "data": [],
                    "status": -1
                }
        else:
            return redirect(url_for("user_bp.login"))


@VIDEO_VIDEO_BP.route('/view_video/<filename>', methods=['GET'])
def view_video(filename):
    if request.method == 'GET':
        return send_from_directory(UPLOAD_FOLDER, filename)


@VIDEO_VIDEO_BP.route('/view_video_1_img/<filename>', methods=['GET'])
def view_video_1_img():
    if request.method == 'GET':
        # 读取视频的第一帧
        # 封装成图片流，发送给客户端
        pass

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
            src_title = request.form['src_title']
            new_title = request.form['new_title']
            category_name = request.form['category_name']
            description = request.form['description']

            video = Video(VIDEO_MYSQL_POOL)

            if 1 == video.exist(new_title, user_id) and src_title != new_title or -1 == video.exist(src_title, user_id):
                return {
                    "data": [],
                    "status": -1
                }

            category = Category(VIDEO_MYSQL_POOL)

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
                # 更新视频标题，时间，分类
                result = video.update_video(user_id, src_title, new_title, category_name, description)
                return {
                    "data": [],
                    "status": result
                }
            else:
                # 删除老视频，更新标题，时间，分类，local_url，保存新视频
                img = video.get_video(src_title, user_id)
                local_url = img[0]['local_url']
                try:
                    os.remove(UPLOAD_FOLDER + os.path.sep + local_url)
                except FileNotFoundError:
                    pass

                # 保存新视频
                filename = str(time.time()) + '_' + secure_filename(file.filename)
                if file and _allowed_file(file.filename):
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    result = video.update_video(user_id, src_title, new_title, category_name, description, filename)
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
