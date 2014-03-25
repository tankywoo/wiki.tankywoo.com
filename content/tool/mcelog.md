---
title: "mcelog"
date: 2014-03-25 14:08
---

MCE - Machine Check Exception(Error)

mcelog 是 X86架构上(32bit and 64bit) 的 Linux 系统上用来检查硬件错误，特别是内存和CPU错误的工具。

要了解mcelog，首先应该了解下官方列出的一些[术语](http://www.mcelog.org/glossary.html)

## 安装 ##

Gentoo 上安装比较简单, emerge就能在官方源里搜到:

*  app-admin/mcelog
      Latest version available: 1.0_pre3_p20130621-r1
      Latest version installed: [ Not Installed ]
      Size of files: 280 kB
      Homepage:      http://mcelog.org/
      Description:   A tool to log and decode Machine Check Exceptions
      License:       GPL-2

其它发行版需要具体参考[官方安装说明](http://www.mcelog.org/installation.html)

安装后启动mcelog服务。

启动后可以通过相关命令检查守护进程是否正常执行: **TODO**

	mcelog --client

如果没有任何输出，表示当前状态是良好的。

默认的配置里，mcelog是使用daemon运行的，可以把它加入开机启动项。

mcelog 安装的主要文件(配置和程序)有:

	tankywoo@gentoo-local::mcelog/ » sudo equery files mcelog
	/etc/cron.daily/mcelog
	/etc/init.d/mcelog
	/etc/logrotate.d/mcelog
	/etc/mcelog/cache-error-trigger
	/etc/mcelog/dimm-error-trigger
	/etc/mcelog/mcelog.conf
	/etc/mcelog/page-error-trigger
	/etc/mcelog/socket-memory-error-trigger
	/usr/lib/systemd/system/mcelog.service
	/usr/sbin/mcelog
	/usr/share/doc/mcelog-1.0_pre3_p20130621-r1/README.bz2
	/usr/share/doc/mcelog-1.0_pre3_p20130621-r1/lk10-mcelog.pdf
	/usr/share/doc/mcelog-1.0_pre3_p20130621-r1/mce.pdf


## mcelog 运行方式 ##

分三种方式: `cronjob`, `trigger`, `daemon`。

推荐使用 daemon 方式运行。

cronjob 方式是通过 cron程序定时检查，这样会导致一些错误被延时汇报, mcelog也无法保存一些扩展的状态。

trigger is a newer method where the kernel runs mcelog on a error. This is configured with echo /usr/sbin/mcelog > /sys/devices/system/machinecheck/machinecheck0/trigger This is faster, but still doesn't allow mcelog to keep state, and has relatively high overhead for each error because a program has to be initialized from scratch.

## 配置 ##

可以参考官方的[配置介绍](http://www.mcelog.org/config.html)。

大部分可以使用默认的选项，下面列出一些需要修改(开启)的:

## 命令行参数选项 ##

具体可以 man mcelog

	tankywoo@gentoo-local::~/ » sudo mcelog --help
	mcelog: unrecognized option '--help'
	Usage:
	  mcelog [options]  [mcelogdevice]
	Decode machine check error records from current kernel.
	  mcelog [options] --daemon
	Run mcelog in daemon mode, waiting for errors from the kernel.
	  mcelog [options] --client
	Query a currently running mcelog daemon for errors
	  mcelog [options] --ascii < log
	  mcelog [options] --ascii --file log
	Decode machine check ASCII output from kernel logs
	Options:
	--cpu CPU           Set CPU type CPU to decode (see below for valid types)
	--cpumhz MHZ        Set CPU Mhz to decode time (output unreliable, not needed on new kernels)
	--raw                (with --ascii) Dump in raw ASCII format for machine processing
	--daemon            Run in background waiting for events (needs newer kernel)
	--ignorenodev       Exit silently when the device cannot be opened
	--file filename     With --ascii read machine check log from filename instead of stdin
	--syslog            Log decoded machine checks in syslog (default stdout or syslog for daemon)
	--syslog-error       Log decoded machine checks in syslog with error level
	--no-syslog         Never log anything to syslog
	--logfile filename  Append log output to logfile instead of stdout
	--dmi               Use SMBIOS information to decode DIMMs (needs root)
	--no-dmi            Don't use SMBIOS information
	--dmi-verbose       Dump SMBIOS information (for debugging)
	--filter            Inhibit known bogus events (default on)
	--no-filter         Don't inhibit known broken events
	--config-file filename Read config information from config file instead of /etc/mcelog/mcelog.conf
	--foreground        Keep in foreground (for debugging)
	--num-errors N      Only process N errors (for testing)
	--pidfile file       Write pid of daemon into file
	--no-imc-log         Disable extended iMC logging
	Valid CPUs: generic p6old core2 k8 p4 dunnington xeon74xx xeon7400 xeon5500 xeon5200 xeon5000 xeon5100 xeon3100 xeon3200 core_i7 core_i5 core_i3 nehalem westmere xeon71xx xeon7100 tulsa intel xeon75xx xeon7500 xeon7200 xeon7100 sandybridge sandybridge-ep ivybridge ivybridge-ep ivybridge-ex haswell

`mcelog --client` 相当于一个mcelog客户端，用来从mcelog进程查询信息

下面的选项都可以通过mcelog的配置文件进行配置。

最下面是合法的cpu类型，在--cpu配置时使用



## 一些依赖 ##

检查 `/dev/mcelog` 是否存在，如果没有，通过 `mknod /dev/mcelog c 10 227` 创建。

内核版本: 32bit(since 2.6.30), 64bit(since 2.6)

内核配置需要开启 `CONFIG_X86_MCE` 选项:

	root@ubuntu_test:/boot# grep 'MCE' /boot/config-`uname -r`
	CONFIG_X86_MCE=y


### 相关资源 ###

* [mcelog 主页](https://github.com/andikleen/mcelog)
* [mcelog 项目源码](https://github.com/andikleen/mcelog)
* man mcelog - 首选文档
* lk10-mcelog.pdf - mcelog 处理的错误简介
* mce.pdf - 比较老的文档，介绍的是mcelog第一个发行版
* mcelog --help
