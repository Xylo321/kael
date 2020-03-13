import traceback
from threading import Thread

import urllib3

from reborn.kdd.blog import ranyifeng
from reborn.kdd.blog.csdn import CSDN
from reborn.kdd.blog.wangyin import pag_article_list as wy_pal
from reborn.settings.mq.blog.client import CRAWL_AMQP_CONFIG
from reborn.settings.mq.blog.server import SAVE_AMQP_CONFIG

urllib3.disable_warnings()
import logging

logging.basicConfig(level=logging.INFO)
import json
from reborn.mq.amqp import Customer, Producter


class RanYiFengArticleListTask(object):

    def main(self):
        pro = None
        try:
            pro = Producter(host=SAVE_AMQP_CONFIG['host'],
                            port=SAVE_AMQP_CONFIG['port'],
                            user=SAVE_AMQP_CONFIG['user'],
                            passwd=SAVE_AMQP_CONFIG['passwd'],
                            queue=SAVE_AMQP_CONFIG['queue'])

            urls = ranyifeng.get_categories()
            print('get categories:', urls)

            for url in urls:

                try:
                    title_urls = ranyifeng.pag_article_list(url)

                    for tu in title_urls:
                        d = {
                            "jd": 'pag_article_list',
                            'data': {
                                'title': tu['title'],
                                'category_name': '阮一峰',
                                'url': tu['url']
                            }
                        }
                        print('data:', d)

                        pro.send_message(json.dumps(d))
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())
        finally:
            if pro: pro.close()


class WangYinPagArticleListTask(object):

    def main(self):
        pro = None
        try:
            pro = Producter(host=SAVE_AMQP_CONFIG['host'],
                            port=SAVE_AMQP_CONFIG['port'],
                            user=SAVE_AMQP_CONFIG['user'],
                            passwd=SAVE_AMQP_CONFIG['passwd'],
                            queue=SAVE_AMQP_CONFIG['queue'])

            title_urls = wy_pal()
            for tu in title_urls:
                d = {
                    "jd": 'pag_article_list',
                    'data': {
                        'title': tu['title'],
                        'category_name': '王垠',
                        'url': tu['url']
                    }
                }
                print('data:', d)

                pro.send_message(json.dumps(d))

        except:
            print(traceback.format_exc())
        finally:
            if pro: pro.close()


class CSDNPagArticleListTask(object):

    def _callback(self, url):
        pro = None
        try:
            pro = Producter(host=SAVE_AMQP_CONFIG['host'],
                            port=SAVE_AMQP_CONFIG['port'],
                            user=SAVE_AMQP_CONFIG['user'],
                            passwd=SAVE_AMQP_CONFIG['passwd'],
                            queue=SAVE_AMQP_CONFIG['queue'])

            c = CSDN()
            for title_urls in c.page_article_list(url, 150):
                for tu in title_urls:
                    d = {
                        "jd": 'pag_article_list',
                        'data': {
                            'title': tu['title'],
                            'category_name': 'CSDN',
                            'url': tu['url']
                        }
                    }
                    print('%s data:' % url, d)

                    pro.send_message(json.dumps(d))

        except:
            print(traceback.format_exc())
        finally:
            if pro != None: pro.close()

    def main(self):
        urls = []
        try:
            c = CSDN()
            urls = c.get_categories()
            print(urls)
        except:
            print(traceback.format_exc())

        for url in urls:
            try:
                p = Thread(target=self._callback, args=(url,))
                p.start()
                p.join()
            except:
                print(traceback.format_exc())


def main():
    def callback(ch, method, properties, body):
        try:
            logging.info(" [x] Received %r", body)
            data = json.loads(body)
            category_name = data['category_name']

            if category_name == 'CSDN':
                plt = CSDNPagArticleListTask()
                plt.main()
            elif category_name == '王垠':
                plt = WangYinPagArticleListTask()
                plt.main()
            elif category_name == '阮一峰':
                plt = RanYiFengArticleListTask()
                plt.main()

            logging.info(" [x] Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(traceback.format_exc())

    c = Customer(host=CRAWL_AMQP_CONFIG['host'],
                 port=CRAWL_AMQP_CONFIG['port'],
                 user=CRAWL_AMQP_CONFIG['user'],
                 passwd=CRAWL_AMQP_CONFIG['passwd'],
                 queue=CRAWL_AMQP_CONFIG['queue'],
                 size=CRAWL_AMQP_CONFIG['size'])
    try:
        c.serve(callback)
    except:
        print(traceback.format_exc())
        c.close()


if __name__ == '__main__':
    main()
