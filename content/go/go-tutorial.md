---
title: "Go入门笔记"
date: 2016-12-15 22:00
---

关于`GOROOT`和`GOPATH`环境变量, 如果是系统默认安装, 而非自定义的安装目录, 则`GOROOT`不需要设置.

> GOROOT must be set only when installing to a custom location. [from](https://golang.org/doc/install#install)

关于`GOPATH`, 必须设置, 在get/build/install包时用到, 第三方的包都会装在这个目录下, 包括里面的二进制文件, 所以建议将`$GOPATH/bin`加入到`$PATH`环境变量中. 更多可以`go help gopath`.
