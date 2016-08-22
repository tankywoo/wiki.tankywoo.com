---
title: "DEB打包"
date: 2016-04-29 14:25
updated: 2016-04-29 14:25
collection: "打包"
tag: ubuntu
log: "初始化基本步骤"
---

[TOC]

本地环境: Ubuntu 12.04

基本构建环境:

* build-essential 打包构建相关的一个meta包，存储了一些信息，使编译打包更简单
* dpkg-dev dpkg开发工具
* dh-make 包含`dh_make`命令，用于更新源码包生成deb包构建模板
* debhelper `dh_*`命令集，编译deb包时需要用到


## 基本步骤 ##

### 获取源码包 ###

一个是通过apt源直接获取源码包，如：

	$ apt-get source busybox

	$ tree -L 1
	.
	├── busybox-1.18.5
	├── busybox_1.18.5-1ubuntu4.1.debian.tar.gz
	├── busybox_1.18.5-1ubuntu4.1.dsc
	└── busybox_1.18.5.orig.tar.bz2

	1 directory, 3 files

其中，\*.debian.tar.gz 是debian rules目录的压缩包(后面提到)，orig.tar.bz2是源码包，顺便还会解压一份出来。

另外一个就是去官网找，比如Github，PyPI，项目主页网站等。


### 生成基本的deb模板 ###

要求上级目录的命名格式:

	<package>-<version>

或者使用参数指定 `-p <package>_<version>`。

否则报错：

	For dh_make to find the package name and version, the current directory
	needs to be in the format of <package>-<version>.  Alternatively use the
	-p flag using the format <name>_<version> to override it.
	I cannot understand the directory name or you have an invalid directory name!

	Your current directory is /root/deb/busybox_1.18.5, perhaps you could try going to
	directory where the sources are?

	Please note that this change is necessary ONLY during the initial
	Debianization with dh_make.  When building the package, dpkg-source
	will gracefully handle almost any upstream tarball.

执行命令：

	$ dh_make -s -e fake@tankywoo.com -p busybox_1.18.5 -f busybox_1.18.5.orig.tar.bz2
	Maintainer name  : root
	Email-Address    : fake@tankywoo.com
	Date             : Fri, 29 Apr 2016 15:39:10 +0800
	Package Name     : busybox
	Version          : 1.18.5
	License          : blank
	Type of Package  : Single
	Hit <enter> to confirm:
	Skipping creating ../busybox_1.18.5.orig.tar.bz2 because it already exists
	Currently there is no top level Makefile. This may require additional tuning.
	Done. Please edit the files in the debian/ subdirectory now. You should also
	check that the busybox Makefiles install into $DESTDIR and not in / .

`-s`指定是single package，其它几种类型还没研究过。**TODO**

会生成一个`debian`目录，里面包含制作deb包的基本模板。
