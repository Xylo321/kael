import time

from reborn.db import MySQLBase


class Category(MySQLBase):
    def get_categories(self, user_id):
        sql = "select name from category where user_id = %s"
        args = (user_id,)
        result = self.rdbms_pool.query(sql, args)
        if result is not None:
            return result
        else:
            return None

    def rename_category(self, old_name, new_name, user_id):
        sql = "update category set name = %s where name = %s and user_id = %s"
        args = (new_name, old_name, user_id)
        affect_rows = self.rdbms_pool.edit(sql, args)
        if affect_rows == 0:
            return -1
        else:
            return 1

    def del_category(self, name, user_id):
        conn = None
        try:
            conn = self.rdbms_pool.get_conn()
            with conn.cursor() as cursor:
                sql = "delete from photo where user_id = %s and category_id in (select id from category where name = %s)"
                args = (user_id, name)
                cursor.execute(sql, args)

                sql = "delete from category where name = %s and user_id = %s"
                args = (name, user_id)
                cursor.execute(sql, args)

            conn.commit()
            return 1
        except Exception as e:
            if conn: conn.rollback()
            return -1
        finally:
            if conn: self.rdbms_pool.back_conn(conn)

    def exist(self, name, user_id):
        sql = "select id from category where name = %s and user_id = %s"
        args = (name, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return 1
        else:
            return -1

    def get_category_id_by_category_name_user_id(self, name, user_id):
        sql = 'select id from category where name = %s and user_id = %s'
        args = (name, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None

    def add_category(self, name, user_id):
        result = self.exist(name, user_id)
        if result == 1:
            return -1
        else:
            sql = "insert into category(name, user_id) value(%s, %s)"
            args = (name, user_id)
            affect_rows = self.rdbms_pool.edit(sql, args)
            if affect_rows == 0:
                return -1
            else:
                return 1

    def get_category_id(self, name, user_id):
        sql = "select id from category where name = %s and user_id = %s"
        args = (name, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None


class Photo(MySQLBase):
    def delete_photo(self, title, user_id):
        sql = "delete from photo where title = %s and user_id = %s"
        args = (title, user_id)
        affect_rows = self.rdbms_pool.edit(sql, args)
        if affect_rows == 0:
            return -1
        else:
            return 1

    def exist(self, title, user_id):
        sql = "select id from photo where title = %s and user_id = %s"
        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return 1
        else:
            return -1

    def get_photo_id(self, title, user_id):
        sql = "select id from photo where title = %s and user_id = %s"
        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None

    def add_photo(self, title, category_name, file_extension, user_id):
        result = self.exist(title, user_id)
        if result == -1:
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                sql = "insert into photo(title, category_id, file_extension, user_id, date) value(%s, %s, %s, %s, %s)"
                args = (title, category_id, file_extension, user_id, int(time.time()))
                affect_rows = self.rdbms_pool.edit(sql, args)
                if affect_rows == 0:
                    return -1
                else:
                    return 1
            else:
                return -1
        else:
            return -1

    def pag_photo(self, page, category_name, user_id):
        if category_name != '':
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                sql = ("select A.title, A.date, B.name as category_name, B.id as category_id "
                       "from photo A inner join category B on A.category_id = B.id "
                       "where A.user_id = %s and A.category_id = %s "
                       "order by date desc limit %s, 10")

                args = (user_id, category_id, (page - 1) * 10)
                result = self.rdbms_pool.query(sql, args)
                if result is not None:
                    return result
                else:
                    return None
            else:
                return None
        else:
            sql = ("select A.title, A.date, B.name as category_name, B.id as category_id "
                   "from photo A inner join category B on A.category_id = B.id "
                   "where A.user_id = %s "
                   "order by date desc limit %s, 10")

            args = (user_id, (page - 1) * 10)
            result = self.rdbms_pool.query(sql, args)
            if result is not None:
                return result
            else:
                return None

    def pag_photo2(self, page, category_id, user_id):
        sql = 'select title from photo where category_id = %s and user_id = %s limit %s, 100'
        args = (category_id, user_id, (page - 1) * 100)
        result = self.rdbms_pool.query(sql, args)
        if result is not None:
            return result
        else:
            return None

    def get_total_pages(self, category_id: int, user_id: int) -> int:
        sql: str = 'select count(id) as total_pages from photo where category_id = %s and user_id = %s'
        args: tuple = (category_id, user_id)
        result: list = self.rdbms_pool.query(sql, args)
        if result is not None:
            return result[0]['total_pages']
        else:
            return None

    def get_photos(self, category_name, user_id):
        category = Category(self.rdbms_pool)
        category_id = category.get_category_id(category_name, user_id)
        if category_id:
            sql = "select local_url from photo where category_id = %s and user_id = %s"
            args = (category_id, user_id)
            result = self.rdbms_pool.query(sql, args)
            if result is not None:
                return result
            else:
                return None
        else:
            return None

    def get_photo(self, title, user_id):
        sql = "select A.title, A.category_id, A.file_extension, A.date, B.name as category_name " + \
              "from photo A inner join category B on A.category_id = B.id where A.title = %s and A.user_id = %s"
        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result is not None and len(result) != 0:
            return result
        else:
            return None

    def update_photo(self, user_id, src_title, new_title, category_name):
        category = Category(self.rdbms_pool)
        category_id = category.get_category_id(category_name, user_id)
        if category_id:
            args = (new_title, category_id, int(time.time()), user_id, src_title)
            sql = ("update photo set title = %s, category_id = %s, date = %s"
                   " where user_id = %s and title = %s")
            result = self.rdbms_pool.edit(sql, args)
            if result != 0:
                return 1
        return -1