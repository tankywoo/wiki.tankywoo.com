---
title: "iptables"
date: 2013-08-17 07:32
updated: 2017-12-18 15:37
collection: "网络相关"
log: "增加多线路由策略"
---


iptables:按照官方文档，是一个ipv4 包过滤和NAT的管理工具

先开始好像使用iptables命令时，报错，提示没有netfilter模块

后来make maenuconfig添加后，重新编译一遍，就OK了

其实这个问题折腾了半天，好像是参考这篇：
[Iptables for newbies](http://en.gentoo-wiki.com/wiki/HOWTO_Iptables_for_newbies)

## 一些术语 ##

### Chain ###

Each chain is a list of rules which can match a set of packets.

### Table ###

` filter `
` nat `
` mangle `
` raw `
` security `


## Example ##

	iptables -L
	iptables -F
	iptables -X


## iptables 配合 iproute2 实现多线策略

一台内网网关机器, 有三个网卡(以下ip为臆造):

- eth0: 内网网关 192.168.0.1
- eth1: 联通出口 1.1.1.1
- eth2: 电信出口 2.2.2.2

内网用户连接网关

对于网段 192.168.1.0/24 的内网用户，从eth1走

对于网段 192.168.2.0/24 的内网用户，从eth2走

使用 `iproute2` 配合 `iptables` 可以处理这种情况.

添加俩个table, wan-ctc和wan-cuc

	$ more /etc/iproute2/rt_tables
	#
	# reserved values
	#
	200     wan-cuc
	201     wan-ctc

	255     local
	254     main
	253     default
	0       unspec
	#
	# local
	#
	#1      inr.ruhep

添加两条路由:

	ip route add default via 1.1.1.1 dev eth1 table wan-cuc
	ip route add default via 2.2.2.2 dev eth2 table wan-ctc

添加策略路由:

	ip rule add fwmark 0x1 table wan-cuc prio 200
	ip rule add fwmark 0x2 table wan-ctc prio 201

配合 iptables `mangle` 表的 `--set-mark` 可以给来自某网段的包加上标记:

	*mangle
	[0:0] -A PREROUTING -i eth0 -s 192.168.1.0/24 -j MARK --set-mark 1
	[0:0] -A PREROUTING -i eth0 -s 192.168.2.0/24 -j MARK --set-mark 2

标记从192.168.1.0/24过来的内网用户，标记为1，从192.168.2.0/24过来的标记为2. 对应 ip rule 里 `fwmark 0x1` 和 `fwmark 0x2`

另外这里还得做好SNAT：

	*nat
	[0:0] -A POSTROUTING -o eth1 -s 192.168.0.0/16 -j SNAT --to-source 1.1.1.1
	[0:0] -A POSTROUTING -o eth2 -s 192.168.0.0/16 -j SNAT --to-source 2.2.2.2


## Read More ##

* [iptables入门：iptables构架、基本命令及扩展（功能）简介](http://lesca.me/archives/iptables-architecture-commands-extensions.html) 
* [iptables的基本概念和数据包流程图](http://www.ha97.com/4093.html)
* [Linux iptables 配置详解](http://www.21andy.com/blog/20120528/2043.html)
* [网络地址转换(NAT)](http://zh.wikipedia.org/wiki/%E7%BD%91%E7%BB%9C%E5%9C%B0%E5%9D%80%E8%BD%AC%E6%8D%A2)
