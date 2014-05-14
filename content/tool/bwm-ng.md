---
title: "bwm-ng"
date: 2013-08-17 07:32
---

Bandwidth Monitor NG (Next Generation), a live bandwidth monitor for network and disk io.

一个用于实时监控网络流量和硬盘io的软件, 在流量监控方面感觉比 `iftop` 更简单一些

gentoo下直接安装`net-analyzer/bwm-ng`就行了

在man手册里看到, 输出显示的格式可以是 curses, curses2, plain, csv, html 等格式  
不过`bwm-ng -h`看到只支持curses, curses2, plain.

查看流量数据:

	bwm-ng

查看硬盘io数据:

	bwm-ng -i disk
