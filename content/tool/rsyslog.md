---
title: "rsyslog"
date: 2013-08-22 23:48
---

RSYSLOG is the rocket-fast system for log processing.

本地Rsyslog版本: `7.4.4`

## 配置 ##

### 基本语法 ###

Rsyslog supports three different types of configuration statements concurrently:
Rsyslog 现在支持三种配置语法格式:

* sysklogd
* legacy rsyslog
* RainerScript

sysklogd 是老的简单格式，一些新的语法特性不支持。legacy rsyslog 是以dollar符($)开头的语法，在v6及以上的版本还在支持，一些插件和特性可能只在此语法下支持。RainnerScript是最新的语法。

老的语法格式(sysklogd & legacy rsyslog)是以行为单位。新的语法格式(RainnerScript)可以分割多行。

注释有两种语法:

* 井号符 `#`
* C-style `/* .. */`

执行顺序:

指令在rsyslog.conf文件中是从上到下的顺序执行的。

控制流语句:

* if expr then ... else ...  条件语句
* stop
* call
* continue

输入和输出 **TODO**

参考: [Basic rsyslog.conf Structure](http://www.rsyslog.com/doc/rsyslog_conf_basic_structure.html)

### 模块(Modules) ###

使用 `$ModLoad` 指令加载模块。

* Input Modules
* Output Modules
* Parser Modules
* Message Modification Modules
* String Generator Modules
* Library Modules

简单的消息工作流:

![Module Workflow](http://www.rsyslog.com/doc/module_workflow.png)

参考: [Modules](http://www.rsyslog.com/doc/rsyslog_conf_modules.html)

### Templates ###

**TODO**

参考: [Templates](http://www.rsyslog.com/doc/rsyslog_conf_templates.html)

### Filter Conditions ###

Rsyslog 提供三种格式的过滤条件语法:

* RainerScript-based filters
* "traditional" severity and facility based selectors
* property-based filters

Selectors:

选择器是过滤syslog消息的传统方法。它使用rsyslog的原始语法，效率高，适合针对优先级(priority)和设施(facility)的过滤。

选择器由两部分组成, 一个priority和一个facility, 中间用句号(`.`)分隔。priority和facility都忽略大小写，并且可以用十进制数字代替，不过不建议这么做。可以通过 `man 3 syslog`更详细的了解这两部分。

facility : auth, authpriv, cron, daemon, kern, lpr, mail, mark, news, security (same as auth), syslog, user, uucp and local0 through local7

priority : debug, info, notice, warning, warn (same as warning), err, error (same as err), crit, alert, emerg, panic (same as emerg)

星号符(`*`)可以表示所有facility或所有priority。

一个priority可以指定多个facilities, 使用逗号(`,`)分隔。(priority不能这么做)

在一个action下配置多个selectors，使用分号(`;`)分隔。

**TODO** 等于号和感叹号.

Property-Based Filters:

可以过滤任何属性，例如 HOSTNAME、msg等。支持的属性见[The Property Replacer](http://www.rsyslog.com/doc/property_replacer.html)

property-based filter必须使用冒号(`:`)开头。

语法:

	:property, [!]compare-operation, "value"

value 是用来比较的值，必须用引号括起来。

注意 property和compare-operation是大小写敏感的。

参考: [Filter Conditions](http://www.rsyslog.com/doc/rsyslog_conf_filter.html)


## Rsyslog Queue ##

Rsyslog的队列。

来至[官方文档](http://www.rsyslog.com/doc/queues_analogy.html)的一幅图：

![dataflow](http://www.rsyslog.com/doc/dataflow.png)

### impstats 模块 ###

[impstats配置讲解](http://www.rsyslog.com/doc/impstats.html)
[使用impstats](http://www.rsyslog.com/how-to-use-impstats/)
[Main Queue输出术语](http://www.rsyslog.com/rsyslog-statistic-counter-queues/)

关于Rsyslog Queue的官方文档:

* [](http://www.rsyslog.com/doc/queues.html)
* [](http://www.rsyslog.com/doc/queues_analogy.html)

## 关于 block queue ##

http://lists.adiscon.net/pipermail/rsyslog/2012-February/029513.html

https://bugs.launchpad.net/ubuntu/+source/sysklogd/+bug/26986

http://blog.chinaunix.net/uid-773723-id-3900229.html

https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/7-Beta/html/System_Administrators_Guide/s1-working_with_queues_in_rsyslog.html

http://www.tuicool.com/articles/Jv2eUvn

http://phpor.net/blog/post/1187

# 更多资料 #
* [rsyslog研究](http://www.cnblogs.com/tobeseeker/archive/2013/03/10/2953250.html)
* [用rsyslog处理日志](http://dmyz.org/archives/394)
* [rsyslogd服务的配置和使用](http://www.litrin.net/2012/08/27/rsyslogd%E6%9C%8D%E5%8A%A1%E7%9A%84%E9%85%8D%E7%BD%AE%E5%92%8C%E4%BD%BF%E7%94%A8/)
* [安装rsyslog](http://opkeep.com/system/linux/rsyslog-install.html)
* [Rsyslog配置文件详解-转载](http://www.lampbo.org/others/opensource/rsyslog-config-file-detail.html)
