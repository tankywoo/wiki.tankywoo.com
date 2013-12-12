---
title: "nmap"
date: 2013-08-17 07:32
---


[官方文档中文版](http://nmap.org/man/zh/)

	nmap 173.252.192.*
	可以检测1～254中有多少机器存活，当然也有可能机器什么端口都没开，但是存活

	nmap -A -T5 localhost
	-A: to enable OS and version detection
	-T5: -T<0-5>: Set timing template (higher is faster)


Nmap支持CIDR风格：

	host/numbit
	eg.
	nmap 192.168.1.1/24
	将会扫描192.168.1..0 ~ 192.168.1.255

Nmap还支持这种格式扫描：

	nmap 192.168.1-2.100-120
	将会扫描192.168.1.100～192.168.1.120 和 192.168.2.100～192.168.2.120
	nmap 192.168.1.1, 3, 5
	将会扫描192.168.1.1、192.168.1.3、192.168.1.5这三个


Ping扫描

	-sL 列表扫描
	-sP Ping扫描
	-P0 无Ping
	-PS
