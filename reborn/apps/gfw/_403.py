"""
网站防火墙
"""
from flask import request, abort

from reborn.apps import APP


@APP.before_request
def refuse_not_pc():
    """
    禁止非pc代理访问
    """
    # print(request.headers)
    user_agent = request.headers.get("User-Agent")
    if "Android" in user_agent \
            or "iPhone" in user_agent \
            or "MicroMessenger" in user_agent:
        abort(403, "Does not support mobile phones.")
