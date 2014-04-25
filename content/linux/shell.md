---
title: "Shell"
date: 2013-08-17 07:23
---



# 什么是Shell #

	shell是一个作为用户与Linux系统间接口的程序，它允许用户向操作系统输入需要执行的命令


# 基本 #
## 重定向 ##

	0	标准输入 <  <<
	1	标准输出 >  >>
	2	错误输出 2> 2>>

	<是输出， <<是以附加的方式输出
	>& kill -9 1234 >killouterr.txt 2>&1



## 管道 ##

	管道用操作符 '|'


# 脚本 #
## 格式 ##

	第一行指定执行shell的文件，一般是#!/bin/bash或#!/bin/sh


## 运行 ##

	* 直接运行 sh xx.sh 或者 bash xx.sh
	* 可执行文件 先chmod +x xx.sh 然后 ./xx.sh


# Shell语法(*) #
## 变量 ##

* 变量不需要提前声明
* 变量名区分大小写
* 创建变量时通过直接赋值给变量 eg. var=abc
* 访问变量时需要在变量名前加一个$符号 eg. echo $var 或 `echo ${var}`
* 在赋值时，等号两边不能有空格 eg. `var=abc`
* 如果字符串里有空格，则必须用双引号把字符串括起来 `var="Hello World"`

		tankywoo@linuxmint /var/www/wiki $ a=hello
		tankywoo@linuxmint /var/www/wiki $ echo $a
		hello
		tankywoo@linuxmint /var/www/wiki $ b=a
		tankywoo@linuxmint /var/www/wiki $ echo $b
		a
		tankywoo@linuxmint /var/www/wiki $ b=world
		tankywoo@linuxmint /var/www/wiki $ echo $b
		world
		tankywoo@linuxmint /var/www/wiki $ echo $a
		hello



### 引号 ###

* read读入数据时，带有空格的数据不需要加引号

		$ read var
		Tanky Woo
		$ echo $var
		Tanky Woo

* 对于变量$var，如果放在双引号""中，则会替换为其值
* 如果放在单引号''中，则不会发生替换
* 还可以在$前面加上'\'符号取消其转义行为

		var="tanky woo"
		echo $var     # tanky woo
		echo "$var"   # tanky woo
		echo '$var'   # $var
		echo \$var    $var


### 环境变量 ###

## 条件 ##

test或[命令

	if test -f file.c ; then
		...
	fi

	或

	if [ -f file.c ]
		...
	fi



* 字符串的比较

		str1 = str2
		str1 != str2
		str1 > str2
		str1 < str2
		-n str  如果字符串不为空则为True
		-z str  如果字符串为null，则结果为真



* 算数比较

		exp1 -eq exp2	==
		exp1 -ne exp2	!=
		exp1 -gt exp2	>
		exp1 -ge exp2	>=
		exp1 -lt exp2	<
		exp1 -le exp2	<=
		!exp			如果exp为假则返回真


* 文件条件测试

		-d file    directory
		-e file    exist
		-f file    common file
		-g file    set-group-id ???
		-r file    readable
		-s file    file space is not 0
		-u file    set-user-id ???
		-w file    writeable
		-x file    executeable


* (( expression ))

		可以使用高级数学特性
		val++
		val--
		++val
		--val
		!		逻辑求反
		~		位求反
		**		幂运算
		<<		左移位
		>>
		&		按位与
		|
		&&		逻辑与
		||	


* [\[ expression ]]

		字符串的比较，但是支持模式匹配



## 控制结构 ##
### if语句 ###

	if condition
	then
		statement
	elif condition; then
		statement
	else
		statement
	fi


### for语句 ###

	for var in values
	do
		statement
	done

循环一个序列:

	for var in {1..5}
	do
		echo $var
	done

[Bash For Loop Examples](http://www.cyberciti.biz/faq/bash-for-loop/)

### while语句 ###

	while condition
	do
		statenment
	done



### while语句 ###

	until condition
	do
		statenment
	done




### case语句 ###

	case var in
		passtern [| pattern]... ) statement1;;
		passtern [| pattern]... ) statement2;;
		...
	esac


注:
每个模式都以`双引号;;`结尾

	eg.
	#!/bin/sh
	# case statement
	echo "Please answer yes or no"
	read ans
	case "$ans" in
	        yes | y | Yes | YES )   echo "yes";;
	        no  | n | No  | NO  )   echo "no";;
	esac

	exit 0


### AND OR列表 ###

`&&` `||`

	con1 && con2 && con3
	con1 || con2 || con3

  
### 语句块 ###

`{}`

### 函数 ###
 

	function_name(){
		statement
	}




### 命令 ###

* `break`
* `:`
* `continue`
* `.`
* `echo`
* `eval` 对语句进行求值

		foo=10
		x=foo #echo $y --> foo
		y='$'$x
		echo $y # --> $foo

		eval y='$'$x
		echo $y # --> 10


* exec
* `exit n`
* `export`
* `expr`

把参数当作表达式来求值

	eg.
	x=`expr $x + 1`
	x=$(expr $x + 1)


* `printf`
* `return`
* `set`
* `shift`
* `trap`
* `unset`
* `find` **
* `grep` **

注：以下需要单独开一篇总结
`find` `grep` `regex`


### 补充 ###

算数运算  
$((...))  
x=$(($x+1))  


## Special Parameters ##
TODO vimwiki的转义怎么弄?

The shell treats several parameters specially. These parameters may only be referenced; assignment to them is not allowed.

`$*` : $* is equivalent to "\$1c\$2c..", where c is the first character of the value of the `IFS` variable

`$@` : `$@` is equivalent to "\$1" "\$2"

`$#` : The number of the parameters

`$?` : The exit status

`$0` : The source file name


# 参考 #

* Linux程序设计
* [Bash Manual](http://www.gnu.org/software/bash/manual/bashref.html)
