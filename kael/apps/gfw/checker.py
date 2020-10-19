"""
网站防火墙
"""
from flask import request, abort, session

from kael.utils.http import pc_or_mobile, MOBILE


def check_request_headers():
    """检查请求头
    """
    # print(request.headers)
    if not request.headers.has_key('User-Agent'):
        abort(403, '错误的请求头。')

    if request.headers.has_key("User-Agent"):
        ua = request.headers['User-Agent']
        if pc_or_mobile(ua) == MOBILE:
            abort(403, '移动端网站正在建设中。')


def let_browser_cache_fonts(response):
    """让浏览器缓存字体
    """
    if request.path in [
        "/static/common/font/WawaTC-Regular.otf",
        "/static/common/font/Monaco.ttf",
        "/static/common/font/WawaSC-Regular.otf"]:
        response.headers['Cache-Control'] = "max-age=31536000"
    return response


def fix_media_file_set_cookie(response):
    """XXX: 服务器返回图片这种都要设置cookie，我觉得没必要，这也许是flask的bug。
    """
    for media_path in ['/video/view_video/', '/video/view_video_1_img/', '/image/view_photo/']:
        if media_path in request.path:
            session.modified = False
            break

    return response