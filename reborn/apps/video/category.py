import os

from flask import request, session, Blueprint

from reborn.apps import ACCOUNT_MYSQL_POOL, VIDEO_MYSQL_POOL
from reborn.db.account import User
from reborn.db.video import Category, Video
from reborn.settings.apps.account import IS_LOGIN
from reborn.settings.apps.video import UPLOAD_FOLDER

VIDEO_CATEGORY_BP = Blueprint('video_category_bp', __name__)


@VIDEO_CATEGORY_BP.route('/get_categories', methods=['POST', "GET"])
def get_categories():
    """
    获取用户栏目

    GET 为 未登录用户获取列表
        url请求参数 ?look=xxx
        返回json 成功： {"data": [{"name": xxx}, {"name": xxx}], "status": 1}
                失败: {"data": [], "status": -1}

    POST 为 已登录用户获取列表
        返回json 成功： {"data": [{"name": xxx}, {"name": xxx}], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        user_id = session.get(IS_LOGIN)
        if user_id != None:
            category = Category(VIDEO_MYSQL_POOL)
            categories = category.get_categories(user_id)

            if categories is not None:
                return {
                    "data": categories,
                    "status": 1
                }
            else:
                return {
                    "data": categories,
                    "status": -1
                }
        else:
            return {
                "data": [],
                "status": -1
            }
    elif request.method == 'GET':
        look = request.args.get("look")
        if look and look.strip() != "":
            user = User(ACCOUNT_MYSQL_POOL)
            vi_user_id = user.get_user_id(look)
            if vi_user_id != None:
                category = Category(VIDEO_MYSQL_POOL)
                categories = category.get_categories(vi_user_id)
                if categories is not None:
                    return {
                        "data": categories,
                        "status": 1
                    }
                else:
                    return {
                        "data": categories,
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


@VIDEO_CATEGORY_BP.route('/rename_category', methods=['POST'])
def rename_category():
    """
    重命名用户栏目

    POST 请求form表单 {"old_name": xxx, "new_name": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        old_name = request.form['old_name']
        new_name = request.form['new_name']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            category = Category(VIDEO_MYSQL_POOL)
            result = category.rename_category(old_name, new_name, user_id)
            return {
                "data": [],
                "status": result
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@VIDEO_CATEGORY_BP.route('/del_category', methods=['POST'])
def del_category():
    """
    删除用户栏目

    POST 请求form表单 {"name": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        name = request.form['name']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            category = Category(VIDEO_MYSQL_POOL)
            video = Video(VIDEO_MYSQL_POOL)
            local_urls = video.get_videos(name, user_id)
            for lu in local_urls:
                try:
                    filename = UPLOAD_FOLDER + os.path.sep + lu['local_url']
                    os.remove(filename)
                    print('删除文件成功：', filename)
                except Exception as e:
                    print(e)
                    print('删除文件失败：', filename)

            result = category.del_category(name, user_id)
            return {
                "data": [],
                "status": result
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@VIDEO_CATEGORY_BP.route('/add_category', methods=['POST'])
def add_category():
    """
    增加用户栏目

    POST 请求form表单 {"name": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        name = request.form['name']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            category = Category(VIDEO_MYSQL_POOL)
            result = category.add_category(name, user_id)
            return {
                "data": [],
                "status": result
            }
        else:
            return {
                "data": [],
                "status": -1
            }
