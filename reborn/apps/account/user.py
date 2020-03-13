import random

from flask import request, session, redirect, url_for, render_template, Blueprint

from reborn.apps import ACCOUNT_MYSQL_POOL
from reborn.db.account import User
from reborn.settings.apps.account import IS_LOGIN, MAIL_CONFIG
from reborn.utils.email import send_text_email

USER_BP = Blueprint('user_bp', __name__)


@USER_BP.route('/login', methods=['GET', 'POST'])
def login():
    """
    登陆

    GET 不需要带任何请求参数，直接返回登陆页面

    POST
        请求form表单: {"name": xxx, "passwd": xxx}

        返回json: 成功 {"data": [], "status": 1}
                  失败 {"data": [], "status": -1}
    """
    if request.method == 'GET':
        if session.get(IS_LOGIN):
            return redirect(url_for("search_index_bp.index"))
        else:
            return render_template("account/login.html")
    elif request.method == 'POST':
        user = User(ACCOUNT_MYSQL_POOL)
        user_id = user.login(request.form['name'], request.form['passwd'])
        if user_id != None:
            session[IS_LOGIN] = user_id
            return {
                "data": [],
                "status": 1
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@USER_BP.route('/check_name_email', methods=['POST'])
def check_name_email():
    """
    检查账号或邮箱是否存在

    POST 请求form表单 {"name": xxx, "email": xxx}
         返回json 已注册: {"data": [], "status": 1}
                 未注册: {"data": [], "status": -1}
    """
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        user = User(ACCOUNT_MYSQL_POOL)
        result = user.existOr(name, email)
        if result == 1:
            return {
                "data": [],
                "status": 1
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@USER_BP.route('/logout', methods=['GET'])
def logout():
    """
    登出

    GET 请求form表单为空
        返回json 成功:  {"data": [], "status": 1}
                失败：{"data": [], "status": -1}
    """
    if request.method == 'GET':
        user_id = session.get(IS_LOGIN)
        if user_id != None:
            session.pop(IS_LOGIN)
            return {
                "data": [],
                "status": 1
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@USER_BP.route('/forget_password', methods=['POST', 'GET'])
def forget_password():
    """
    忘记密码

    GET 返回忘记密码页面
    POST 请求form表单 {"name": xxx,
                      "email": xxx,
                      "check_code": xxx,
                      "new_passwd": xxx }
         返回json  成功: {"data": [], "status": 1}
                  失败 {"data": [], "status": -1}
    """
    if request.method == 'GET':
        return render_template('account/forget_password.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        check_code = request.form['check_code']
        new_passwd = request.form['new_passwd']
        if session.get(email) != check_code:
            return {
                "data": [],
                "status": -1
            }
        else:
            user = User(ACCOUNT_MYSQL_POOL)
            result = user.forget_password(name, email, new_passwd)
            if result == 1:
                session.pop(email)

                return {
                    "data": [],
                    "status": 1
                }
            else:
                return {
                    "data": [],
                    "status": -1
                }


@USER_BP.route('/send_check_code', methods=['POST'])
def send_check_code():
    """
    发送邮箱验证码

    POST 请求form表单 {"email": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        to = request.form['email']
        rand_n = random.randint(100000, 1000000)
        result = send_text_email(MAIL_CONFIG['host'], MAIL_CONFIG['port'],
                                 MAIL_CONFIG['username'], MAIL_CONFIG['password'],
                                 MAIL_CONFIG['username'], [to], "验证码",
                                 MAIL_CONFIG['username'], to,
                                 MAIL_CONFIG['forget_password_msg'] % rand_n)
        if result == 1:
            session[to] = str(rand_n)
            return {
                "data": [],
                "status": 1
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@USER_BP.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册

    GET 返回注册页面
    POST 请求form表单 {"name": xxx, "passwd": xxx
                      "email": xxx, "check_code": xxx}
         返回json 成功：{"data": [], "status": 1}
                 失败: {"data": [], "status": -1}
    """
    if request.method == 'GET':
        return render_template('account/register.html')
    elif request.method == 'POST':
        name = request.form['name']
        passwd = request.form['passwd']
        email = request.form['email']
        check_code = request.form['check_code']
        if session.get(email) != check_code:
            return {
                "data": [],
                "status": -1
            }
        else:
            user = User(ACCOUNT_MYSQL_POOL)
            result = user.register(name, passwd, email)
            if result == 1:
                session.pop(email)
                return {
                    "data": [],
                    "status": 1
                }
            else:
                return {
                    "data": [],
                    "status": -1
                }
