---
title: "ethtool"
date: 2013-08-25 10:01
---


用来查询网卡信息

直接接网卡名:

	19:36 tankywoo@gentoo-gs /home/tankywoo/wiki
	% sudo ethtool enp2s1
	Settings for enp2s1:
			Supported ports: [ TP ]
			Supported link modes:   10baseT/Half 10baseT/Full
									100baseT/Half 100baseT/Full
									1000baseT/Full
			Supported pause frame use: No
			Supports auto-negotiation: Yes
			Advertised link modes:  10baseT/Half 10baseT/Full
									100baseT/Half 100baseT/Full
									1000baseT/Full
			Advertised pause frame use: No
			Advertised auto-negotiation: Yes
			Speed: 1000Mb/s
			Duplex: Full
			Port: Twisted Pair
			PHYAD: 0
			Transceiver: internal
			Auto-negotiation: on
			MDI-X: off
			Supports Wake-on: d
			Wake-on: d
			Current message level: 0x00000007 (7)
								   drv probe link
			Link detected: yes


`Link detected` <strike>可用来检测网线是否连接</strike>。在这里被坑过，之前一直错误的理解为链路连接正常，即插上线就是yes，其实这里是指网卡是否up。

就算插上线，但是网卡没有启动，依然是no。

这个[回答](http://stackoverflow.com/a/808595/1276501)中@Jamie Kitson的评论也提到了这点。


`-i` 参数可以查看网卡驱动类型:

	tankywoo@gentoo-local::~/ » sudo ethtool -i enp0s5
	driver: e1000
	version: 7.3.21-k8-NAPI
	firmware-version:
	bus-info: 0000:00:05.0
	supports-statistics: yes
	supports-test: yes
	supports-eeprom-access: yes
	supports-register-dump: yes
	supports-priv-flags: no


* [9 Linux ethtool Examples to Manipulate Ethernet Card (NIC Card)](http://www.thegeekstuff.com/2010/10/ethtool-command/)
