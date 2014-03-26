---
title: "mcelog"
date: 2014-03-25 14:08
---

MCE - Machine Check Exception(Error)

[解释1](http://www.cyberciti.biz/tips/linux-server-predicting-hardware-failure.html):

> MCE is nothing but feature of AMD / Intel 64 bit systems which is used to detect an unrecoverable hardware problem. MCE can detect:
> 
> * Communication error between CPU and motherboard.
> * Memory error - ECC problems.
> * CPU cache errors and so on.
> 
> Program such mcelog decodes machine check events (hardware errors) on x86-64 machines running a 64-bit Linux kernel.


mcelog 是 X86架构上(32bit and 64bit) 的 Linux 系统上用来检查硬件错误，特别是内存和CPU错误的工具。

[官方介绍](http://www.mcelog.org/README.html):

> mcelog is the user space backend for logging machine check errors reported by the hardware to the kernel. 
> The kernel does the immediate actions (like killing processes etc.) and mcelog decodes the errors and manages various other advanced error responses like offlining memory, CPUs or triggering events.


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

> trigger is a newer method where the kernel runs mcelog on a error. This is configured with echo /usr/sbin/mcelog > /sys/devices/system/machinecheck/machinecheck0/trigger This is faster, but still doesn't allow mcelog to keep state, and has relatively high overhead for each error because a program has to be initialized from scratch.

trigger 是一种新的方式，通过配置:

	echo /usr/sbin/mcelog > /sys/devices/system/machinecheck/machinecheck0/trigger 

这种方式更快，但是仍然也无法保存状态，且因为每次错误都需要初始化，所以开销大。

## 配置 ##

可以参考官方的[配置介绍](http://www.mcelog.org/config.html)。

大部分可以使用默认的选项，下面列出一些需要修改(开启)的:

	# 修改cpu类型，可以通过 mcelog --help 看到支持的合法类型选项
	cpu = type 
	
	# 使用daemon方式运行
	daemon = yes

	# cpu主频，可以通过 cat /proc/cpuinfo 输出的 `cpu MHz` 看到
	cpuhz = 1800.00

	# 配置是否写入syslog
	syslog = yes
	syslog-error = yes
	no-syslog = yes
	logfile = filename

	# server 区域可以配置读取mcelog socket的权限，建议使用 root 权限。
	client-user = yes

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

下面的选项都可以通过mcelog的配置文件进行配置。建议直接在配置文件中配置，其中还有一些配置是参数选项中没有的。

最下面是合法的cpu类型，在--cpu配置时使用

下面可以从指定文件中读取内核日志进行解码输出:

	# Decode machine check ASCII output from kernel logs
	mcelog [options] --ascii < log

比如在 mcelog 项目源码中的 input/ 目录中有一些samples可以直接使用:

	tankywoo@gentoo-local::input/ (master*) » cat dimm0
	# dimm0, channel0 corrected error
	CPU 0 2
	PROCESSOR 0:0x106a0
	STATUS 0x8800000000000080
	MISC 0

	tankywoo@gentoo-local::input/ (master*) » sudo mcelog --ascii < dimm0
	# dimm0, channel0 corrected error
	Hardware event. This is not a software error.
	CPU 0 BANK 2
	MISC 0
	MCG status:
	MCi status:
	Corrected error
	MCi_MISC register valid
	MCA: MEMORY CONTROLLER GEN_CHANNEL0_ERR
	Transaction: Generic undefined request
	Memory corrected error count (CORE_ERR_CNT): 0
	Memory transaction Tracker ID (RTId): 0
	Memory DIMM ID of error: 0
	Memory channel ID of error: 0
	Memory ECC syndrome: 0
	STATUS 8800000000000080 MCGSTATUS 0
	CPUID Vendor Intel Family 6 Model 26

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
* [mcelog-lk10-pres.pdf](http://www.halobates.de/mcelog-lk10-pres.pdf)
* [mce的一些零散记录](http://blog.casparant.com/posts/some-misc-items-of-mce.html)
* [Linux系统无法ping通，导致需要重启系统](http://www.flatws.cn/article/program/linux/2011-05-04/23961.html)
