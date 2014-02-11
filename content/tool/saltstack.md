---
layout: post
title: "SaltStack"
date: 2014-02-11 17:11
---

* [官网](http://www.saltstack.com/)
* [官方文档](http://docs.saltstack.com/)
* [Github](https://github.com/saltstack/salt)

## 安装 ##

参考 [doc - Installation](http://docs.saltstack.com/topics/installation/index.html)。

部分常用系统支持使用 [salt-bootstrip](https://github.com/saltstack/salt-bootstrap) 脚本快速安装, 每个平台也有专门的安装教程, 见 [PLATFORM-SPECIFIC INSTALLATION INSTRUCTIONS](http://docs.saltstack.com/topics/installation/index.html#platform-specific-installation-instructions)

## 遇到的问题 ##

### 修改主机名后, 默认id不变 ##

按照文档说的, 在客户端没有配置 id 的时候, 通过 socket.getfqdn() -> hostname 的顺序定义 id。但是我修改主机名并重启机器后，通过 salt-key -L 看未接受主机，还是原来的主机名。

后来发现，在 /etc/salt/ 下有一个 `minion_id` 文件，里面保存的是原来的文件名。

猜测：在客户端初始化时是通过上面说的顺便获取一个默认id，然后存储在此文件中，如果 /etc/salt/minion 里定义了 id，则使用这个id，如果未定义，则使用 `/etc/salt/minion_id` 里存储的id。那么，如果修改了主机名，又没有定义id，那么就应该手动修改这个文件。


## 资料 ##

* [系统自动化配置和管理工具 SaltStack](http://www.vpsee.com/2013/08/a-system-configuration-management-and-orchestration-tool-saltstack/)
* [使用saltstack批量管理服务器](http://www.groovyq.net/node/727)
* [SaltStack中国用户组wiki](http://wiki.saltstack.cn/docs)
