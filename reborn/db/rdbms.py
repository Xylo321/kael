"""
RDBMS-关系型数据库缩写
"""
import logging
import traceback
from collections import deque
from threading import Lock

import pymysql

LOCK = Lock()


class MySQLPool(object):
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
            self.pool.append(self._get_conn())

    def _get_conn(self):
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

    def get_conn(self):
        with LOCK:
            try:
                if len(self.pool) != 0:
                    conn = self.pool.popleft()
                    conn.ping()
                    return conn
                else:
                    raise Exception('连接池已为空')
            except:
                # 有可能是conn.ping的异常，先关闭，然后再初始化连接池
                self.release()

                self._init_pool()
                return self.pool.popleft()

    def back_conn(self, conn):
        with LOCK:
            self.pool.append(conn)

    def release(self):
        for conn in self.pool:
            try:
                conn.close()
            except:
                pass

        self.pool.clear()

    def query(self, sql, args):
        conn = None
        try:
            conn = self.get_conn()

            with conn.cursor() as cursor:
                cursor.execute(sql, args)

                return cursor.fetchall()
        except (pymysql.err.InterfaceError, pymysql.err.OperationalError):
            print(traceback.print_exc())
            conn = None
        except (
                pymysql.err.DatabaseError, pymysql.err.DataError, pymysql.err.IntegrityError,
                pymysql.err.ProgrammingError,
                pymysql.err.NotSupportedError):
            logging.error(sql)
            logging.error(args)
            print(traceback.print_exc())
        finally:
            if conn != None: self.back_conn(conn)

    def edit(self, sql, args):
        affect_rows = 0
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
            conn.commit()
            affect_rows = conn.affected_rows()
        except (pymysql.err.InterfaceError, pymysql.err.OperationalError):
            print(traceback.print_exc())
            conn = None
        except (
                pymysql.err.DatabaseError, pymysql.err.DataError, pymysql.err.IntegrityError,
                pymysql.err.ProgrammingError,
                pymysql.err.NotSupportedError):
            logging.error(sql)
            logging.error(args)
            print(traceback.print_exc())

            conn.rollback()
        finally:
            if conn != None: self.back_conn(conn)
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
        except (pymysql.err.InterfaceError, pymysql.err.OperationalError):
            print(traceback.print_exc())
            conn = None
        except (
                pymysql.err.DatabaseError, pymysql.err.DataError, pymysql.err.IntegrityError,
                pymysql.err.ProgrammingError,
                pymysql.err.NotSupportedError):
            logging.error(sql)
            logging.error(many_args)
            print(traceback.print_exc())

            conn.rollback()
        finally:
            if conn != None: self.back_conn(conn)
            return affect_rows
