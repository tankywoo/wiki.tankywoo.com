---
title: "Keepalived"
collection: "系统集群"
date: 2016-09-29 15:30
updated: 2016-09-29 15:30
log: ""
---

[TOC]

## 基本

Keepalived用于保证系统集群的高可用(HA, High Availability)。

核心是VRRP协议。

[keepalived配置应用与VRRP协议](http://bbs.linuxtone.org/home.php?mod=space&uid=11671&do=blog&id=550)中关于VRRP协议简介和工作机制介绍的挺清晰的。


## 问题

### bogus VRRP packet received

两台网关机器(gw-node-1, gw-node-2)，发现日志一直在报：

```text
2016-09-28T23:07:48.858959+08:00 gw-node-2 Keepalived_vrrp[63030]: bogus VRRP packet received on eth1 !!!
2016-09-28T23:07:48.858962+08:00 gw-node-2 Keepalived_vrrp[63030]: VRRP_Instance(GW-NODE-2) Dropping received VRRP packet...
2016-09-28T23:07:49.860028+08:00 gw-node-2 Keepalived_vrrp[63030]: VRRP_Instance(GW-NODE-2) IPSEC-AH : sequence number 25950 already proceeded. Packet dropped. Local(25959)
2016-09-28T23:07:49.860042+08:00 gw-node-2 Keepalived_vrrp[63030]: bogus VRRP packet received on eth1 !!!
2016-09-28T23:07:49.860046+08:00 gw-node-2 Keepalived_vrrp[63030]: VRRP_Instance(GW-NODE-2) Dropping received VRRP packet...
2016-09-28T23:07:50.861108+08:00 gw-node-2 Keepalived_vrrp[63030]: VRRP_Instance(GW-NODE-2) IPSEC-AH : sequence number 25951 already proceeded. Packet dropped. Local(25961)
```

因为是说有假冒的VRRP包，于是抓ip `224.0.0.18`的包，也可以使用域名`vrrp.mcast.net`：

> By default keepalived uses 224.0.0.18 IP address for VRRP (Virtual Router Redundancy Protocol) for communication between two nodes for health check.

```text
$ tcpdump -v -i eth1 host 224.0.0.18
test-node-0 > vrrp.mcast.net: AH(spi=0x0aff253d,sumlen=16,seq=0x65d2): vrrp test-node-0 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 51, prio 90, authtype ah, intvl 1s, length 24, addrs(2): gw-node-1,0.0.0.0
```

(P.S 但是不清楚为何指定协议来抓包就抓不到包：`tcpdump -p -v -i eth1 vrrp`)

发现有台机器也在发vrrp包，并且处于同一个vrid，默认就是51。

后来想起来这台机器是原来的网关，但是有故障，无法登录，所以还在对外持续发vrrp包。

这时只能修改现有网关的Keepalived配置，修改`virtual_router_id`为另外一个值，而不是默认的51。

## 更多

* [官网](http://www.keepalived.org/)
* [借助LVS+Keepalived实现负载均衡](http://www.cnblogs.com/edisonchou/p/4281978.html)
* [CentOS6.5上LVS和KeepAlived搭建高可用负载均衡集群](http://www.pycoding.com/2015/04/23/lvs-keepalived.html#4-KeepAlivde的配置)
