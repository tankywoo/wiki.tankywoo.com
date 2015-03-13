---
title: "Supervisord"
date: 2014-12-04 15:31
---

> [Supervisor](http://supervisord.org/) is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.

Supervisor是一个Python写的工具, 可以用系统的包管理器安装, 也可以通过`pip`或`easy_install`安装.

当前测试的版本是`3.1.3`. 安装后有几个工具:

	tankywoo@gentoo-local::~/ » equery files supervisor | grep 'bin\/'
	/usr/bin/echo_supervisord_conf
	/usr/bin/pidproxy
	/usr/bin/supervisorctl
	/usr/bin/supervisord

`echo_supervisord_conf` 是一个自动生成默认配置的工具, 没有任何参数选项, 输出是/dev/stdout.

因为supervisor默认使用的配置在`/etc/supervisord.conf`, 可以重定向默认配置到这，然后根据具体需求修改:

	echo_supervisord_conf > /etc/supervisord.conf

其中 `supervisord` 是一个守护进程, 用于控制服务的启动和相关的一些全局设置.

> supervisord -- run a set of applications as daemons.

`supervisorctl` 控制由supervisord运行的程序.

> supervisorctl -- control applications run by supervisord from the cmd line.

直接运行程序进入交互式命令行模式，调试服务非常方便(实际运行中两条命令间并没有空行, 此为查看方便):

	# 进入交互式模式, 会提示当前管理的服务状态
	$ supervisorctl
	captcha2022                      RUNNING   pid 18356, uptime 17:24:16
	captcha2023                      RUNNING   pid 13961, uptime 0:17:40

	# 查看可用的命令
	supervisor> help

	default commands (type help <topic>):
	=====================================
	add    clear  fg        open  quit    remove  restart   start   stop  update
	avail  exit   maintail  pid   reload  reread  shutdown  status  tail  version

	# help <cmd> 可以查看相关命令的用法
	supervisor> help status
	status <name>           Get status for a single process
	status <gname>:*        Get status for all processes in a group
	status <name> <name>    Get status for multiple named processes
	status                  Get all process status info

	# status 命令查看当前管理的服务状态, 确认服务是正常运行的RUNNING状态
	supervisor> status
	captcha2022                      RUNNING   pid 18356, uptime 17:24:20
	captcha2023                      RUNNING   pid 13961, uptime 0:17:44

	# 修改配置后, 执行 update 命令更新状态, 非常方便
	supervisor> update
	captcha2023: stopped
	captcha2023: updated process group

	# update后再次确认服务状态
	supervisor> status
	captcha2022                      RUNNING   pid 18356, uptime 17:25:03
	captcha2023                      RUNNING   pid 16872, uptime 0:00:03

	supervisor>

当然，也可以直接在SHELL终端执行命令:

	$ supervisorctl help

	default commands (type help <topic>):
	=====================================
	add    clear  fg        open  quit    remove  restart   start   stop  update
	avail  exit   maintail  pid   reload  reread  shutdown  status  tail  version

	$ supervisorctl status
	captcha2022                      RUNNING   pid 18356, uptime 17:32:56
	captcha2023                      RUNNING   pid 16872, uptime 0:07:56

	$ supervisorctl update
	captcha2023: stopped
	captcha2023: updated process group


## 关于配置这块 ##

(**NOTE** 下面代码直接用Gist贴的，加载会很缓慢)

<script src="https://gist.github.com/tankywoo/603cb17f49f8c3114b22.js"></script>


## 与daemontool对比 ##

* [Server Monitoring: How does supervisord compare to daemontools?](http://www.quora.com/Server-Monitoring/How-does-supervisord-compare-to-daemontools)
* [Ask HN: keeping services up and running?](https://news.ycombinator.com/item?id=1368855)

Tornado配合Supervisor非常好用，尝试用daemontools对一个Tornado程序开多个端口，必须每个端口一个目录，没有Supervisor直观和方便, 且用户权限上后者也比较方便.
