---
title: "aria2"
date: 2016-05-21 20:30
collection: "其它"
---

[TOC]

## 介绍 ##

aria2是一个轻量级的下载工具，跨平台，使用C++编写，支持多种协议：

* HTTP(S)
* FTP
* SFTP
* BitTorrent
* ...

链接：

* [官网页面](https://aria2.github.io/)
* [manual](https://aria2.github.io/manual/en/html/)
* [Github](https://github.com/aria2/aria2)

## 基本用法 ##

命令行`aria2c`，直接接下载url，默认无配置会下载到当前目录下。

如：

	aria2c -s 5 -c http://mirrors.aliyun.com/linux-kernel/v4.x/linux-4.4.6.tar.gz

其中：

* `-s N` 分段下载
* `-c` 断点续传

## rpc server ##

TODO

## 参考 ##

* [aria2配置示例](http://blog.binux.me/2012/12/aria2-examples/)
* [Aria2——Unix 系统中潜行的下载神器](http://azeril.me/blog/Aria2.html)
