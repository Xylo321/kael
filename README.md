# REBORN

[文档](http://serv_pro:5000/reborn/ "文档")
[安装](http://serv_pro:3000/zswj123/reborn/src/master/INSTALL.md "安装")
[百度](http://serv_pro:3000/zswj123/reborn/src/master/PROJECT.md "百度")

基于FLASK构建自己的WEB应用。

## APP:SEARCH

想做一个自己想要的搜索，基于现实的批判和与机器的攀比。

![](http://serv_pro:3000/zswj123/reborn/raw/master/search.png)

## APP:BLOG

博客的设计灵感来自于我携带多年的书籍《且以永日》的外表和VIM。

![](http://serv_pro:3000/zswj123/reborn/raw/master/blog.png)

## APP:IMAGE

用于为博客提供图片资源服务的图片管理系统。

![](http://serv_pro:3000/zswj123/reborn/raw/master/image.png)

## APP:VIDEO

用于为自己播放想要的视频。

![](http://serv_pro:3000/zswj123/reborn/raw/master/video.png)

## Future

1. 更新博客中引用图片的地址；
2. 视频搜索，数据拉取，数据抓取；
3. 用户提交视频文件名称，然后，根据视频文件名称再获取这个文件的第一帧的图片就行了；
4. 做完这个后，需要考虑接入自己mingmq的项目了，另外，还需要开始爬数据，首先是将pika的代码全都换程自己的mingmq，然后再考虑编写视频爬虫；
5. 由于浏览器无法支持所有的视频格式的视频，所以我统一将所有的非flv视频全部转换成flv格式；
6. 由于opencv无法安装，所以无法提取视频的第一帧图片，所以搜索视频结果中无法显示图片；