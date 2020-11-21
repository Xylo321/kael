import math

from kael.db import MySQLBase
from kael.settings.apps.search import ROBOT, HUMAN


class ArticleSearch(MySQLBase):
    def search(self, key_word, page, type):
        if type == HUMAN:
            return self._search_human(key_word, page)
        elif type == ROBOT:
            return self._search_robot(key_word, page)

    def _search_robot(self, key_word, page):
        if len(key_word) == 0:
            sql = (
                "select A.id, A.title, left(A.content, 100) content, A.date, B.name as category_name, A.url from blog.article_s A "
                "inner join blog.category_s B on A.category_id = B.id "
                "where "
                "A.user_id = 0 "
                "order by A.date desc limit %s, 10")
        else:
            sql = (
                "select A.id, A.title, left(A.content, 100) content, A.date, B.name as category_name, A.url from blog.article_s A "
                "inner join blog.category_s B on A.category_id = B.id inner join account.user C on A.user_id = C.id "
                "where (match(A.content, A.title) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) "
                "and A.user_id = 0 "
                "order by A.date desc limit %s, 10")

        args = (key_word, key_word, key_word, (page - 1) * 10)
        if len(key_word) == 0:
            args = ((page - 1) * 10,)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result
        return None

    def _search_human(self, key_word, page):
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

        args = (key_word, key_word, key_word, (page - 1) * 10)
        if len(key_word) == 0:
            args = ((page - 1) * 10,)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result
        return None

    def _search_human_total_pages(self, key_word):
        sql = None
        args = ()
        if len(key_word) == 0:
            sql = ("select count(id) total_page from blog.article")
        else:
            sql = ("select count(A.id) total_page from blog.article A "
                   "inner join blog.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id "
                   "where (match(A.content, A.title) against(%s in natural language mode) "
                   "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) "
                   "and A.user_id != 0")
            args = (key_word, key_word, key_word)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            total_page = result[0]['total_page']
            # print(total_page, math.ceil(total_page / 10))
            return math.ceil(total_page / 10)
        return None

    def _search_robot_total_pages(self, key_word):
        sql = None
        args = ()
        if len(key_word) == 0:
            sql = ("select count(id) total_page from blog.article_s")
        else:
            sql = ("select count(A.id) total_page from blog.article_s A "
                   "inner join blog.category_s B on A.category_id = B.id inner join account.user C on A.user_id = C.id "
                   "where (match(A.content, A.title) against(%s in natural language mode) "
                   "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) "
                   "and A.user_id = 0")
            args = (key_word, key_word, key_word)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            total_page = result[0]['total_page']
            # print(total_page, math.ceil(total_page / 10))
            return math.ceil(total_page / 10)
        return None

    def search_total_pages(self, key_word, type):
        if type == HUMAN:
            return self._search_human_total_pages(key_word)
        elif type == ROBOT:
            return self._search_robot_total_pages(key_word)

    def get_article_uid(self, article_id, type):
        sql = "select user_id from blog.article where id = %s"
        if type == ROBOT:
            return ROBOT
        args = (article_id,)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['user_id']
        else:
            return None


