---
title: "npm"
date: 2016-04-09 16:50
collection: "包管理"
log: "增加npm源说明"
---

[TOC]

## 基本使用 ##

对npm不熟, 记录一下.

	* npm help install
	* npm help 5 npm-folders
	* npm install [-g] <package>
	* npm list [-g] <package>

本地情况, `npm install <package>` 默认装到当前用户目录下的「node_modules」目录, 加上「-g」(global)则安装到`/usr/local/lib/node_modules/`下

`.npmrc`可以控制安装的prefix和路径等

原先`/usr/local/lib/node_modules/`的属主是nobody, 导致加上「-g」安装权限报错, 需要:

	$ sudo chown -R $USER /usr/local/lib/node_modules

查看包信息:

    npm install <package>

### NPM源 ###

本地访问官方npm源timeout，可以改为国内(如淘宝NPM)源。

查看当前的npm registry地址:

    $ npm config get registry

临时设置npm registry地址:

    $ npm config set registry https://registry.npm.taobao.org

或者只在install时指定:

    npm --registry https://registry.npm.taobao.org install <package>

永久则可以写入`.npmrc`:

    registry = https://registry.npm.taobao.org

或者使用`cnpm`:

* [CNPMJS](http://cnpmjs.org/)
* [淘宝NPM](http://npm.taobao.org/)

参考: [npm 换源 npm 国内镜像 cnpm](http://www.jianshu.com/p/ad29d97b0e9d)


参考:

* [NPM throws error without sudo](http://stackoverflow.com/questions/16151018/npm-throws-error-without-sudo)
* [How to run npm without sudo](http://www.competa.com/blog/2014/12/how-to-run-npm-without-sudo/)
* [NODE.JS HOWTO: INSTALL NODE+NPM AS USER](http://tnovelli.net/blog/blog.2011-08-27.node-npm-user-install.html)
* [A Beginner’s Guide to npm — the Node Package Manager](http://www.sitepoint.com/beginners-guide-node-package-manager/)
* [Introduction to npm](http://howtonode.org/introduction-to-npm)
