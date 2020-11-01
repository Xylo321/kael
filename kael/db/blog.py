import time

from kael.db import MySQLBase


class Category(MySQLBase):
    def get_categories(self, user_id):
        sql = "select name from category where user_id = %s"
        if user_id == 0:
            sql = "select name from category_s where user_id = %s"
        args = (user_id,)
        result = self.rdbms_pool.query(sql, args)
        if result is not None:
            return result
        else:
            return None

    def rename_category(self, old_name, new_name, user_id):
        sql = "update category set name = %s where name = %s and user_id = %s"
        if user_id == 0:
            sql = "update category_s set name = %s where name = %s and user_id = %s"
        args = (new_name, old_name, user_id)
        affect_rows = self.rdbms_pool.edit(sql, args)
        if affect_rows == 0:
            return -1
        else:
            return 1

    def del_category(self, name, user_id):
        affect_rows = 0
        conn = None
        try:
            conn = self.rdbms_pool.get_conn()
            with conn.cursor() as cursor:
                sql = "delete from article where user_id = %s and category_id in (select id from category where name = %s)"
                if user_id == 0:
                    sql = "delete from article_s where user_id = %s and category_id in (select id from category_s where name = %s)"
                args = (user_id, name)
                cursor.execute(sql, args)

                sql = "delete from category where name = %s and user_id = %s"
                if user_id == 0:
                    sql = "delete from category_s where name = %s and user_id = %s"
                args = (name, user_id)
                cursor.execute(sql, args)
            conn.commit()
            return 1
        except Exception as e:
            if conn: conn.rollback()
            return -1
        finally:
            if conn: self.rdbms_pool.back_conn(conn)

    def _exist(self, name, user_id):
        sql = "select id from category where name = %s and user_id = %s"
        if user_id == 0:
            sql = "select id from category_s where name = %s and user_id = %s"
        args = (name, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return 1
        else:
            return -1

    def add_category(self, name, user_id):
        result = self._exist(name, user_id)
        if result == 1:
            return -1
        else:
            sql = "insert into category(name, user_id) value(%s, %s)"
            if user_id == 0:
                sql = "insert into category_s(name, user_id) value(%s, %s)"
            args = (name, user_id)
            affect_rows = self.rdbms_pool.edit(sql, args)
            if affect_rows == 0:
                return -1
            else:
                return 1

    def get_category_id(self, name, user_id):
        sql = "select id from category where name = %s and user_id = %s"
        if user_id == 0:
            ql = "select id from category_s where name = %s and user_id = %s"
        args = (name, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None


class Article(MySQLBase):
    SHOW = 0
    HIDDEN = 1

    def delete_article(self, title, user_id):
        sql = "delete from article where title = %s and user_id = %s"
        if user_id == 0:
            sql = "delete from article_s where title = %s and user_id = %s"
        args = (title, user_id)
        affect_rows = self.rdbms_pool.edit(sql, args)
        if affect_rows == 0:
            return -1
        else:
            return 1

    def _exist(self, title, user_id):
        sql = "select id from article where title = %s and user_id = %s"
        if user_id == 0:
            sql = "select id from article_s where title = %s and user_id = %s"
        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return 1
        else:
            return -1

    def add_article(self, title, category_name, content, is_public, user_id):
        result = self._exist(title, user_id)
        if result == -1:
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                sql = "insert into article(title, category_id, is_public, content, user_id, date) value(%s, %s, %s, %s, %s, %s)"
                if user_id == 0:
                    sql = "insert into article_s(title, category_id, is_public, content, user_id, date) value(%s, %s, %s, %s, %s, %s)"
                args = (title, category_id, is_public, content, user_id, int(time.time()))
                affect_rows = self.rdbms_pool.edit(sql, args)
                if affect_rows == 0:
                    return -1
                else:
                    return 1
            else:
                return -1
        else:
            return -1

    def robot_add_article(self, title, is_public, category_name, content, user_id, url):
        result = self._exist(title, user_id)
        if result == -1:
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                # 据说ignore能增加插入速度
                sql = "insert ignore into article(title, category_id, is_public, content, user_id, date, url) value(%s, %s, %s, %s, %s, %s, %s)"
                if user_id == 0:
                    sql = "insert ignore into article_s(title, category_id, is_public, content, user_id, date, url) value(%s, %s, %s, %s, %s, %s, %s)"
                args = (title, category_id, is_public, content, user_id, int(time.time()), url)
                affect_rows = self.rdbms_pool.edit(sql, args)
                if affect_rows == 0:
                    return -1
                else:
                    return 1
            else:
                return -1
        else:
            return -1

    def save_article(self, title, category_name, content, user_id):
        category = Category(self.rdbms_pool)
        category_id = category.get_category_id(category_name, user_id)
        if category_id:
            sql = "update article set title = %s, category_id = %s, user_id = %s, date = %s, content = %s where user_id = %s"
            if user_id == 0:
                sql = "update article_s set title = %s, category_id = %s, user_id = %s, date = %s, content = %s where user_id = %s"
            args = (title, category_id, user_id, int(time.time()), content, user_id)
            affect_rows = self.rdbms_pool.edit(sql, args)
            if affect_rows == 0:
                return -1
            else:
                return 1
        else:
            return -1

    def pag_article(self, page, category_name, user_id):
        if category_name != '':
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                sql = "select title, date from article where category_id = %s order by date desc limit %s, 10"
                if user_id == 0:
                    sql = "select title, date from article_s where category_id = %s order by date desc limit %s, 10"
                args = (category_id, (page - 1) * 10)
                result = self.rdbms_pool.query(sql, args)
                if result is not None:
                    return result
                else:
                    return None
        else:
            sql = "select title, date from article where user_id = %s order by date desc limit %s, 10"
            if user_id == 0:
                sql = "select title, date from article_s where user_id = %s order by date desc limit %s, 10"
            args = (user_id, (page - 1) * 10)
            result = self.rdbms_pool.query(sql, args)
            if result is not None:
                return result
            else:
                return None

    def get_article(self, title, user_id):
        sql = "select A.title, A.content, A.date, B.name as category_name, A.is_public " \
              "from article A inner join category B on A.category_id = B.id " \
              "where A.title = %s and A.user_id = %s"
        if user_id == 0:
            sql = "select A.title, A.content, A.date, B.name as category_name, A.is_public " \
                  "from article_s A inner join category_s B on A.category_id = B.id " \
                  "where A.title = %s and A.user_id = %s"
        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result is not None and len(result) != 0:
            return result
        else:
            return None

    def update_article(self, src_title, new_title, category_name, is_public, content, user_id):
        sql = "update article set title = %s, content = %s, " \
              "category_id = (select id from category where name = %s), " \
              "date = %s, is_public = %s where title = %s and user_id = %s"
        if user_id == 0:
            sql = "update article_s set title = %s, content = %s, " \
                  "category_id = (select id from category_s where name = %s), " \
                  "date = %s, is_public = %s where title = %s and user_id = %s"
        args = (new_title, content, category_name, int(time.time()), is_public, src_title, user_id)
        result = self.rdbms_pool.edit(sql, args)
        if result != 0:
            return 1
        else:
            return -1
