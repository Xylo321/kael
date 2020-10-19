from kael.settings.apps import MINGMQ_CONFIG
from kael.settings.apps.image import MYSQL_CONFIG as IMAGE_MYSQL_CONFIG
from kael.settings.apps.video import MYSQL_CONFIG as VIDEO_MYSQL_CONFIG
from kael.db.rdbms import MySQLPool
from kael.db.image import Photo
from kael.db.video import Video
from mingmq.client import Pool as MingMQPool
from mingmq.message import FAIL
import json
import logging
import traceback
import time


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
    _VIDEO_MYSQL_POOL = MySQLPool(host=VIDEO_MYSQL_CONFIG['host'],
                                  user=VIDEO_MYSQL_CONFIG['user'],
                                  passwd=VIDEO_MYSQL_CONFIG['passwd'],
                                  db=VIDEO_MYSQL_CONFIG['db'],
                                  size=VIDEO_MYSQL_CONFIG['size'])


def _release_mysql_pool() -> None:
    global _IMAGE_MYSQL_POOL, _VIDEO_MYSQL_POOL
    _IMAGE_MYSQL_POOL.release()
    _VIDEO_MYSQL_POOL.release()


def _init_mingmq_pool() -> None:
    global _MINGMQ_POOL
    _MINGMQ_POOL = MingMQPool(MINGMQ_CONFIG['delete_category']['host'],
                              MINGMQ_CONFIG['delete_category']['port'],
                              MINGMQ_CONFIG['delete_category']['user_name'],
                              MINGMQ_CONFIG['delete_category']['passwd'],
                              MINGMQ_CONFIG['delete_category']['pool_size'])


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
                photo_files = photo.pag_photo2(page, category_id, user_id)
                _LOGGER.debug('分页从数据库中查找的文件为: %s', photo_files)
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
            total_pages: int = video.get_total_pages(category_id, user_id)
            page = 1
            while page <= total_pages:
                photo_files = video.pag_video2(page, category_id, user_id)
                _LOGGER.debug('分页从数据库中查找的文件为: %s', photo_files)
                for video_file in photo_files:
                    title = video_file['title']
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
    except:
        _LOGGER.error(traceback.format_exc())
        b = False

    return b


def _get_data_from_queue(queue_name):
    global _MINGMQ_POOL, _LOGGER
    _MINGMQ_POOL.opera('declare_queue', *(queue_name,))
    while True:
        mq_res: dict = _MINGMQ_POOL.opera('get_data_from_queue', *(queue_name, ))
        _LOGGER.debug('从消息队列中获取的消息为: %s', mq_res)

        if mq_res and mq_res['status'] != FAIL:
            message_data = json.loads(mq_res['json_obj'][0]['message_data'])
            user_id: int = message_data['user_id']
            category_id: int = message_data['category_id']
            db_name: str = message_data['db_name']
            b: bool = _delete_file_by_category_id_db_name(category_id, user_id, db_name)
            if b == True:
                message_id = mq_res['json_obj'][0]['message_id']
                mq_res = _MINGMQ_POOL.opera('ack_message', *(queue_name, message_id))
                if mq_res and mq_res['status'] != FAIL:
                    _LOGGER.debug('消息确认成功')
                else:
                    _LOGGER.error('消息确认失败: queue_name=%s, message_id=%s', queue_name, message_id)
        else:
            time.sleep(10)


def main(debug=logging.DEBUG) -> None:
    logging.basicConfig(level=debug)
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


if __name__ == '__main__':
    main()