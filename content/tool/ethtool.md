---
title: "ethtool"
date: 2013-08-25 10:01
---


# ethtool #

用来查询网卡信息的

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


`Link detected` 可用来检测网线是否连接

# 修改历史 #

* 2013-07-11 : 创建
