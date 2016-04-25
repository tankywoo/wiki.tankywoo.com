---
title: "cgroup"
date: 2016-04-25 22:50
collection: "系统工具"
log: "简单总结"
---

[TOC]

`Control Group`的简写。

> cgroups (abbreviated from control groups) is a Linux kernel feature that limits, accounts for, and isolates the resource usage (CPU, memory, disk I/O, network, etc.) of a collection of processes.

(摘自[维基百科](https://en.wikipedia.org/wiki/Cgroups))

通过cgroups, 可以对cpu使用率、内存、网络带宽等资源进行控制(限额)。

## 安装 ##

首先需要保证内核开启了cgroups的支持。

Gentoo下:

	$ emerge -auv dev-libs/libcgroup

安装的二进制工具:

	$ equery files libcgroup | grep 'bin/'
	/usr/bin/cgclassify
	/usr/bin/cgcreate
	/usr/bin/cgdelete
	/usr/bin/cgexec
	/usr/bin/cgget
	/usr/bin/cgset
	/usr/bin/cgsnapshot
	/usr/bin/lscgroup
	/usr/bin/lssubsys
	/usr/sbin/cgclear
	/usr/sbin/cgconfigparser
	/usr/sbin/cgrulesengd

相应的控制器都会分别挂载上:

	$ cat /proc/mounts | grep cgroup
	cgroup_root /sys/fs/cgroup tmpfs rw,nosuid,nodev,noexec,relatime,size=10240k,mode=755 0 0
	openrc /sys/fs/cgroup/openrc cgroup rw,nosuid,nodev,noexec,relatime,release_agent=/lib64/rc/sh/cgroup-release-agent.sh,name=openrc 0 0
	cpuset /sys/fs/cgroup/cpuset cgroup rw,nosuid,nodev,noexec,relatime,cpuset 0 0
	cpu /sys/fs/cgroup/cpu cgroup rw,nosuid,nodev,noexec,relatime,cpu 0 0
	cpuacct /sys/fs/cgroup/cpuacct cgroup rw,nosuid,nodev,noexec,relatime,cpuacct 0 0
	blkio /sys/fs/cgroup/blkio cgroup rw,nosuid,nodev,noexec,relatime,blkio 0 0
	memory /sys/fs/cgroup/memory cgroup rw,nosuid,nodev,noexec,relatime,memory 0 0
	devices /sys/fs/cgroup/devices cgroup rw,nosuid,nodev,noexec,relatime,devices 0 0
	freezer /sys/fs/cgroup/freezer cgroup rw,nosuid,nodev,noexec,relatime,freezer 0 0
	net_cls /sys/fs/cgroup/net_cls cgroup rw,nosuid,nodev,noexec,relatime,net_cls 0 0
	perf_event /sys/fs/cgroup/perf_event cgroup rw,nosuid,nodev,noexec,relatime,perf_event 0 0
	net_prio /sys/fs/cgroup/net_prio cgroup rw,nosuid,nodev,noexec,relatime,net_prio 0 0
	hugetlb /sys/fs/cgroup/hugetlb cgroup rw,nosuid,nodev,noexec,relatime,hugetlb 0 0


## 命令 ##

### cgcreate ###

新建cgroup(s)，最简单是只使用`-g`参数:

	cgcreate -g <controllers>:<path>

如:

	$ cgcreate -g cpu:/cpulimited

其中cpu是控制的类型, /cpulimited是相对于指定controller(这里是cpu)的cgroup的路径:

	$ tree /sys/fs/cgroup/cpu/cpulimited
	/sys/fs/cgroup/cpu/cpulimited
	├── cgroup.clone_children
	├── cgroup.procs
	├── cpu.cfs_period_us
	├── cpu.cfs_quota_us
	├── cpu.rt_period_us
	├── cpu.rt_runtime_us
	├── cpu.shares
	├── cpu.stat
	├── notify_on_release
	└── tasks

	0 directories, 10 files


### cgset ###

配置指定cgroup(s)的参数:

	cgset [-r <name=value>] <cgroup_path>

如:

	$ cgset -r cpu.shares=512 cpulimited

其中`cpu.shares`用于控制cpu的使用率，默认是1024，这里设置为其一般，则当其它资源也要使用全部的cpu时，会和这个控制组下的进程以2:1分配资源。

	$ cd /sys/fs/cgroup/cpu/cpulimited
	$ cat cpu.shares
	1024
	$ cgset -r cpu.shares=512 cpulimited
	$ cat cpu.shares
	512


### cgexec ###

在指定的cgroup(s)中执行任务:

	cgexec [-g <controllers>:<path>] command

如:

	$ cgexec -g cpu:cpulimited matho-primes 0 9999999999 > /dev/null

这里`matho-primes`是质数生成器，用来CPU负载测试。


### lscgroup ###

列出所有的cgroups。

本机上的结果:

	$ lscgroup
	name=openrc:/
	name=openrc:/sshd
	name=openrc:/udev
	name=openrc:/nginx
	name=openrc:/samba
	name=openrc:/vixie-cron
	name=openrc:/rsyslog
	name=openrc:/lvmetad
	name=openrc:/svscan
	cpuset:/
	cpu:/
	cpu:/cpulimited    # 这个是先前手动建立的
	cpuacct:/
	blkio:/
	memory:/
	devices:/
	freezer:/
	net_cls:/
	perf_event:/
	net_prio:/
	hugetlb:/

TODO: 其它是内置的?


### cgdelete ###

删除指定的cgroup(s)。

	cgdelete [[-g] <controllers>:<path>]

没指定`<controllers>:<path>`则会删除所有自定义添加的；`-g`可写可不写:

	$ cgdelete cpu:/cpulimited

可以通过`lscgroup`来确认。


### cgclear ###

卸载cgroup文件系统


## 例子 ##

基于上面的配置，在控制组下只运行一个matho-primes进程时，cpu占用率是100%:

	 PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command
	6375 root       20   0  9080  3344  1456 R 100.  0.2  0:13.20 matho-primes 0 9999999999

然后额外运行一个matho-primes进程(非cgroup下):

	 PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command
	6761 root       20   0  9080  3240  1344 R 67.0  0.2  0:03.16 matho-primes 0 9999999999
	6375 root       20   0  9080  3344  1456 R 33.0  0.2  2:15.17 matho-primes 0 9999999999

可以看到，新开的进程(pid 6761)的cpu使用率是前者的两倍。


## TODO ##

通过`cgclear`卸载文件系统后，如果不重启的情况下恢复？

	service cgconfig start

未解决问题。

看是inittab有控制cgroup。

另外/etc/配置文件这块需要了解。


## 参考 ##

* [RESTRICTING PROCESS CPU USAGE USING NICE, CPULIMIT, AND CGROUPS](http://blog.scoutapp.com/articles/2014/11/04/restricting-process-cpu-usage-using-nice-cpulimit-and-cgroups)
* [使用 nice、cpulimit 和 cgroups 限制 cpu 占用率](https://linux.cn/article-4742-1.html) 上面的翻译版
* [Docker基础技术：Linux CGroup](http://coolshell.cn/articles/17049.html)
* [HowTo: CGroups](https://www.cloudsigma.com/howto-cgroups/)
* [How to limit CPU consumtion of a process group with standard GNU/Linux tools?](http://superuser.com/questions/921086/how-to-limit-cpu-consumtion-of-a-process-group-with-standard-gnu-linux-tools)
* [How To Limit CPU Usage On Ubuntu 12.10](https://www.digitalocean.com/community/tutorials/how-to-limit-cpu-usage-on-ubuntu-12-10)
* [cpulimit](https://github.com/opsengine/cpulimit)
* [cpulimit: 限制进程的 CPU 占用率](https://linuxtoy.org/archives/cpulimit.html)
* [How to create a CPU spike with a bash command](http://stackoverflow.com/questions/2925606/how-to-create-a-cpu-spike-with-a-bash-command)
