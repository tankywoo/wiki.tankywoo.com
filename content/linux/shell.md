---
title: "Shell"
date: 2013-08-17 07:23
---


shell是一个作为用户与Linux系统间接口的程序，它允许用户向操作系统输入需要执行的命令

> In computing, a shell is a user interface for access to an operating system's services. --- [维基百科](https://en.wikipedia.org/wiki/Shell\_(computing))

shell的实现比较多, 如常见内置的sh, bash, 以及强大的zsh

Linux/Unix 都有默认的shell, 使用环境变量`$SHELL`可以查看当前的默认shell:

	% echo $SHELL
	/bin/zsh

以shell控制结构为框架, 使用shell内置命令(shell builtin)或其它命令编写的脚本叫shell脚本.

## 基本 ##

重定向

	0	标准输入 <  <<
	1	标准输出 >  >>
	2	错误输出 2> 2>>

	<是输出， <<是以附加的方式输出
	% >& kill -9 1234 >killouterr.txt 2>&1

	% cat foo
	hello
	% cat bar
	world
	% cat foo >> bar
	% cat bar
	world
	hello


管道用操作符 `|`


## 脚本 ##

格式:

第一行指定执行shell的文件, 成为shell bang, 一般是

	#!/bin/bash

或

	#!/bin/sh

运行时加`-x`是line-by-line的方式执行脚本, 每行都会输出

	% bash -x /path/to/script

注释用井号符(`#`)

多行注释每行前面都要加上#

不过也有一些trick可以实现多行注释:

使用[HERE Document](https://en.wikipedia.org/wiki/Here_document)

基本格式:

	cmd << delimiter
	  Here Document Content
	delimiter

如:

	echo 'xxx'

	<<COMMENT
	这是一段很长的说明
	用来测试多行注释
	By Tanky Woo
	COMMENT

	echo 'xxx'

这种方式经常用到在shell命令行下写多行到文件:

	% cat << EOF > test.txt
	heredoc> hello, my name is Tanky Woo
	heredoc> this is here document
	heredoc> for testing
	heredoc> EOF

	% more test.txt
	hello, my name is Tanky Woo
	this is here document
	for testing

另一种方法就是:

	echo 'xxx'

	: '
	这是一段很长的说明
	用来测试多行注释
	By Tanky Woo
	'

	echo 'xxx'

参考:

* [Shell Script Put Multiple Line Comment](http://www.cyberciti.biz/faq/bash-comment-out-multiple-line-code/)
* [Commenting out a set of lines in a shell script](http://stackoverflow.com/questions/1444367/commenting-out-a-set-of-lines-in-a-shell-script)


## Shell语法 ##

变量:

* 变量不需要提前声明
* 变量名区分大小写
* 创建变量时通过直接赋值给变量 eg. var=abc
* 访问变量时需要在变量名前加一个$符号 eg. `echo $var` 或 `echo ${var}`
* 在赋值时，等号两边不能有空格 eg. `var=abc`
* 如果字符串里有空格，则必须用双引号把字符串括起来 `var="Hello World"`

<!-- -->

	% a=hello
	% echo $a
	hello
	% b=a
	% echo $b
	a
	% b=world
	% echo $b
	world
	% echo $a
	hello

可以将命令的结果赋值给变量:

	% x='foo'
	% echo $x
	foo
	% y=`echo $x`
	% echo $y
	foo

特殊变量:

具体看`man bash`的`Special Parameters`一节

`$0`: 当前执行的脚本名. 和python里的sys.argv[0]一样
`$X`: X是数字, 表示第几个参数, 比如脚本后接的第一个参数, 就是$1
`$?`: 上一条命令的返回值
`$$`: 当前shell pid
`$#`: 传递给脚本或函数 参数的个数
`$*`: 参数列表. 当有双引号阔起来时, 则是一个元素
`$@`: 参数列表. 当有双引号阔起来时, 还是多个元素

	% more foo.sh
	#!/bin/bash

	echo '$#: ' $#
	echo '$1: ' $1
	echo '$*: '$*
	echo '$@: ' $@
	echo 'for in "$*"'
	for v in "$*"
	do
			echo $v
	done
	echo 'for in "$@"'
	for v in "$@"
	do
			echo $v
	done

	% ./foo.sh one two three
	$#:  3
	$1:  one
	$*: one two three
	$@:  one two three
	for in "$*"
	one two three
	for in "$@"
	one
	two
	three


引号:

* read读入数据时，带有空格的数据不需要加引号
* 对于变量$var，如果放在双引号""中，则会替换为其值
* 如果放在单引号''中，则不会发生替换
* 还可以在$前面加上'\'符号取消其转义行为

<!-- -->

	% read var
	Tanky Woo
	% echo $var
	Tanky Woo

	var="Tanky Woo"
	echo $var     # Tanky Woo
	echo "$var"   # Tanky Woo
	echo '$var'   # $var
	echo \$var    $var

变量的一些基本操作:

这个和Python调用format的变量格式类似

	% more foo.sh
	#!/bin/bash

	bar="hello, world"

	echo ${#bar}    # 取字符串长度
	echo ${bar:1:4} # 提取字符串, index从0开始, 注意包括第4个

	% ./foo.sh
	12
	ello

条件:

`test` 或 `[` 命令

	if test -f file.c ; then
		...
	fi

	或

	if [ -f file.c ]
		...
	fi


字符串比较:

	str1 = str2
	str1 != str2
	str1 > str2
	str1 < str2
	-n str  如果字符串不为空则为True
	-z str  如果字符串为null，则结果为真


算数比较:

	exp1 -eq exp2	==
	exp1 -ne exp2	!=
	exp1 -gt exp2	>
	exp1 -ge exp2	>=
	exp1 -lt exp2	<
	exp1 -le exp2	<=
	!exp			如果exp为假则返回真


文件条件测试:

	-d file    directory
	-e file    exist
	-f file    common file
	-g file    set-group-id ???
	-r file    readable
	-s file    file space is not 0
	-u file    set-user-id ???
	-w file    writeable
	-x file    executeable

高级数学运算:

	(( expression ))

可以使用高级数学特性

	var++ / var-- / ++var / --var  前/后 自增/自减
	+= / -= 
	!		逻辑求反
	~		位求反
	**		幂运算
	<<		左移位
	>>
	&		按位与
	|
	&&		逻辑与
	||	


支持模式匹配的字符比较: TODO

	[[ expression ]]


### 控制结构 ###

if 判断:

	if condition
	then
		statement
	elif condition; then
		statement
	else
		statement
	fi


for 循环:

	for var in item1 item2
	do
		statement
	done

如循环一个序列:

	for var in {1..5}
	do
		echo $var
	done

[Bash For Loop Examples](http://www.cyberciti.biz/faq/bash-for-loop/)

C语言风格的for循环:

	#!/bin/bash

	for (( i=1; i<=5; ++i ))
	do
			echo $i
	done

while 循环:

	while condition
	do
		statenment
	done

无限循环(这里又用到了`:`shell builtin命令):

	#!/bin/bash

	while :
	do
		echo 'hello'
		sleep 1
	done

也可以:

	while true

或者

	for (( ; ; ))


until 循环:

	until condition
	do
		statenment
	done


case 语句:

	case var in
		passtern [| pattern]... ) statement1;;
		passtern [| pattern]... ) statement2;;
		...
	esac

如:

	#!/bin/sh
	# case statement
	echo "Please answer yes or no"
	read ans
	case "$ans" in
	    yes | y | Yes | YES )   echo "yes";;
	    no  | n | No  | NO  )   echo "no";;
	    * )                     echo "not match";;
	esac

	exit 0


