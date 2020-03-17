"""
网站防火墙
"""
from flask import request, abort

from reborn.apps import APP


@APP.before_request
def check_request_headers():
    """
    检查请求头
    """
    # print(request.headers)
    if not request.headers.has_key('User-Agent'):
        abort(403, 'Wrong User-Agent.')