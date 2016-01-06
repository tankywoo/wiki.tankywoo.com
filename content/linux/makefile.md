---
title: "Makefile & CMakeLists"
date: 2016-01-06 23:09
---

[TOC]


## Makefile ##

Makefile的使用非常广, 除了作为C/C++项目用于构建, 在日常的一些其它小项目里, 也可以简单的使用target来快速做一些操作集合, 类似于一个shell script带有一些子命令.

如我的项目[Simiki](http://simiki.org/)的[Makefile](https://github.com/tankywoo/simiki/blob/master/Makefile).

注释: 使用 `#`

宏:

有默认的值, 也可以修改:

	CC=gcc

然后使用宏:

	build:
		$(CC) xxx.c

最基本的结构 target(目标):

	test: clean
		nosetests -v --no-byte-compile --with-coverage --cover-package=simiki --cover-erase -s

这里target是test, clean是dependency(依赖), 下面的是这个target要执行的主体.

	make test

等价于:

	make clean
	nosetests -v --no-byte-compile --with-coverage --cover-package=simiki --cover-erase -s

依赖是线性串联的, 使用起来非常方便.

第一个target是默认的目标, 如果单纯的执行`make`, 则会执行第一个target.

target主体中命令加上`@`符号(at sign):

	test:
		echo 'print this command and then run'
		@echo 'only run this command'

一般情况逐行执行, 先打印一条命令的内容, 再执行这条命令, 加上`@`符号表示不打印这条命令, 直接执行.

如上结果是:

	echo 'print this command and then run'
	print this command and then run
	only run this command

参考: [Recipe Echoing](http://www.gnu.org/software/make/manual/make.html#index-_0040-_0028in-recipes_0029)

另外, target主体必须要以 `tab` 开始, 不能是4个空格.

伪目标(.PHONY), 一般用于clean, 用于避免目录下有与clean target同名文件, 导致make失败; 另外还可以提高make时的效率?(没有感触)

	.PHONY: clean

	clean:
		rm -rf *.o

## CMakefile ##

TODO


## 参考 ##

* [GNU make](http://www.gnu.org/software/make/manual/make.html) 官方文档
* [跟我一起写Makefile](http://blog.csdn.net/haoel/article/details/2886) 陈皓写的一个系列, 非常详细
* [makefile 入门学习](http://ylwhere.cf/2015/06/03/makefile-%E5%85%A5%E9%97%A8%E5%AD%A6%E4%B9%A0/)
* [Makefile入门](http://harttle.com/2014/01/01/makefile.html)
* [Makefile入门](http://lesca.me/archives/makefiles.html)
