# INSTALL

Ubuntu操作系统下，项目环境搭建。

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