---
title: "cURL"
date: 2013-08-17 07:32
update: 2016-12-24 16:00
collection: "网络相关"
log: "增加--resolve"
---

[TOC]

## Argument ##

* `-o` - output to file
* `-O` - output to file named the same with the remote name
* `-i` - Include the HTTP-header in the output
* `-I` - only get the HTTP-header
* `-u`

## Example ##

	# get the file source and output to the STDOUT
	curl http://wiki.wutianqi.com/index.html

	# download the file
	curl -o myindex.html http://wiki.wutianqi.com/index.html
	curl -O http://wiki.wutianqi.com/index.html

	# get the HTTP-header only
	curl -I http://wiki.wutianqi.com/index.html


## IPv6 ##

curl ipv6 localhost:8000, 注意要加`-g`和`-6`, url要用方括号(bracket):

    curl -g -6 'http://[::1]:8000'

参考: [How can I use curl with ::1 for ipv6 based loopback?](http://superuser.com/a/885757/251495)


## --resolve

除了通过`/etc/hosts`绑定主机. 对于http请求, 可以在`-H 'Host: example.com'`中来绑定host访问某台机器.

对于SNI, 因为**证书验证时的CN匹配是通过url来判断**的, 所以上面的方法没用.

可以考虑`--resolve <host:port:address>`来绑定主机和端口 (所以除了SNI, 其它协议都可以). 手册讲得有点不清楚.

这里host:port表示要访问的`域名:端口`, address绑定将这个域名绑定到哪个地址(ip)上. 这里指定的域名和端口(协议)是在后面的url里用到的.

比如场景: 域名example.com, 配置了SNI. proxy_server反代配置了缓存, 限制*内网*才可以做cache purge操作, real_server是实际的server.

所以无法通过如下清理缓存:

```bash
curl -I https://example.com/cache_purge/path/to/page.html
```

需要考虑将这个url host绑定到proxy_server的内网ip上, 这时就可以考虑`--resolve`了:

```bash
curl -I --resolve example.com:443:192.168.0.101 https://example.com/cache_purge/path/to/page.html
```


## Read More ##

* [15 Practical Linux cURL Command Examples](http://www.thegeekstuff.com/2012/04/curl-examples/)
* [curl tutorial with examples of usage](http://www.yilmazhuseyin.com/blog/dev/curl-tutorial-examples-usage)
* [curl网站开发指南](http://www.ruanyifeng.com/blog/2011/09/curl.html)

