<!-- title : inotify -->

# inotify #

Inotify是一种文件变化通知机制, Linux内核从 2.6.13 开始引入.

在使用前, 需要先检查内核是否开启了inotify的支持:

	# /path/to/kernel_config 是内核的配置文件
	# 比如在gentoo下, 是 `/usr/src/linux/.config` 这个文件
	grep INOTIFY_USER /path/to/kernel_config

如果显示 `CONFIG_INOTIFY_USER=y` 则表示已开启支持.

# inotify-tools #


# pyinotify #

[pyinotify](https://github.com/seb-m/pyinotify) 是一个 Python 的模块, 用于监控文件系统变化, 它基于 Linux Kernel 的 inotify 特性.

安装好 pyinotify 后, 可以测试一下:

	python -m pyinotify -v /my-dir-to-watch

可以把 pyinotify 模块当一个脚本来执行. 然后 cd 到 /my-dir-to-watch, 就会看见监控窗口有一系列的事件日志显示.

pyinotify 的 [wiki](https://github.com/seb-m/pyinotify/wiki) 讲的非常详细.

# 参考资料 #

* [Inotify: 高效、实时的Linux文件系统事件监控框架](http://www.infoq.com/cn/articles/inotify-linux-file-system-event-monitoring)
* [pyinotify wiki](http://github.com/seb-m/pyinotify/wiki)
* [IBM - 用 inotify 监控 Linux 文件系统事件](http://www.ibm.com/developerworks/cn/linux/l-inotify/)
* [inotify+rsync实现触发式文件同步](http://www.517sou.net/Article/367.aspx)
* [linux inotify 监控文件系统事件](http://www.51know.info/system_security/inotify.html)

# 修改历史 #

* 2013-08-16 : 创建
