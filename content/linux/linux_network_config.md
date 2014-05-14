---
title: "Linux Network Configuration"
date: 2013-08-17 07:23
---


## 直接用ifconfig配置 ##

	设置网卡eth0的IP地址和子网掩码
	sudo ifconfig eth0 192.168.2.106 netmask 255.255.255.0
	设置网关
	sudo route add default gw 192.168.2.254
	配置DNS
	sudo vim /etc/resolv.conf

## Gentoo 网络配置文件 ##

	sudo vim /etc/conf.d/net
	# 我的网卡名叫 enp2s1
	
	# This blank configuration will automatically use DHCP for any net.*
	# scripts in /etc/init.d.  To create a more complete configuration,
	# please review /usr/share/doc/openrc*/net.example* and save your configuration
	# in /etc/conf.d/net (this file :]!).

	# DHCP 方式
	config_enp2s1=("dhcp")

	# 静态 IP
	config_enp2s1=("192.168.1.100 netmask 255.255.255.0 brd 192.168.1.255")
	routes_enp2s1=("default via 192.168.1.1")	# 设置默认路由(网关)
	dns_servers="8.8.8.8"
	dns_search="the.dnsdomain.to.search"		# 设置 dns 默认搜索域

	#配置多个路由:
	routes_enp2s1=(
		"192.0.0.0/8 via 192.0.0.1"
		"default via 192.168.1.1"
	)

详细配置参考: /usr/share/doc/openrc\*/net.example\*

## Ubuntu 网络配置文件 ##

	sudo vim /etc/network/interfaces

	DHCP连接
	auto eth0
	iface eth0 inet dhcp

	手动配置静态ip
	auto eth0
	iface eth0 inet static
	address 192.169.2.106
	gateway 192.168.2.254
	netmask 255.255.255.0
	#network ?.?.?.?
	#broadcast ?.?.?.?

	# dns设置
	# 我印象中重启后resolv.conf的内容会删除
	# 所以DNS服务器的配置也是在/etc/network/interfaces下
	dns-nameservers 8.8.8.8
	dns-search xxx.xxx.xxx...

	# 添加一条静态路由
	up route add -net 192.0.0.0/8 gw 192.0.0.1 dev eth0

## 参考链接 ##

* [static routing](http://wiki.gentoo.org/wiki/Static_Routing)

