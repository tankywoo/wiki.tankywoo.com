---
title: "mitmproxy"
date: 2015-11-09 23:00
---

[TOC]

## 简介 ##

[mitmproxy](http://mitmproxy.org/) 是一个HTTP抓包命令行工具集. 包含`mitmproxy`和`mitmdump`

* mitmproxy: 交互式的, http包代理, 分析, 修改等.
* mitmdump: 非交互式的. 轻量级的tcpdump for http.

mitmproxy工具集是用Python写的, 直接pip安装:

	pip install mitmproxy

[文档](http://docs.mitmproxy.org/en/stable/)

![mitmproxy screenshot](http://mitmproxy.org/images/mitmproxy.png)

## mitmproxy ##

> An interactive console program that allows traffic flows to be intercepted, inspected, modified and replayed.

> An interactive, SSL-capable man-in-the-middle proxy for HTTP with a console interface.

[详细文档](http://docs.mitmproxy.org/en/stable/mitmproxy.html) 非常详细, 截图介绍了交互窗口各区域的说明.

执行`mitmproxy`命令默认进入交互式终端, 监控 `0.0.0.0:8080`, 这些都可以写入配置文件或者用命令行参数覆盖.

测试可以本地用`python -m SimpleHTTPServer`起一个http server, 然后`curl --proxy http://localhost:8080 http://example.com`来经过mitmproxy代理访问网站. 或者浏览器设置一个proxy.

mitmproxy交互界面支持鼠标点击到某个请求展开, 也可以使用上下移动到指定的请求并按Enter展开; Tab或左右用于在展开后的Request, Response, Detail之间切换.

具体可以按`?`问号在请求列表(Flow List)页面或请求(Flow View)页面查看帮助.


## mitmdump ##

> Think tcpdump for HTTP - the same functionality as mitmproxy without the frills.

> Command-line version of mitmproxy. Think tcpdump for HTTP.

[详细文档](http://docs.mitmproxy.org/en/stable/mitmdump.html)

未研究 TODO

## 其它选择? ##

* [Mac 下 Http 协议抓包工具哪款比较好呢](https://www.v2ex.com/t/219374)
* [Mac 下抓 http 请求的工具求推荐](https://www.v2ex.com/t/233892)
