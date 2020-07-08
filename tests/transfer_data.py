import logging
import traceback
from collections import deque
from threading import Lock

import pymysql


class MySQLPool:
    _LOCK = Lock()
    _LOGGER = logging.getLogger('MySQLPool')

    def __init__(self, host, user, passwd, db, size):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.size = size
        self.pool = deque()

        self._init_pool()

    def _init_pool(self):
        for i in range(self.size):
            conn = self._get_conn()
            if conn is not None:
                self.pool.append(conn)

    def _get_conn(self):
        try:
            connection = pymysql.connect(host=self.host,
                                         user=self.user,
                                         password=self.passwd,
                                         db=self.db,
                                         charset='utf8mb4',
                                         write_timeout=60,
                                         read_timeout=60,
                                         connect_timeout=60,
                                         # autocommit=True,
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except:
            MySQLPool._LOGGER.error(traceback.format_exc())
            return None

    def get_conn(self):
        with MySQLPool._LOCK:
            try:
                pool_size = len(self.pool)
                i = 0
                while i < pool_size:
                    try:
                        conn = self.pool.popleft()
                        conn.ping()
                        return conn
                    except:
                        MySQLPool._LOGGER.error(traceback.format_exc())
                    finally:
                        i += 1

                raise Exception('连接池已为空')
            except:
                self.release()
                try:
                    self._init_pool()
                except:
                    MySQLPool._LOGGER.error(traceback.format_exc())

                pool_size = len(self.pool)
                i = 0
                while i < pool_size:
                    conn = self.pool.popleft()
                    try:
                        conn.ping()
                        return conn
                    except:
                        MySQLPool._LOGGER.error(traceback.format_exc())
                    finally:
                        i += 1

                raise Exception('我已经尽力了。')

    def back_conn(self, conn):
        with MySQLPool._LOCK:
            self.pool.append(conn)

    def release(self):
        for conn in self.pool:
            try:
                conn.close()
            except:
                MySQLPool._LOGGER.error(traceback.format_exc())

        self.pool.clear()

    def query(self, sql, args):
        conn = None
        try:
            conn = self.get_conn()

            with conn.cursor() as cursor:
                cursor.execute(sql, args)

                return cursor.fetchall()
        except:
            MySQLPool._LOGGER.error(traceback.format_exc())
            MySQLPool._LOGGER.error(sql)
            MySQLPool._LOGGER.error(args)
            conn = None
        finally:
            if conn: self.back_conn(conn)

    def edit(self, sql, args):
        affect_rows = 0
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
            conn.commit()
            affect_rows = conn.affected_rows()
        except:
            MySQLPool._LOGGER.error(traceback.format_exc())
            MySQLPool._LOGGER.error(sql)
            MySQLPool._LOGGER.error(args)
            try:
                conn.rollback()
            except Exception as rollback_err:
                MySQLPool._LOGGER.error('回滚时出现错误: %s', str(rollback_err))

            conn = None
        finally:
            if conn: self.back_conn(conn)
            return affect_rows

    def edit_many(self, sql, many_args):
        affect_rows = 0
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cursor:
                cursor._do_execute_many(sql, many_args)
            conn.commit()
            affect_rows = conn.affected_rows()
        except:
            MySQLPool._LOGGER.error(sql)
            MySQLPool._LOGGER.error(many_args)
            try:
                conn.rollback()
            except Exception as rollback_err:
                MySQLPool._LOGGER.error('回滚时出现错误: %s', str(rollback_err))

            conn = None
        finally:
            if conn: self.back_conn(conn)
            return affect_rows



MYSQL_CONFIG = {
    "host": 'serv_pro',
    "user": "root",
    "passwd": "mm5201314",
    "db": "",
    "size": 1
}


import requests
from requests_toolbelt import MultipartEncoder
from mimetypes import guess_type
import traceback
import os


def upload(upload_url, api_token, third_user_id, category_id, title, file_path, file_name):
    try:
        m = MultipartEncoder(fields={
            'api_key': api_token,
            'category_id': str(category_id),
            'third_user_id': str(third_user_id),
            'title': title,
            'upload_file_name': (file_name, open(file_path, 'rb'), guess_type(file_name)[0] or "application/octet-stream")
        })
        r = requests.post(upload_url, data=m, headers={'Content-Type': m.content_type})
        r.raise_for_status()
        print(r.json())
    except:
        print(traceback.format_exc())


def transfer_data_mdfs():
    msql = MySQLPool(host=MYSQL_CONFIG['host'],
                     user=MYSQL_CONFIG['user'],
                     passwd=MYSQL_CONFIG['passwd'],
                     db=MYSQL_CONFIG['db'],
                     size=MYSQL_CONFIG['size'])
    imgs = msql.query('select user_id, category_id, title, local_url from image.photo', args=())
    vis = msql.query('select user_id, category_id, title, local_url from video.video', args=())
    msql.release()

    api_token = '1a9b365c2b2ec10357d551ef5dbdc8e9'
    upload_url = 'http://serv_pro:15675/file/upload'
    src_folder = '/Volumes/GoodByeUbuntu/reborn'

    for img in imgs:
        print(img)
        third_user_id = img['user_id']
        category_id = img['category_id']
        title = img['title']

        file_path = src_folder + os.path.sep + 'image' + os.path.sep + img['local_url']
        upload(upload_url, api_token, third_user_id, category_id, title, file_path, img['local_url'])

    for video in vis:
        print(video)
        third_user_id = video['user_id']
        category_id = video['category_id']
        title = video['title']

        file_path = src_folder + os.path.sep + 'video' + os.path.sep + video['local_url']

        upload(upload_url, api_token, third_user_id, category_id, title, file_path, video['local_url'])


import logging
logging.basicConfig(level=logging.DEBUG)

transfer_data_mdfs()