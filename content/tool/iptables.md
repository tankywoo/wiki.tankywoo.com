---
title: "iptables"
date: 2013-08-17 07:32
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


## Read More ##

* [iptables入门：iptables构架、基本命令及扩展（功能）简介](http://lesca.me/archives/iptables-architecture-commands-extensions.html) 
* [iptables的基本概念和数据包流程图](http://www.ha97.com/4093.html)
* [Linux iptables 配置详解](http://www.21andy.com/blog/20120528/2043.html)
* [网络地址转换(NAT)](http://zh.wikipedia.org/wiki/%E7%BD%91%E7%BB%9C%E5%9C%B0%E5%9D%80%E8%BD%AC%E6%8D%A2)
