MYSQL_CONFIG = {
    "host": '192.168.1.30',
    "user": "root",
    "passwd": "mm5201314",
    "db": "image",
    "size": 5
}

SAVE_AMQP_CONFIG = dict(
    host='192.168.1.30',
    port=5672,
    user='admin',
    passwd='mm5201314',
    queue='save_photo',
    size=5,
    no_ack=True
)
