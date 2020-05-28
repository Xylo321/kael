from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging
import traceback
from datetime import timedelta

from flask import Flask
# 设置APP和SESSION
from flask_session import Session
from redis import StrictRedis

from reborn.db.rdbms import MySQLPool
# 静态文件和模板
from reborn.settings.apps import TEMPLATES_FOLDER, STATIC_FOLDER
from reborn.settings.apps.account import MYSQL_CONFIG as ACCOUNT_MYSQL_CONFIG
from reborn.settings.apps.account import REDIS_CONFIG
from reborn.settings.apps.account import SECRET_KEY
# 数据库
from reborn.settings.apps.blog import MYSQL_CONFIG as BLOG_MYSQL_CONFIG
from reborn.settings.apps.image import MYSQL_CONFIG as IMAGE_MYSQL_CONFIG
from reborn.settings.apps.search import MYSQL_CONFIG as SEARCH_MYSQL_CONFIG
from reborn.settings.apps.video import MYSQL_CONFIG as VIDEO_MYSQL_CONFIG

# ssl key crt file
from reborn.settings import SSL_KEYFILE, SSL_CERTFILE

# 设置MySQL和Redis
REDIS_CLI = StrictRedis(host=REDIS_CONFIG['host'],
                        port=REDIS_CONFIG['port'],
                        db=REDIS_CONFIG['db'],
                        password=REDIS_CONFIG['passwd'],
                        socket_timeout=60,
                        socket_connect_timeout=60,
                        socket_keepalive=True)

ACCOUNT_MYSQL_POOL = MySQLPool(host=ACCOUNT_MYSQL_CONFIG['host'],
                               user=ACCOUNT_MYSQL_CONFIG['user'],
                               passwd=ACCOUNT_MYSQL_CONFIG['passwd'],
                               db=ACCOUNT_MYSQL_CONFIG['db'],
                               size=ACCOUNT_MYSQL_CONFIG['size'])

BLOG_MYSQL_POOL = MySQLPool(host=BLOG_MYSQL_CONFIG['host'],
                            user=BLOG_MYSQL_CONFIG['user'],
                            passwd=BLOG_MYSQL_CONFIG['passwd'],
                            db=BLOG_MYSQL_CONFIG['db'],
                            size=BLOG_MYSQL_CONFIG['size'])

IMAGE_MYSQL_POOL = MySQLPool(host=IMAGE_MYSQL_CONFIG['host'],
                             user=IMAGE_MYSQL_CONFIG['user'],
                             passwd=IMAGE_MYSQL_CONFIG['passwd'],
                             db=IMAGE_MYSQL_CONFIG['db'],
                             size=IMAGE_MYSQL_CONFIG['size'])

VIDEO_MYSQL_POOL = MySQLPool(host=VIDEO_MYSQL_CONFIG['host'],
                             user=VIDEO_MYSQL_CONFIG['user'],
                             passwd=VIDEO_MYSQL_CONFIG['passwd'],
                             db=VIDEO_MYSQL_CONFIG['db'],
                             size=VIDEO_MYSQL_CONFIG['size'])

SEARCH_MYSQL_POOL = MySQLPool(host=SEARCH_MYSQL_CONFIG['host'],
                              user=SEARCH_MYSQL_CONFIG['user'],
                              passwd=SEARCH_MYSQL_CONFIG['passwd'],
                              db=SEARCH_MYSQL_CONFIG['db'],
                              size=SEARCH_MYSQL_CONFIG['size'])

# 设置FLASK
APP = Flask(__name__, static_folder=STATIC_FOLDER,
            template_folder=TEMPLATES_FOLDER)

APP.config.from_mapping(
    SECRET_KEY=SECRET_KEY,
    SEND_FILE_MAX_AGE_DEFAULT=timedelta(seconds=24 * 60 * 60),
    SESSION_TYPE="redis",
    SESSION_REDIS=REDIS_CLI,
    SESSION_KEY_PREFIX="SESSION:",
    # session超时时间
    PERMANENT_SESSION_LIFETIME=timedelta(seconds=60 * 60),
    # MAX_CONTENT_LENGTH=16 * 1024 * 1024
)

Session(APP)

# 蓝图
from reborn.apps.blog.category import BLOG_CATEGORY_BP
from reborn.apps.blog.article import BLOG_ARTICLE_BP
from reborn.apps.blog.home import BLOG_HOME_BP

from reborn.apps.account.user import USER_BP

from reborn.apps.search.index import SEARCH_INDEX_BP

from reborn.apps.image.home import IMAGE_HOME_BP
from reborn.apps.image.category import IMAGE_CATEGORY_BP
from reborn.apps.image.photo import IMAGE_PHOTO_BP

from reborn.apps.video.home import VIDEO_HOME_BP
from reborn.apps.video.category import VIDEO_CATEGORY_BP
from reborn.apps.video.video import VIDEO_VIDEO_BP

# 防火墙
from reborn.apps.gfw.checker import check_request_headers
APP.before_request(check_request_headers)

# 注册蓝图
APP.register_blueprint(USER_BP, url_prefix="/account")

APP.register_blueprint(BLOG_CATEGORY_BP, url_prefix="/blog")
APP.register_blueprint(BLOG_ARTICLE_BP, url_prefix="/blog")
APP.register_blueprint(BLOG_HOME_BP, url_prefix="/blog")

APP.register_blueprint(SEARCH_INDEX_BP, url_prefix="/search")
APP.register_blueprint(SEARCH_INDEX_BP, url_prefix="/")

APP.register_blueprint(IMAGE_HOME_BP, url_prefix="/image")
APP.register_blueprint(IMAGE_CATEGORY_BP, url_prefix="/image")
APP.register_blueprint(IMAGE_PHOTO_BP, url_prefix="/image")

APP.register_blueprint(VIDEO_HOME_BP, url_prefix="/video")
APP.register_blueprint(VIDEO_CATEGORY_BP, url_prefix="/video")
APP.register_blueprint(VIDEO_VIDEO_BP, url_prefix="/video")


def main():
    print(SSL_CERTFILE, SSL_KEYFILE)
    try:
        monkey.patch_all()

        http_server = WSGIServer(('0.0.0.0', 8000), APP, keyfile=SSL_KEYFILE, certfile=SSL_CERTFILE)
        http_server.serve_forever()
    except Exception as e:
        logging.error(e)
    finally:
        try:
            REDIS_CLI.close()
        except:
            logging.error(traceback.format_exc())
        try:
            ACCOUNT_MYSQL_POOL.release()
        except:
            logging.error(traceback.format_exc())
        try:
            BLOG_MYSQL_POOL.release()
        except:
            logging.error(traceback.format_exc())
        try:
            IMAGE_MYSQL_POOL.release()
        except:
            logging.error(traceback.format_exc())
        try:
            VIDEO_MYSQL_POOL.release()
        except:
            logging.error(traceback.format_exc())

        try:
            http_server.close()
        except:
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    import platform
    if 'Linux' in platform.platform():
        main()
    else:
        APP.run(host='0.0.0.0', port=8000, debug=True, ssl_context=(SSL_CERTFILE, SSL_KEYFILE))