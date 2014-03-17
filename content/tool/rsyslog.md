---
title: "rsyslog"
date: 2013-08-22 23:48
---

> RSYSLOG is the rocket-fast system for log processing.

本地Rsyslog版本: `7.4.4`

## 配置 ##

### 基本语法 ###

Rsyslog 现在支持三种配置语法格式:

* sysklogd
* legacy rsyslog
* RainerScript

sysklogd 是老的简单格式，一些新的语法特性不支持。legacy rsyslog 是以dollar符($)开头的语法，在v6及以上的版本还在支持，一些插件和特性可能只在此语法下支持。RainnerScript是最新的语法。

老的语法格式(`sysklogd` & `legacy rsyslog`)是以行为单位。新的语法格式(`RainnerScript`)可以分割多行。

注释有两种语法:

* 井号符 `#`
* C-style `/* .. */`

执行顺序: 指令在rsyslog.conf文件中是**从上到下**的顺序执行的。

### 模块(Modules) ###

Rsyslog 使用 `$ModLoad` 指令加载模块。常用的模块类型是 Input Modules 和 Output Modules。

输入模块(Input Modules) 用于从多个来源收集(读取)消息，比如tcp/udp, 文本等。

<table border="1">
<tr><th>模块</th><th>作用</th></tr>
<tr><td>imfile</td><td>input module for text files</td></tr>
<tr><td>imrelp</td><td>RELP input module</td></tr>
<tr><td>imudp</td><td>udp syslog message input</td></tr>
<tr><td>imtcp</td><td>input plugin for tcp syslog</td></tr>
<tr><td>imptcp</td><td>input plugin for plain tcp syslog (no TLS but faster)</td></tr>
<tr><td>immark</td><td>support for mark messages</td></tr>
<tr><td>imklog</td><td>kernel logging</td></tr>
<tr><td>imuxsock</td><td>unix sockets, including the system log socket</td></tr>
<tr><td>impstats</td><td>provides periodic statistics of rsyslog internal counters</td></tr>
</table>

输出模块(Output Modules)处理消息。通过它，可以格式化消息以及传递消息到不通的目标(target)。

<table border="1">
<tr><th>模块</th><th>作用</th></tr>
<tr><td>omfile</td><td>file output module</td></tr>
<tr><td>omfwd</td><td>????????</td></tr>
<tr><td>ompipe</td><td>named pipe output module</td></tr>
<tr><td>omrelp</td><td>RELP output module</td></tr>
<tr><td>ommysql</td><td>output module for MySQL</td></tr>
<tr><td>omprog</td><td>permits sending messages to a program for custom processing</td></tr>
<tr><td>omuxsock</td><td>output module Unix domain sockets</td></tr>
</table>

