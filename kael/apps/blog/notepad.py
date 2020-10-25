import base64
from flask import request, render_template, Blueprint, session, redirect, url_for
from kael.settings.apps.account import IS_LOGIN

BLOG_NOTEPAD_BP = Blueprint('blog_notepad_bp', __name__)


@BLOG_NOTEPAD_BP.route('/notepad', methods=['GET'])
def notepad():
    """
    访问便利工具

    GET 请求参数 ?url='https://www.baidu.com
    """
    if request.method == 'GET':
        user_id = session.get(IS_LOGIN)
        if user_id is None:
            return redirect(url_for("user_bp.login"))

        url = ''
        try:
            url = base64.standard_b64decode(request.args.get('url').encode()).decode()
        except: pass
        context = {
            'url': url
        }
        return render_template("blog/pc/notepad.html", **context)