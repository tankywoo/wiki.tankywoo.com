---
title: "Python Tips"
date: 2016-02-06 22:00
updated: 2016-02-06 22:00
description: "Python查漏补缺, 或收集一些不错的链接"
---

[TOC]

## variable with underscore ##

* [Python Docs - Private Variables and Class-local References](https://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references)
* [The meaning of a single- and a double-underscore before an object name in Python](http://stackoverflow.com/questions/1301346/the-meaning-of-a-single-and-a-double-underscore-before-an-object-name-in-python)
* [Underscore vs Double underscore with variables and methods](http://stackoverflow.com/questions/6930144/underscore-vs-double-underscore-with-variables-and-methods)
* [Private, protected and public in Python](http://radek.io/2011/07/21/private-protected-and-public-in-python/)

@nmichaels's answer:

	- _single_leading_underscore: weak "internal use" indicator.  E.g. "from M
	  import *" does not import objects whose name starts with an underscore.

	- single_trailing_underscore_: used by convention to avoid conflicts with
	  Python keyword, e.g.

	  Tkinter.Toplevel(master, class_='ClassName')

	- __double_leading_underscore: when naming a class attribute, invokes name
	  mangling (inside class FooBar, __boo becomes _FooBar__boo; see below).

	- __double_leading_and_trailing_underscore__: "magic" objects or
	  attributes that live in user-controlled namespaces.  E.g. __init__,
	  __import__ or __file__.  Never invent such names; only use them
	  as documented.

## property method ##

* [Python Docs - property](https://docs.python.org/2/library/functions.html#property)
* [Python @property versus getters and setters](http://stackoverflow.com/questions/6618002/python-property-versus-getters-and-setters)
* [Python进阶之“属性（property）”详解](http://python.jobbole.com/80955/)
* [Properties vs. Getters and Setters](http://www.python-course.eu/python3_properties.php)


## 计算目录的md5 ##

也就是遍历目录, 计算所有文件内容合并后的md5值。

**注意**: 保证遍历目录的路径是一致的, 否则跨平台遍历方式不一致导致md5不同。

见Simiki中的实现: [Add directory md5 hash function](https://github.com/tankywoo/simiki/commit/09039e10a9eba2436b1ec74c5d8a6e1cf84c0f5b), 另外, 这个可能还需要考虑内存溢出的情况? TODO

另外可参考:

* [How do I get the MD5 sum of a directory's contents as one sum?](http://unix.stackexchange.com/questions/35832/how-do-i-get-the-md5-sum-of-a-directorys-contents-as-one-sum)
* [Getting the SHA-1 (or MD5) hash of a directory (Python recipe)](http://code.activestate.com/recipes/576973-getting-the-sha-1-or-md5-hash-of-a-directory/)


### pip install from git repo ###

	$ pip install -e git+https://github.com/username/projname.git#egg=projname

参考:

* [pip install from github repo branch](http://stackoverflow.com/questions/20101834/pip-install-from-github-repo-branch)
* [pip doc - VCS Support](https://pip.pypa.io/en/latest/reference/pip_install/#vcs-support)
