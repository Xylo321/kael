import json
import traceback

from reborn.db.image import Photo, Category
from reborn.db.rdbms import MySQLPool
from reborn.mq.amqp import Customer, ProducterPool
from reborn.settings.apps.search import ROBOT
from reborn.settings.mq.downloader import SAVE_AMQP_CONFIG as DOWNLOADER_AMQP_CONFIG
from reborn.settings.mq.image.server import MYSQL_CONFIG, SAVE_AMQP_CONFIG


class Main(object):
    MYSQL_POOl = MySQLPool(host=MYSQL_CONFIG['host'],
                           user=MYSQL_CONFIG['user'],
                           passwd=MYSQL_CONFIG['passwd'],
                           db=MYSQL_CONFIG['db'],
                           size=MYSQL_CONFIG['size'])

    photo = Photo(MYSQL_POOl)

    category = Category(MYSQL_POOl)

    c = Customer(host=SAVE_AMQP_CONFIG['host'],
                 port=SAVE_AMQP_CONFIG['port'],
                 user=SAVE_AMQP_CONFIG['user'],
                 passwd=SAVE_AMQP_CONFIG['passwd'],
                 queue=SAVE_AMQP_CONFIG['queue'],
                 size=SAVE_AMQP_CONFIG['size'])

    pp = ProducterPool(host=DOWNLOADER_AMQP_CONFIG['host'],
                       port=DOWNLOADER_AMQP_CONFIG['port'],
                       user=DOWNLOADER_AMQP_CONFIG['user'],
                       passwd=DOWNLOADER_AMQP_CONFIG['passwd'],
                       queue=DOWNLOADER_AMQP_CONFIG['queue'],
                       size=DOWNLOADER_AMQP_CONFIG['size'])

    def main(self):
        def callback(ch, method, properties, body):
            try:
                print(" [x] Received %r", body)
                d = json.loads(body)
                jd = d['jd']
                data = d['data']

                if jd == 'pag_photo_list':
                    title = data['title']
                    category_name = data['category_name']
                    user_id = ROBOT
                    remote_url = data['url']
                    local_url = title + '.' + remote_url.rsplit(".")[-1]

                    if category_name in ['唯一图库']:
                        photo_exist = self.photo.exist(title, user_id)
                        cat_exist = self.category.exist(category_name, user_id)
                        if photo_exist != 1 and cat_exist == 1:
                            self.photo.robot_add_photo(title, category_name, local_url, user_id, remote_url)
                            print(" [x] Image added. %s" % title)

                            data = {
                                "type": "image",
                                "filename": local_url,
                                "title": title,
                                'download_url': remote_url
                            }
                            try:
                                p = self.pp.get_producter()
                                p.send_message(json.dumps(data))
                                self.pp.back_producter(p)
                            except:
                                print(traceback.print_exc())
                        else:
                            print(" [x] Image exists or Category not exists. %s" % title)
                    else:
                        raise Exception(str(" [x] What do you want? %s" % str(d)))

                print(" [x] Done")
            except:
                print(traceback.format_exc())
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        try:
            self.c.serve(callback)
        except:
            print(traceback.format_exc())

            self.c.close()
            self.pp.release()

            self.MYSQL_POOl.release()


if __name__ == '__main__':
    Main().main()
