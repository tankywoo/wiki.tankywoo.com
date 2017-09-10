---
title: "SQLite 3"
date: 2015-09-29 19:00
updated: 2017-09-10 17:28
logs: "增加插入列方法"
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


### 增加列

如果是附加列到末尾，则直接：

```
ALTER TABLE table_name ADD new_column_name column_type;
```

但是如果想插入列到中间某个地方，则比较麻烦，解决方法是先将表更名，然后新建一个带有新列的新表，并将旧表的值复制过去，参考[回答](https://stackoverflow.com/a/4253879/1276501)：

```
sqlite> ALTER TABLE table_name RENAME TO table_name_old;

# 新建表并新增列 col_new
sqlite> CREATE TABLE IF NOT EXISTS table_name (id INTEGER PRIMARY KEY, name TEXT, col1 INTEGER, col_new INTEGER, col2 INTEGER);

# 将旧表数据复制过来并将新列 col_new 默认置为 0
sqlite> INSERT INTO table_name (name, col1, col_new, col2) SELECT name, col1, 0, col2 FROM table_name_old;
```
