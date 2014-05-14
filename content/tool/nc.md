---
title: "nc"
date: 2013-09-03 22:03
---


## netcat ##

TCP/IP swiss army knife

装的是 `net-analyzer/netcat6`, 这个是增强版, 支持IPv6.

见过的有三个版本: `net-analyzer/netcat6`, `net-analyzer/netcat`, `net-analyzer/gnu-netcat`. 不同的版本参数上也会有些差异, 好像是第三个实现版本在监听端口时不需要指定`-p`参数.

### Argument ###

` -l ` : 监听模式

` -s ` : 指定本地的地址. 默认是全部, 可以是本地环回地址, 或者指定某一个绑定的具体ip地址

` -p ` : 指定本地开启的端口

` -u ` : 连接模式设置为udp, 默认是tcp

` -v/-vv ` : 更详细的输出内容

` -e, --exec=CMD ` : 连接后执行命令. 这个看起来很牛逼, 还没试过. **TODO**


### Example ###

传输文件:

	# Server端
	>> nc -l -p 9999 < getfile.txt

	# Client端
	$ nc -l 9999 > sendfile.txt

<!-- comment -->

扫描端口( **NOTE**: 这个好像是gnu-netcat版才有的功能 ):

	$ nc -v -z localhost 20-100
	>>
	localhost [127.0.0.1] 80 (http) open
	localhost [127.0.0.1] 22 (ssh) open

<!-- comment -->

假设本机内网ip是192.168.1.99, 开启一个针对此ip的udp端口:

	$ nc -l -s 192.168.1.99 -p 1234 -u

使用 `netstat -uanp` 就可以看到此端口, 显示的Program name是nc

我在写snmp扫描端口的代码时, 因为要调试查看端口获取是否准确, 就用到了nc, 包括区分tcp/udp, 区分wan/lan等, 非常牛逼.


## Read More ##

* [8 Practical Linux Netcat NC Command Examples](http://www.thegeekstuff.com/2012/04/nc-command-examples/)

