import threading
from collections import deque

import pika


class Producter(object):
    def __init__(self, host, port, user, passwd, queue):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.queue = queue

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host,
                                      port=self.port,
                                      heartbeat=0,
                                      credentials=pika.credentials.PlainCredentials(self.user, self.passwd)))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True)

    def send_message(self, message):
        if self._is_close() == 1:
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue,
                                       body=message,
                                       properties=pika.BasicProperties(
                                           delivery_mode=2,  # make message persistent
                                       ))
        else:
            raise Exception('pika connection is closed, I had retry to reconnect it, but failed.')

    def _reconnect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host,
                                      port=self.port,
                                      credentials=pika.credentials.PlainCredentials(self.user, self.passwd)))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True)

    def _is_close(self):
        if self.connection.is_closed:
            self._reconnect()
            return 1
        else:
            return 1

    def is_close(self):
        return self._is_close()

    def close(self):
        self.channel.close()
        self.connection.close()


LOCK = threading.Lock()


class ProducterPool(object):
    def __init__(self, host, port, user, passwd, queue, size):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.queue = queue
        self.size = size

        self.pool = deque()

        self.init_pool()

    def init_pool(self):
        for i in range(self.size):
            pro = Producter(host=self.host,
                            port=self.port,
                            user=self.user,
                            passwd=self.passwd,
                            queue=self.queue)
            self.pool.append(pro)

    def get_producter(self):
        with LOCK:
            if len(self.pool) == 0:
                self.init_pool()

            return self.pool.popleft()

    def back_producter(self, pro):
        with LOCK:
            self.pool.append(pro)

    def release(self):
        for i in range(self.size):
            self.pool.pop().close()


class Customer(object):
    def __init__(self, host, port, user, passwd, queue, size=1, no_ack=False):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.queue = queue
        self.size = size

        # 如果设置True，则只关系将消息取出，取出的数据会放在rabbitmq客户端主机的内存中，如果这个客户端异常关闭，则
        # 丢失所有的数据，如果设置为False，则可以保证数据的安全性，但是会降低AMQP的消费速度。所以，这个值的设置是分
        # 侧重点的，如果是关系数据从队列中被取出之后的处理结果，则需要设置为False，如果不关心数据的处理结果则设置为
        # True。但是，会给rabbitmq的主机带来性能问题，但是可省去客户端的开销和开发成本，总的来说，爬虫大数据，就用
        # True，也可以这么说，对于数据处理结果关注的必须设置为True；所以，这个值比kafaka要好很多。
        self.no_ack = no_ack

        self.pool = []

    def _create_conn_ch(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host,
                                      port=self.port,
                                      heartbeat=0,
                                      credentials=pika.credentials.PlainCredentials(self.user, self.passwd)))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_qos(prefetch_count=self.size)

        return connection, channel

    def serve(self, callback):
        def _consume(channel, func):
            channel.basic_consume(queue=self.queue, on_message_callback=func, auto_ack=self.no_ack)
            channel.start_consuming()

        for i in range(self.size):
            conn, ch = self._create_conn_ch()
            self.pool.append((conn, ch))
            threading.Thread(target=_consume, args=(ch, callback)).start()

    def close(self):
        for ele in self.pool:
            ele[1].close()
            ele[0].close()
