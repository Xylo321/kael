from reborn.settings.apps import MINGMQ_CONFIG
from reborn.settings.apps.image import MYSQL_CONFIG as IMAGE_MYSQL_CONFIG
from reborn.db.rdbms import MySQLPool
from reborn.db.image import Photo
from reborn.db.video import Video
from mingmq.client import Pool as MingMQPool
from mingmq.message import FAIL
import json
import logging
import traceback


_IMAGE_MYSQL_POOL: MySQLPool = None
_VIDEO_MYSQL_POOL: MySQLPool = None
_MINGMQ_POOL: MingMQPool = None

_LOGGER = logging.getLogger('delete_category')


def _init_mysql_pool() -> None:
    global _IMAGE_MYSQL_POOL, _VIDEO_MYSQL_POOL
    _IMAGE_MYSQL_POOL = MySQLPool(host=IMAGE_MYSQL_CONFIG['host'],
                                  user=IMAGE_MYSQL_CONFIG['user'],
                                  passwd=IMAGE_MYSQL_CONFIG['passwd'],
                                  db=IMAGE_MYSQL_CONFIG['db'],
                                  size=IMAGE_MYSQL_CONFIG['size'])


def _release_mysql_pool() -> None:
    global _IMAGE_MYSQL_POOL, _VIDEO_MYSQL_POOL
    _IMAGE_MYSQL_POOL.release()


def _init_mingmq_pool() -> None:
    global _MINGMQ_POOL
    _MINGMQ_POOL = MingMQPool(MINGMQ_CONFIG['delete_category']['host'],
                              MINGMQ_CONFIG['delete_category']['port'],
                              MINGMQ_CONFIG['delete_category']['user_name'],
                              MINGMQ_CONFIG['delete_category']['passwd'],
                              MINGMQ_CONFIG['delete_category']['size'])


def _release_mingmq_pool() -> None:
    global _MINGMQ_POOL
    _MINGMQ_POOL.release()


def _delete_file_by_category_id_db_name(category_id: int, user_id: int, db_name: str) -> bool:
    global _IMAGE_MYSQL_POOL, _VIDEO_MYSQL_POOL, _MINGMQ_POOL, _LOGGER

    b = True
    try:
        if db_name == 'image':
            photo: Photo = Photo(_IMAGE_MYSQL_POOL)
            total_pages: int = photo.get_total_pages(category_id, user_id)
            page = 1
            while page <= total_pages:
                photo_files = photo.pag_photo2(category_id, user_id)
                for photo_file in photo_files:
                    title = photo_file['title']
                    message_data = json.dumps({
                        'user_id': user_id,
                        'category_id': category_id,
                        'title': title,
                        'db_name': db_name
                    })
                    _LOGGER.debug('分发删除文件任务: %s', message_data)
                    mq_res = _MINGMQ_POOL.opera('send_data_to_queue',
                                                *(MINGMQ_CONFIG['delete_file_by_category']['queue_name'], message_data))
                    if mq_res and mq_res['status'] != FAIL:
                        _LOGGER.debug('成功')
                    else:
                        _LOGGER.error('失败: %s', message_data)
                        b = False
                page += 1

        elif db_name == 'video':
            video: Video = Video(_VIDEO_MYSQL_POOL)
    except:
        _LOGGER.error(traceback.format_exc())
        b = False

    return b


def _get_data_from_queue(queue_name):
    global _MINGMQ_POOL, _LOGGER
    while True:
        mq_res: dict = _MINGMQ_POOL.opera('get_data_from_queue', *(queue_name, ))
        _LOGGER.debug('从消息队列中获取的消息为: %s', mq_res)

        if mq_res and mq_res['status'] != FAIL:
            message_data = json.loads(mq_res['message_data'])
            user_id: int = message_data['user_id']
            category_id: int = message_data['category_id']
            db_name: str = message_data['db_name']
            b: bool = _delete_file_by_category_id_db_name(category_id, user_id, db_name)
            if b == True:
                message_id = mq_res['message_id']
                mq_res = _MINGMQ_POOL.opera('ack_message', *(queue_name, message_id))
                if mq_res and mq_res['status'] != FAIL:
                    _LOGGER.debug('消息确认成功')
                else:
                    _LOGGER.error('消息确认失败: queue_name=%s, message_id=%s', queue_name, message_id)


def main() -> None:
    global _LOGGER
    try:
        _init_mysql_pool()
        _init_mingmq_pool()

        _get_data_from_queue(MINGMQ_CONFIG['delete_category']['queue_name'])
    except:
        _LOGGER.error(traceback.format_exc())
        try:
            _release_mingmq_pool()
            _release_mysql_pool()
        except:
            _LOGGER.error(traceback.format_exc())