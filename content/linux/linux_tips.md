---
title: "Linux Tips"
date: 2013-08-17 07:23
updated: 2016-05-23 16:20
description: "查漏补缺, Tricks/Tips/Fragments"
log: "增加cron的%符号"
---

[TOC]

### 查看现在使用的是哪一个shell ###

	echo $0


### 修改login shell ###

	chsh


### 快速返回到上一个目录 ###

有时候移到一个目录, 想直接返回去

	cd -


### 关于export C ###

建议在脚本开始处加上`export C`，且如果man手册乱码，也可以:

	$ export C man xxx


### 查看本机最常用的10条命令 ###

	history | awk '{a[$2]++}END{for(i in a){print a[i] " " i}}' | sort -rn | head


### 获取一个字符串的长度 ###

三种方法:

	len `expr length $str`
	echo ${str} | wc -L
	echo ${str} # 推荐


### 统计当前目录下（包括子目录）以.py结尾文件的个数及总代码行数 ###

文件个数: 

	find . -name "*.py" | wc -l

单个文件代码行数及总行数:

	find . -name "*.py" | xargs wc -l


### 输出错误重定向 ###

	ls 1>/dev/null 2>/dev/null
	ls >/dev/null 2>&1


### Show number of connections per remote IP ###

	netstat -antu | awk '$5 ~ /[0-9]:/{split($5, a, ":"); ips[a[1]]++} END {for (ip in ips) print ips[ip], ip | "sort -k1 -nr"}'


### 以root身份执行上一条命令 ###

	sudo !!


### 开启一个Web服务器(传输) ###

	# -m 表示找到模块, 执行相应的.py文件
	# SimpleHTTPServer 是一个 Http Server 模块
	python -m SimpleHTTPServer


### vim里强制保存 ###

有时候, 一些文件编辑后, 才发现只有root可写

	:w !sudo tee %


### 替换上条命令的关键字并执行 ###

	# 将上一条命令的pint换成traceroute
	^ping^traceroute^


### 复制一个备份文件 ###

有时候, 为了测试, 为防止意外, 可能需要把 filename 在备份一个 filename.bak

	cp filename{,.bak}


### 搜索最近一条符合关键字的命令 ###

比如上面执行过命令是ping wutianqi.com, 想再执行, 可以

	# p是关键字, 也可以 pi, pin, ping都行
	!p


### 给远程机器添加公钥认证 ###

	ssh-copy-id user@host

很多人喜欢生成公私钥后, 用scp传过去, 再登录上去设置。
其实完全没必要, ssh-copy-id会自动把公钥添加到~/.ssh/authorized_keys末尾。
如果 ssh-add -L 里面有内容，会优先使用里面的公钥; 其次，可以用 -i 指定要添加的公钥，最后会用默认的 ~/.ssh/id_rsa.pub


### 把 Linux 桌面录制为视频 ###

*TODO* 这个命令先记录一下, 还没尝试

	ffmpeg -f x11grab -s wxga -r 25 -i :0.0 -sameq /tmp/out.mpg


### 快速清空arp缓存表 ###

	for a in `arp | grep "eth1" | cut -d " " -f1`; do arp -d $a; done


### 检查硬盘是HDD还是SSD ###

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


### Ext3关闭日志特性 ###

	tune2fs -O ^has_journal /dev/sdX

关闭前后可以确认下文件系统的特性:

	$ tune2fs -l /dev/sda1 | grep features
	Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery sparse_super large_file

关闭后 `has_journal` 日志特性没了

参考 [Disable journaling in ext3 file system](http://blog.serverbuddies.com/disable-journaling-in-ext3-file-system/)


### 获取当前的terminal name ###

	$ tty

参考 [Find Out What tty I’m Using](http://www.cyberciti.biz/faq/linux-unix-appleosx-bsd-what-tty-command/)


### w命令idle ###

> The idle time is supposed to tell how long it has been since the user typed any input on that terminal. For Xwindows sessions, it is broken since Xwindows never reads input from a terminal, but instead gathers input directly from your mouse and keyboard, so the terminal never gets its timestamp updated since it is never read from.

> Without a qualifier, it means MM:SS -- that is, minutes and whole seconds. As an added bonus, there's a fourth format you don't have in that output -- a number of days (NNdays) of inactivity.

参考:

* [What does idle time output from “w” command tell?](http://askubuntu.com/questions/283337/what-does-idle-time-output-from-w-command-tell)
* [How to read the “IDLE” column in the output of the Linux 'w' command?](http://serverfault.com/questions/302455/how-to-read-the-idle-column-in-the-output-of-the-linux-w-command)

### awk 显示某些列 ###

比如显示第3列及以后所有列:

	ps aux | grep ngin[x] | awk '{for (i=3; i<=NF; i++) printf $i " "} {print ""}'

参考 [Print all but the first three columns](http://stackoverflow.com/questions/2626274/print-all-but-the-first-three-columns)

### useradd新建用户的目录权限 ###

默认情况下, `useradd` 的 `UMASK` 是在 `/etc/login.defs` 中控制的, Gentoo下是`0022`.

这样新建用户时, 创建的home目录就是0755了, 针对同一个用户组的, 权限较大, 限制为0700比较合适.

可以通过useradd时指定UMASK:

    useradd -m -K UMASK=0077 testuser

`/etc/login.defs` 的UMASK参数只是针对 useradd 创建用户目录时用的.

参考:

* [Understanding UMASK value in Linux](http://www.golinuxhub.com/2014/05/understanding-umask-value-in-linux.html) 讲解的挺详细
* [What type of permissions should a user's home directory and files have?](http://unix.stackexchange.com/questions/76532/what-type-of-permissions-should-a-users-home-directory-and-files-have)
* [Why is the default umask value for useradd in openSuSE set to 022?](http://unix.stackexchange.com/questions/37194/why-is-the-default-umask-value-for-useradd-in-opensuse-set-to-022)

### 重定向命令的stderr到stdout ###

	command 2>&1

参考 [How to pipe stderr, and not stdout?](http://stackoverflow.com/questions/2342826/how-to-pipe-stderr-and-not-stdout)


### 删除文件的最后一个newline符 ###

	$ perl -pe 'chomp if eof' filename >filename2

或

	$ perl -pi -e 'chomp if eof' filename

参考: [How can I delete a newline if it is the last character in a file?](http://stackoverflow.com/questions/1654021/how-can-i-delete-a-newline-if-it-is-the-last-character-in-a-file)


### 查看网卡类型 ###

	$ lspci | egrep -i --color 'network|ethernet'
	$ lspci | grep -i net
	$ lshw -class network
	$ dmesg | grep 'Ethernet driver'


### cron命令中的`%`

本来是准备通过crontab把命令的标准输出重定向到文件中，于是写为：

	*/1 * * * * root /tmp/test.sh >> /tmp/$(date +%d-%m-%Y).log

结果没有产生日志文件，且cron日志显示：

	CMD (/tmp/test.sh >> /tmp/$(date +)

`man 8 crontab` 有提到百分号`%`在cron中的特殊意义：

> The entire command portion of the line, up to a newline or % character, will be executed by /bin/sh or by the shell specified in the SHELL variable of the cronfile.  Percent-signs (%) in the command, unless escaped with  backslash (\), will be changed into newline characters, and all data after the first % will be sent to the command as standard input.

除非转义，否则`%`相当于换行符, 命令中第一个%之后的都被当做标准输入(`read`可以读到)。改为：

	*/1 * * * * root /tmp/test.sh >> /tmp/$(date +\%d-\%m-\%Y).log
