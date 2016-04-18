---
title: "Python Tips"
date: 2016-02-06 22:00
updated: 2016-04-18 11:40
description: "Python查漏补缺, 或收集一些不错的链接"
log: "新增list和dict释放空间"
---

[TOC]

### variable with underscore ###

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

### property method ###

* [Python Docs - property](https://docs.python.org/2/library/functions.html#property)
* [Python @property versus getters and setters](http://stackoverflow.com/questions/6618002/python-property-versus-getters-and-setters)
* [Python进阶之“属性（property）”详解](http://python.jobbole.com/80955/)
* [Properties vs. Getters and Setters](http://www.python-course.eu/python3_properties.php)


### 计算目录的md5 ###

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


### virtualenv对系统级包的策略 ###

最近发现使用virtualenv进入一个隔离环境时, 每次cd切换目录都会报错, 原因是autojump(py写的)模块找不到。

排查后发现是系统级的python包目录不在`sys.path`中。

看了virtualenv的changelog发现这个是在1.7版本做的变更:

* virtualenv-1.7 之前, 默认策略是把把系统包路径也加入 `sys.path`. 有 `--no-site-packages` 在创建虚拟环境时, 可以不加入系统包路径.
* virtualenv-1.7和之后, 默认策略是上面的 `--no-site-packages`. 并且增加了新选项 `--system-site-packages`, 即上面情况的默认策略.

具体可以看看virtualenv 的 [changelog](https://virtualenv.pypa.io/en/latest/changes.html)

我之前应该很长一阵子都处于1.7之前的版本, 最近才作了下升级.


### list和dict释放空间 ###

list:

* [how to release used memory immediately in python list?](http://stackoverflow.com/questions/12417498/how-to-release-used-memory-immediately-in-python-list)
* [python memory del `list[:]` vs `list = []`](http://stackoverflow.com/questions/2055107/python-memory-del-list-vs-list)

<!-- -->

* `a = []` 新赋值, 其它引用不变
* `del a` 删除a, 其它引用不变
* `del a[:]` 清空a的元素, 所有引用和a保持一样变化, 也为空

dict:

* [Difference between dict.clear() and assigning {} in Python](http://stackoverflow.com/questions/369898/difference-between-dict-clear-and-assigning-in-python)
* [Does dictionary's clear() method delete all the item related objects from memory?](http://stackoverflow.com/questions/10446839/does-dictionarys-clear-method-delete-all-the-item-related-objects-from-memory)

<!-- -->

* `d = {}` 新赋值，其它引用不变
* `del d` 删除d, 其它引用不变
* `d.clear()` 清空d的元素, 所有引用和d保持一样变化, 也为空
