---
title: "Linux Tricks"
date: 2013-08-17 07:23
description: "Tricks/Tips/Fragments"
---


* 查看现在使用的是哪一个shell  

		echo $0

* 修改login shell  

		chsh

* 快速返回到上一个目录

	有时候移到一个目录, 想直接返回去

		cd -

* 关于export C  

	建议在脚本开始处加上`export C`，且如果man手册乱码，也可以:

		$ export C man xxx

* 查看本机最常用的10条命令  

		history | awk '{a[$2]++}END{for(i in a){print a[i] " " i}}' | sort -rn | head


* 获取一个字符串的长度  

	三种方法:

		len `expr length $str`
		echo ${str} | wc -L
		echo ${str} # 推荐


* 统计当前目录下（包括子目录）以.py结尾文件的个数及总代码行数  

	文件个数: 
	
		find . -name "*.py" | wc -l

	单个文件代码行数及总行数: 

		find . -name "*.py" | xargs wc -l


* 输出错误重定向  

		ls 1>/dev/null 2>/dev/null
		ls >/dev/null 2>&1


* Show number of connections per remote IP  

		netstat -antu | awk '$5 ~ /[0-9]:/{split($5, a, ":"); ips[a[1]]++} END {for (ip in ips) print ips[ip], ip | "sort -k1 -nr"}'


* 以root身份执行上一条命令  

		sudo !!


* 开启一个Web服务器(传输)  

		# -m 表示找到模块, 执行相应的.py文件
		# SimpleHTTPServer 是一个 Http Server 模块
		python -m SimpleHTTPServer


* vim里强制保存  

	有时候, 一些文件编辑后, 才发现只有root可写

		:w !sudo tee %


* 替换上条命令的关键字并执行  

		# 将上一条命令的pint换成traceroute
		^ping^traceroute^


* 复制一个备份文件  

	有时候, 为了测试, 为防止意外, 可能需要把 filename 在备份一个 filename.bak

		cp filename{,.bak}


* 搜索最近一条符合关键字的命令  

	比如上面执行过命令是ping wutianqi.com, 想再执行, 可以

		# p是关键字, 也可以 pi, pin, ping都行
		!p


* 给远程机器添加公钥认证

		ssh-copy-id user@host

	很多人喜欢生成公私钥后, 用scp传过去, 再登录上去设置。
	其实完全没必要, ssh-copy-id会自动把公钥添加到~/.ssh/authorized_keys末尾。
	如果 ssh-add -L 里面有内容，会优先使用里面的公钥; 其次，可以用 -i 指定要添加的公钥，最后会用默认的 ~/.ssh/id_rsa.pub


* 把 Linux 桌面录制为视频  

	*TODO* 这个命令先记录一下, 还没尝试

		ffmpeg -f x11grab -s wxga -r 25 -i :0.0 -sameq /tmp/out.mpg


* 快速清空arp缓存表

		for a in `arp | grep "eth1" | cut -d " " -f1`; do arp -d $a; done

* 检查硬盘是HDD还是SSD

	方法1:

		cat /sys/block/sda/queue/rotational

	输出`1`则是HDD, 输出`0`则是SSD

	方法2:

	安装`smartmontools`工具，使用`smartctl`命令查看信息。

		tankywoo@gentoo-local::~/ » sudo smartctl -a /dev/sda
		smartctl 6.1 2013-03-16 r3800 [x86_64-linux-3.7.10-gentoo-r1-ks] (local build)
		Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org

		=== START OF INFORMATION SECTION ===
		Device Model:     gentoo-0 SSD
		Serial Number:    36CBA5PYHBJMH4MDR0YY
		Firmware Version: F.9AGAJ4
		User Capacity:    34,359,738,368 bytes [34.3 GB]
		Sector Sizes:     512 bytes logical, 4096 bytes physical
		Rotation Rate:    Solid State Device
		Device is:        Not in smartctl database [for details use: -P showall]
		ATA Version is:   ATA8-ACS, ATA/ATAPI-5 T13/1321D revision 1
		SATA Version is:  SATA 2.6, 3.0 Gb/s
		Local Time is:    Mon Jun 23 23:31:46 2014 CST
		SMART support is: Unavailable - device lacks SMART capability.

		A mandatory SMART command failed: exiting. To continue, add one or more '-T permissive' options.

	其中`Rotation Rate:    Solid State Device` 显示了是HDD还是SSD

	+ [How to Find Out if a Drive is a SSD or an HDD](http://linuxg.net/how-to-find-out-if-a-drive-is-a-ssd-or-an-hdd/)
	+ [How to know if a disk is an SSD or an HDD](http://stackoverflow.com/questions/908188/is-there-any-way-of-detecting-if-a-drive-is-a-ssd)
	+ [http://linuxg.net/how-to-find-out-if-a-drive-is-a-ssd-or-an-hdd/](http://stackoverflow.com/questions/908188/is-there-any-way-of-detecting-if-a-drive-is-a-ssd)

* Ext3关闭日志特性:

		tune2fs -O ^has_journal /dev/sdX

	关闭前后可以确认下文件系统的特性:

		$ tune2fs -l /dev/sda1 | grep features
		Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery sparse_super large_file

	关闭后 `has_journal` 日志特性没了

	参考 [Disable journaling in ext3 file system](http://blog.serverbuddies.com/disable-journaling-in-ext3-file-system/)
