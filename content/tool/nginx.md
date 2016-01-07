---
title: "Nginx"
date: 2016-01-07 21:11
---

[TOC]


## 中文域名 ##

中文域名之所以可以解析/访问, 并不是说dns, nginx等都可以识别, 而是再浏览器层面会做一个转码.

这个转码技术是[Punycode](https://en.wikipedia.org/wiki/Punycode), 将Unicode码转为ASCII码.

其实不光是中文域名, 只要支持的Unicode编码的域名, 都可以经过Punycode转码.

这种域名一般称为[IDN](https://en.wikipedia.org/wiki/Internationalized_domain_name) (Internationalized domain name).

相关的rfc规定一般转为`xn--<puny>.<suffix>`这样的格式. 如`中国.com`, 转码后是`xn--fiqs8s.com`

	$ python -c 'import sys;print sys.argv[1].decode("utf-8").encode("idna")' "中国.com"
	xn--fiqs8s.com

也可以安装额外的工具, 如Gentoo下`net-dns/libidn`, [参考](http://serverfault.com/questions/335073/how-can-i-convert-an-idn-to-punicode-in-bash).

浏览器也可以直接看到, 如Chrome下点击地址栏最左边的"View site information".

相应的在nginx的配置中, server_name不能直接写中文域名, 应该写解析后的ascii编码的英文域名, 如:

	server
	{
		listen			80;
		server_name		xn--fiqs8s.com;
	}
