from mingmq.client import Pool
from reborn.settings.mq.apps import SAVE_AMQP_CONFIG, MYSQL_CONFIG


def main():
    host = SAVE_AMQP_CONFIG['host']
    port = SAVE_AMQP_CONFIG['port']
    user = SAVE_AMQP_CONFIG['user']
    passwd = SAVE_AMQP_CONFIG['passwd']
    queue = SAVE_AMQP_CONFIG['queue']
    size = SAVE_AMQP_CONFIG['size']

    try:
        pool = Pool(host, port, user, passwd, size)
        pool.opera('declare_queue', (queue, ))
        while True:
            data = pool.opera('get_data_from_queue', (queue, ))
            # TODO
    finally:
        if pool: pool.release()