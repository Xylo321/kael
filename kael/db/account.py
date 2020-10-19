from kael.db import MySQLBase


class User(MySQLBase):
    def login(self, name, passwd):
        sql = "select id from user where name = %s and passwd = %s"
        args = (name, passwd)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None

    def _existAnd(self, name, email):
        sql = "select id from user where name = %s and email = %s"
        args = (name, email)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None

    def existOr(self, name, email):
        sql = "select id from user where name = %s or email = %s"
        args = (name, email)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return 1  # 已注册
        else:
            return -1  # 未注册

    def register(self, name, passwd, email):
        is_reg = self.existOr(name, email)
        if is_reg == -1:
            sql = "insert user(name, passwd, email) value(%s,%s,%s)"
            args = (name, passwd, email)
            affect_rows = self.rdbms_pool.edit(sql, args)
            if affect_rows != 0:
                return 1
            else:
                return -1
        else:
            return -1  # 注册失败

    def get_user_id(self, name):
        sql = "select id from user where name = %s"
        args = (name,)
        result = self.rdbms_pool.query(sql, args)
        if result != None and len(result) != 0:
            return result[0]['id']
        else:
            return None

    def forget_password(self, name, email, new_password):
        user_id = self._existAnd(name, email)
        if user_id != None:
            sql = "update user set passwd = %s where id = %s"
            args = (new_password, user_id)
            affect_rows = self.rdbms_pool.edit(sql, args)
            if affect_rows != 0:
                return 1
            else:
                return -1
        else:
            return -1

    def get_name(self, user_id):
        sql = 'select name from user where id = %s'
        args = (user_id,)
        result = self.rdbms_pool.query(sql, args)
        if result is not None and len(result) != 0:
            return result[0]['name']
        else:
            return None
