"""
分类
"""
import json

from flask import request, session, Blueprint, redirect, url_for

from reborn.apps import ACCOUNT_MYSQL_POOL, IMAGE_MYSQL_POOL
from reborn.db.account import User
from reborn.db.image import Category, Photo
from reborn.settings.apps.account import IS_LOGIN
from reborn.apps import MINGMQ_POOL_CATEGORY
from reborn.settings.apps import MINGMQ_CONFIG
from mingmq.message import FAIL


IMAGE_CATEGORY_BP = Blueprint('image_category_bp', __name__)


@IMAGE_CATEGORY_BP.route('/get_categories', methods=['POST', "GET"])
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
        if user_id is not None:
            category = Category(IMAGE_MYSQL_POOL)
            categories = category.get_categories(user_id)

            if categories is not None:
                return {"data": categories, "status": 1}
        return redirect(url_for("user_bp.login"))

    elif request.method == 'GET':
        look = request.args.get("look")
        if look and look.strip() != "":
            user = User(ACCOUNT_MYSQL_POOL)
            vi_user_id = user.get_user_id(look)
            if vi_user_id is not None:
                category = Category(IMAGE_MYSQL_POOL)
                categories = category.get_categories(vi_user_id)
                if categories is not None:
                    return {"data": categories, "status": 1}
        return redirect(url_for("user_bp.login"))


@IMAGE_CATEGORY_BP.route('/rename_category', methods=['POST'])
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
        if user_id is not None:
            category = Category(IMAGE_MYSQL_POOL)
            result = category.rename_category(old_name, new_name, user_id)
            return {"data": [], "status": result}
        return redirect(url_for("user_bp.login"))


@IMAGE_CATEGORY_BP.route('/del_category', methods=['POST'])
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
        if user_id is not None:
            category = Category(IMAGE_MYSQL_POOL)
            category_id = category.get_category_id(name, user_id)
            if category_id is None:
                return {"data": [], "status": -1}

            message_data = json.dumps({
                'user_id': user_id,
                'category_id': category_id,
                'db_name': 'image'
            })
            mq_res = MINGMQ_POOL_CATEGORY.opera("send_data_to_queue",
                                                *(MINGMQ_CONFIG['delete_category']['queue_name'], message_data))
            if mq_res and mq_res['status'] == FAIL:
                print('推送删除栏目消息到消息队列失败', message_data)
                return {"data": [], "status": -1}

            result = category.del_category(name, user_id)
            return {"data": [], "status": result}
        return redirect(url_for("user_bp.login"))


@IMAGE_CATEGORY_BP.route('/add_category', methods=['POST'])
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
        if user_id is not None:
            category = Category(IMAGE_MYSQL_POOL)
            result = category.add_category(name, user_id)
            return {"data": [], "status": result}
        return redirect(url_for("user_bp.login"))