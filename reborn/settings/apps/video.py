MYSQL_CONFIG = {
    "host": 'serv_pro',
    "user": "root",
    "passwd": "mm5201314",
    "db": "video",
    "size": 5
}

import os.path
import platform

UPLOAD_FOLDER = os.path.expanduser('~') + os.path.sep + "/reborn/video"

if 'Windows' in platform.platform():
    UPLOAD_FOLDER = "E:" + os.path.sep + "reborn/video"
elif 'macOS' in platform.platform():
    UPLOAD_FOLDER = "/Volumes/GoodByeUbuntu" + os.path.sep + "reborn/video"
elif 'Linux' in platform.platform():
    UPLOAD_FOLDER = '/mnt/hgfs/reborn/video'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
