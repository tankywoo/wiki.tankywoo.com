# ClassMethod and StaticMethod #

# 主要 #

* Functions
	* staticmethod
	* classmethod
* Decorator

# Example #

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	# wutq@2013-02-20

	class A(object):
	    @classmethod
	    def cm(cls):
	        print '类方法cm(cls)调用者：', cls.__name__

	    @staticmethod
	    def sm():
	        print '静态方法sm()被调用'

	class B(A):
	    pass

	A.cm()
	B.cm()
	A.sm()
	B.sm()

	# $ Output
	# 类方法cm(cls)调用者： A
	# 类方法cm(cls)调用者： B
	# 静态方法sm()被调用
	# 静态方法sm()被调用


* [python之静态和类方法：staticmethod和classmethod内置函数](http://blog.csdn.net/qigan30125/article/details/7550338)
* [理解python的staticmethod与classmethod实现](http://luozhaoyu.iteye.com/blog/1506376)

Python文档里有一句话：
**Static methods in Python are similar to those found in Java or C++.**

把python的static method理解成为c++/java的类的static方法就差不多了

一个staticmethod和一个普通的global method没有太大的区别，放在类里面主要基于模块化的考虑。

SOF上关于两者的讨论:

* [What is the difference between @staticmethod and @classmethod in Python?](http://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python)
* [Python @classmethod and @staticmethod for beginner?](http://stackoverflow.com/questions/12179271/python-classmethod-and-staticmethod-for-beginner)
