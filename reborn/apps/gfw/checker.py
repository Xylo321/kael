"""
网站防火墙
"""
from flask import request, abort

from reborn.utils.http import pc_or_mobile, MOBILE


def check_request_headers():
    """
    检查请求头
    """
    # print(request.headers)
    if not request.headers.has_key('User-Agent'):
        abort(403, '错误的请求头。')

    if request.headers.has_key("User-Agent"):
        ua = request.headers['User-Agent']
        if pc_or_mobile(ua) == MOBILE:
            abort(403, '移动端网站正在建设中。')