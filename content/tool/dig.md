---
title: "dig"
date: 2013-08-17 07:32
---


## dig ##

dig - domain information groper

典型的dig命令是:

	dig @server name type

当没有指定 type 时, 默认是查询 **A记录**

查询BIND DNS的版本号:

	dig chaos txt version.bind @dns-host

## 参数 ##

当没有任何参数选项时(直接敲dig并回车), dig会默认查询 root(.) 的 NS 记录.  
输出结果可以看到全球**13个根域**.

	;; ANSWER SECTION:
	.                       105475  IN      NS      g.root-servers.net.
	.                       105475  IN      NS      d.root-servers.net.
	.                       105475  IN      NS      k.root-servers.net.
	.                       105475  IN      NS      j.root-servers.net.
	.                       105475  IN      NS      m.root-servers.net.
	.                       105475  IN      NS      c.root-servers.net.
	.                       105475  IN      NS      b.root-servers.net.
	.                       105475  IN      NS      h.root-servers.net.
	.                       105475  IN      NS      i.root-servers.net.
	.                       105475  IN      NS      f.root-servers.net.
	.                       105475  IN      NS      l.root-servers.net.
	.                       105475  IN      NS      e.root-servers.net.
	.                       105475  IN      NS      a.root-servers.net.

`-x` : 用于逆解析查询

