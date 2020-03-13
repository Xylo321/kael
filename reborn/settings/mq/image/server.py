MYSQL_CONFIG = {
    "host": 'serv_pro',
    "user": "root",
    "passwd": "mm5201314",
    "db": "image",
    "size": 5
}

SAVE_AMQP_CONFIG = dict(
    host='serv_pro',
    port=5672,
    user='admin',
    passwd='mm5201314',
    queue='save_photo',
    size=5,
    no_ack=True
)
