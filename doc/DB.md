# DB

有关业务相关的一些数据库，表，索引，等等。此文档主要分为如下几个版块：

* 思考
* MYSQL8
* REDIS

## 一、思考

* 因为这模块是数据库模块，所以，又要被网站调用，又要被爬数据调用，这样就产生冲突了，爬虫这边对mysql操作，其实也不是，我这边不是有
任务队列这里为mysql分担了压力吗？我就给存数据的队列安排5个连接就够了，但是，总有一天，mysql的所有连接数要被用完的啊？那问题来了，mysql
服务器一共支持多少个连接？show variables like '%max_connections%'; 这个命令是可以查看的，也就是说mysql服务器的连接也是可以设置的，
那设置多少合适？设置过高，又会导致mysql服务器内存要求很高，设置过低好像又不太好。我感觉mysql还是有点不太靠得住。其实我觉得mysql存下业务
数据还是可以的，但是如果要存爬虫数据，我感觉太牵强了，这根本就不现实。所以，是不是我的架构错了呢？爬虫数据是海量的。如果仅仅靠python肯定
是不行的。这次真的是我错了。我不该这么做。我应该思考的是hbase数据库，对，下一步研发的目标应该是这个。这才是我的专业。

## 二、MYSQL8

安装mysql：
```bash
wget https://repo.mysql.com//mysql-apt-config_0.8.14-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.14-1_all.deb
sudo apt update
sudo apt install mysql-server
```
关于mysql.deb包的详细使用官方文档https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/。

设置远程连接（mysql8不需要修改配置文件）：
```
$ mysql -u root -p123456;
>>> CREATE USER  'root'@'%' identified by 'mm5201314';
>>> GRANT ALL ON *.* TO 'root'@'%';
>>> ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'mm5201314';
>>> flush privileges;
```

账号密码修改，不然有时候会报错ssh这种错误：
```
$ mysql -u root -p123456;
>>> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
>>> ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'mm5201314';
>>> flush privileges;
```

设置mysqld默认事物隔离级别：
```
$ sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
transaction-isolation = READ-COMMITTED
$ sudo service mysql restart
```

### 二一、创建数据库和表的SQL语句：

#### ACCOUNT数据库

```sql
CREATE DATABASE `account` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `passwd` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

增加机器人账号：
```
insert into account.user(id, name, email, passwd) value(0, 'robot', '858556393@qq.com', 'robot');
```

为name字段增加全文索引:
```sql
create fulltext index name on user(name) with parser ngram;
```

#### 二二、BLOG数据库

```sql
CREATE DATABASE `blog` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `date` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `url` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title_user_id` (`title`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58499 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(4) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_uid` (`name`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

如果没有创建全文索引，创建文章全文索引：
```sql
create fulltext index name on category(name) with parser ngram;
create fulltext index title_content on article(title, content) with parser ngram;
```
如果不加with parser ngram中文分词，中文搜索是不会出结果的。

需要注意的是，采用mysqlworkbech同步数据库之后创建的全文索引没有默认增加中文分词插件，需要删除后，使用命令行追加才能搜索到中文结果。

#### 二三、IMAGE数据库

```sql
CREATE DATABASE `image` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(4) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_user_id` (`name`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `photo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `url` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title_user_id` (`title`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create fulltext index title on photo(title) with parser ngram;
create fulltext index name on category(name) with parser ngram;
```

#### 二四、VIDEO数据库

```sql
CREATE DATABASE `video`;

CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `video` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `date` int NOT NULL,
  `local_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `remote_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_id` int NOT NULL,
  `category_id` int NOT NULL,
  `downloaded` smallint DEFAULT '0',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

create fulltext index title_description on video(title, description) with parser ngram;
create fulltext index name on category(name) with parser ngram;
```

## 三、REDIS

安装Reids
```
sudo apt install redis-server
```

* flushdb清除当前db的所有key；

* flushall清除所有db的所有key；

* keys *查看所有的key，当前db数字下；

* 启动，停止，重启，查看redis服务器：
`service redis start|stop|restart|status`；

* pttl key 查看某个key的过期时间，以毫秒为单位，1000毫秒=1秒；

* auth 密码，用于使用redis-cli之后进行权限验证；

开启远程连接
```
$ vi /etc/redis/redis.conf
# bind 127.0.0.1 ::1 # 注释掉这一行
```

永久设置密码访问
```
$ vi /etc/redis/redis.conf
requirepass mm5201314
```

配置修改完毕后，重启服务`service redis-server restart`

命令使用密码进入redis:
```bash
$ redis-cli -h [ip] -p [端口] -a [密码]
```