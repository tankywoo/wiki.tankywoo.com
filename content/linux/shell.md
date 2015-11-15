---
title: "Shell"
date: 2013-08-17 07:23
---

[TOC]

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

变量分为全局变量(环境变量)和局部变量:

> Global variables or environment variables are available in all shells. --- [Bash Beginners Guide](http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_03_02.html)

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

例子:

	% more foo.sh
	#!/bin/bash
	x=10
	echo $x
	x=$(( $x + 1 ))
	echo $x
	(( x += 1 ))
	echo $x

	% ./foo.sh
	10
	11
	12

支持模式匹配的字符比较:

	[[ expression ]]

如:

	% more foo.sh
	#!/bin/bash
	foo='hello'
	if [[ $foo =~ llo$ ]]; then
		echo 'match'
	else
		echo 'not match'
	fi

	% ./foo.sh
	match

参考:

* [bash regex match string](http://stackoverflow.com/questions/17420994/bash-regex-match-string)
* [check if string match a regex in BASH Shell script](http://stackoverflow.com/questions/21112707/check-if-string-match-a-regex-in-bash-shell-script)


控制结构

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


## 内置命令(shell builtin) ##

内置的命令列表及解释都可以在`man 1 bash`中看到, 也可以通过`type`命令确定命令的类型:

	% type echo
	echo is a shell builtin

`:` 命令, 之前已经用到了, 后可接参数, 没有任何作用, 相当于Python里的pass

> : [arguments]
> 
>    No effect; the command does nothing beyond expanding arguments and performing any specified redirections.  A zero exit code is returned.

`.`和`source`命令, 后接脚本文件名, 执行指定的脚本.

> .  filename [arguments]
> 
> source filename [arguments]
> 
>    Read and execute commands from filename in the current shell environment and return the exit status of the last command executed from filename.

`printf` 输出:

和C语言的printf函数类似:

	% more foo.sh
	#!/bin/bash

	printf "Hello %s %d\n" 'Shell' 1024
	% ./foo.sh
	Hello Shell 1024

简单的输出还有`echo`命令

循环控制 `break` 和 `continue`, 和C/Python等有点不同, 可以后接数字, 表示break/continue的层级, 默认是1, 多级退出一般用在多级循环; 类似于C里的goto配合break/continue.

`eval` 对语句进行求值

    % more foo.sh
    #!/bin/bash

    foo=10

    x=foo
    echo $x

    y='$'$x
    echo $y

    eval y='$'$x
    echo $y

	# 执行结果
    % ./foo.sh
    foo
    $foo
    10

`expr` 把参数当作表达式来求值

	% more foo.sh
	#!/bin/bash
	x=5

	x=`expr $x + 1`
	echo $x

	x=$(expr $x+2)
	echo $x

	% ./foo.sh
	6
	6+2

`exec` 后接命令, 用fork的子进程替换原来的父进程

> exec [-cl] [-a name] [command [arguments]]
> 
>    If command is specified, it replaces the shell.  No new process is created.

`exit n` 退出当前shell, 指定退出状态码

`return` 函数退出并返回返回值

`export` 和直接赋值变量的区别是export后, 子进程也可以使用这个变量

> export [-fn] [name[=word]] ...
> 
> export -p
> 
>    The supplied names are marked for automatic export to the environment of subsequently executed commands.

	% foo=100
	% bash -c 'echo $foo'

	% export foo
	% bash -c 'echo $foo'
	100

[Defining a variable with or without export](http://stackoverflow.com/questions/1158091/defining-a-variable-with-or-without-export)

`set` 当没接参数时, 输出所有shell的变量, 包括全局变量和局部变量; 如果接参数, 则是开启/关闭shell的属性.

> set [--abefhkmnptuvxBCEHPT] [-o option-name] [arg ...]
> 
> set [+abefhkmnptuvxBCEHPT] [+o option-name] [arg ...]
> 
>    Without  options,  the  name  and  value  of each shell variable are displayed in a format that can be reused as input for setting or resetting the currently-set variables.  Read-only variables cannot be reset.  In posix mode, only shell variables are listed.  The output is sorted according to the current locale.  When options are specified, they set or unset shell attributes.

% set -o 显示所有的set选项配置情况, on/off形式
% set +o 显示所有的set选项配置情况, 命令形式

参考:

* [shell 下的 set 命令](https://www.zybuluo.com/haokuixi/note/23988)
* [shell的set命令](http://segmentfault.com/a/1190000003005706)
* [What do the bash-builtins 'set' and 'export' do?](http://unix.stackexchange.com/questions/71144/what-do-the-bash-builtins-set-and-export-do)

`env`命令查看系统环境变量

使用export后的变量会出现在这里, unset后则去掉

`shift` 位置参数向左便宜

> shift [n]
> 
>    The positional parameters from n+1 ... are renamed to $1 ....  Parameters represented by the numbers $# down to $#-n+1 are unset.

	% more foo.sh
	#!/bin/bash
	echo $@
	echo $1
	shift
	echo $1
	shift
	echo $1

	% ./foo.sh one two
	one two
	one
	two
			  # <---- 空行, 因为参数为空了


`unset` 取消指定变量

注意, unset 命令不是对set命令做反操作!!!

	% echo $foo
	100
	% unset foo
	% echo $foo

	%

> unset [-fv] [name ...]
> 
>    For each name, remove the corresponding variable or function.


## 补充 ##

关于`true`和`false`:

shell里没有boolean值, 不过有true和false这两个shell builtin命令:

TankyWoo ~/dev_env/bash_learn % which true false
true: shell built-in command
false: shell built-in command

既然是命令, 就不能用`[ ]`或`test`来判断, 直接使用:

	#!/bin/bash
	if true; then
		echo 'True'
	else
		echo 'False'
	fi

或者:

	TankyWoo ~/dev_env/bash_learn % true && echo $?
	0
	TankyWoo ~/dev_env/bash_learn % false && echo $?

因为false, 所以后面不会输出echo $?

一般情况下, 判断某个变量是true/false:

	#!/bin/bash
	flag=true
	if [ "$flag" = false ]; then
		echo 'False'
	elif [ "$flag" = true ]; then
		echo 'True'
	else
		echo 'Nothing'
	fi

具体讨论见:

* [Bash if [ false ] ; returns true](http://stackoverflow.com/questions/19670061/bash-if-false-returns-true)
* [How to declare and use boolean variables in shell script?](http://stackoverflow.com/questions/2953646/how-to-declare-and-use-boolean-variables-in-shell-script)

生成一个range, 如1到10:

    echo `seq 1 10`

或者:

    echo {1..10}

## 参考 ##

* Linux程序设计
* [Bash Manual](http://www.gnu.org/software/bash/manual/bashref.html)
* [如何调试bash脚本](http://coolshell.cn/articles/1379.html)
* [Shell脚本编程30分钟入门](https://github.com/qinjx/30min_guides/blob/master/shell.md) 入门小手册
* [shell小教程](http://c.biancheng.net/cpp/view/6994.html) 和上一个内容基本一样, 不过多了一些实际例子
* [Advanced Bash-Scripting Guide](http://www.tldp.org/LDP/abs/html/) 最经典的教程了?
* [Linux Shell Scripting Tutorial](http://www.freeos.com/guides/lsst/) 还没看
* [Bash scripting Tutorial](http://linuxconfig.org/bash-scripting-tutorial)
* [Learning the shell](http://linuxcommand.org/learning_the_shell.php)
* [Writing shell script](http://linuxcommand.org/writing_shell_scripts.php)
* `man bash` 最根本的

