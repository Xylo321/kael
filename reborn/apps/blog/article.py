from flask import request, session, Blueprint

from reborn import ACCOUNT_MYSQL_POOL
from reborn import BLOG_MYSQL_POOL
from reborn.db.account import User
from reborn.db.blog import Article
from reborn.settings.apps.account import IS_LOGIN

BLOG_ARTICLE_BP = Blueprint('blog_article_bp', __name__)


@BLOG_ARTICLE_BP.route('/del_article', methods=['POST'])
def del_article():
    """
    删除文章

    POST 请求form表单 {"title": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        title = request.form['title']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            article = Article(BLOG_MYSQL_POOL)
            result = article.delete_article(title, user_id)
            return {
                "data": [],
                "status": result
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@BLOG_ARTICLE_BP.route('/add_article', methods=['POST'])
def add_article():
    """
    增加文章

    POST 请求form表单 {"title": xxx, "category_name": xxx, "content" xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        title = request.form['title']
        category_name = request.form['category_name']
        content = request.form['content']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            article = Article(BLOG_MYSQL_POOL)
            result = article.add_article(title, category_name, content, user_id)
            return {
                "data": [],
                "status": result
            }
        else:
            return {
                "data": [],
                "status": -1
            }


@BLOG_ARTICLE_BP.route('/pag_article', methods=['POST', 'GET'])
def pag_article():
    """
    文章分页

    GET 获取未登录用户的文章列表
        url参数 ?look=xxx
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "date": xxx}, {"name": xxx, "date": xxx}], "status": 1}
                失败: {"data": [], "status": -1}


    POST 获取已登录用户的文章列表
        请求form表单 {"page": 1, "category_name": xxx}
        返回json 成功: {"data": [{"title": xxx, "date": xxx}, {"name": xxx, "date": xxx}], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        page = int(request.form['page'])
        category_name = request.form['category_name']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            article = Article(BLOG_MYSQL_POOL)
            result = article.pag_article(page, category_name, user_id)
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
                article = Article(BLOG_MYSQL_POOL)
                result = article.pag_article(page, category_name, vi_user_id)

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
        else:
            return {
                "data": [],
                "status": -1
            }


@BLOG_ARTICLE_BP.route('/get_article', methods=['POST', 'GET'])
def get_article():
    """
    获取文章内容

    GET 获取未登录用户
        url参数 ?look=xxx
        返回json 成功: {"data": [{"title": xxx, "date": xxx, "content": xxx, "category_name": xxx}], "status": 1}
        失败: {"data": [], "status": -1}

    POST 获取已登录用户
        请求form表单 {"title": xxx}
        返回json 成功: {"data": [{"title": xxx, "date": xxx, "content": xxx, "category_name": xxx}], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        title = request.form['title']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            article = Article(BLOG_MYSQL_POOL)
            result = article.get_article(title, user_id)
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
                title = request.args.get('title')

                article = Article(BLOG_MYSQL_POOL)
                result = article.get_article(title, vi_user_id)
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
        else:
            return {
                "data": [],
                "status": -1
            }


@BLOG_ARTICLE_BP.route('/update_article', methods=['POST'])
def update_article():
    """
    修改文章内容

    POST 请求form表单 {"src_title": xxx, "new_title", xxx, "category_name": xxx, "content": xxx}
        返回json 成功: {"data": [], "status": 1}
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        src_title = request.form['src_title']
        new_title = request.form['new_title']
        category_name = request.form['category_name']
        content = request.form['content']

        user_id = session.get(IS_LOGIN)
        if user_id != None:
            article = Article(BLOG_MYSQL_POOL)
            result = article.update_article(src_title, new_title,
                                            category_name, content, user_id)
            return {
                "data": [],
                "status": result
            }
        else:
            return {
                "data": [],
                "status": -1
            }