class ImageSearch(MySQLBase):
    def search(self, key_word, page, type):
        if type == HUMAN:
            return self._search_human(key_word, page)
        elif type == ROBOT:
            return self._search_robot(key_word, page)

    def _search_robot(self, key_word, page):
        sql = None
        args = ()
        if len(key_word) == 0:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from image.photo_s A " \
                  "inner join image.category_s B on A.category_id = B.id " \
                  "where " \
                  "A.user_id = 0 " \
                  "order by A.date desc limit %s, 6"
            args = ((page - 1) * 6,)
        else:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from image.photo_s A " \
                  "inner join image.category_s B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                  "where (match(A.title) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                  "and A.user_id = 0 " \
                  "order by A.date desc limit %s, 6"
            args = (key_word, key_word, key_word, (page - 1) * 6)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result
        return None

    def _search_human(self, key_word, page):
        sql = None
        args = ()
        if len(key_word) == 0:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from image.photo A " \
                  "inner join image.category B on A.category_id = B.id " \
                  "where " \
                  "A.user_id != 0 " \
                  "order by A.date desc limit %s, 6"
            args = ((page - 1) * 6,)
        else:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from image.photo A " \
                  "inner join image.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                  "where (match(A.title) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                  "and A.user_id != 0 " \
                  "order by A.date desc limit %s, 6"
            args = (key_word, key_word, key_word, (page - 1) * 6)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result
        return None

    def _search_human_total_pages(self, key_word):
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

    def _search_robot_total_pages(self, key_word):
        if len(key_word) == 0:
            sql = "select count(A.id) total_page from image.photo_s A " \
                  "inner join image.category_s B on A.category_id = B.id " \
                  "where A.user_id = 0 and A.downloaded = 1"
        else:
            sql = "select count(A.id) total_page from image.photo_s A " \
                  "inner join image.category_s B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                  "where (match(A.title) against(%s in natural language mode) " \
                  "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                  "and A.user_id = 0 and A.downloaded = 1"

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

    def search_total_pages(self, key_word, type):
        if type == HUMAN:
            return self._search_human_total_pages(key_word)
        elif type == ROBOT:
            return self._search_robot_total_pages(key_word)

    def get_image_uid(self, photo_id, type):
        sql = "select user_id from image.photo where id = %s"
        if type == ROBOT:
            sql = "select user_id from image.photo_s where id = %s"

        args = (photo_id,)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['user_id']
        else:
            return None


class VideoSearch(MySQLBase):
    def search(self, key_word, page, type):
        if type == HUMAN:
            return self._search_human(key_word, page)
        elif type == ROBOT:
            return self._search_robot(key_word, page)

    def _search_robot(self, key_word, page):
        sql = None
        if len(key_word) == 0:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from video.video_s A " \
                  "inner join video.category_s B on A.category_id = B.id " \
                  "where " \
                  "A.user_id = 0 and A.downloaded = 1 " \
                  "order by A.date desc limit %s, 6"
        else:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from video.video_s A " \
                  "inner join video.category_s B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                  "where (match(A.title, A.description) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                  "and A.user_id = 0 and A.downloaded = 1 " \
                  "order by A.date desc limit %s, 6"

        args = (key_word, key_word, key_word, (page - 1) * 6)
        if len(key_word) == 0:
            args = ((page - 1) * 6,)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result
        else:
            return None

    def _search_human(self, key_word, page):
        sql = None
        if len(key_word) == 0:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from video.video A " \
                  "inner join video.category B on A.category_id = B.id " \
                  "where " \
                  "A.user_id != 0 " \
                  "order by A.date desc limit %s, 6"
        else:
            sql = "select A.id, A.title, A.category_id, A.user_id, B.name as category_name from video.video A " \
                  "inner join video.category B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                  "where (match(A.title, A.description) against(%s in natural language mode) or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                  "and A.user_id != 0 " \
                  "order by A.date desc limit %s, 6"

        args = (key_word, key_word, key_word, (page - 1) * 6)
        if len(key_word) == 0:
            args = ((page - 1) * 6,)

        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result
        else:
            return None

    def search_total_pages(self, key_word, type):
        if type == HUMAN:
            return self._search_human_total_pages(key_word)
        elif type == ROBOT:
            return self._search_robot_total_pages(key_word)

    def _search_robot_total_pages(self, key_word):
        sql = None
        if len(key_word) == 0:
            sql = "select count(A.id) total_page from video.video_s A " \
                  "inner join video.category_s B on A.category_id = B.id " \
                  "where A.user_id = 0 and A.downloaded = 1"
        else:
            sql = "select count(A.id) total_page from video.video_s A " \
                  "inner join video.category_s B on A.category_id = B.id inner join account.user C on A.user_id = C.id " \
                  "where (match(A.title, A.description) against(%s in natural language mode) " \
                  "or match(B.name) against(%s in natural language mode) or match(C.name) against(%s in natural language mode)) " \
                  "and A.user_id = 0 and A.downloaded = 1"

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

    def _search_human_total_pages(self, key_word):
        sql = None
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

    def get_video_uid(self, video_id, type):
        sql = "select user_id from video.video where id = %s"
        if type == ROBOT:
            sql = "select user_id from video.video_s where id = %s"
        args = (video_id,)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['user_id']
        else:
            return None
