---
title: "top / htop / atop"
date: 2013-08-17 07:32
description: "进程管理监控工具"
---


htop及类似的工具很多, 暂时接触过的有以下几个:

* top
* htop
* atop

没有最好, 完全看个人爱好了. 我就比较喜欢htop.

## top ##

关于top, 直接借用好基友 磊妹 的文章:

* [Top基本介绍](http://kumu-linux.github.io/blog/2013/06/02/top/)
* [Top实践小技巧](http://kumu-linux.github.io/blog/2013/06/07/top-hacks/)

很多用法也是从他那里学到的

最近在公司的一台服务器发现一台好像是8核cpu的机器, 一个进程的cpu跑到了9999%. 但是htop显示一切正常, 应该是top计算有bug.

常用的参数:

* `-b`: 以 `batch`方式运行, 如果没有加-n参数, 则和正常top一样, 一直循环输出. 适合输出给其它程序或文件
* `-n <X>`: 指定循环次数
* `-c`: command-line/program-name切换, 按c
* `-H`: 线程模式, 默认只输出进程, 按H
* `-p <pid>`: 监控指定的pid
* `-u <username>`: 监控指定用户进程


## htop ##

htop底部已经显示了一些帮助的快捷键, 不过有一些功能键我这里按不了, 估计是虚拟机按键受限的原因.

htop有几个亮点:

* 直接按 `h` 可以看到帮助
* 可以通过`方向键上下`或`鼠标`选择相应的进程
* 可以按进程用户筛选
* 按`space`键来高亮标记一些进程, 方便查看
* 可以直接使用快捷键`l`调用lsof查看该进程开启的文件
* ...

## atop ##

这玩意暂时还不熟, 输出的内容太多了.

* [One-stop performance analysis using atop](https://lwn.net/Articles/387202/)
* [How to Perform Load Monitoring in Linux Using atop](https://www.maketecheasier.com/load-monitoring-linux-atop/)
* [Linux Basics: Monitor System Resources And Processes Using Atop](http://www.unixmen.com/linux-basics-monitor-system-resources-processes-using-atop/)
