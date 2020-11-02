from flask import Blueprint, render_template, session, request, abort, redirect, url_for

from kael.apps import ACCOUNT_MYSQL_POOL
from kael.apps import SEARCH_MYSQL_POOL
from kael.db.account import User
from kael.db.search import ArticleSearch, ImageSearch, VideoSearch
from kael.settings.apps.account import IS_LOGIN
from kael.utils.http import pc_or_mobile, PC, MOBILE
from kael.settings.apps import MDFS_API_KEY, MDFS_DOWNLOAD_MANY_URL, MDFS_GET_MANY_VIDEO_FIRST_PHOTO_URL
from kael.utils.mdfs import (download_many as mdfs_download_many,
                             get_many_video_first_photo as mdfs_get_many_video_first_photo)

SEARCH_INDEX_BP = Blueprint('search_index_bp', __name__)


@SEARCH_INDEX_BP.route('/', methods=['GET'])
@SEARCH_INDEX_BP.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        user_id = session.get(IS_LOGIN, None)
        if user_id != None:
            user = User(ACCOUNT_MYSQL_POOL)
            user_name = user.get_name(user_id)
            if user_name is not None:
                context = {"user_name": user_name}
                if pc_or_mobile(request.headers['User-Agent']) == PC:
                    return render_template("search/pc/index.html", **context)
                return render_template("search/pc/index.html")
            else:
                print('user_id不为none，但是user_name为none', user_id, user_name)
                session.pop(IS_LOGIN)
                if pc_or_mobile(request.headers['User-Agent']) == PC:
                    return redirect(url_for('user_bp.login'))
                abort(403, '移动端网站暂时不支持。')
        else:
            if pc_or_mobile(request.headers['User-Agent']) == PC:
                return render_template("search/pc/index.html")
            abort(403, '移动端网站暂时不支持。')


@SEARCH_INDEX_BP.route('/search_article', methods=['POST'])
def search_article():
    """
    搜索文章

    POST 请求form表单 {"key_word", xxx, "page": xxx, "type": xxx}
        返回json 成功 {
                        "data": [
                                    {"id": xxx, "title": xxx, "date": xxx, "category_name": xxx}
                                ],
                        "status": 1
                    }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        key_word = request.form['key_word']

        page = int(request.form['page'])
        type = int(request.form['type'])
        article_search = ArticleSearch(SEARCH_MYSQL_POOL)
        result = article_search.search(key_word, page, type)

        if result != None:
            return {"data": result, "status": 1}
        return {"data": [], "status": -1}


@SEARCH_INDEX_BP.route('/search_article_total_page', methods=['POST'])
def search_article_total_page():
    """
    获取搜索文章的总页数

    POST 请求form表单 {"key_word", xxx, "type": xxx}
        返回json 成功 {
                        "data": [
                                    {"total_page": xxx}
                                ],
                        "status": 1
                    }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        key_word = request.form['key_word']
        type = int(request.form['type'])
        article_search = ArticleSearch(SEARCH_MYSQL_POOL)
        total_page = article_search.search_total_pages(key_word, type)

        if total_page != None:
            return {"data": [{"total_page": total_page}], "status": 1}
        return {"data": [], "status": -1}


@SEARCH_INDEX_BP.route('/go_article_page', methods=['GET'])
def go_article_page():
    """
    去文章页面

    GET url请求参数 ?article_id=xxx&article_title=xxx&type=xxx
    """
    if request.method == 'GET':
        article_id = request.args.get('article_id')
        article_title = request.args.get('article_title')
        type = int(request.args.get('type'))
        if article_id != None and article_title != None:
            article_search = ArticleSearch(SEARCH_MYSQL_POOL)
            user_id = article_search.get_article_uid(article_id, type)
            if user_id != None:
                user = User(ACCOUNT_MYSQL_POOL)
                look = user.get_name(user_id)
                if look != None:
                    return redirect(url_for('blog_home_bp.home',
                                            look=look, article_title=article_title
                                            ))
        abort(404)


@SEARCH_INDEX_BP.route('/search_image', methods=['POST'])
def search_image():
    """
    搜索图片

    POST 请求form表单 {"key_word", xxx, "page": xxx, "type": xxx}
        返回json 成功 {
                        "data": [
                                    {"id": xxx, "title": xxx, "local_url": xxx, "remote_url": xxx}
                                ],
                        "status": 1
                    }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        key_word = request.form['key_word']

        page = int(request.form['page'])
        type = int(request.form['type'])
        image_search = ImageSearch(SEARCH_MYSQL_POOL)
        result = image_search.search(key_word, page, type)

        if result != None:
            req_data = []
            for row in result:
                user_id = row['user_id']
                title = row['title']
                category_id = row['category_id']
                req_data.append({
                    'third_user_id': user_id,
                    'category_id': category_id,
                    'title': title,
                    'expire': 9000
                })
            res_data = mdfs_download_many(MDFS_DOWNLOAD_MANY_URL, MDFS_API_KEY, req_data)
            if res_data is None:
                return {"data": [], "status": -1}

            response_data = []
            for row in result:
                for res_d in res_data:
                    if row['title'] == res_d['title'] and str(row['category_id']) == str(res_d['category_id']) \
                            and str(user_id) == str(res_d['third_user_id']):
                        response_data.append({
                            'category_name': row['category_name'],
                            'url': res_d.get('url', None),
                            'title': row['title'],
                            'id': row['id'],
                        })
                        break

            return {"data": response_data, "status": 1}
            # return {'data': result, 'status': 1}
        return {"data": [], "status": -1}


@SEARCH_INDEX_BP.route('/search_image_total_page', methods=['POST'])
def search_image_total_page():
    """
    获取搜索图片的总页数

    POST 请求form表单 {"key_word", xxx, "type": xxx}
        返回json 成功 {
                        "data": [
                                    {"total_page": xxx}
                                ],
                        "status": 1
                    }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        key_word = request.form['key_word']
        type = int(request.form['type'])
        image_search = ImageSearch(SEARCH_MYSQL_POOL)
        total_page = image_search.search_total_pages(key_word, type)

        if total_page != None:
            return {"data": [{"total_page": total_page}], "status": 1}
        return {"data": [], "status": -1}


