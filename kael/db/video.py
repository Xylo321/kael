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
        sql = "delete from category where name = %s and user_id = %s"
        if user_id == 0:
            sql = "delete from category_s where name = %s and user_id = %s"

        args = (name, user_id)
        affect_rows = self.rdbms_pool.edit(sql,args)
        if affect_rows != 0:
            return 1
        return 0


    def exist(self, name, user_id):
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
        result = self.exist(name, user_id)
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
            sql = "select id from category_s where name = %s and user_id = %s"

        args = (name, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None


class Video(MySQLBase):
    def pag_video2(self, page, category_id, user_id):
        sql = 'select title from video where category_id = %s and user_id = %s limit %s, 100'
        if user_id == 0:
            sql = 'select title from video_s where category_id = %s and user_id = %s limit %s, 100'

        args = (category_id, user_id, (page - 1) * 100)
        result = self.rdbms_pool.query(sql, args)
        if result is not None:
            return result
        else:
            return None

    def get_total_pages(self, category_id: int, user_id: int) -> int:
        sql: str = 'select count(id) as total_pages from video where category_id = %s and user_id = %s'
        if user_id == 0:
            sql: str = 'select count(id) as total_pages from video_s where category_id = %s and user_id = %s'

        args: tuple = (category_id, user_id)
        result: list = self.rdbms_pool.query(sql, args)
        if result is not None:
            return result[0]['total_pages']
        else:
            return None

    def delete_video(self, title, user_id):
        sql = "delete from video where title = %s and user_id = %s"
        if user_id == 0:
            sql = "delete from video_s where title = %s and user_id = %s"

        args = (title, user_id)
        affect_rows = self.rdbms_pool.edit(sql, args)
        if affect_rows == 0:
            return -1
        else:
            return 1

    def exist(self, title, user_id):
        sql = "select id from video where title = %s and user_id = %s"
        if user_id == 0:
            sql = "select id from video_s where title = %s and user_id = %s"

        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return 1
        else:
            return -1

    def add_video(self, title, category_name, file_extension, description, user_id):
        result = self.exist(title, user_id)
        if result == -1:
            category = Category(self.rdbms_pool)
            category_id = category.get_category_id(category_name, user_id)
            if category_id:
                sql = "insert into video(title, category_id, file_extension, user_id, date, description) value(%s, %s, %s, %s, %s, %s)"
                if user_id == 0:
                    sql = "insert into video_s(title, category_id, file_extension, user_id, date, description) value(%s, %s, %s, %s, %s, %s)"

                args = (title, category_id, file_extension, user_id, int(time.time()), description)
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
                if user_id == 0:
                    sql = "insert ignore into video_s(title, category_id, local_url, user_id, date, remote_url, description) value(%s, %s, %s, %s, %s, %s, %s)"

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
                if user_id == 0:
                    sql = ("select A.title, A.date "
                           "from video_s A inner join category_s B on A.category_id = B.id "
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
            if user_id == 0:
                sql = ("select A.title, A.date "
                       "from video_s A inner join category_s B on A.category_id = B.id "
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
            if user_id == 0:
                sql = "select local_url from video_s where category_id = %s and user_id = %s"

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

        if user_id == 0:
            sql = "select A.title, A.date, B.name as category_name, A.description, A.category_id, A.file_extension " \
                  "from video_s A inner join category_s B on A.category_id = B.id " \
                  "where A.title = %s and A.user_id = %s"
        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result is not None and len(result) != 0:
            return result
        else:
            return None

    def get_category_id_file_extension_by_title(self, title, user_id):
        sql = 'select category_id, file_extension from video where title = %s and user_id = %s'
        if user_id == 0:
            sql = 'select category_id, file_extension from video_s where title = %s and user_id = %s'

        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result is not None and len(result) != 0:
            return result
        return None

    def get_category_id_by_title(self, title, user_id):
        sql = 'select category_id, file_extension from video where title = %s and user_id = %s'
        if user_id == 0:
            sql = 'select category_id, file_extension from video_s where title = %s and user_id = %s'

        args = (title, user_id)
        result = self.rdbms_pool.query(sql, args)
        if result is not None and len(result) != 0:
            return result[0]['category_id']
        return None

    def update_video(self, user_id, src_title, new_title, category_name, description, file_extension):
        category = Category(self.rdbms_pool)
        category_id = category.get_category_id(category_name, user_id)
        if category_id:
            args = (new_title, category_id, int(time.time()), description, file_extension, user_id, src_title)
            sql = ("update video set title = %s, category_id = %s, date = %s, description = %s"
                   ", file_extension=%s where user_id = %s and title = %s")
            if user_id == 0:
                sql = ("update video_s set title = %s, category_id = %s, date = %s, description = %s"
                       ", file_extension=%s where user_id = %s and title = %s")
            result = self.rdbms_pool.edit(sql, args)
            if result != 0:
                return 1
            else:
                return -1
