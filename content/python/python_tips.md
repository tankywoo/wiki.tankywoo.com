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
