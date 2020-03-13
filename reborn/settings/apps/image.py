MYSQL_CONFIG = {
    "host": 'localhost',
    "user": "root",
    "passwd": "123456",
    "db": "image",
    "size": 5
}

import os.path

UPLOAD_FOLDER = os.path.expanduser('~') + os.path.sep + "/reborn/image"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
