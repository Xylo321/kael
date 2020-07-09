import json
import logging
import traceback
import time

from mingmq.client import Pool as MingMQPool
from mingmq.message import FAIL

from reborn.db.image import Photo
from reborn.db.rdbms import MySQLPool
from reborn.db.video import Video
from reborn.settings.apps import MDFS_API_KEY, MDFS_DELETE_URL
from reborn.settings.apps import MINGMQ_CONFIG
from reborn.settings.apps.image import MYSQL_CONFIG as IMAGE_MYSQL_CONFIG
from reborn.utils.mdfs import delete as mdfs_delete

_IMAGE_MYSQL_POOL: MySQLPool = None
_VIDEO_MYSQL_POOL: MySQLPool = None
_MINGMQ_POOL: MingMQPool = None

_LOGGER = logging.getLogger('delete_file_by_category')


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
                              MINGMQ_CONFIG['delete_category']['pool_size'])


def _release_mingmq_pool() -> None:
    global _MINGMQ_POOL
    _MINGMQ_POOL.release()


def _delete_file(mq_res) -> bool:
    global _LOGGER
    b: bool = False

    message_data = json.loads(mq_res['json_obj'][0]['message_data'])
    user_id: int = message_data['user_id']
    category_id: int = message_data['category_id']
    db_name: str = message_data['db_name']
    title: str = message_data['title']
    if 1 == mdfs_delete(MDFS_DELETE_URL, MDFS_API_KEY, user_id, category_id, title):
        if db_name == 'image':
            photo = Photo(_IMAGE_MYSQL_POOL)
            if -1 != photo.delete_photo(title, user_id):
                _LOGGER.debug('删除photo成功')
                b = True
            else:
                _LOGGER.error('删除photo失败, %s', message_data)
        elif db_name == 'video':
            video = Video(_VIDEO_MYSQL_POOL)
            if -1 != video.delete_video(title, user_id):
                _LOGGER.debug('删除video成功')
                b = True
            else:
                _LOGGER.error('删除video失败, %s', message_data)
    return b


def _ack_task(b: bool, mq_res, queue_name) -> None:
    global _MINGMQ_POOL, _LOGGER

    if b == True:
        message_id = mq_res['json_obj'][0]['message_id']
        mq_res = _MINGMQ_POOL.opera('ack_message', *(queue_name, message_id))
        if mq_res and mq_res['status'] != FAIL:
            _LOGGER.debug('消息确认成功')
        else:
            _LOGGER.error('消息确认失败, %s', mq_res)


def _get_data_from_queue(queue_name: str):
    global _MINGMQ_POOL, _IMAGE_MYSQL_POOL, _VIDEO_MYSQL_POOL, _LOGGER
    _MINGMQ_POOL.opera('declare_queue', *(queue_name,))
    while True:
        mq_res: dict = _MINGMQ_POOL.opera('get_data_from_queue', *(queue_name,))
        _LOGGER.debug('从消息队列中获取的消息为: %s', mq_res)

        if mq_res and mq_res['status'] != FAIL:
            b: bool = _delete_file(mq_res)
            _ack_task(b, mq_res, queue_name)
        else:
            time.sleep(10)


def main(debug=logging.DEBUG) -> None:
    logging.basicConfig(level=debug)
    global _LOGGER
    try:
        _init_mysql_pool()
        _init_mingmq_pool()

        _get_data_from_queue(MINGMQ_CONFIG['delete_file_by_category']['queue_name'])
    except:
        _LOGGER.error(traceback.format_exc())
        try:
            _release_mingmq_pool()
            _release_mysql_pool()
        except:
            _LOGGER.error(traceback.format_exc())


if __name__ == '__main__':
    main()