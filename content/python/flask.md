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

## Flask-SQLAlchemy ##

逆序排序desc:

	Blog.query.order_by(Blog.date.desc()).all()

或者:

	Blog.query.order_by(db.desc(Blog.date)).all()


## 部署 ##

### Nginx ###

    server {
        listen       80;
        server_name  localhost;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:/tmp/uwsgi.sock;
        }
    }

或者参考[Flask - uWSGI](http://flask.pocoo.org/docs/0.10/deploying/uwsgi/#configuring-nginx)文档:

    location / { try_files $uri @yourapplication; }
    location @yourapplication {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/uwsgi.sock;
    }

将`yourapplication`改为实际的包或模块名.

这里使用了location的`@`语法, 参考[nginx文档](http://wiki.nginx.org/NginxHttpCoreModule#location)

> The prefix "@" specifies a named location. Such locations are not used during normal processing of requests, they are intended only to process internally redirected requests (see error_page, try_files).

### uWSGI ###

安装[uwsgi](https://uwsgi-docs.readthedocs.org/en/latest/)

执行命令:

    uwsgi -s /tmp/uwsgi.sock --chmod-sock=666 --pythonpath /path/to/project/root --module yourmodulename --callable app

其中:

* `--pythonpath` 将模块(包)的父目录加到PYTHONPATH, 否则无法搜到相应的模块
* `--module` load a WSGI module
* `--callable` set default WSGI callable name, 一般因为`app = Flask(__name__)`, 所以这里配置app
* `--module yourmodulename --callable app` 也可以简写为 `-w yourmodulename:app`

如果使用了virtualenv, 当没有active这个virtualenv时, 需要用`H|--home|--virtualenv|--venv|--pyhome`指定virtualenv的路径

也可以写成配置文件, 如ini, xml等:

	$ cat uwsgi_example.ini
	[uwsgi]
	# application's base folder
	base =

	# python module to import
	app = blogwall
	module = %(app)

	# set PYTHONHOME/virtualenv
	# if use virtual, set this option
	#home =
	# add directory (or glob) to pythonpath
	pythonpath = %(base)

	# socket file's location
	socket =

	# permissions for the socket file
	chmod-socket = 666

	# the variable that holds a flask application inside the module imported at line #6
	callable = app

	# location of log files
	logto =

详细可参考[uWSGI配置文档](http://uwsgi-docs.readthedocs.org/en/latest/Configuration.html)

其它一些参考文档:

* Serving Flask With Nginx [en](http://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/) | [zh](http://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu)
* [Deploying Flask With Nginx](http://flaviusim.com/blog/Deploying-Flask-with-nginx-uWSGI-and-Supervisor/) 里面提到了使用supervisor管理
* [flask-uwsgi](https://github.com/mking/flask-uwsgi) Tutorial for setting up Flask with uWSGI + Nginx


## FAQ ##

运行Flask自带的example [flaskr](https://github.com/mitsuhiko/flask/tree/master/examples/flaskr), 提示:

	AttributeError: 'Flask' object has no attribute 'cli'

原因是flask命令行方式在dev版才支持, [issue](https://github.com/mitsuhiko/flask/issues/1048)
