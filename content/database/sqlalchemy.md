---
title: "SQLAlchemy"
date: 2015-09-30 19:00
---

[TOC]

## ORM是什么 ##

摘自[维基百科](https://en.wikipedia.org/wiki/Object-relational_mapping):

> Object-relational mapping (ORM, O/RM, and O/R mapping) in computer science is a programming technique for converting data between incompatible type systems in object-oriented programming languages. This creates, in effect, a "virtual object database" that can be used from within the programming language.

* O (Object) 表示对象, 是指object-oriented (OO) objects. 即在程序中根据数据表结构定义的对象模型.
* R (Relational) 关系数据模型, 即关系数据库的表结构
* M (Mapping) 将O与R之间建立映射关系

常规的方法是根据关系数据库表结构, 在程序中定义相应的对象模型, 如类. 但是这种做法既要维护代码逻辑层面, 还要维护存储层面. 表结构的改变也会带来很多的变动. ORM就是一个中间层, 封装了数据库底层的操作(如[CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)), 直接在代码层面定义数据模型, 进而方便操作, 因为封装了数据库底层API, 所以对于数据库的更换也不会影响到代码层面.

这篇[博客](http://blog.csdn.net/u010028869/article/details/47094973)总结的挺不错的, 包括图解.

StackOverflow上还有两个关于什么是ORM, 以及其作用的讨论:

* [What is an ORM and where can I learn more about it?](http://stackoverflow.com/questions/1279613/what-is-an-orm-and-where-can-i-learn-more-about-it)
* [What is an Object-Relational Mapping Framework?](http://stackoverflow.com/questions/1152299/what-is-an-object-relational-mapping-framework)

这里有两个反对的讨论, 还没去看:

* [ORM Is an Offensive Anti-Pattern](http://www.yegor256.com/2014/12/01/orm-offensive-anti-pattern.html)
* [Why I Do Not Use ORM](http://database-programmer.blogspot.sg/2008/06/why-i-do-not-use-orm.html)


## SQLAlchemy ##

* [SQLAlchemy Doc](http://docs.sqlalchemy.org/en/latest/index.html)
* [Overview](http://docs.sqlalchemy.org/en/latest/intro.html)
* [Object Relational Tutorial](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html) 必看
* [Relationship Configuration](http://docs.sqlalchemy.org/en/latest/orm/relationships.html)
* [SQLAlchemy 0.7学习笔记](http://wangye.org/blog/archives/718/) 基于0.7, 参考的是Object Relational Tutorial, 总结的不错.
* [SQLAlchemy参考](http://www.zouyesheng.com/sqlalchemy.html) 总结的很详细, 好资料


## Flask w/ SQLAlchemy ##

* [Flask-SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/) 对SQLAlchemy的封装, 简化了很多操作.
* [Declaring Models](https://pythonhosted.org/Flask-SQLAlchemy/models.html) 介绍了简单的/一对多/多对多三种模型
* [SQLAlchemy in Flask](http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/) 介绍了原生的SQLAlchemy在Flask中的操作



## 其它参考 ##

* [SQLAlchemy 使用经验](http://www.keakon.net/2012/12/03/SQLAlchemy%E4%BD%BF%E7%94%A8%E7%BB%8F%E9%AA%8C)
* [SQLAlchemy 学习笔记](https://github.com/lzjun567/note/blob/master/note/python/sqlalchemy.md)
* [SQLAlchemy中文指南](http://www.91python.com/archives/393)
