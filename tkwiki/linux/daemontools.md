# daemontools #

daemontools is a collection of tools for managing UNIX services.

它用于监控服务的运行状态, 如果服务退出, 则会自动重启服务, 以保证服务的正常运行.

在这次写 [wiki](https://github.com/tankywoo/wiki) 的监控程序时, 想要把他当做一个守护进程来运行, 先开始用的是 `pyinotify` 自带的 `daemonize` 参数, 后来老大给我推荐 `daemontools` 这个工具, 感觉实在太好用了.


## 使用 ##

### Gentoo ###
emerge 安装 `sys-process/daemontools` 后, 它自动在 `/分区` 下新建一个 `/service` 目录. `svscan` 服务会对这个目录下的子目录作检测, 如果子目录里有 `run` sh脚本, 则会使用 `supervise` 启动它.

所以只需要把要管理的服务在 `/service` 下, 把 svscan 加入到启动项, 就可以了.

参考: [Service creation](http://cr.yp.to/daemontools/faq/create.html)

### Ubuntu ###
安装了 daemontools, 发现并没有自动新建 `/service` 目录, 也没有启动脚本...

可参考 [Manage your services with Daemontools](http://isotope11.com/blog/manage-your-services-with-daemontools)



## 参考链接 ##

* [官方网站](http://cr.yp.to/daemontools.html) (官网里的资料都非常有用)
* [Manage your services with Daemontools](http://isotope11.com/blog/manage-your-services-with-daemontools)
* [使用daemontools确保指定进程的运行](http://idaemon.net/post-797.html)
* [Daemontools: Tutorial](http://blog.teksol.info/pages/daemontools/tutorial)

## 历史日志 ##

* 2013-08-25 : 创建
