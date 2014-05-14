---
title: "daemontools"
date: 2013-09-06 19:06
---


daemontools is a collection of tools for managing UNIX services.

它用于监控服务的运行状态, 如果服务退出, 则会自动重启服务, 以保证服务的正常运行.


## 使用 ##

### Gentoo ###
emerge 安装 `sys-process/daemontools` 后, 它自动在 `/分区` 下新建一个 `/service` 目录. 

`svscan` 服务会对这个目录下的子目录作检测, 如果子目录里有 `run` sh脚本, 则会使用 `supervise` 启动它.

注意 run 脚本要加上 **可执行** 权限.

所以只需要把要管理的服务在 `/service` 下, 把 svscan 加入到启动项, 就可以了.

参考: [Service creation](http://cr.yp.to/daemontools/faq/create.html)

daemontools 还有一些工具, 如 `svc`, `svstat` 等

`svc` 用于控制单个服务的 up, down, pause, continue, hangup 等:

	svc -h /service/yourdaemon: sends HUP 
	svc -t /service/yourdaemon: sends TERM, and automatically restarts the daemon after it dies 
	svc -d /service/yourdaemon: sends TERM, and leaves the service down 
	svc -u /service/yourdaemon: brings the service back up 
	svc -o /service/yourdaemon: runs the service once

`svstat` 用于查看某个服务的状态, 比如:

	» sudo svstat /service/test
	/service/test: up (pid 1541) 1 seconds

### Ubuntu ###
<strike>安装了 daemontools, 发现并没有自动新建 `/service` 目录, 也没有启动脚本...</strike>

ubuntu 有个 `daemontools-run` 程序, 我原先是把服务放在自己新建的 /service 下的, 安装后, 它会建立 `/etc/service` 这个目录, 并把 /service 的内容 mv 过去, 然后 `ln -s` 建一个软连接到 /service, 如果开始没有新建 /service 目录, 则不会做软连接.

装好 daemontools-run 后, 还会创建启动脚本 `/etc/init/svscan.conf`.

可参考:

* [Manage your services with Daemontools](http://isotope11.com/blog/manage-your-services-with-daemontools)
* [How to start daemontools](http://cr.yp.to/daemontools/start.html)

网上找了两个启动脚本:

* [Configuring Daemontools for Ubuntu 10](https://gist.github.com/gregory80/563598)
* [chkconfig-compatible init script for daemontools / svscan](https://blog.darmasoft.net/2011/06/24/chkconfig-compatible-daemontools-init-script.html)

## 参考链接 ##

* [官方网站](http://cr.yp.to/daemontools.html) (官网里的资料都非常有用)
* [Manage your services with Daemontools](http://isotope11.com/blog/manage-your-services-with-daemontools)
* [使用daemontools确保指定进程的运行](http://idaemon.net/post-797.html)
* [Daemontools: Tutorial](http://blog.teksol.info/pages/daemontools/tutorial)
