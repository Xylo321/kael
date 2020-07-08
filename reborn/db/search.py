import math

from reborn.db import MySQLBase
from reborn.settings.apps.search import ROBOT, HUMAN


class ArticleSearch(MySQLBase):
    def  search(self, key_word, page, type):
        sql = None
        if type == ROBOT:
            if len(key_word) == 0:
                sql = (
                    "select A.id, A.title, left(A.content, 100) content, A.date, B.name as category_name, A.url from blog.article A "
                    "inner join blog.category B on A.category_id = B.id "
                    "where "
                    "A.user_id = 0 "
                    "order by A.date desc limit %s, 10")
            else:
                sql = (
                    "select A.id, A.title, left(A.content, 100) content, A.date, B.name as category_name, A.url from blog.article A "
                    "inner join blog.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id "
                    "where (match(A.content, A.title) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) "
                    "and A.user_id = 0 "
                    "order by A.date desc limit %s, 10")
                print(sql)
        if type == HUMAN:
            if len(key_word) == 0:
                sql = (
                    "select A.id, A.title, left(A.content, 100) content, A.date, B.name as category_name, A.url from blog.article A "
                    "inner join blog.category B on A.category_id = B.id "
                    "where "
                    "A.user_id != 0 "
                    "order by A.date desc limit %s, 10")
            else:
                sql = (
                    "select A.id, A.title, left(A.content, 100) content, A.date, B.name as category_name, A.url from blog.article A "
                    "inner join blog.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id "
                    "where (match(A.content, A.title) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) "
                    "and A.user_id != 0 "
                    "order by A.date desc limit %s, 10")

        if sql != None:
            args = (key_word, key_word, key_word, (page - 1) * 10)
            if len(key_word) == 0:
                args = ((page - 1) * 10,)

            result = self.rdbms_pool.query(sql, args)
            if result != None and len(result) != 0:
                return result
            else:
                return None
        else:
            raise Exception("type不合法的类型")

    def search_total_pages(self, key_word, type):
        sql = None
        if type == HUMAN:
            if len(key_word) == 0:
                sql = ("select count(A.id) total_page from blog.article A "
                       "inner join blog.category B on A.category_id = B.id "
                       "where A.user_id != 0")
            else:
                sql = ("select count(A.id) total_page from blog.article A "
                       "inner join blog.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id "
                       "where (match(A.content, A.title) against(%s in natural language mode) "
                       "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) "
                       "and A.user_id != 0")
        if type == ROBOT:
            if len(key_word) == 0:
                sql = ("select count(A.id) total_page from blog.article A "
                       "inner join blog.category B on A.category_id = B.id "
                       "where A.user_id = 0")
            else:
                sql = ("select count(A.id) total_page from blog.article A "
                       "inner join blog.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id "
                       "where (match(A.content, A.title) against(%s in natural language mode) "
                       "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) "
                       "and A.user_id = 0")
        if sql != None:
            args = (key_word, key_word, key_word)

            if len(key_word) == 0:
                args = ()

            result = self.rdbms_pool.query(sql, args)
            if result != None and len(result) != 0:
                total_page = result[0]['total_page']
                # print(total_page, math.ceil(total_page / 10))
                return math.ceil(total_page / 10)
            else:
                return None
        else:
            raise Exception("type不合法的类型")

    def get_article_uid(self, article_id):
        sql = "select user_id from blog.article where id = %s"
        args = (article_id,)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['user_id']
        else:
            return None


