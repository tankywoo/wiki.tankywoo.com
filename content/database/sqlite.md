---
title: "SQLite 3"
date: 2015-09-29 19:00
updated: 2016-04-11 23:33
logs: "增加备份命令"
---

[TOC]

## 常用命令 ##

命令都是以`.` dot 开头:

	.help 查看帮助
	.quit 退出

## Tips ##

### 备份 ###

因为sqlite3数据库直接是一个实体文件，最简单的就是拷贝一份，不过如果是拷贝时正在写操作等，会导致数据库不完整。

使用sqlite3提供的`.backup`命令可以完成:

	$ sqlite3 mydb.sqlite3
	> .backup mydb.bak.sqlite3

或者直接在命令行而不进入交互来完成:

	$ sqlite3 mydb.sqlite3 ".backup mydb.bak.sqlite3"

参考: [How to backup sqlite database?](http://stackoverflow.com/a/25684912/1276501)

