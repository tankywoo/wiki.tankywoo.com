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

注: Ubuntu下, 默认配置在 `/etc/supervisor/`, 安装后就存在一些基本配置

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


## 配置文件 ##

(**NOTE** 下面代码直接用Gist贴的，加载会很缓慢)

<script src="https://gist.github.com/tankywoo/603cb17f49f8c3114b22.js"></script>

配置文件更多参考: [Configuration File](http://supervisord.org/configuration.html)

它的配置是Windows-INI格式(Python ConfigParser). 初始情况下可以先用 `echo_supervisord_conf` 输出后再根据需求编辑.

首先注释使用分号 `;`, 并且如果注释是和配置项在同一行, 则分号前面必须有一个前置空格.

不支持SHELL的环境变量, 如 `~` 和 `$HOME`, 可以用 `%(ENV_HOME)s` 替代.

首先配置分为几大块(section):

`unix_http_server` 和 `inet_http_server` 是配置supervisor的http server, 至少需要其一, supervisorctl管理时用到.

`supervisord` 用于对守护进程的全局性配置, 有些配置可以在 `program` 块覆盖

`supervisorctl` 用于supervisorctl管理supervisor服务的配置, 如serverurl 等, 这些也可以直接命令行指定参数, 比如如果在上面配置的是 `inet_http_server` , 则这里配置 `serverurl` 为相应路径后, 则直接使用 `supervisorctl` 命令即可, 否则要指定命令行参数.

`program` 是最主要的配置部分. 关于这块, 首先要提到的是状态, 详细可参考 [Supervisor - Process States](http://supervisord.org/subprocess.html#process-states)

![](http://supervisord.org/_images/subprocess-transitions.png)

其中 `BACKOFF` 状态是启动时退出太快, 根据 `startretries` 达到重试次数后, 会进入到 `FATAL` 状态.

如果状态在 `EXITED`, 如果配置了 `autorestart=false`, 则停留在此状态不再重启; 如果 `autorestart=true`, 则会一直重启; 如果 `autorestart=unexpected`, 则如果exitcode在 `exitcodes` 配置的列表里, 则不再重启, 否则重启

如果状态在 `FATAL` , 则永远不会再自动重启.

如果执行了 `supervisorctl stop` 命令, 则会进入 `STOP` 状态. 并且在 `stopwaitsecs` 秒后发送 `SIGKILL` 信号.

另外观察到, 在 `startretries` 重试次数达到之前, 如果频繁在 `BACKOFF` 和 `STARTING` 或 `RUNNING` 状态之间切换, 则重启等待时间会逐步增大.

`include` 块用于加载一些自定义配置, 一般 `/etc/supervisord.conf` 可以用于一些全局配置, 然后每个服务一个单独的 `program` 配置, 用include导入, 类似于nginx等配置.

`group` 块用于把一些 `program` 分为一个组, 然后做一些基本配置.

`rpcinterface` 用于自定义一些接口, 这个一般保持默认就行, 但是不能删除, 必须保留在配置文件中.

## 与daemontool对比 ##

* [Server Monitoring: How does supervisord compare to daemontools?](http://www.quora.com/Server-Monitoring/How-does-supervisord-compare-to-daemontools)
* [Ask HN: keeping services up and running?](https://news.ycombinator.com/item?id=1368855)

Tornado配合Supervisor非常好用，尝试用daemontools对一个Tornado程序开多个端口，必须每个端口一个目录，没有Supervisor直观和方便, 且用户权限上后者也比较方便.
