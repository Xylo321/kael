import json
import logging
import traceback

from reborn.mq.amqp import Customer
from reborn.settings.apps.search import ROBOT

logging.basicConfig(level=logging.INFO)

from reborn.db.blog import Article
from reborn.settings.mq.blog.server import MYSQL_CONFIG, SAVE_AMQP_CONFIG
from reborn.db.rdbms import MySQLPool


class Main(object):
    MYSQL_POOl = MySQLPool(host=MYSQL_CONFIG['host'],
                           user=MYSQL_CONFIG['user'],
                           passwd=MYSQL_CONFIG['passwd'],
                           db=MYSQL_CONFIG['db'],
                           size=MYSQL_CONFIG['size'])

    ARTICLE = Article(MYSQL_POOl)

    def main(self):
        def callback(ch, method, properties, body):
            try:
                logging.info(" [x] Received %r", body)
                d = json.loads(body)
                jd = d['jd']
                data = d['data']

                if jd == 'pag_article_list':
                    title = data['title'],
                    category_name = data['category_name']
                    content = '',
                    user_id = ROBOT,
                    url = data['url']

                    if category_name in ["CSDN", '王垠', '阮一峰']:
                        self.ARTICLE.robot_add_article(title, category_name, content, user_id, url)
                    else:
                        raise Exception(str(" [x] What do you want? %s" % str(d)))

                logging.info(" [x] Done")
            except:
                print(traceback.format_exc())
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        c = Customer(host=SAVE_AMQP_CONFIG['host'],
                     port=SAVE_AMQP_CONFIG['port'],
                     user=SAVE_AMQP_CONFIG['user'],
                     passwd=SAVE_AMQP_CONFIG['passwd'],
                     queue=SAVE_AMQP_CONFIG['queue'],
                     size=SAVE_AMQP_CONFIG['size'])
        try:
            c.serve(callback)
        except:
            print(traceback.format_exc())

            c.close()
            self.MYSQL_POOl.release()


if __name__ == '__main__':
    Main().main()
