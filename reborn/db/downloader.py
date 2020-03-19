from reborn.db import MySQLBase


class Downloader(MySQLBase):
    def set_photo_downloaded(self, title, user_id):
        sql = "update image.photo set downloaded = 0 where title = %s and user_id = %s"
        args = (title, user_id)

        self.rdbms_pool.edit(sql, args)

    def set_article_downloaded(self, title, user_id):
        sql = "update blog.article set downloaded = 1 where title = %s and user_id = %s"
        args = (title, user_id)

        self.rdbms_pool.edit(sql, args)

    def set_video_downloaded(self, title, user_id):
        sql = "update video.video set downloaded = 1 where title = %s and user_id = %s"
        args = (title, user_id)

        self.rdbms_pool.edit(sql, args)
