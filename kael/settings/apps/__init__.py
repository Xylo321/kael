import os
import platform


STATIC_FOLDER = "../static"
TEMPLATES_FOLDER = "../templates"

# 静态文件缓存时间
STATIC_FILE_EXPIRE = 1

# mdfs的设置
MDFS_API_KEY = '1a9b365c2b2ec10357d551ef5dbdc8e9'
MDFS_UPLOAD_URL = 'https://master:15675/file/upload'
MDFS_DOWNLOAD_URL = 'https://master:15675/file/download'
MDFS_EDIT_URL = 'https://master:15675/file/edit'
MDFS_DOWNLOAD_MANY_URL = 'https://master:15675/file/download_many'
MDFS_DELETE_URL = 'https://master:15675/file/delete'
MDFS_GET_MANY_VIDEO_FIRST_PHOTO_URL = "https://master:15675/file/get_many_video_first_photo"

CACHE_DIR = os.path.expanduser('~') + os.path.sep + "cache"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


# 消息队列设置
MINGMQ_CONFIG = {
    'delete_category': {
        'host': 'mingmq',
        'port': 15673,
        'user_name': 'mingmq',
        'passwd': 'mm5201314',
        'pool_size': 10,
        'queue_name': 'kael_delete_category'
    },
    'delete_file_by_category': {
        'host': 'mingmq',
        'port': 15673,
        'user_name': 'mingmq',
        'passwd': 'mm5201314',
        'pool_size': 10,
        'queue_name': 'kael_delete_file_by_category'
    }
}