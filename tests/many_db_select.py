from reborn.db.rdbms import MySQLPool

msp = MySQLPool('localhost', 'root', '123456', '', 5)
sql = 'select A.title, B.title from image.photo A, blog.blog B limit 1'
args = ()
result = msp.query(sql, args)
print(result)
msp.release()
