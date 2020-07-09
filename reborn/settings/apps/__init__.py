import os
import platform


STATIC_FOLDER = "../static"
TEMPLATES_FOLDER = "../templates"

# 静态文件缓存时间
STATIC_FILE_EXPIRE = 1

# mdfs的设置
MDFS_API_KEY = '1a9b365c2b2ec10357d551ef5dbdc8e9'
MDFS_UPLOAD_URL = 'http://serv_pro:15675/file/upload'
MDFS_DOWNLOAD_URL = 'http://serv_pro:15675/file/download'
MDFS_EDIT_URL = 'http://serv_pro:15675/file/edit'
MDFS_DOWNLOAD_MANY_URL = 'http://serv_pro:15675/file/download_many'
MDFS_DELETE_URL = 'http://serv_pro:15675/file/delete'

CACHE_DIR = os.path.expanduser('~') + os.path.sep + "reborn" + os.path.sep + "cache"

if 'Windows' in platform.platform():
    pass
elif 'macOS' in platform.platform():
    CACHE_DIR = "/Volumes/GoodByeUbuntu" + os.path.sep + "reborn" + os.path.sep + "cache"
elif 'Linux' in platform.platform():
    CACHE_DIR = '/mnt/hgfs' + os.path.sep + 'reborn' + os.path.sep + "cache"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


# 消息队列设置
MINGMQ_CONFIG = {
    'delete_category': {
        'host': 'serv_pro',
        'port': 15673,
        'user_name': 'mingmq',
        'passwd': 'mm5201314',
        'pool_size': 10,
        'queue_name': 'reborn_delete_category'
    },
    'delete_file_by_category': {
        'host': 'serv_pro',
        'port': 15673,
        'user_name': 'mingmq',
        'passwd': 'mm5201314',
        'pool_size': 10,
        'queue_name': 'reborn_delete_file_by_category'
    }
}