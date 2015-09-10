---
title: "sed"
date: 2013-08-17 07:32
---

使用的是gnu sed, mac 下默认是bsd sed, mac下可以`brew install gnu-sed`

Stream EDitor, 流编辑器

## 格式 ##

	sed options script file

	* -e script 可以指定多个-e(后面举例)
	* -f file 从文件读取sed规则
	* -n 只输出匹配的行

## 替换(substitute) ##

	s/pattern/replacement/flag

	* 数字	    表明新文本将替换第几处模式匹配的地方
	* g		    所有匹配的都替换
	* p		    原来的内容也打印出来
	* w file    将替换的结果写到文件中

## 限制行数 ##

	* 数字			指定行数
	* 数字1,数字2	限定范围
	* $表示结尾行
	*
	* 其实还可以使用文本模式过滤器
	* /pattern/command 
	* eg. $ sed '/tankywoo/s/bash/csh/' /etc/passwd

## 删除行 ##

	sed 'd' mydata		#删除全部
	sed '1d' mydata		#删除第一行

这个同样也可以用于上面的模式匹配

## 插入和附加 ##

	插入i会在指定行前插入一个新行
	插入a会在指定行后插入一个新行
	echo "Test Line 2" | sed 'i\Test Line 1'
	echo "Test Line 2" | sed 'a\Test Line 1'

指定在某行插入字符串:

    # 在第5行插入hello world
    % sed -i '5ihello world' FILE

