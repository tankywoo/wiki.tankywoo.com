---
title: "效率工具"
date: 2013-08-17 07:32
updated: 2016-05-11 22:15
log: "更新梯子"
---

[TOC]

## 云笔记本 ##

1. EveryNote

    类似的还有 <strike>`OneNote`</strike>, `有道笔记`, `麦库笔记`等等. 一直觉得还是EverNote好用！各种功能都比较人性化, 且他们还有一些非常棒的插件, 包括`悦读`, `剪切`等等。现在用的是`印象笔记`, 国内的EverNote。

2. OneNote

    推翻上面说的，最近在用OneNote，感觉很不错(不确定之前用的版本，至少当前2016版挺好的)，唯一就是有点重量级。


## TODO工具 ##

1. t

    一个命令行下的todo工具. 来源于 [t](https://github.com/sjl/t) , 我自己也写了一个, 有些功能直接引用了他的代码。现在增加了日期显示, 以及按日期排序的功能。

    具体可以去 [我的github](https://github.com/tankywoo/t) 上看, 我现在用的就是我自己写的, 感觉非常不错.  


## 思维导图 ##

1. FreeMind

    类似有`XMind`, `MindManager`等等。<strike>用过`XMind`, 在三台电脑(win7 64bit)上试了, 都有点问题. 虽然看起来很强大, 最终还是放弃了。</strike>

    FreeMind相对而言比较简洁和轻量级, 而且功能也都非常不错。有时候帮助自己规划一些事情, 非常合适。

2. XMind

    现在一直在用，唯一的缺点就是有点重量级。不过确实是一款很不错的工具。比FreeMind更丰富。


## 书签 ##

1. Delicious

    1~2年前一度打开非常慢, 难以容忍. 后来换了国内的`美味书签`. 结果有次发现我添加的一些书签都弄丢了. 彻底放弃!  

2. Xmarks

    这个是为了多浏览器之间同步书签用的。不过把我Chrome的书签搞的非常乱, 可能是我自己的原因. 不过我也只用Chrome, 不需要跨浏览器, 所以还是卸了。


## 网盘 ##

1. Sina微盘

    试过`Dropbox`和一些其他网盘, `微云`是我见过最差劲了, Dropbox还行, 命令行下也可以同步, 这点超赞! 可惜国内经常性的墙。

    最终找到了Sina微盘, 感觉非常不错. 现在我有10多G的空间了, 放一些书籍和资料足够了。


## RSS ##

1. Feedly

    自从`Google Reader`宣布2013-07-01关闭, 于是找到了这个, 不过也偶尔需要自备梯子。

    <strike>整体还行吧, 对RSS阅读器要求不高</strike>。现在感觉feedly做的还是不错的. 当然, 也许还有更多优秀的rss阅读器, 还没去尝试.


## 梯子 ##

note: 以下链接用base64转码

已用：

* vpnso: *aHR0cDovL3ZwbnNvLmNvbS8K* 年付，用了三年, 可选列表很多, 买的 v?n 还带有chrome插件, 走socks代理。也提供ss。
* 鱼摆摆: *aHR0cHM6Ly95YmIxMDI0LmNvbS8K* 只能mac下用, 走的socks代理。支持月付，用过一阵子，还行。
* shadowsocks.cn：aHR0cDovL3ZpcC5zaGFkb3dzb2Nrcy5jbi8K 用的付费的，10R/月，速度很快。
* 熊猫翻滚: *aHR0cHM6Ly93d3cucGFuZGFmYW4ub3JnLz9yPTIyNjAxCg==* 带尾巴. http(s)代理。支持月付，一般般。
* 佛跳墙: *aHR0cDovL3d3dy5nb2R1c2V2cG4uaW8K* 支持月付。试用了下，还行。

未用：

* Shadowsocks: *aHR0cHM6Ly9zaGFkb3dzb2Nrcy5jb20vCg==* 年付，非ss官网。(未使用)
* 红杏: *aHR0cDovL2hvbnguaW4vaS9WVEpHLVlrV0doakMydURtCg==* 只能邀请注册, 所以url带尾巴. 只支持Chrome浏览器, 以插件形式使用。 (未使用)
* 云梯: *aHR0cHM6Ly93d3cueXRwdWIuY29tLwo=* (未使用)

最近在用ss (socks5代理), 感觉还是挺方便的。

关于ss的配置: [shadowsocks](https://shadowsocks.org/en/index.html)，另外浏览器端配置可参考: [Chrome + Proxy SwitchOmega](https://ii-i.org/archives/289)。

ss转http代理，官方wiki提供了[polipo](https://github.com/jech/polipo)这个工具，具体见[Convert Shadowsocks into an HTTP proxy](https://github.com/shadowsocks/shadowsocks/wiki/Convert-Shadowsocks-into-an-HTTP-proxy)：

	$ brew install polipo
	$ polipo socksParentProxy=localhost:1080

也可以写入配置文件，默认是`/etc/polipo/config`，这里放在家目录：

	$ cat ~/.polipo
	socksParentProxy = "localhost:1080"
	socksProxyType = socks5
	logFile=/tmp/polipo.log
	logLevel=4

	$ polipo -c ~/.polipo

更详细的配置可以看看这篇文章：[为终端设置Shadowsocks代理](http://droidyue.com/blog/2016/04/04/set-shadowsocks-proxy-for-terminal/)

polipo默认启动的端口是8123。

	# apt-get
	$ http_proxy=http://localhost:8123 apt-get update

	# curl
	$ http_proxy=http://localhost:8123 curl www.google.com

	# wget
	$ http_proxy=http://localhost:8123 wget www.google.com

	# git
	$ git config --global http.proxy 127.0.0.1:8123
	$ git clone https://github.com/xxx/xxx.git
	$ git xxx
	$ git config --global --unset-all http.proxy

	# brew
	$ http_proxy=http://localhost:8123 brew install xxx

另外, `brew`更新也可以直接使用socks5:

	$ ALL_PROXY=socks5://127.1:1080 brew update

参考这两篇:

* [Homebrew behind proxy?](https://github.com/Homebrew/legacy-homebrew/issues/11114)
* [homebrew使用socks-proxy](http://blog.suchasplus.com/2014/10/homebrew-using-socks-proxy.html) 配置的curl socks代理

其它工具:

* [cow](https://github.com/cyfdecyf/cow) go写的http代理
* [proxychains](https://github.com/shadowsocks/shadowsocks/wiki/Using-Shadowsocks-with-Command-Line-Tools) 这个工具有时间也尝试下
