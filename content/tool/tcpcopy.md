---
title: "TCPCopy"
date: 2015-05-05 11:10
---

[TOC]

[TCPCopy](https://github.com/session-replay-tools/tcpcopy) 线上流量复制工具.

Github上的README讲的非常详细.

## 架构原理 ##

当前版本是v1.0, 架构原理图:

![Architecture Advance](https://raw.githubusercontent.com/wangbin579/auxiliary/master/images/advanced_archicture.GIF)

以前的架构是(网上一些博客还是基于这个架构):

![Architecture Traditional](https://raw.githubusercontent.com/wangbin579/auxiliary/master/images/traditional_archicture.GIF)

(图片来源[wangbin579/auxiliary](https://github.com/wangbin579/auxiliary))

以新架构为例，主要分三个部分:

* online server
* target server
* assistant server

两个工具:

* tcpcopy. 在online server上运行, 主要负责在截取实时请求
* intercept. 在assistant server上运行, 主要负责一些辅助的工作, 如将回应包信息传回给tcpcopy

测试程序在target server上运行

大致流程:

* tcpcopy在网络层(network layer)截取请求, 复制一份进行相应处理, 然后发给target server
* target server处理复制过来请求, 然后将相应信息返回给assistant server
* intercept收到传过来的包, 处理相应头, 然后传回给tcpcopy

target server唯一要做的就是保证有路由可以让包发送到assistant server

几点注意的地方:

* `ip_forward` should not be set on the assistant server

遇到的问题:

在编译安装intercept时, 遇到错误:

    checking for pcap.h … not found

需要先安装:

     apt-get install libpcap0.8-dev

## 例子 ##

服务器A(1.1.1.1)是线上机器, 服务器B(2.2.2.2)是测试机器, 需要将A的80端口流量复制到B的80端口

根据新架构, 将assistant server和target server放在一台机器上就行, 其实也就是在assistant server上部署web server来处理请求, 然后返回给自身的intercept.

assistant server/target server:

    /usr/local/intercept/sbin/intercept -l /var/log/intercept.log -b 2.2.2.2 -i eth1 -F 'tcp and src port 80' -d

* `-i` 指定监听的网卡
* `-b` 指定网卡上的地址, 默认是全部地址, 这里我指定地址是因为机器有多ip

这里有一点需要注意, intercept默认监听的端口是`36524`, 所以相应的防火墙需要对这个端口打开.

online server:

    /usr/local/tcpcopy/sbin/tcpcopy -l /var/log/tcpcopy.log -x 80-2.2.2.2:80 -s 2.2.2.2 -d

* `-x` 语法格式`localServerPort-targetServerIP:targetServerPort`
* `-s` intercept server的地址

还有`-c`参数用于修改请求的client ip, 但是我这里改了后有问题, 暂时未解决.

另外还有个需要注意的地方, 因为tcpcopy的通信端口默认是`36524`, 所以如果有规则限制则要把这个端口做相应范围的开放

    iptables -A INPUT -i eth1 -p tcp -s x.x.x.x/32 -m multiport --dports 36524 -j ACCEPT


## 参考 ##

* [使用tcpcopy导入线上流量进行功能和压力测试](http://jqlblue.github.io/2014/01/08/use-tcpcopy-test-online/)
* [初试tcpcopy](http://navyaijm.blog.51cto.com/4647068/1340809)
* [TCPCopy 应用](http://www.cnblogs.com/chenny7/p/3912515.html)