逻辑条件 与(`&&`) 和 或(`||`):

	con1 && con2 && con3
	con1 || con2 || con3

  
函数:

	function_name(){
		statement
	}

或者:

	function function_name() {
		statement
	}

关键字`function`可有可无

函数里可以通过`return`语句返回结果或返回值

函数也可以传参, 不过参数没有在圆括号里定义, 和特殊变量里一样, 直接通过`$X`, `$@`等获取


数组:

定义格式

	array_name=(value1 value 2 value3 ...)

或者

	array_name[0]=xxx
	array_name[1]=xxx
	...

例子:

	% more foo.sh
	#!/bin/bash

	array=('one' 'two' 'three')

	array[3]='four'

	echo ${array[3]}  # 获取单个元素
	echo ${array[*]}  # 获取整个数组
	echo ${array[@]}  # 获取整个数组
	echo ${#array[*]}  # 获取数组的长度
	echo ${#array[@]}  # 获取数组的长度
	echo ${#array[2]}  # 获取单个元素的长度

	for v in "${array[*]}"
	do
			echo $v
	done

	for v in "${array[@]}"
	do
			echo $v
	done
	% ./foo.sh
	four
	one two three four
	one two three four
	4
	4
	5
	one two three four
	one
	two
	three
	four

其中`*`和`@`的关系和`$*`与`$@`一样.

printf输出:

和C语言的printf函数类似:

	% more foo.sh
	#!/bin/bash

	printf "Hello %s %d\n" 'Shell' 1024
	% ./foo.sh
	Hello Shell 1024

循环控制break和continue, 没啥好说...




#### 命令 ####

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


#### 补充 ####

算数运算  
$((...))  
x=$(($x+1))  



## 参考 ##

* Linux程序设计
* [Bash Manual](http://www.gnu.org/software/bash/manual/bashref.html)
* [Shell脚本编程30分钟入门](https://github.com/qinjx/30min_guides/blob/master/shell.md) 入门小手册
* [shell小教程](http://c.biancheng.net/cpp/view/6994.html) 和上一个内容基本一样, 不过多了一些实际例子
* [Advanced Bash-Scripting Guide](http://www.tldp.org/LDP/abs/html/) 最经典的教程了?
* [Linux Shell Scripting Tutorial](http://www.freeos.com/guides/lsst/) 还没看
* [Bash scripting Tutorial](http://linuxconfig.org/bash-scripting-tutorial)
* [Learning the shell](http://linuxcommand.org/learning_the_shell.php)
* [Writing shell script](http://linuxcommand.org/writing_shell_scripts.php)
* `man bash` 最根本的

