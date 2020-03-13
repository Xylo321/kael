import json
import logging
import traceback

from reborn.mq.amqp import Customer

logging.basicConfig(level=logging.INFO)
from reborn.settings.mq.downloader import SAVE_AMQP_CONFIG, MYSQL_CONFIG

from reborn.settings.apps.image import UPLOAD_FOLDER as IMAGE_UPLOAD_FOLDER
from reborn.db.downloader import Downloader
from reborn.db.rdbms import MySQLPool

from reborn.settings.apps.search import ROBOT

import os
import requests


class Main(object):
    c = Customer(host=SAVE_AMQP_CONFIG['host'],
                 port=SAVE_AMQP_CONFIG['port'],
                 user=SAVE_AMQP_CONFIG['user'],
                 passwd=SAVE_AMQP_CONFIG['passwd'],
                 queue=SAVE_AMQP_CONFIG['queue'],
                 size=SAVE_AMQP_CONFIG['size'],
                 no_ack=SAVE_AMQP_CONFIG['no_ack'])

    MYSQL_POOl = MySQLPool(host=MYSQL_CONFIG['host'],
                           user=MYSQL_CONFIG['user'],
                           passwd=MYSQL_CONFIG['passwd'],
                           db=MYSQL_CONFIG['db'],
                           size=MYSQL_CONFIG['size'])

    downloader = Downloader(MYSQL_POOl)

    def main(self):
        def callback(ch, method, properties, body):
            filename = None
            try:
                logging.info(" [x] Received %r", body)

                data = json.loads(body)
                type = data['type']
                download_url = data['download_url']
                title = data['title']
                filename = data['filename']

                if type in ['image']:
                    r = requests.get(download_url, stream=True)

                    if r.status_code != 404:
                        save_file = IMAGE_UPLOAD_FOLDER + os.path.sep + filename
                        with open(save_file, 'wb') as f:
                            f.write(r.content)

                        if not os.path.exists(save_file):
                            raise Exception("下载文件失败!")

                        self.downloader.set_photo_downloaded(title, ROBOT)

                    r.close()
                logging.info(" [x] Done")
            except:
                print('文件下载失败:', filename)
                print(traceback.format_exc())
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        try:
            self.c.serve(callback)
        except:
            print(traceback.format_exc())

            self.c.close()


if __name__ == '__main__':
    Main().main()
