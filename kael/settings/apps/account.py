# session 盐值
SECRET_KEY = 'mm5201314'

MYSQL_CONFIG = {
    "host": 'master',
    "user": "root",
    "passwd": "mm5201314",
    "db": "account",
    "size": 5
}

IS_LOGIN = 'user_id'

MAIL_CONFIG = {
    'host': "smtp.qq.com",
    'port': 465,
    'username': '858556393@qq.com',
    'password': 'payzkmajwvjybfbg',
    'forget_password_msg': "%d"
}

REDIS_CONFIG = {
    "host": 'master',
    "port": 6379,
    "db": 0,
    "passwd": 'mm5201314'
}

# session超时时间
SESSION_EXPIRE = 60 * 60 * 24