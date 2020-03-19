# INSTALL

Ubuntu操作系统下，Python3.8，Redis, MySQL8, UWSGI, SUPERVISOR。

## REDIS

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

## PYTHON3.8.0

```bash
apt update -y
apt install make gcc -y
apt install libreadline-dev -y
apt install libssl-dev openssl -y
apt install libxml2 libxml2-dev -y
apt install zlibc zlib1g-dev
apt install libffi-dev -y
apt intall libsqlite3-dev

apt instll supervisor -y
wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
tar zxf Python-3.8.0.tgz
cd Python-3.8.0
./configure --prefix=/usr/local/python3.8.0
make && make install
ln -s /usr/local/python3.8.0/bien/python3.8 /usr/bin/
ln -s /usr/local/python3.8.0/bin/pip3.8 /usr/bin/
ln -s /usr/local/python3.8.0/bin/pyvenv-3.8 /usr/bin/
```

如果重新编译，可以执行make clean。

## UWSGI

打包并安装项目：
```
pip3.8 install dist/reborn-x.x.tar.gz
```

如果没有将项目打包成tar.gz则先下载项目源码，然后进入项目主目录进行打包，然后复制出dist文件夹中的tar.gz文件，上传到服务器上安装即可。

```
git clone https://github.com/zswj123/reborn
cd reborn
python3.8 setup sdist
cd dist
scp reborn-x.x.tar.gz [用户名]@[主机名]:[上传到主机的路径]
ssh [用户名]@[主机名]
cd 上传到主机的路径
pip3.8 install reborn-x.x.tar.gz
```

安装uwsgi并用uwsgi启动项目：
```
pip3.8 install uwsgi
ln -s /usr/local/python3.8.0/bin/uwsgi /usr/bin/
uwsgi --http 0.0.0.0:5000 --module reborn.apps:APP
```

这种方式并不好，耦合度太高，增加了用户部署项目的复杂度。

## SUPERVISOR

安装supervisor：
```bash
sudo apt install supervisor
```

进程监控配置：
```ini
[program:{进程名}]
process_name=%(program_name)s_%(process_num)02d;
command=uwsgi --http 0.0.0.0:80 --module reborn.apps.[包名]:APP
priority=1
numprocs=1
autostart=true
autorestart=true
startretries=3
redirect_stderr=true
stdout_logfile=/var/log/%(program_name)s_%(process_num)02d.log
```

启动进程监控服务：
```
sudo supervisord
```

默认，进程监控服务启动的时候就会启动配置文件管理的进程，如果失败，可以在进程监控状态看到，另外，可以在
/var/log目录下查看supervisord的服务log。更多信息，请前往项目官方文档。

如果修改了配置文件，则需要重新加载配置文件：
```
supervisorctl reload
```

查看进程运行的状态：
```
supervisorctl status
```

重启进程监控下的所有进程：
```
supervisorctl restart all
```

## PYPI-SERVER

由于使用的都是第三方库开发的软件，所以不得不对这些包进行备份，以防止某一天这些库不能用了。

安装pypi-server：
```bash
pip3.8 install pypi-server
ln -s /usr/local/python3.8.0/bin/pypi-server /usr/bin/
mkdir /root/packages

pypi-server -p 9000 /root/packages
```

再下载一个库到`/root/packages`中：
```bash
cd /root/packages
pip3.8 download aiohttp
```

测试：
```bash
pip3.8 install aiohttp -i http://106.12.7.49:9000/simple
```

更新所有的包：
```bash
pypi-server -U
```

pypi-server的官方说明：https://pypi.org/project/pypiserver/

## STATIC-FILE-SERVER

搭建静态文件服务器。

```bash
cd /root
mkdir downloads

cd /root/downloads
python3.8 -m http.server 5000
```

需要注意的是启动必须cd到要提供静态文件服务的目录才能。

这样搭建的静态文件服务，在web页面只能下载不能上传。如果需要增加文件，可以使用bash命令行将文件复制到这个目录中即可。

浏览器中访问http://localhost:5000即可查看所有的目录。

## RABBITMQ

消息队列，如果不做存储，只做消息转发，这个消息队列应该是最优秀的消息队列了。

```bash
apt install rabbitmq-server

sudo rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server restart

rabbitmqctl add_user admin admin 
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*" 
rabbitmqctl list_users
```

浏览器访问http://localhost:15672，输入admin/admin登录，然后删掉guest用户。

## 主机安全加固

禁止任何非本MAC地址的机器访问ssh服务：
```bash
iptables -A INPUT -s 0.0.0.0/0 -p tcp --dport 22 -j DROP
iptables -A INPUT -p tcp --dport 22 -m mac --mac-source 30:35:ad:a2:98:ce -j ACCEPT
```
上面是错的，基于mac地址是不可能实现的。禁用ip还是可以用。

### T用户下线

使用who查看目前有哪些用户登录了服务器:
```bash
$ who
root     pts/0        2015-03-27 10:23 (192.168.9.188)
```

看看root都在什么时间登录过系统 
```
$ last root
root     pts/0        192.168.9.188    Fri Mar 27 10:23   still logged in    
```
 
使用pkill -kill -t pts/0命令踢出第一个用户，即强制下线。
```bash
$ pkill -kill -t pts/0
```
