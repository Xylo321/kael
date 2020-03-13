import traceback

import urllib3

from reborn.kdd.image import wei1tuku
from reborn.settings.mq.image.client import CRAWL_AMQP_CONFIG
from reborn.settings.mq.image.server import SAVE_AMQP_CONFIG

urllib3.disable_warnings()
import logging

logging.basicConfig(level=logging.INFO)
import json
from reborn.mq.amqp import Customer, ProducterPool


class Wei1tukuPagPhotoListTask(object):

    def main(self):
        pro = None
        try:
            propool = ProducterPool(host=SAVE_AMQP_CONFIG['host'],
                                    port=SAVE_AMQP_CONFIG['port'],
                                    user=SAVE_AMQP_CONFIG['user'],
                                    passwd=SAVE_AMQP_CONFIG['passwd'],
                                    queue=SAVE_AMQP_CONFIG['queue'],
                                    size=SAVE_AMQP_CONFIG['size'])

            ca = wei1tuku.Categories()

            for tag in ca.main():
                print("0", tag)
                xp = wei1tuku.XiangcePagnation(tag)

                for xiangce_hrefs in xp.main():
                    print("1", xiangce_hrefs)
                    for xh in xiangce_hrefs:
                        dp = wei1tuku.DetailPagnation(xh)
                        for photo_title_url in dp.main():
                            print("2", photo_title_url)
                            d = {
                                "jd": 'pag_photo_list',
                                'data': {
                                    'title': photo_title_url['photo_title'],
                                    'category_name': '唯一图库',
                                    'url': photo_title_url['photo_url']
                                }
                            }
                            print('data:', d)

                            try:
                                p = propool.get_producter()
                                p.send_message(json.dumps(d))
                                propool.back_producter(p)
                            except:
                                print(traceback.print_exc())

        except:
            print(traceback.format_exc())
        finally:
            if pro: pro.close()


def main():
    def callback(ch, method, properties, body):
        try:
            logging.info(" [x] Received %r", body)
            data = json.loads(body)
            category_name = data['category_name']

            if category_name == '唯一图库':
                wpplt = Wei1tukuPagPhotoListTask()
                wpplt.main()

            logging.info(" [x] Done")
        except:
            print(traceback.format_exc())
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

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
