---
title: "Ubuntu"
date: 2016-01-06 10:16
---

[TOC]

![Ubuntu Logo](http://design.ubuntu.com/wp-content/uploads/ubuntu-orange.gif)

* [Ubuntu官网](http://www.ubuntu.com/server)
* [Ubuntu Help](https://help.ubuntu.com/)


## 其它 ##

### remove vs purge ###

`apt-get` 的 `remove` 和 `purge` 区别:

* `remove`: 只删除软件包, 保留配置文件
* `purge`: 删除软件包和配置文件

这里的配置文件是指包添加的系统配置, 不包括用户自定义的配置.

参考:

* man apt-get
* [What is the Difference Between `apt-get purge` and `apt-get remove`?](http://askubuntu.com/questions/231562/what-is-the-difference-between-apt-get-purge-and-apt-get-remove)
* [What is the correct way to completely remove an application?](http://askubuntu.com/questions/187888/what-is-the-correct-way-to-completely-remove-an-application)
