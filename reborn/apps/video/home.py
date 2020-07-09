from flask import request, session, redirect, url_for, render_template, Blueprint, abort

from reborn.apps import ACCOUNT_MYSQL_POOL, VIDEO_MYSQL_POOL
from reborn.db.account import User
from reborn.db.video import Video
from reborn.settings.apps.account import IS_LOGIN

VIDEO_HOME_BP = Blueprint('video_home_bp', __name__)


@VIDEO_HOME_BP.route('/home', methods=['GET'])
@VIDEO_HOME_BP.route('/', methods=['GET'])
def home():
    """
    访问视频主页

    GET 请求参数 ?look=xxx&video_title=xxx
    """
    if request.method == 'GET':
        user_id = session.get(IS_LOGIN)
        if user_id is not None:
            look = request.args.get("look")
            video_title = request.args.get("video_title")

            if look:
                user = User(ACCOUNT_MYSQL_POOL)
                vi_user_id = user.get_user_id(look)
                if vi_user_id is not None:
                    context = {}
                    if video_title:
                        video = Video(VIDEO_MYSQL_POOL)
                        if None is not video.get_video(
                                video_title, vi_user_id):
                            context = {
                                "look": look,
                                "back_home": 1,
                                "user_name": look,
                                "video_title": video_title
                            }
                            return render_template(
                                "video/pc/video.html", **context)
                        else:
                            abort(404, '视屏不存在。')
                    else:
                        context = {
                            "look": look,
                            "back_home": 1,
                            "user_name": look
                        }
                        return render_template("video/pc/video.html", **context)
                else:
                    abort(404, '用户不存在。')
            else:
                user = User(ACCOUNT_MYSQL_POOL)
                user_name = user.get_name(user_id)
                context = {
                    "user_name": user_name
                }
                return render_template("video/pc/video.html", **context)
        else:
            look = request.args.get("look")
            video_title = request.args.get("video_title")

            if look:
                user = User(ACCOUNT_MYSQL_POOL)
                user_id = user.get_user_id(look)
                if user_id is not None:
                    if video_title:
                        context = {
                            "look": look,
                            "user_name": look,
                            "video_title": video_title
                        }
                    else:
                        context = {
                            "look": look,
                            "user_name": look
                        }
                    return render_template("video/pc/video.html", **context)
                else:
                    abort(404, '用户不存在。')
            else:
                return redirect(url_for("user_bp.login"))
