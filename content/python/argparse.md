---
title: "argparse"
date: 2013-08-17 07:39
---


最近在写Nagios的插件，因为一个插件会涉及到很多的命令行参数选项，所以argparse这个模块就大大的发挥了作用

在python 2.7以前是optparse，不过到了python 2.7，optparse已经不推荐了，官方新出了argparse

使用command-line parser要比sys.argv方便&友好多了

# 基本步骤 #

* Creating a parser : `ArgumentParser`
* Adding arguments : `add_argument`
* Parsing arguments : `parse_args`


# add_argument #

## name or flags ##

positional argument是什么意思？

example:

	import argparse
	parser = argparse.ArgumentParser(description="argparse test")
	parser.add_argument('-f', '--foo')
	parser.add_argument('bar')
	print parser.print_help()

	>>>
	$ python test.py
	usage: test.py [-h] [-f FOO] bar

	argparse test

	positional arguments:	<---注意这里
	  bar

	optional arguments:
	  -h, --help         show this help message and exit
	  -f FOO, --foo FOO
	None


## action ##

这个参数用来设置保存

默认是`store`，保存的是str类型

其中`store_const`的用法见example:


	import argparse
	parser = argparse.ArgumentParser(description="argparse test")
	parser.add_argument('-f', '--foo', action='store_const', const=42)

	print parser.parse_args(['-f'])

	>>>
	$ python test.py
	Namespace(foo=42)


example中-w的store_const配合`const`来使用，如果有-w参数，则其值为42，不能指定值;如果没有-w参数，则其值是None

学过C/C++的就很好容易理解const这个的意义了

`store_true`和`store_false`这两个是用来保存boolean值的，不过容易搞混，可以写个test example来理解

*TODO*

`append`是附加，用于输入多个相同参数，example:

	import argparse
	parser = argparse.ArgumentParser(description="argparse test")
	parser.add_argument('-f', '--foo', action='append')

	print parser.parse_args("-f 5 -f 8".split())

	>>>
	$ python test.py
	Namespace(foo=['5', '8'])

如果不使用append，则-f的值只有8

关于`append_const`，就是`append`和`const`的结合，example:

	import argparse
	parser = argparse.ArgumentParser(description="argparse test")
	parser.add_argument('--str', dest='types', action='append_const', const=str)
	parser.add_argument('--int', dest='types', action='append_const', const=int)
	print parser.parse_args('--str --int'.split())

	>>>
	$ python test.py
	Namespace(types=[<type 'str'>, <type 'int'>])

这个example很有意义

首先可以看到，两个add_argument的dest值是一样的，以前没注意到，这样也可以append

另外，const还可以是类型值


`count`就是记录参数个数的值

还可以自定义help和version信息

## nargs ##

`nargs`指定某个参数后面要接的值得个数，有以下几个值可以使用

`N(an integer)`	-	比如2，那么其后接的值的个数就必须是2个
`?`	-	表示可以接0或1个值
`*`	-	表示可以接0或多个值
`+`	-	表示可以接1或多个值

*TODO*

这个在与`store_const`混用要注意，本来`store_const`后面不能接值，但是比如和nargs='?'一起用后，则可以接1个值，example:

	import argparse
	parser = argparse.ArgumentParser(description="argparse test")
	parser.add_argument('-f', '--foo', nargs='?', const=42)

	print parser.parse_args("".split())
	print parser.parse_args("-f".split())
	print parser.parse_args("-f 100".split())

	>>>
	$ python test.py
	Namespace(foo=None)
	Namespace(foo=42)
	Namespace(foo='100')


## const ##

这个是配合：

* `store_const` 或 `append_const`
* nargs='?'

使用的

具体还需要研究 *TODO*


## default ##
用于设置默认值

## type ##
用于指定参数值的类型

## choices ##
用于限定参数的值的范围

比如choice = ['a', 'b', 'c']则参数只能在这几个中选择

example:

	import argparse
	parser = argparse.ArgumentParser(description="argparse test")
	parser.add_argument('-f', '--foo', choices=['a', 'b', 'c'])

	print parser.parse_args("-f d".split())

	>>>
	$ python test.py
	usage: test.py [-h] [-f {a,b,c}]
	test.py: error: argument -f/--foo: invalid choice: 'd' (choose from 'a', 'b', 'c')


## required ##
表明这个参数是必须写的

## dest ##
用于指定存储参数值的变量名

## metavar ##
不写此参数时，help信息会自动成成usage的命令行格式

metavar可以修改help信息中的命令行的参数

example:

	import argparse
	parser = argparse.ArgumentParser(description="argparse test")
	parser.add_argument('-f', '--foo')
	parser.add_argument('-w', '--woo', metavar='hello')

	print parser.print_usage()

	>>>
	$ python test.py
	usage: test.py [-h] [-f FOO] [-w hello]	<--- 这里-w后面就不是WOO了，而是hello
	None



# Read More #

* [python doc -- argparse](http://docs.python.org/2/library/argparse.html)
* [PyMOTW -- argparse](http://www.doughellmann.com/PyMOTW/argparse/)


# History #

Create 2013/02/07

Last modified 2013/02/07
