---
title: "inotify"
date: 2013-09-06 19:06
---


Inotify是一种文件变化通知机制, Linux内核从 2.6.13 开始引入.

## 内核支持 ##

在使用前, 需要先检查内核是否开启了inotify的支持:

```bash
# /path/to/kernel_config 是内核的配置文件
# 比如在gentoo下, 是 `/usr/src/linux/.config` 这个文件
grep INOTIFY_USER /path/to/kernel_config
```

如果显示 `CONFIG_INOTIFY_USER=y` 则表示内核的配置里已开启支持.

然后看看 `/proc/sys/fs/inotify` 目录:

```bash
9:50 root@gentoo-jl /root
% ll /proc/sys/fs/inotify
total 0
dr-xr-xr-x 1 root root 0 Aug 18 07:07 .
dr-xr-xr-x 1 root root 0 Aug 18 06:42 ..
-rw-r--r-- 1 root root 0 Aug 18 07:07 max_queued_events
-rw-r--r-- 1 root root 0 Aug 18 07:07 max_user_instances
-rw-r--r-- 1 root root 0 Aug 18 07:07 max_user_watches
```

确保有这三个文件.

> /proc/sys/fs/inotify/max\_queued\_events  
> 默认值: 16384 该文件中的值为调用inotify\_init时分配给inotify instance中可排队的event的数目的最大值，超出这个值得事件被丢弃，但会触发IN\_Q\_OVERFLOW事件  
> The value in this file is used when an application calls inotify\_init(2) to set an upper limit on the number of events that can be queued to the corresponding inotify instance. Events in excess of this limit are dropped, but an IN\_Q\_OVERFLOW event is always generated.  

> /proc/sys/fs/inotify/max\_user\_instances  
> 默认值: 128 指定了每一个real user ID可创建的inotify instatnces的数量上限  
> This specifies an upper limit on the number of inotify instances that can be created per real user ID.  

> /proc/sys/fs/inotify/max\_user\_watches  
> 默认值: 8192 指定了每个inotify instance相关联的watches的上限  
> This specifies a limit on the number of watches that can be associated with each inotify instance.  

参考 [LinuxInsight](http://www.linuxinsight.com/proc_sys_fs_inotify.html)

可以通过 `echo` 或 `sysctl` 更改这些值. 

* [参考1](http://forums.slimdevices.com/showthread.php?78939-SbS-7-6-inotify-What-are-max_user_watches)
* [参考2](http://askubuntu.com/questions/148171/dropbox-error-echo-100000-sudo-tee-proc-sys-fs-inotify-max-user-watches)


注意: max\_queued\_events 是 Inotify 管理的队列的最大长度，文件系统变化越频繁，这个值就应该越大 

如果你在日志中看到Event Queue Overflow，说明max\_queued\_events太小需要调整参数后再次使用.

## inotify-tools ##

包含两个工具:

* inotifywait : wait for changes to files using inotify
* inotifywatch : gather filesystem access statistics using inotify


## pyinotify ##

[pyinotify](https://github.com/seb-m/pyinotify) 是一个 Python 的模块, 用于监控文件系统变化, 它基于 Linux Kernel 的 inotify 特性.

安装好 pyinotify 后, 可以测试一下:

```bash
python -m pyinotify -v /my-dir-to-watch
```

可以把 pyinotify 模块当一个脚本来执行. 然后 cd 到 /my-dir-to-watch, 就会看见监控窗口有一系列的事件日志显示.

pyinotify 的 [wiki](https://github.com/seb-m/pyinotify/wiki) 讲的非常详细.

还有一些 inotify 的`坑`, pyinotify 的作者已经列举了这些常见的问题: [Frequently Asked Questions](https://github.com/seb-m/pyinotify/wiki/Frequently-Asked-Questions)


## 参考资料 ##

* [Inotify: 高效、实时的Linux文件系统事件监控框架](http://www.infoq.com/cn/articles/inotify-linux-file-system-event-monitoring)
* [pyinotify wiki](http://github.com/seb-m/pyinotify/wiki)
* [IBM - 用 inotify 监控 Linux 文件系统事件](http://www.ibm.com/developerworks/cn/linux/l-inotify/)
* [inotify+rsync实现触发式文件同步](http://www.517sou.net/Article/367.aspx)
* [linux inotify 监控文件系统事件](http://www.51know.info/system_security/inotify.html)
