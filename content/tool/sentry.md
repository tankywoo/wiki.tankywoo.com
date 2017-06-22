---
title: "Sentry"
date: 2017-06-21 15:18
collection: "日志管理"
log: "新增"
---

[TOC]

## 简介 ##

Sentry 是一个跨平台的日志收集、聚合的平台。

它自身的 UI Web Server 是用 Python（Django）写的，所以可以使用 pip 直接安装（当然，官方推荐是使用 Docker）。不过它的API有很多语言的实现版本，所以使用上并不限于 Python。

* [项目主页](https://github.com/getsentry/sentry)
* [官网](https://sentry.io)
* [文档](https://docs.sentry.io/)


## 部署 ##

参考：[Installation](https://docs.sentry.io/server/installation/)

* 系统：Gentoo
* Sentry版本：8.17.0

部署选择了 pip 安装，所以更具体的可以参考 [Installation with Python](https://docs.sentry.io/server/installation/python/)

部署前需要一些基本的服务：

* PostgreSQL
* Redis
* 本机域名

关于 PostgreSQL，可以更改为 MySQL，之前没有接触 Sentry，不过看一些资料，貌似以前默认使用 MySQL？目前的文档都没有提使用 MySQL，不过使用了的 Django，可以通过配置 db engine 改为 mysql 即可。

但是，因为 Sentry 有个依赖包 `psycopg2`，而这个包安装时如果没有 `pg_config` 命令，则报错进而导致 Sentry 安装失败。我为了偷懒还是先装上了 PostgreSQL。不想装 PG 的话可以试试将项目克隆下来，修改 `setup.py` 去掉 `psycopg2` 这个依赖包，我没去实际测试，但是问题不大，除非还有级联的依赖等。

改用 MySQL 的话记得安装 `mysql-python` 包。

将 MySQL 起来，建立一个数据库，考虑安全性的话可以考虑增加一个专用的数据库用户。

安装完 Sentry 后生成配置：

```
sentry init <sentry_config_dir>
```

里面会生成 `sentry.conf.py` 和 `config.yml` 两个配置文件，前者配置 PostgreSQL/MySQL 等，后者配置 Redis 和一个加密私钥。

```
# sentry.conf.py 中 MySQL 配置相关
DATABASES = {
    'default': {
        # 'ENGINE': 'sentry.db.postgres' ,
        'ENGINE': 'django.db.backends.mysql' ,
        'NAME': 'sentry',
        'USER': 'sentry',
        'PASSWORD': 'xxxxxxxx',
        'HOST': '',
        'PORT': '',
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
    }
}

# config.yml 中加密私钥和 Redis 相关
system.secret-key: 'a random string'

redis.clusters:
  default:
    hosts:
      0:
        host: 127.0.0.1
        port: 6379
        password: xxxxxxxx
```

文档里写：

> Starting with 8.0.0, init now creates two files, sentry.conf.py and config.yml. To avoid confusion, config.yml will slowly be replacing sentry.conf.py, but right now, the uses of config.yml are limited.

最开始我还以为目前暂时还是使用 `sentry.conf.py`，结果是两个都需要配置……

然后初始化创建数据表，并会创建用户：

```
sentry --config <sentry_config_dir> upgrade
```

这块用到的 Python 包 `symsynd`，里面会用到 `libncurses.so.5`，先开始我本地装的是 `ncurses 6.x` 的版本导致找不到动态库，所以需要安装 `ncurses 5.x` 的版本。

运行 Web 服务，通过 `http://x.x.x.x:9000` 访问测试：

```
SENTRY_CONF=<sentry_config_dir> sentry run web
```

在运行时点击 Members 时发现连接报错：

> ResponseError: NOAUTH Authentication required.

这个是 `sentry.conf.py` 中的配置：

```
BROKER_URL = 'redis://:<password>@localhost:6379'
```

因为 redis 配置了密码，所以这里也需要指定，注意前面的冒号，因为 redis 没有用户的概念。参考了[这个](https://github.com/niwinz/django-redis/issues/112)和[这个](https://github.com/getsentry/sentry/issues/2655)才想起来这里没有配置密码。

最后线上正式部署时，可以配合 `Supervisord` 来使用。记得同时启动 `sentry run worker` 和 `sentry run cron`。