class ImageSearch(MySQLBase):
    def search(self, key_word, page, type):
        sql = None
        if type == ROBOT:
            if len(key_word) == 0:
                sql = "select A.id, A.title, A.local_url, A.remote_url, B.name as category_name from image.photo A " \
                      "inner join image.category B on A.category_id = B.id " \
                      "where " \
                      "A.user_id = 0 " \
                      "order by A.date desc limit %s, 6"
            else:
                sql = "select A.id, A.title, A.local_url, A.user_id, B.name as category_name from image.photo A " \
                      "inner join image.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id = 0 " \
                      "order by A.date desc limit %s, 6"
        if type == HUMAN:
            if len(key_word) == 0:
                sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from image.photo A " \
                      "inner join image.category B on A.category_id = B.id " \
                      "where " \
                      "A.user_id != 0 " \
                      "order by A.date desc limit %s, 6"
            else:
                sql = "select A.id, A.title, A.local_url, A.remote_url, B.name as category_name from image.photo A " \
                      "inner join image.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id != 0 " \
                      "order by A.date desc limit %s, 6"

        if sql != None:
            args = (key_word, key_word, key_word, (page - 1) * 6)
            if len(key_word) == 0:
                args = ((page - 1) * 6,)

            result = self.rdbms_pool.query(sql, args)
            if result != None and len(result) != 0:
                return result
            else:
                return None
        else:
            raise Exception("type不合法的类型")

    def search_total_pages(self, key_word, type):
        sql = None
        if type == HUMAN:
            if len(key_word) == 0:
                sql = "select count(A.id) total_page from image.photo A " \
                      "inner join image.category B on A.category_id = B.id " \
                      "where A.user_id != 0"
            else:
                sql = "select count(A.id) total_page from image.photo A " \
                      "inner join image.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title) against(%s in natural language mode) " \
                      "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id != 0"
        if type == ROBOT:
            if len(key_word) == 0:
                sql = "select count(A.id) total_page from image.photo A " \
                      "inner join image.category B on A.category_id = B.id " \
                      "where A.user_id = 0"
            else:
                sql = "select count(A.id) total_page from image.photo A " \
                      "inner join image.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title) against(%s in natural language mode) " \
                      "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id = 0"
        if sql != None:
            args = (key_word, key_word, key_word)

            if len(key_word) == 0:
                args = ()

            result = self.rdbms_pool.query(sql, args)
            if result != None and len(result) != 0:
                total_page = result[0]['total_page']
                # print(total_page, math.ceil(total_page / 10))
                return math.ceil(total_page / 6)
            else:
                return None
        else:
            raise Exception("type不合法的类型")

    def get_image_uid(self, photo_id):
        sql = "select user_id from image.photo where id = %s"
        args = (photo_id,)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['user_id']
        else:
            return None


class VideoSearch(MySQLBase):
    def search(self, key_word, page, type):
        sql = None
        if type == ROBOT:
            if len(key_word) == 0:
                sql = "select A.id, A.title, A.local_url, A.remote_url, B.name as category_name from video.video A " \
                      "inner join video.category B on A.category_id = B.id " \
                      "where " \
                      "A.user_id = 0 " \
                      "order by A.date desc limit %s, 6"
            else:
                sql = "select A.id, A.title, A.local_url, A.remote_url, B.name as category_name from video.video A " \
                      "inner join video.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title, A.description) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id = 0 " \
                      "order by A.date desc limit %s, 6"
        if type == HUMAN:
            if len(key_word) == 0:
                sql = "select A.id, A.title, A.local_url, A.remote_url, B.name as category_name from video.video A " \
                      "inner join video.category B on A.category_id = B.id " \
                      "where " \
                      "A.user_id != 0 " \
                      "order by A.date desc limit %s, 6"
            else:
                sql = "select A.id, A.title, A.local_url, A.remote_url, B.name as category_name from video.video A " \
                      "inner join video.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title, A.description) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id != 0 " \
                      "order by A.date desc limit %s, 6"

        if sql != None:
            args = (key_word, key_word, key_word, (page - 1) * 6)
            if len(key_word) == 0:
                args = ((page - 1) * 6,)

            result = self.rdbms_pool.query(sql, args)
            if result != None and len(result) != 0:
                return result
            else:
                return None
        else:
            raise Exception("type不合法的类型")

    def search_total_pages(self, key_word, type):
        sql = None
        if type == HUMAN:
            if len(key_word) == 0:
                sql = "select count(A.id) total_page from video.video A " \
                      "inner join video.category B on A.category_id = B.id " \
                      "where A.user_id != 0"
            else:
                sql = "select count(A.id) total_page from video.video A " \
                      "inner join video.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title, A.description) against(%s in natural language mode) " \
                      "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id != 0"
        if type == ROBOT:
            if len(key_word) == 0:
                sql = "select count(A.id) total_page from video.video A " \
                      "inner join video.category B on A.category_id = B.id " \
                      "where A.user_id = 0"
            else:
                sql = "select count(A.id) total_page from video.video A " \
                      "inner join video.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                      "where (match(A.title, A.description) against(%s in natural language mode) " \
                      "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                      "and A.user_id = 0"
        if sql != None:
            args = (key_word, key_word, key_word)

            if len(key_word) == 0:
                args = ()

            result = self.rdbms_pool.query(sql, args)
            if result != None and len(result) != 0:
                total_page = result[0]['total_page']
                # print(total_page, math.ceil(total_page / 10))
                return math.ceil(total_page / 6)
            else:
                return None
        else:
            raise Exception("type不合法的类型")

    def get_video_uid(self, video_id):
        sql = "select user_id from video.video where id = %s"
        args = (video_id,)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['user_id']
        else:
            return None
