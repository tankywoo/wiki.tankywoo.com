---
title: "awk"
date: 2013-08-17 07:32
---


## 格式 ##

	gawk options program file

	Options:
	* -F fs
	* -f file
	* -v var=value
	* -mf N
	* -mr N
	* -W keyword

## * ##

	gawk程序用一对花括号来定义
	gawk默认的字段分隔符是任意的空白字符
	$0、$1、$2...的含义
	gawk变成语言允许将多条命令组合成一个正常的程序，用冒号分开
	在处理数据前运行脚本使用BEGIN
	在处理数据后运行脚本使用END

## Example ##

	$ gawk '{print "Hello, TankyWoo"}'

	$ gawk -F: '{print $1}' /etc/passwd

	$ echo "My name is TankyWoo" | gawk '{$4="TK"; print $0}'

	$ cat myscript
	{ print $1 "'s home dir is " $6 }
	$ gawk -F: -f myscript /etc/passwd

	$ gawk 'BEGIN {print "Hello World"}'

	$ cat mydata
	Line 1
	Line 2
	Line 3
	$ gawk 'BEGIN { print "The data fileL"} { print $0 }' mydata

	p
	$ gawk 'BEGIN { print "The data fileL"} { print $0 }\
			END { print "End of File"}' mydata
