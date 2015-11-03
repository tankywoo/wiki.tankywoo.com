---
title: "stunnel"
date: 2015-08-03 11:00
---

[TOC]

## 简介 ##

[stunnel](https://www.stunnel.org/index.html) 是一个自由的跨平台软件, 用于提供全局的TLS/SSL服务. 针对本身无法进行TLS或SSL通信的客户端及服务器, Stunnel可提供安全的加密连接. --- 引自[维基百科](https://zh.wikipedia.org/wiki/Stunnel)

stunnel 是一个c/s结构. 在不可信的网络环境里(如公网), 通过stunnel 的server 和 client之间建立安全的加密隧道, 然后两边的网络服务之间通信就可以通过这个安全隧道来通信.

比如redis主从环境, redis自身是没有提供安全的通信接口的, 所以这块需要配合stunnel来做:

![redis stunnel](http://tankywoo-wb.b0.upaiyun.com/redis-stunnel.png)

(图片摘自[USING REDIS IN A HOSTILE ENVIRONMENT](https://www.packtpub.com/books/content/using-redis-hostile-environment-advanced))

以上图为例, redis client和server是跨公网的不可信环境, 如果两者需要通信, 则需要配合一个安全的通信隧道, 如stunnel.

加上stunnel后, 相当于redis client/server 都隐藏在后端.

在redis server端, 部署stunnel server, 一端连接redis server, 另一端对公网开放(listen)一个安全的加密隧道端口.

在redis client端, 部署stunnel client, 一端链接 stunnel server, 另一端对内开放(listen)一个安全的加密隧道端口.

redis client连接stunnel client的listen端口, 最终就和redis server通信.

## 配置 ##

配置的样例:

stunnel server (gentoo 环境):

    setuid = stunnel
    setgid = stunnel
    pid = /run/stunnel/stunnel.pid

    ; Some performance tunings
    socket = l:TCP_NODELAY=1
    socket = r:TCP_NODELAY=1

    ; The following options provide additional security at some performance penalty
    ; Default ECDH/DH parameters are strong/conservative, so it is quite safe to
    ; comment out these lines in order to get a performance boost
    options = SINGLE_ECDH_USE
    options = SINGLE_DH_USE

    options = NO_SSLv2
    compression = zlib
    debug = notice

    CAfile = /path/to/ca.pem
    cert = /path/to/stunnel.pem
    CRLfile = /path/to/crl.pem
    verify = 2

    [redis]
    connect = 127.0.0.1:6379
    accept = 7379

stunnel client (ubuntu 环境):

    setuid = stunnel4
    setgid = stunnel4
    pid = /run/stunnel4/stunnel4.pid

    ; Some performance tunings
    socket = l:TCP_NODELAY=1
    socket = r:TCP_NODELAY=1

    ; The following options provide additional security at some performance penalty
    ; Default ECDH/DH parameters are strong/conservative, so it is quite safe to
    ; comment out these lines in order to get a performance boost
    options = SINGLE_ECDH_USE
    options = SINGLE_DH_USE

    options = NO_SSLv2
    compression = zlib
    debug = notice

    cert = /path/to/client.pem
    CAfile = /path/to/ca.pem

    [redis]
    client = yes
    connect = X.X.X.X:7379     ; X.X.X.X 是 stunnel server的公网ip
    accept = 127.0.0.1:7379

这时, redis client 连接本地stunnel client的7379端口就可以了.

`stunnel -version` 可以看到一些默认的配置等信息.

更详细的配置可以参考[stunnel config](https://www.stunnel.org/config_unix.html)

## 其它 ##

### 加密 ###

如果想配置加密算法为不加密, 可以两边都加上:

    ciphers = eNULL

抓包确认是明文传输.

参考:

* [stunnel faq](http://www.onsight.com/faq/stunnel/stunnel-faq-1.html)
* [Turning off compression and encryption](http://osdir.com/ml/network.stunnel.user/2003-12/msg00058.html)


### CentOS6相关 ###

stunnel(版本4.29)在CentOS6下, 没有启动脚本(`rpm -ql stunnel` 可以查看相关的安装文件列表). 网上找了下, 下面几个脚本大同大异:

* [Installing Stunnel client on CentOS 6.6](https://randomcentos.wordpress.com/2015/04/21/installing-stunnel-client-on-centos-6-6/)
* [how create a service for installed STUNNEL on CentOS 5.10](http://stackoverflow.com/questions/23545797/how-create-a-service-for-installed-stunnel-on-centos-5-10)
* [Stunnel init script for RHEL / CentOS](http://www.riccardoriva.info/blog/?p=1047)
* [duritong/puppet-stunnel](https://github.com/duritong/puppet-stunnel/blob/master/files/CentOS/stunnel.init)

另外简单的就是不使用sys-v init脚本, 直接使用upstarts脚本管理服务:

    # stunnel
    #
    start on stopped rc RUNLEVEL=[2345]

    stop on runlevel [!2345]

    respawn
    exec /usr/bin/stunnel /etc/stunnel/*.conf

    pre-start script
      if ! [ -d /var/run/stunnel ]; then
        install -d -o nobody -g nobody /var/run/stunnel
      fi
    end script

关于pid目录的文件. 因为stunnel自身没有在启动时去创建`/var/run/stunnel` 这个目录. 所以需要在服务管理脚本中做处理.

上面的init脚本借鉴了ubuntu下的/etc/init.d/stunnel, 在`pre-start`区做了处理. 具体可以看看upstart的手册.

加入开机启动, 删除/etc/init/stunnel.override文件. 具体可以看看[这篇回答](http://askubuntu.com/questions/19320/how-to-enable-or-disable-services), 非常详细.

FIPS_mode_set:fingerprint does not match 问题:

> openssl-fips是符合FIPS标准的Openssl.
> 联邦信息处理标准（Federal Information Processing Standards，FIPS）是一套描述文件处理、加密算法和其他信息技术标准（在非军用政府机构和与这些机构合作的政府承包商和供应商中应用的标准）的标准。

这里可以关闭fips, 详见[官方文档](https://www.stunnel.org/static/stunnel.html), 配置文件中加上:

    fips = no

文档说5.0版本后默认no, 不过在ubuntu下stunnel4.42, 这个就是关闭的. centos下stunnel4.29是默认开启.

参考:

* [OpenSSL基础知识](http://www.cnblogs.com/274914765qq/p/4513362.html)
* [Stunnel refuses to work after update](http://www.vcloudnine.de/stunnel-refuses-to-work-after-update/)
* [[stunnel-users] FIPS_mode_set:fingerprint does not match](https://www.stunnel.org/pipermail/stunnel-users/2012-March/003608.html)

---

参考资料:

* [USING REDIS IN A HOSTILE ENVIRONMENT](https://www.packtpub.com/books/content/using-redis-hostile-environment-advanced) 讲解很详细
* [Sending redis traffic through an SSL tunnel with stunnel](http://bencane.com/2014/02/18/sending-redis-traffic-through-an-ssl-tunnel-with-stunnel/) 讲解很详细
* [How To Set Up an SSL Tunnel Using Stunnel on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-ssl-tunnel-using-stunnel-on-ubuntu)
* [Redis over SSL](http://stephenmeehan.com/2014/04/redis-over-ssl/)
* [Redis Security](http://redis.io/topics/security)
* [Redis Encryption](http://redis.io/topics/encryption)