还有其它类型的模块, 可以参考[官方模块文档](http://www.rsyslog.com/doc/rsyslog_conf_modules.html)

简单的消息工作流:

![Module Workflow](http://www.rsyslog.com/doc/module_workflow.png)

消息从 Input Modules 接收，然后传递给 Parser Modules，最终传递给 Output Module。

### Templates ###

模板是 rsyslog 一个重要的属性，它可以控制日志的格式，支持类似`template()`语句的基于string或plugin的模板

legacy 格式使用 `$template` 的语法，不过这个在以后要移除，所以最好使用新格式 `template()`:

	$template name, param[, options]

name 是模板的名称，param 指定模板内容，options 用来设置模板选项。TODO

基于string的模板:

    $template strtpl,"PRI: %pri%, MSG: %msg%\n"

基于plugin的模板:

    $template plugintpl,=myplugin

举个例子:

	$template MyTemplateName,"Text %property% some more text\n",<options>

模板指令定义一个模板 MyTemplateName，模板的格式是引号阔起来的，其中`百分号%`标记的是`property`，可以获取rsyslog的消息内容，更多参考 [property replacer](http://www.rsyslog.com/doc/property_replacer.html)


### Filter Conditions ###

Rsyslog 提供三种格式的过滤条件语法:

* RainerScript-based filters
* "traditional" severity and facility based selectors : 基于严重程度和设施的选择器
* property-based filters : 基于属性的过滤器

选择器(Selectors):

选择器是过滤syslog消息的传统方法。它使用rsyslog的原始语法，效率高，适合针对优先级(priority)和设施(facility)的过滤。

选择器由两部分组成, 一个facility和一个priority, 中间用句号(`.`)分隔。priority和facility都忽略大小写，并且可以用十进制数字代替，不过不建议这么做。可以通过 `man 3 syslog`更详细的了解这两部分。

Facility 用来指定哪个程序发送的日志消息，可以让配置通过不同的消息来源做不通的处理。

* auth
* authpriv
* cron
* daemon
* kern
* lpr
* mail
* mark
* news
* security (same as auth)
* syslog
* user
* uucp
* local0 - local7

priority 列表: 
debug
info
notice
warning
warn (same as warning)
err
error (same as err)
crit, alert
emerg
panic (same as emerg)

error, warn, panic已经过时，不应该再使用。

星号符(`*`)可以表示所有facility或所有priority。 
关键词none表示为指定级别的。

一个priority可以指定多个facilities, 使用逗号(`,`)分隔。(priority不能这么做)

在一个action下配置多个selectors，使用分号(`;`)分隔。

priority前面加等于号(`=`)表示仅选择当前级别的。

priority前面加感叹号(`!`)表示排除该级别的。 **TODO 测试** 测试失败，不能用?

如果要同时使用感叹号和等于号，感叹号应该在等于号之前。

举例:

TODO

Property-Based Filters:

可以过滤任何属性，例如 HOSTNAME、msg等。支持的属性见[The Property Replacer](http://www.rsyslog.com/doc/property_replacer.html)

property-based filter必须使用冒号(`:`)开头。

语法:

	:property, [!]compare-operation, "value"

value 是用来比较的值，必须用引号括起来。

注意 property和compare-operation是大小写敏感的。

compare-operation 有:

contains : property 包含指定 value
isequal : property 和指定 value 相等
startswith : 以 value 起始的property
regex
ereregex



## Rsyslog Queue ##

队列，rsyslog 的重点。

<!-- 来至[官方文档](http://www.rsyslog.com/doc/queues_analogy.html)的一幅图： -->
<!-- ![dataflow](http://www.rsyslog.com/doc/dataflow.png) -->

![message flow](http://tankywoo-wb.b0.upaiyun.com/rsyslog_message_flow.png)

图片[来源](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/7-Beta/html/System_Administrators_Guide/s1-working_with_queues_in_rsyslog.html)

队列分为 `Main Queue` 和 `Action Queue`，Main Queue 只有一个，Action Queue 有多个，每一个 Action 前面都有一个 Action Queue。Main Queue 的配置一般以`MainMsg`开头，Action Queue的配置以`Action`开头，两者的配置基本相同。

队列的模式有`Direct`, `Disk`, `In-Memory`, `Disk-Assisted Memory`四种，最后一种后面都简称DA，这种队列模式是Disk 和 In-Memory的结合体。其中 In-Memory 又包括 `FixedArray` 和 `LinkedList`两种模式。

### Direct Queues ###

实际上是一个 `non-queuing` queue。它直接把消息从 producer 传递给 customer。

这种模式适合简单的把日志写入本地, 效率非常高。

所以 Action Queue 的默认模式就是 Direct Queues。

### Disk Queues ###

这种对了使用硬盘当做缓存，因为没有使用内存，所以缓存速度最慢，但是可靠性最高，一般用于数据非常重要的情景下。

缓存文件存在指定的目录下，文件名是 `队列名.7位数字`，从 `0000001`开始，当一个文件达到限制的最大大小，会继续新建文件，文件名加一。

### In-Memory Queues ###

这种队列是最常使用的队列，它分为 `FixedArray` 和 `LinkedList` 两种。它们使用内存作为缓存，这也导致它们的可靠性没有Disk Queue好。

FixedArray 是预分配固定大小的队列，也是Main Queue的默认模式。它针对的是队列日志相对较小的情况，拥有很好的性能。

LinkedList 是动态分配大小的队列，适合队列日志很大的情况。

官方建议这两者间优先选择 LinkedList。

### Disk-Assisted Queues ###

它集成了In-Memory 和 Disk 这两种队列的优点。

如果一个In-Memory Queue定义了队列名(通过 `$<object>QueueFileName`)，它自动就变成 `Disk-Assisted`(DA)模式。

DA队列实际是两个队，一个普通的memory队列 (called the "primary queue")和一个disk队列(called the "DA queue")。当达到一定条件后，DA队列就会被激活。

---

Main Queue 的默认模式是 `FixedArray`，Action Queue 的默认模式是 `Direct`

关于Rsyslog Queue的官方文档:

* [Understanding rsyslog Queues](http://www.rsyslog.com/doc/queues.html)
* [Turning Lanes and Rsyslog Queues - an Analogy](http://www.rsyslog.com/doc/queues_analogy.html)


### impstats 模块 ###

队列的相关统计信息可以使用输出模块 `impstats` 来查看。参考配置:

	$ModLoad impstats
	$PStatInterval 5
	$PStatSeverity 7

	syslog.=debug  /var/log/rsyslog-stats
	&~

样例表示每5s(默认是300s)生成一个统计信息，日志等级是7及以上(默认是6)，日志写入/var/log/rsyslog-stats后丢弃。

更多的可以参考:

* [impstats配置讲解](http://www.rsyslog.com/doc/impstats.html)
* [使用impstats](http://www.rsyslog.com/how-to-use-impstats/)
* [Main Queue输出术语](http://www.rsyslog.com/rsyslog-statistic-counter-queues/)


# 更多资料 #
* [rsyslog研究](http://www.cnblogs.com/tobeseeker/archive/2013/03/10/2953250.html)
* [用rsyslog处理日志](http://dmyz.org/archives/394)
* [rsyslogd服务的配置和使用](http://www.litrin.net/2012/08/27/rsyslogd%E6%9C%8D%E5%8A%A1%E7%9A%84%E9%85%8D%E7%BD%AE%E5%92%8C%E4%BD%BF%E7%94%A8/)
* [安装rsyslog](http://opkeep.com/system/linux/rsyslog-install.html)
* [Rsyslog配置文件详解-转载](http://www.lampbo.org/others/opensource/rsyslog-config-file-detail.html)

## 官方资料 ##
* [Basic rsyslog.conf Structure](http://www.rsyslog.com/doc/rsyslog_conf_basic_structure.html)
* [Templates](http://www.rsyslog.com/doc/rsyslog_conf_templates.html)
* [Filter Conditions](http://www.rsyslog.com/doc/rsyslog_conf_filter.html)
