from flask import request, session, redirect, url_for, render_template, Blueprint, abort

from reborn import apps
from reborn_db.account import User
from reborn_db.blog import Article
from reborn.settings.apps.account import IS_LOGIN
from reborn.utils.http import pc_or_mobile, PC, MOBILE

BLOG_HOME_BP = Blueprint('blog_home_bp', __name__)


@BLOG_HOME_BP.route('/home', methods=['GET'])
@BLOG_HOME_BP.route('/', methods=['GET'])
def home():
    """
    访问博客主页

    GET 请求参数 ?look=xxx&article_title=xxx
    """
    if request.method == 'GET':
        user_id = session.get(IS_LOGIN)
        # 是否已经登录
        if user_id != None:  # 是
            # 从url参数中取出 look 和 article_title
            look = request.args.get("look")
            article_title = request.args.get("article_title")

            # 是否 look 为 空 或者 不在 url参数中
            if look:  # 是
                user = User(apps.ACCOUNT_MYSQL_POOL)
                # 根据 look 查询出 look 用户名的 user_id
                vi_user_id = user.get_user_id(look)

                # 判断 当前用户名 的 用户id是否存在
                if vi_user_id != None:  # 存在
                    context = {};
                    if article_title:
                        article = Article(apps.BLOG_MYSQL_POOL)
                        if None != article.get_article(article_title, vi_user_id):
                            context = {
                                "look": look,
                                "back_home": 1,
                                "user_name": look,
                                "article_title": article_title
                            }
                            if PC == pc_or_mobile(request.headers['User-Agent']):
                                return render_template("blog/pc/blog.html", **context)
                            else:
                                abort(403, "移动端网站正在建设中。")

                        else:
                            abort(404, 'Article does not exist.')
                    else:
                        context = {
                            "look": look,
                            "back_home": 1,
                            "user_name": look
                        }

                        if pc_or_mobile(request.headers['User-Agent']) == PC:
                            return render_template("blog/pc/blog.html", **context)
                        else:
                            abort(403, "移动端网站正在建设中。")

                else:  # 不存在
                    abort(404, 'User does not exist.')
            else:  # 否
                user = User(apps.ACCOUNT_MYSQL_POOL)
                user_name = user.get_name(user_id)
                context = {
                    "user_name": user_name
                }
                if pc_or_mobile(request.headers['User-Agent']) == PC:
                    return render_template("blog/pc/blog.html", **context)
                else:
                    abort(403, "移动端网站正在建设中。")

        else:  # 否
            look = request.args.get("look")
            article_title = request.args.get("article_title")

            if look:
                user = User(apps.ACCOUNT_MYSQL_POOL)
                user_id = user.get_user_id(look)
                if user_id != None:
                    if article_title:
                        article = Article(apps.BLOG_MYSQL_POOL)
                        if None != article.get_article(article_title, user_id):
                            context = {
                                "look": look,
                                "user_name": look,
                                "article_title": article_title
                            }
                            if pc_or_mobile(request.headers['User-Agent']) == PC:
                                return render_template("blog/pc/blog.html", **context)
                            else:
                                abort(403, "移动端网站正在建设中。")

                        else:
                            abort(404, 'Article does not exist.')
                    else:
                        context = {
                            "look": look,
                            "user_name": look
                        }
                        if pc_or_mobile(request.headers['User-Agent']) == PC:
                            return render_template("blog/pc/blog.html", **context)
                        else:
                            abort(403, "移动端网站正在建设中。")

                else:
                    abort(404, 'User does not exist.')
            else:
                return redirect(url_for("user_bp.login"))
