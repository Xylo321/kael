import pdb

from reborn.apps import BLOG_MYSQL_POOL, ACCOUNT_MYSQL_POOL
from reborn.db import blog, account

user = account.User(ACCOUNT_MYSQL_POOL)
category = blog.Category(BLOG_MYSQL_POOL)

uname = 'zswj123'

uid = user.get_user_id(uname)

pdb.set_trace()
category.del_category('测试', uid)
