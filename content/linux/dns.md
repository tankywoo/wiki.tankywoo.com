---
title: "DNS"
date: 2017-08-28 15:30
---

关于 DNS 这块，<b>TCP/IP协议详解</b> 有专门一章讲解，入门非常合适。这里再补充一些其它方面的。

首先看下 DNS 首部结构图，图片来至 <http://www.troyjessup.com> (这个网站好像无法打开了，从其它站点找到的图)：

![DNS HEADER](https://tankywoo-wb.b0.upaiyun.com/dns/dns-header.jpg)

例1：

```
$ dig tankywoo.com @114.114.114.114 A

; <<>> DiG 9.10.3-P2 <<>> tankywoo.com @114.114.114.114 A
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12839
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 11

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;tankywoo.com.                  IN      A

;; ANSWER SECTION:
tankywoo.com.           496     IN      A       192.168.1.100

;; AUTHORITY SECTION:
tankywoo.com.           86370   IN      NS      f1g1ns2.dnspod.net.
tankywoo.com.           86370   IN      NS      f1g1ns1.dnspod.net.

;; ADDITIONAL SECTION:
f1g1ns1.dnspod.net.     3928    IN      A       180.163.19.15
f1g1ns1.dnspod.net.     3928    IN      A       182.140.167.166
...

;; Query time: 3 msec
;; SERVER: 114.114.114.114#53(114.114.114.114)
;; WHEN: Mon Aug 28 08:43:08 UTC 2017
;; MSG SIZE  rcvd: 271

```

## DNS 包的 Flags

具体可以看看 [RFC 1035](http://www.ietf.org/rfc/rfc1035.txt) 的 `Header section format` 部分。

常见的如：

- RD(Recursion Desired) 表示请求时(QUERY)期望递归
- RA(Recursion Available) 表示响应(RESPONSE)带的标记，标识NS服务器是否支持递归

也可以看看 [DNS, Domain Name System](http://www.networksorcery.com/enp/protocol/dns.htm#RD, Recursion Desired)


## 递归(Recursive)和迭代(Iterative)

迭代，即非递归(Non-Recursive)。

如上例1中 `;; flags: qr rd ra;`，一般的 dns 请求工具如 dig，默认都是期望递归(rd)，并且一般我们直接请求的 ns 服务器也支持递归请求(ra)。

如下这幅图，[图片来源](http://slideplayer.com/slide/9431631/)：

![Recursive and Iterative](https://tankywoo-wb.b0.upaiyun.com/dns/dns-recursive-and-iterative.jpg)

可以看到 `1, 8` 这个过程是递归查询，其余是非递归查询。一般我们直接请求的 ns 服务器承担了递归、转发(forward)、缓存的作用。

如果查询的域名没有在缓存和zone中，则向根域请求，根域是非递归服务器，会告诉请求ns需要向哪个ns服务器作查询，然后迭代直到查到记录并返回给用户。

直接执行 `dig` 可以获取所有根域服务器。

如果不想递归请求，针对 dig 可以：

```
dig +norecurse tankywoo.com A @114.114.114.114
```

再比如 DNS 服务器使用 bind 的话，可以设置 `recursion no` 使 NS 服务器作为一个非递归服务器，这时 dig 查询可以看到没有 `ra` 这个标记。


## 权威(Authoritative) DNS

权威DNS就是管理域名zone记录的DNS服务器，DNS查询最终会到权威DNS并返回记录。

比如DNSPOD提供的NS服务，我们可以将域名放到DNSPOD上解析，在权威上可以设置，修改，删除该区域内的解析记录，而非权威DNS只能是查询。

具体可以可以看维基百科 [Authoritative name server](https://en.wikipedia.org/wiki/Name_server#Authoritative_name_server)

如下这幅图，[图片来源](http://social.dnsmadeeasy.com/blog/authoritative-vs-recursive-dns-servers-whats-the-difference/)：

![Authoritative DNS](https://tankywoo-wb.b0.upaiyun.com/dns/dns-authoritative-server.png)

可以看到，中间经过递归查询，最终查询到权威服务器，然后返回记录。

例1中的 `;; AUTHORITY SECTION:` 就是授权DNS部分。

通过 `nslookup` 命令也可以看：

```
# 直接查询的 dns 是非授权服务器
root ~ % nslookup tankywoo.com 114.114.114.114
Server:         114.114.114.114
Address:        114.114.114.114#53

Non-authoritative answer:   // <- 注意这个说明
Name:   tankywoo.com
Address: 192.168.1.100

# 直接查询的 dns 是授权服务器
root ~ % nslookup tankywoo.com f1g1ns2.dnspod.net.
Server:         f1g1ns2.dnspod.net.
Address:        182.140.167.188#53

Name:   tankywoo.com
Address: 192.168.1.100
```

## Bind 中的转发与递归

在 Bind 中，转发是通过 `forward` 和 `forwarders` 来配置的，比如配置 `forward only` 则此 DNS 服务器只将请求转到 `forwarders` 列表中，而不请求到 root server。

通过抓包也可以看到，比如A记录查询，在 `first first` 时会只向 `forwarders` 请求 A 记录；而后者则会同时请求 `A` 记录，如果没有则向 root server 请求。

这两者本身来说没有什么关联性，递归是一种查询/响应的方式，而转发则是对查询请求的处理方式。

一个常见的使用尝试就是个人部署一个只做转发的DNS缓存服务器。

扩展阅读：

- [What’s the difference between recursion and forwarding in bind](https://serverfault.com/questions/661821/what-s-the-difference-between-recursion-and-forwarding-in-bind)
- [How To Configure Bind as a Caching or Forwarding DNS Server on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-caching-or-forwarding-dns-server-on-ubuntu-14-04)


## 扩展阅读

- [A DNS Primer](https://danielmiessler.com/study/dns/)
- [A Comparison of DNS Server Types: How To Choose the Right DNS Configuration](https://www.digitalocean.com/community/tutorials/a-comparison-of-dns-server-types-how-to-choose-the-right-dns-configuration)
- [10 frequently asked questions about DNS solved with DIG](http://anouar.adlani.com/2011/12/useful-dig-command-to-troubleshot-your-domains.html)
- [Use dig to query nameservers](https://support.rackspace.com/how-to/using-dig-to-query-nameservers/)
