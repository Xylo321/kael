MYSQL_CONFIG = {
    "host": 'serv_pro',
    "user": "root",
    "passwd": "mm5201314",
    "db": "blog",
    "size": 15
}

SAVE_AMQP_CONFIG = dict(
    host='serv_pro',
    port=5672,
    user='admin',
    passwd='mm5201314',
    queue='save_article',
    size=10,
    no_ack=True
)
