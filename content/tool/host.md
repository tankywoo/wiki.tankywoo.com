---
title: "host"
date: 2013-08-17 07:32
---


## host ##

host - DNS lookup utility

host 命令式一个查询dns的小工具. 它可以通过域名查询ip, 或者相反.


## 基本方法 ##

	host name/ip [server]

	# 通过域名查询地址
	host domainname

	# 通过ip地址反向查询域名 **TODO**
	host ipaddress

	# 指定ns服务器, 这样就不会从/etc/resolv.conf下查询ns
	host domainname ns

## 参数 ##

`-a` - 相当于指定了`-v`并查询`ANY`类型
`-t` - 后面接查询的指定类型(CNAME, NS, SOA, SIG, KEY, AXFR, etc). 当没有指定类型时, host会自动选择合适的查询类型, 默认是 A, AAAA, MX 类型. 如果使用了`-C`参数, 显然会查询`SOA`记录. 如果`name`是ip, 则会查询`PTR`类型.
