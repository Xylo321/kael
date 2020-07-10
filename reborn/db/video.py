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
                sql = "delete from video where user_id = %s and category_id in (select id from category where name = %s)"
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


class Video(MySQLBase):
    def delete_video(self, title, user_id):
        sql = "delete from video where title = %s and user_id = %s"
        args = (title, user_id)
        affect_rows = self.rdbms_pool.edit(sql, args)
        if affect_rows == 0:
            return -1
        else:
            return 1

    def exist(self, title, user_id):
        sql = "select id from video where title = %s and user_id = %s"
        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return 1
        else:
            return -1

    def add_video(self, title, category_name, local_url, description, user_id):
        result = self.exist(title, user_id)
        if result == -1:
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                sql = "insert into video(title, category_id, local_url, user_id, date, description) value(%s, %s, %s, %s, %s, %s)"
                args = (title, category_id, local_url, user_id, int(time.time()), description)
                affect_rows = self.rdbms_pool.edit(sql, args)
                if affect_rows == 0:
                    return -1
                else:
                    return 1
            else:
                return -1
        else:
            return -1

    def robot_add_video(self, title, category_name, local_url, user_id, remote_url, description):
        result = self.exist(title, user_id)
        if result == -1:
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                # 据说ignore能增加插入速度
                sql = "insert ignore into video(title, category_id, local_url, user_id, date, remote_url, description) value(%s, %s, %s, %s, %s, %s, %s)"
                args = (title, category_id, local_url, user_id, int(time.time()), remote_url, description)
                affect_rows = self.rdbms_pool.edit(sql, args)
                if affect_rows == 0:
                    return -1
                else:
                    return 1
            else:
                return -1
        else:
            return -1

    def pag_video(self, page, category_name, user_id):
        if category_name != '':
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                sql = ("select A.title, A.date "
                       "from video A inner join category B on A.category_id = B.id "
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
            sql = ("select A.title, A.date "
                   "from video A inner join category B on A.category_id = B.id "
                   "where A.user_id = %s "
                   "order by date desc limit %s, 10")

            args = (user_id, (page - 1) * 10)
            result = self.rdbms_pool.query(sql, args)
            if result is not None:
                return result
            else:
                return None

    def get_videos(self, category_name, user_id):
        category = Category(self.rdbms_pool)
        category_id = category.get_category_id(category_name, user_id)
        if category_id:
            sql = "select local_url from video where category_id = %s and user_id = %s"
            args = (category_id, user_id)
            result = self.rdbms_pool.query(sql, args)
            if result is not None:
                return result
            else:
                return None
        else:
            return None

    def get_video(self, title, user_id):
        sql = "select A.title, A.date, B.name as category_name, A.description, A.category_id, A.file_extension " \
              "from video A inner join category B on A.category_id = B.id " \
              "where A.title = %s and A.user_id = %s"

        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result is not None and len(result) != 0:
            return result
        else:
            return None

    def update_video(self, user_id, src_title, new_title, category_name, description, local_url=None):
        category = Category(self.rdbms_pool)
        category_id = category.get_category_id(category_name, user_id)
        if category_id:
            args = (new_title, category_id, int(time.time()), description, user_id, src_title)
            sql = ("update video set title = %s, category_id = %s, date = %s, description = %s"
                   " where user_id = %s and title = %s")
            if local_url != None:
                args = (new_title, category_id, int(time.time()), local_url, description, user_id, src_title)
                sql = ("update video set title = %s, category_id = %s, date = %s, local_url = %s, description = %s"
                       " where user_id = %s and title = %s")
            result = self.rdbms_pool.edit(sql, args)
            if result != 0:
                return 1
            else:
                return -1
