MYSQL_CONFIG = {
    "host": 'localhost',
    "user": "root",
    "passwd": "123456",
    "db": "blog",
    "size": 15
}

SAVE_AMQP_CONFIG = dict(
    host='localhost',
    port=5672,
    user='admin',
    passwd='mm5201314',
    queue='save_article',
    size=10,
    no_ack=True
)
