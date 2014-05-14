---
title: "samba"
date: 2013-08-17 07:36
---


## SAMBA ##

## Installation ##

	sudo emerge net-fs/samba


## About ##
NFS、CIFS？

Samba是用来让Unix系列的操作系统和微软Windows操作系统的SMB/CIFS（Server Message Block/Common Internet File System）网络协议做连接的自由软件

Samba是架构在NetBIOS（Network Basic Input/Output System）这个通信协议上面开发出来的。NetBIOS是无法跨路由的，但是现在又NetBIOS over TCP/IP技术可以实现。目前Samba还是广泛用于LAN中。

[官方网站传送门](http://www.samba.org)

## Configuration ##

	# TODO
	cd /etc/samba
	# the is a smb.conf.default in the dir
	sudo cp smb.conf.default smb.conf
	vim smb.conf
	# edit the [global] section
	# workgroup is the windows pc's workgroup name
	# security can be user or shareo
	# in the end, you can uncomment the [tmp] section

修改完smb.conf后，可以用testparm命令来检查配置文件的语法合法性

## Start Service ##

	sudo /etc/init.d/samba start

## Read More ##

* [Linux中Samba详细安装](http://www.cnblogs.com/whiteyun/archive/2011/05/27/2059670.html)
* [samba安装和配置文档以及和域控制器配合部分](http://bbs.chinaunix.net/thread-716599-1-1.html)
* [快速搭建Samba服务器](http://bbs.chinaunix.net/thread-1003730-1-1.html)
* [一步一学Linux与Windows 共享文件Samba](http://bbs.chinaunix.net/thread-1148734-1-1.html)
