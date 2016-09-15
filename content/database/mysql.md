---
title: "MySQL"
date: 2013-08-17 07:36
updated: 2016-09-15 16:30
log: "增加单引号/反引号区别"
---

[TOC]

`<>` 括起来的表示变量, 根据实际情况而定。

## 基础&常用命令 ##

### 单引号/双引号/反引号

参考[SO上回答](http://stackoverflow.com/a/11321508/1276501)：

> Backticks are to be used for table and column identifiers, but are only necessary when the identifier is a [MySQL reserved keyword](http://dev.mysql.com/doc/refman/5.5/en/reserved-words.html), or when the identifier contains whitespace characters or characters beyond a limited set (see below) It is often recommended to avoid using reserved keywords as column or table identifiers when possible, avoiding the quoting issue.

反引号(backticks/backquote)一般用于针对表/列名包含保留关键字，或者包含空格的情况。下面有提到这种情况。

> Single quotes should be used for string values like in the `VALUES()` list.  Double quotes are supported by MySQL for string values as well, but single quotes are more widely accepted by other RDBMS, so it is a good habit to use single quotes instead of double.

单双引号用于将一些字符串值阔起来，单引号用的多一些。

> `'` for enclosing string literals
>
> `` ` `` for enclosing identifiers such as table and column names

```mysql
Backtick (`)
table & column ───────┬─────┬──┬──┬──┬────┬──┬────┬──┬────┬──┬───────┐
                      ↓     ↓  ↓  ↓  ↓    ↓  ↓    ↓  ↓    ↓  ↓       ↓
$query = "INSERT INTO `table` (`id`, `col1`, `col2`, `date`, `updated`)
                   VALUES (NULL, 'val1', 'val2', '2001-01-01', NOW())";
                               ↑↑↑↑  ↑    ↑  ↑    ↑  ↑          ↑  ↑↑↑↑↑
Unquoted keyword          ─────┴┴┴┘  │    │  │    │  │          │  │││││
Single-quoted (') strings ───────────┴────┴──┴────┘  │          │  │││││
Single-quoted (') DATE    ───────────────────────────┴──────────┘  │││││
Unquoted function         ─────────────────────────────────────────┴┴┴┴┘
```


### 查看/新建/删除 用户

查看mysql用户:

	SELECT User, Host FROM mysql.user;

带上主机是因为用户和主机是相关的，否则意义不大，会显示多个相同的用户。

如果要显示唯一的用户:

	SELECT DISTINCT User FROm mysql.user;

删除用户:

	DROP USER '<username>'@'<host>';

带上引号是个好习惯, 否则主机名包含`-`等符号必须用引号阔起来。

创建用户:

	CREATE USER '<username>'@'<host>' IDENTIFIED BY '<password>';


### 用户权限

查看指定用户@主机的权限:

	SHOW GRANTS FOR '<username>'@<host>;

	mysql> SHOW GRANTS FOR tankywoo@localhost;
	+-------------------------------------------------------------------------------+
	| Grants for blog1@localhost                                                    |
	+-------------------------------------------------------------------------------+
	| GRANT USAGE ON *.* TO 'tankywoo'@'localhost' IDENTIFIED BY PASSWORD '*xxxxxx' |
	+-------------------------------------------------------------------------------+
	1 row in set (0.00 sec)

`USAGE`表示没有任何权限。

给用户赋予权限:

	GRANT <privilege> ON <database>.<table> TO '<username>'@'<host>';

如给用户设置所有权限给所有数据库:

	GRANT ALL ON *.* TO 'tankywoo'@'localhost';

赋予所有权限给指定的数据库:

	GRANT ALL ON testdb.* TO 'tankywoo'@'localhost';

赋予所有权限给指定的数据库的某个表:

	GRANT ALL ON testdb.testtable TO 'tankywoo'@'localhost';

赋予查询,插入权限给指定的数据库的某个表:

	GRANT SELECT,INSERT ON testdb.testtable TO 'tankywoo'@'localhost';

**注意**: `grant`命令赋予权限也可以创建用户, 比如上面如果tankywoo@localhost不存在, 则会创建此用户。所以一定要注意host, 如果赋予权限时忘了带上host, 则默认会创建user@%.

赋予权限后刷新权限是个好习惯:

	FLUSH PRIVILEGES;


### 用户密码

修改用户密码:

	SET PASSWORD FOR '<username>'@'<host>' = Password('<password>');

`Password()`函数用来给密码加密。


### 修改表中某一列的类型


```mysql
# 显示表中各列的类型
# http://dev.mysql.com/doc/refman/5.7/en/show-columns.html
mysql> SHOW COLUMNS FROM mytable;
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| name        | varchar(50)  | NO   |     | NULL    |                |
| desc        | varchar(50)  | NO   |     | NULL    |                |
| create_date | datetime(6)  | NO   |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
9 rows in set (0.00 sec)

# 修改指定列的类型, 从varchar改为text
# 这里MODIFY用CHANGE也可以
# 如果要保持NOT NULL，也要加上，否则默认会被改为YES
# http://dev.mysql.com/doc/refman/5.7/en/alter-table.html
mysql> ALTER TABLE mytable MODIFY name TEXT NOT NULL;
Query OK, 22 rows affected (0.54 sec)
Records: 22  Duplicates: 0  Warnings: 0

# 修改指定列的类型, 从datetime改为date
mysql> ALTER TABLE mytable MODIFY create_date DATE NOT NULL;
Query OK, 22 rows affected, 22 warnings (0.57 sec)
Records: 22  Duplicates: 0  Warnings: 22
```

注：如果表名或列名等是保留关键字，记得要加上反引号，之前改desc时没注意，然后就报错。


## 问题 ##

### 无法删除数据库 ###

删除数据库时报错:

	mysql> drop database testdb;
	ERROR 1010 (HY000): Error dropping database (can't rmdir './testdb', errno: 39)

之前数据库有问题, 不确定是异常退出还是升级导致, binlog问题导致mysqld启动不了, 于是删除了binlog等问题, 可能和这块有关。

最后手动把数据库目录删除了。暂时没去查这个错误码的意义。

参考: [Error Dropping Database (Can't rmdir '.test\', errno: 17)](http://stackoverflow.com/questions/4584458/error-dropping-database-cant-rmdir-test-errno-17)

### 查看单个数据库或表的大小 ###

要想知道每个数据库的大小的话，步骤如下：

1、进入`information_schema` 数据库（存放了其他的数据库的信息）

	use information_schema;


2、查询所有数据的大小：

	select concat(round(sum(data_length/1024/1024),2),'MB') as data from tables;

3、查看指定数据库的大小：

比如查看数据库home的大小

	select concat(round(sum(data_length/1024/1024),2),'MB') as data from tables where table_schema='home';

4、查看指定数据库的某个表的大小

比如查看数据库home中 members 表的大小

	select concat(round(sum(data_length/1024/1024),2),'MB') as data from tables where table_schema='home' and table_name='members';

(转载至网上)


### 创建名称带点号(dot)的数据库 ###

如创建叫 www.xxx.com 的数据库:

	CREATE DATABASE `www.xxx.com`

引号不行, 要用双引号。

在[这个回答](https://bytes.com/topic/mysql/answers/75624-how-do-you-create-database-dash-name#post260958)上看到, 不过还没看到权威文档说明。