参考 [Insert a line at specific line number with sed or awk](http://stackoverflow.com/a/6537587/1276501)


## 修改 ##

	字符c是修改指定行的整行内容
	sed '3c\'		#修改第三行


## 转换 ##

	字符y是进行单个字符映射的转换，且是全局的
	sed 'y/abc/123' mydata
	会将所有的a转换成1，b转换成2，c转换成3


## 打印 ##

	* p 打印问本行
	* #	打印行号
	* l	列出行


## 文件操作 ##

	* w	写入文件
	* r	读入文件

---

(以下内容参考 Software Design 03期的sed详解及用法)

源文件:

	$ more input.txt
	aaabbbcccddd aaabbbcccddd
	AAABBBCCCDDD aaabbbcccddd
	1234567890!? !"#$%&'()?/'"

简单的替换:

	$ sed -e 's/bbb/eee/' input.txt
	aaaeeecccddd aaabbbcccddd
	AAABBBCCCDDD aaaeeecccddd
	1234567890!? !"#$%&'()?/'"

第一行前半部分的bbb被替换了, 后半部分没有; 第二行替换了;

因为sed是流编辑器, 以行为处理单元, 默认一行处理一次;

这里的`-e`没什么用, 可以不写.

可以加上`g`标志, 表示全局作用:

	$ sed -e 's/bbb/eee/g' input.txt
	aaaeeecccddd aaaeeecccddd
	AAABBBCCCDDD aaaeeecccddd
	1234567890!? !"#$%&'()?/

也可以在指定行上操作, 如只在第一行:

	$ sed -e '1s/bbb/eee/g' input.txt
	aaaeeecccddd aaaeeecccddd
	AAABBBCCCDDD aaabbbcccddd
	1234567890!? !"#$%&'()?/

sed的基本格式:

	sed [选项, 如-e] '[开始行,结束行]命令/查找字符串/替换字符串/[标志, 如g]' 输出文本 [> 输出文本]

关于命令, 除了s(替换), 还有:

* d (删除)
* p (打印)
* y (替换一个字符)
* w (写文件)
* n TODO

标志除了g(global全局), 还有:

* p (print 打印)
* w (write 输出文件)

可以同时指定多个标志

sed的默认分隔符是`/', 可以替换为其它字符. 比如替换路径时, 因为用反斜杠转义比较麻烦, 可以改分隔符:

	$ sed 's!/bin/bash!/bin/zsh!' /etc/passwd

替换字符串中, `&`表示匹配的字符串:

	$ sed -e 's/bbb/+&+/g' input.txt
	aaa+bbb+cccddd aaa+bbb+cccddd
	AAABBBCCCDDD aaa+bbb+cccddd
	1234567890!? !"#$%&'()?/

	$ sed -e 's/.*/output: &/g' input.txt
	output: aaabbbcccddd aaabbbcccddd
	output: AAABBBCCCDDD aaabbbcccddd
	output: 1234567890!? !"#$%&'()?/

p标志会打印替换的行(替换后的内容), 可以配合-n只输出替换的行:

	$ sed -e 's/aaa/EEE/' input.txt
	EEEbbbcccddd aaabbbcccddd
	AAABBBCCCDDD EEEbbbcccddd
	1234567890!? !"#$%&'()?/

	$ sed -e 's/aaa/EEE/p' input.txt
	EEEbbbcccddd aaabbbcccddd
	EEEbbbcccddd aaabbbcccddd
	AAABBBCCCDDD EEEbbbcccddd
	AAABBBCCCDDD EEEbbbcccddd
	1234567890!? !"#$%&'()?/

	$ sed -n -e 's/aaa/EEE/p' input.txt
	EEEbbbcccddd aaabbbcccddd
	AAABBBCCCDDD EEEbbbcccddd

w标志后接输出文件, 只写入替换的行; w命令输出包括不匹配的行:

	$ sed -e 's/aaa/EEE/w output.txt' input.txt
	EEEbbbcccddd aaabbbcccddd
	AAABBBCCCDDD EEEbbbcccddd
	1234567890!? !"#$%&'()?/

	$ more output.txt
	EEEbbbcccddd aaabbbcccddd
	AAABBBCCCDDD EEEbbbcccddd

	$ sed -e 's/aaa/EEE/' -e 'w output.txt' input.txt
	EEEbbbcccddd aaabbbcccddd
	AAABBBCCCDDD EEEbbbcccddd
	1234567890!? !"#$%&'()?/

	$ more output.txt
	EEEbbbcccddd aaabbbcccddd
	AAABBBCCCDDD EEEbbbcccddd
	1234567890!? !"#$%&'()?/

y 命令替换1个字符, 可以同时替换多个字符(和s命令不一样, y会替换一行中所有匹配的, 不需要g标志):

	# a -> E
	$ sed -e 'y/a/E/' input.txt
	EEEbbbcccddd EEEbbbcccddd
	AAABBBCCCDDD EEEbbbcccddd
	1234567890!? !"#$%&'()?/

	# a -> E; b -> F
	$ sed -e 'y/ab/EF/' input.txt
	EEEFFFcccddd EEEFFFcccddd
	AAABBBCCCDDD EEEFFFcccddd
	1234567890!? !"#$%&'()?/


d 命令删除, 可以指定行或全部:

	$ sed -e '2d' input.txt
	aaabbbcccddd aaabbbcccddd
	1234567890!? !"#$%&'()?/

	$ sed -e '1,2d' input.txt
	1234567890!? !"#$%&'()?/

	# 输出空
	$ sed -e 'd' input.txt

地址(限制行数):

* 默认未指定则是所有数据
* 3: 第3行
* 20,$: 从第20行到最后一行
* 10,5: 第10行; 如果结束行比开始行小, 则只有开始行
* /^[0-9]/ : 所有以数字开头的行
* 15,/Z$/ : 从第15行到以Z结束的行为止
* 5,10! : 第第5行到除第10行以外的行(5-9, 11-最后一行)

例子:

	$ more input.txt
	abcd
	1234
	1aff
	cd23

	$ sed '/^[0-9]/s/.*/output: &/' input.txt
	abcd
	output: 1234
	output: 1aff
	cd23

执行多个命令. 这里就是`-e`的用处了; 还可以用`;`分割:

	$ sed -e '2d' -e 's/bbb/EEE/' input.txt
	aaaEEEcccddd aaabbbcccddd
	1234567890!? !"#$%&'()?/

	$ sed '2d;s/bbb/EEE/' input.txt
	aaaEEEcccddd aaabbbcccddd
	1234567890!? !"#$%&'()?/

关于写文件, 除了之前用到的重定向标准输出, w命令/标志, 还可以用`-i`直接写源文件本身.

在-i可接一个后缀表示先备份替换前的源文件, 再直接写入源文件:

	$ sed -i.bak '2d;s/bbb/EEE/' input.txt

	$ more input.txt
	aaaEEEcccddd aaabbbcccddd
	1234567890!? !"#$%&'()?/

	$ more input.txt.bak
	aaabbbcccddd aaabbbcccddd
	AAABBBCCCDDD aaabbbcccddd
	1234567890!? !"#$%&'()?/

注意, 一般情况下, sed的替换规则用单引号, 除非想使用一些自定义或环境变量.

可以把sed的替换命令写入文件, 使用`-f`选项读取.

	$ more sample.sed
	2d
	s/bbb/EEE/

	$ sed -f sample.sed input.txt
	aaaEEEcccddd aaabbbcccddd
	1234567890!? !"#$%&'()?/

可以用花括号`{}`对命令进行组合:

	$ more sample.sed
	1,3{
			s/aaa/EEE/g
			y/abc/XYZ/
	}

	$ sed -f sample.sed input.txt
	EEEYYYZZZddd EEEYYYZZZddd
	AAABBBCCCDDD EEEYYYZZZddd
	1234567890!? !"#$%&'()?/

## 资料 ##

* [man手册](http://unixhelp.ed.ac.uk/CGI/man-cgi?sed)
* [sed](http://sed.sourceforge.net/sed1line_zh-CN.html)
* [sed](http://www.grymoire.com/Unix/Sed.html)
* [Software Design 03 - sed详解及用法]()
