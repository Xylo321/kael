from flask import request, session, redirect, url_for, render_template, Blueprint, abort

from kael.apps import ACCOUNT_MYSQL_POOL, BLOG_MYSQL_POOL
from kael.db.account import User
from kael.db.blog import Article
from kael.settings.apps.account import IS_LOGIN
from kael.utils.http import pc_or_mobile, PC, MOBILE

BLOG_NOTEPAD_BP = Blueprint('blog_notepad_bp', __name__)


@BLOG_NOTEPAD_BP.route('/notepad', methods=['GET'])
def notepad():
    """
    访问便利工具

    GET 请求参数 ?url='https://www.baidu.com
    """
    if request.method == 'GET':
        context = {
            'url': request.args.get('url', '')
        }
        return render_template("blog/pc/notepad.html", **context)