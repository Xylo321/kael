from flask import request, session, redirect, url_for, render_template, Blueprint, abort

from reborn import ACCOUNT_MYSQL_POOL, IMAGE_MYSQL_POOL
from reborn.db.account import User
from reborn.db.image import Photo
from reborn.settings.apps.account import IS_LOGIN
from reborn.utils.http import pc_or_mobile, PC, MOBILE

IMAGE_HOME_BP = Blueprint('image_home_bp', __name__)


@IMAGE_HOME_BP.route('/home', methods=['GET'])
@IMAGE_HOME_BP.route('/', methods=['GET'])
def home():
    """
    访问图片主页

    GET 请求参数 ?look=xxx&photo_title=xxx
    """
    if request.method == 'GET':
        user_id = session.get(IS_LOGIN)
        if user_id != None:
            look = request.args.get("look")
            photo_title = request.args.get("photo_title")

            if look:
                user = User(ACCOUNT_MYSQL_POOL)
                vi_user_id = user.get_user_id(look)
                if vi_user_id != None:
                    context = {};
                    if photo_title:
                        photo = Photo(IMAGE_MYSQL_POOL)
                        if None != photo.get_photo(photo_title, vi_user_id):
                            context = {
                                "look": look,
                                "back_home": 1,
                                "user_name": look,
                                "photo_title": photo_title
                            }
                            if pc_or_mobile(request.headers['User-Agent']) == PC:
                                return render_template("image/pc/image.html", **context)
                            else:
                                abort(403, "移动端网站正在建设中。")
                        else:
                            abort(404, 'Photo does not exist.')
                    else:
                        context = {
                            "look": look,
                            "back_home": 1,
                            "user_name": look
                        }
                        if pc_or_mobile(request.headers['User-Agent']) == PC:
                            return render_template("image/pc/image.html", **context)
                        else:
                            abort(403, '移动端网站正在建设中。')
                else:
                    abort(404, 'User does not exist.')
            else:
                user = User(ACCOUNT_MYSQL_POOL)
                user_name = user.get_name(user_id)
                context = {
                    "user_name": user_name
                }
                if pc_or_mobile(request.headers['User-Agent']) == PC:
                    return render_template("image/pc/image.html", **context)
                else:
                    abort(403, '移动端网站正在建设中。')
        else:
            look = request.args.get("look")
            photo_title = request.args.get("photo_title")

            if look:
                user = User(ACCOUNT_MYSQL_POOL)
                user_id = user.get_user_id(look)
                if user_id != None:
                    if photo_title:
                        context = {
                            "look": look,
                            "user_name": look,
                            "photo_title": photo_title
                        }
                    else:
                        context = {
                            "look": look,
                            "user_name": look
                        }
                    if pc_or_mobile(request.headers['User-Agent']) == PC:
                        return render_template("image/pc/image.html", **context)
                    else:
                        abort(403, '移动端网站正在建设中。')
                else:
                    abort(404, 'User does not exist.')
            else:
                return redirect(url_for("user_bp.login"))
