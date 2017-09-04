---
title: "动态配置管理"
date: 2017-09-04 18:45
log: ""
---

（目前只是浅显的研究）

涉及到的工具：

- confd: [website](http://www.confd.io/) / [github](https://github.com/kelseyhightower/confd)
- etcd: [website](https://coreos.com/etcd/) / [github](https://github.com/coreos/etcd)
- consul: [website](https://www.consul.io/) / [github](https://github.com/hashicorp/consul)

这几个工具都是 Go 写的，开箱即用。

consul 和 etcd 提供类似的服务，还没去研究，只是看到有人提到使用时遇到不少坑，所以暂时先不去研究了。


## etcd

etcd 是一个分布式的k/v存储，通过Raft保证一致性。

扩展阅读：

- [etcd 使用入门](http://cizixs.com/2016/08/02/intro-to-etcd)
- [服务发现之 Etcd VS Consul](http://www.jianshu.com/p/6160d414dd5e)
- [服务发现：Zookeeper vs etcd vs Consul](http://dockone.io/article/667)
- [Consul 和 ZooKeeper、Doozerd、Etcd 的区别](https://toutiao.io/posts/s866l/preview)


## confd

confd 是一个轻量的配置管理工具，配合 `etcd`、`consul`、`redis` 等后端提供配置数据，模板配置使用 toml，模板使用 Go Text 来管理配置，通过间隔周期检查后端存储里的变动，进而动态的更新配置。

扩展阅读：

- [etcd 和confd 实现nginx配置文件自动管理](http://www.pydevops.com/2015/10/29/etcd-%E5%92%8Cconfd-%E5%AE%9E%E7%8E%B0nginx%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E8%87%AA%E5%8A%A8%E7%AE%A1%E7%90%86/)
- [开源分布式配置中心选型](http://vernonzheng.com/2015/02/09/%E5%BC%80%E6%BA%90%E5%88%86%E5%B8%83%E5%BC%8F%E9%85%8D%E7%BD%AE%E4%B8%AD%E5%BF%83%E9%80%89%E5%9E%8B/)
- [关于配置的思考](http://www.zenlife.tk/%E5%85%B3%E4%BA%8E%E9%85%8D%E7%BD%AE%E7%9A%84%E6%80%9D%E8%80%83.md)
- [配置中心](https://poweryang1990.github.io/2016-03-24/configmanage/)


## 考虑点和想法

目前关注这么几点：

- 和传统的静态配置管理工具如 SaltStack/Ansible 有什么区别？
- etcd 这样的存储是否提供了安全性的配置
- 既然是直接存储的，那么是否有方便的大量配置管理工具，如可视化的 Web 平台
- 实践场景介绍

像 confd + etcd 这类配置模式，可以做到动态更新，不过 Salt/Ansible 这些其实也可以通过定时任务执行检查diff进而直接应用或者发邮件告警。所以这块还有没有其它的特点呢？目前没有想到。

看了下 etcd（目前 V3 版本），V3 版本好像没有直接提供安全性的处理，可能需要外部来做了。

而管理方面，常规手法就是 Web 上管理，这个搜下还是有的，不过规模看起来都不大；可能更使用以静态配置管理，定期导入到 etcd 中？

实践场景方面，其实是想看看其它朋友是否有一些经验可以介绍，不过找了很久，似乎除了和官方教程一样的 nginx 配置外，没什么好的经验介绍了。

关于我们目前的配置管理，都是 salt 定期检查并且将 diff 以邮件方式告警，因为配置和进程管理这块不敢百分百相信第三方工具，毕竟像这类工具由太多人一起维护，质量上我不敢担保，所以我们一般确认 diff 后会手动更新。那么像 confd + etcd 这种模式，姑且认为工具是百分百可靠，那么人为失误导致配置更新有误怎么办呢？没有一个显式的 diff 来确认，就这么自动更新了，感觉不太安心啊……

如果看到的朋友有这块经验，欢迎邮件一起交流下：）

