---
title: "Flask Primer"
date: 2015-05-28 08:00
---

[TOC]


## 文档 ##

* Flask官方文档 [en](http://flask.pocoo.org/docs/0.10/) | [zh](http://docs.jinkan.org/docs/flask/)
* Explore Flask [en](https://exploreflask.com/index.html) | [zh-1](http://www.pythondoc.com/exploreflask/preface.html) | [zh-2](http://spacewander.github.io/explore-flask-zh/index.html)
* The Flask Mega-Tutorial [en](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) | [zh](http://www.oschina.net/translate/the-flask-mega-tutorial-part-i-hello-world)
* [Flask Web开发](http://book.douban.com/subject/26274202/)
* [Discover Flask](https://github.com/realpython/discover-flask) 扫了一眼, 发现基本是视频教程
* [Awesome Flask](https://github.com/humiaozuzu/awesome-flask) Flask资源汇总大全

[Miguel Grinberg](https://github.com/miguelgrinberg)的[博客](http://blog.miguelgrinberg.com/)内容很多, 上面的The Flask Mega-Tutorial就是其博客上的在线教程, Flask Web开发是他出的书, 有中文版.


## FAQ ##

运行Flask自带的example [flaskr](https://github.com/mitsuhiko/flask/tree/master/examples/flaskr), 提示:

	AttributeError: 'Flask' object has no attribute 'cli'

原因是flask命令行方式在dev版才支持, [issue](https://github.com/mitsuhiko/flask/issues/1048)