@SEARCH_INDEX_BP.route('/go_image_page', methods=['GET'])
def go_image_page():
    """
    去文章页面

    GET url请求参数 ?photo_id=xxx&photo_title=xxx
    """
    if request.method == 'GET':
        photo_id = request.args.get('photo_id')
        photo_title = request.args.get('photo_title')
        if photo_id != None and photo_title != None:
            image_search = ImageSearch(SEARCH_MYSQL_POOL)
            user_id = image_search.get_image_uid(photo_id)
            if user_id != None:
                user = User(ACCOUNT_MYSQL_POOL)
                look = user.get_name(user_id)
                if look != None:
                    return redirect(url_for('image_home_bp.home',
                                            look=look, photo_title=photo_title
                                            ))
        abort(404)


@SEARCH_INDEX_BP.route('/search_video', methods=['POST'])
def search_video():
    """
    搜索视频

    POST 请求form表单 {"key_word", xxx, "page": xxx, "type": xxx}
        返回json 成功 {
                        "data": [
                                    {"id": xxx, "title": xxx, "local_url": xxx, "remote_url": xxx}
                                ],
                        "status": 1
                    }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        key_word = request.form['key_word']

        page = int(request.form['page'])
        type = int(request.form['type'])
        video_search = VideoSearch(SEARCH_MYSQL_POOL)
        result = video_search.search(key_word, page, type)

        if result != None:
            """[{'category_id': 27,
                  'category_name': 'UNIX',
                  'id': 22,
                  'title': '20_文件的查找',
                  'user_id': 4},
                ]
            """
            req_data = []
            for row in result:
                user_id = row['user_id']
                title = row['title']
                category_id = row['category_id']
                req_data.append({
                    'third_user_id': user_id,
                    'category_id': category_id,
                    'title': title,
                    'expire': 9000
                })
            res_data = mdfs_get_many_video_first_photo(MDFS_GET_MANY_VIDEO_FIRST_PHOTO_URL, MDFS_API_KEY, req_data)
            if res_data is None:
                return {"data": [], "status": -1}

            response_data = []
            for row in result:
                for res_d in res_data:
                    if row['title'] == res_d['title'] and str(row['category_id']) == str(res_d['category_id']) \
                            and str(user_id) == str(res_d['third_user_id']):
                        response_data.append({
                            'category_name': row['category_name'],
                            'url': res_d.get('url', None),
                            'title': row['title'],
                            'id': row['id'],
                        })
                        break

            return {"data": response_data, "status": 1}
        return {"data": [], "status": -1}


@SEARCH_INDEX_BP.route('/search_video_total_page', methods=['POST'])
def search_video_total_page():
    """
    获取搜索视频的总页数

    POST 请求form表单 {"key_word", xxx, "type": xxx}
        返回json 成功 {
                        "data": [
                                    {"total_page": xxx}
                                ],
                        "status": 1
                    }
                失败: {"data": [], "status": -1}
    """
    if request.method == 'POST':
        key_word = request.form['key_word']
        type = int(request.form['type'])
        video_search = VideoSearch(SEARCH_MYSQL_POOL)
        total_page = video_search.search_total_pages(key_word, type)

        if total_page != None:
            return {"data": [{"total_page": total_page}], "status": 1}
        return {"data": [], "status": -1}


@SEARCH_INDEX_BP.route('/go_video_page', methods=['GET'])
def go_video_page():
    """
    去视频页面

    GET url请求参数 ?video_id=xxx&video_title=xxx
    """
    if request.method == 'GET':
        video_id = request.args.get('video_id')
        video_title = request.args.get('video_title')
        if video_id != None and video_title != None:
            video_search = VideoSearch(SEARCH_MYSQL_POOL)
            user_id = video_search.get_video_uid(video_id)
            if user_id != None:
                user = User(ACCOUNT_MYSQL_POOL)
                look = user.get_name(user_id)
                if look != None:
                    return redirect(url_for('video_home_bp.home',
                                            look=look, video_title=video_title
                                            ))
        abort(404)