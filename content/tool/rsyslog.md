---
title: "rsyslog"
date: 2013-08-22 23:48
---

[TOC]

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

队列是 rsyslog 的核心。下图([来源](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/7-Beta/html/System_Administrators_Guide/s1-working_with_queues_in_rsyslog.html)) 展示了rsyslog处理消息的流程:

<!-- 来至[官方文档](http://www.rsyslog.com/doc/queues_analogy.html)的一幅图： -->
<!-- ![dataflow](http://www.rsyslog.com/doc/dataflow.png) -->

![message flow](http://tankywoo-wb.b0.upaiyun.com/rsyslog_message_flow.png)


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

这种队列是最常使用的队列，它分为 `FixedArray` 和 `LinkedList` 两种。它们使用内存作为缓存，所以效率非常高，但是相对的它们的可靠性没有Disk Queue好。

FixedArray 是预分配固定大小的队列，也是Main Queue的默认模式。它针对的是队列日志相对较小的情况，拥有很好的性能。

LinkedList 是动态分配大小的队列，适合队列日志很大的情况。

官方建议这两者间优先选择 LinkedList。

### Disk-Assisted Queues ###

它集成了In-Memory 和 Disk 这两种队列的优点。

如果一个In-Memory Queue定义了队列名(通过 `$<object>QueueFileName`)，它自动就变成 `Disk-Assisted`(DA)模式。

DA队列实际是两个队列，一个普通的memory队列 (called the "primary queue")和一个disk队列(called the "DA queue")。当达到一定条件后，DA队列就会被激活。

### 关于队列的配置 ###

因为 MainMsgQueue 和 ActionQueue 的配置基本一样(除了有些默认值可能不同)， 所以这里以MainMsgQueue 为例:

* `$MainMsgQueueType [FixedArray/LinkedList/Direct/Disk]`
* `$MainMsgQueueFileName <name>` 针对disk queue的配置，定义队列名，存储队列数据时用的文件名就是这个名称
* `MainMsgQueueCheckpointInterval <number>` 针对disk queue的配置，单位条数，设置在检查点写入相关信息，增加可靠性，但是会降低性能
* `$MainMsgQueueDequeueBatchSize <number>` [default 32] 设置多少条队列作为一个batch一起出队，针对一个日志量很大的系统，可以考虑把这个值调高来增加性能，不过要结合可使用内存考虑实际情况

对于DA队列，最有特点就是队列阈值的设置了。主要包括这几个配置:

* `$MainMsgQueueSize` 设置队列的最大大小
* `$MainMsgQueueDiscardMark <number>` [default 9750] 配合下面的 `$MainMsgQueueDiscardSeverity`，超过这个watermark后，不重要的日志都会丢弃，包括新进来和已经在队列里的
* `$MainMsgQueueDiscardSeverity <severity>` [default 4 (warning)] 0-Emergency, 1-Alert, 2-Critical, 3-Error, 4-Warning, 5-Notice, 6-Informational, 7-Debug
* `$MainMsgQueueHighWaterMark <number>` [default 8000] 设置 high watermark
* `$MainMsgQueueLowWaterMark <number>` [default 2000] 设置 low watermark
* `$MainMsgQueueMaxFileSize <size_nbr>` [default 1m] 针对disk情况下，单个文件的最大大小
* `$MainMsgQueueMaxDiskSpace` 控制占用硬盘总空间大小

DA 对于阈值处理的逻辑比较有意思，并不是单纯的内存满了就开始使用硬盘。首先，有 `low watermark` 和 `high watermark` 这两个概念。

如果队列大小达到 high watermark，队列开始写数据到disk
如果队列大小降到 low watermark，停止写入disk(直到再次达到 high watermark); 或者 disk queue 队列为空(即da队列里的数据处理完)，这两种情况都会进入in-memory 模式

关于终止队列的一些处理配置:

* `$MainMsgQueueTimeoutEnqueue` [number is timeout in ms (1000ms is 1sec!), default 2000, 0 means indefinite] 当队列或硬盘满了，在这个超时时间后新来的日志，设置0可以直接丢弃掉
* `$MainMsgQueueTimeoutShutdown <number>` [number is timeout in ms (1000ms is 1sec!), default 0 (indefinite)] 当队列关闭时，还有数据在进入队列，rsyslog会尽可能在这个timeout周期内处理掉这些数据
* `$MainMsgQueueTimeoutActionCompletion <number>` [number is timeout in ms (1000ms is 1sec!), default 1000, 0 means immediate!] 配置需要多久来处理完当前的数据
* `$MainMsgQueueSaveOnShutdown  [**on**/off]` 针对disk queue的配置，当运行中的队列关闭时，会先把队列中的数据存在硬盘中
* `$MainMsgQueueDequeueSlowdown <number>` [number is timeout in microseconds (1000000us is 1sec!), default 0 (no delay). Simple rate-limiting!] 简单的出队速度限制，单位微秒
* `$MainMsgQueueImmediateShutdown [on/off]` 弃用的选项

当配置的队列大小或硬盘空间满了以后，rsyslogd 会限制数据submitter。配置 `$MainMsgQueueTimeoutEnqueue` 后，当超过这个时间后新来的日志会被丢弃；设置0为直接丢弃。

`$MainMsgQueueTimeoutShutdown`、`$MainMsgQueueTimeoutActionCompletion` 和 `$MainMsgQueueSaveOnShutdown` 是在队列终止后可以做的一系列措施。

关于队列的worker thread:

* `$MainMsgQueueWorkerThreadMinumumMessages <number>` [default 100]
* `$MainMsgQueueWorkerThreads <number>` [num worker threads, default 1, recommended 1]
* `$MainMsgQueueWorkerTimeoutThreadShutdown <number>` [number is timeout in ms (1000ms is 1sec!), default 60000 (1 minute)]

每个队列(direct queue除外)都有一个工作线程池(worker thread pool).
初始时，是没有worker thread的，当有消息来是，会自动启动一个.
`$MainMsgQueueWorkerThreadMinumumMessages` 配置一个worker thread处理的消息大小，
`$MainMsgQueueWorkerThreads` 配置work thread的上限值。

比如设置一个worker thread的最小处理消息大小是100个，当小于100个是，只有一个worker，当超过100个，小于200个时，会有两个worker...

以上配置要注意`单位`, `默认值`，Main Queue 和 Action Queue 可能有些配置的默认值不一样。

另外所有指明`针对disk`的配置，都是包括 disk queue 和 DA queue.

更多配置参考[这里](http://www.rsyslog.com/doc/rsyslog_conf_global.html)

在一般情况下，大部分的配置都可以直接使用默认的配置，这里给出一份Action使用DA队列的配置:

	# 这两个是全局的 
	$ActionResumeRetryCount                  3
	$ActionResumeInterval                    10
	# 以下是每个ActionQueue自己的配置
	$ActionQueueType                         LinkedList
	$ActionQueueFileName                     da_queue
	$ActionQueueMaxFileSize                  100M         # 设置单个disk文件的大小
	$ActionQueueMaxDiskSpace                 10G          # 设置最大占用空间
	$ActionQueueDisacdSeverity               3            # 设置忽略的等级
	$ActionQueueLowWaterMark                 5000         # 默认是2000
	$ActionQueueHighWatermark                15000        # 默认是8000
	$ActionQueueDiscardMark                  30000        # 默认是9750
	$ActionQueueSize                         80000        # 文档没写，测试发现默认是1000
	$ActionQueueSaveOnShutdown               on
	
	*.* @log-center.xxx.com:514


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

这里我配置为DA类型，通过 impstats 模块观察:

	2014-03-14T17:51:16.744660+08:00 localhost rsyslogd-pstats: imuxsock: submitted=3086634 ratelimit.discarded=0 ratelimit.numratelimiters=0
	2014-03-14T17:51:16.744712+08:00 localhost rsyslogd-pstats: action 1 queue[DA]: size=138176 enqueued=138176 full=0 maxqsize=138176
	2014-03-14T17:51:16.744720+08:00 localhost rsyslogd-pstats: action 1 queue: size=13808 enqueued=151976 full=0 maxqsize=20009
	2014-03-14T17:51:16.744727+08:00 localhost rsyslogd-pstats: main Q[DA]: size=0 enqueued=0 full=0 maxqsize=0
	2014-03-14T17:51:16.744732+08:00 localhost rsyslogd-pstats: main Q: size=4 enqueued=3087045 full=0 maxqsize=261

可以看到，action queue使用了da队列，因为默认的 `$WorkDirectory /var/spool/rsyslog`，在 /var/spool/rsyslog 下可以看到存储的日志:

	root@localhost:/var/spool/rsyslog# ll
	total 160384
	drwxr-xr-x 2 syslog adm        36864 Mar 14 17:50 ./
	drwxr-xr-x 7 root   root        4096 Oct 29 13:27 ../
	-rw------- 1 syslog syslog 100000283 Mar 14 17:50 fwdacq.00000001
	-rw------- 1 syslog syslog  50443050 Mar 14 17:52 fwdacq.00000002
	
	root@localhost:/var/spool/rsyslog# du -sh *
	96M     fwdacq.00000001
	49M     fwdacq.00000002

存储文件默认是用`队列名.7位数字`以递增方式命名的，因为定义了存储文件的最大值是100M，所以可以看到第一个是96M，再存储就存不了了，进而新建第二个文件存储。
	
	2014-03-14T17:27:07.485964+08:00 localhost rsyslogd-pstats: imuxsock: submitted=32005 ratelimit.discarded=0 ratelimit.numratelimiters=0
	2014-03-14T17:27:08.090574+08:00 localhost rsyslogd-pstats: action 1 queue[DA]: size=0 enqueued=0 full=0 maxqsize=0
	2014-03-14T17:27:08.090590+08:00 localhost rsyslogd-pstats: action 1 queue: size=1000 enqueued=1065 full=65 maxqsize=1000
	2014-03-14T17:27:08.090598+08:00 localhost rsyslogd-pstats: main Q[DA]: size=0 enqueued=0 full=0 maxqsize=0
	2014-03-14T17:27:08.090604+08:00 localhost rsyslogd-pstats: main Q: size=9940 enqueued=32042 full=18 maxqsize=10000

在没有配置 `$MainMsgQueueSize` 和 `$ActionQueueSize` 时，可以看到队列最大值分别是10000和1000。

对于Action Queue, 可以看到默认是'Action 1'、'Action 2'...命名的，可以通过 `$ActionName <name>`来对Action Queue命名. 在文档中还没找到这个配置，不过在[mail list](http://lists.adiscon.net/pipermail/rsyslog/2012-May/029913.html)中看到了回答.

更多的可以参考:

* [impstats配置讲解](http://www.rsyslog.com/doc/impstats.html)
* [使用impstats](http://www.rsyslog.com/how-to-use-impstats/)
* [Main Queue输出术语](http://www.rsyslog.com/rsyslog-statistic-counter-queues/)

## 实践 ##

遇到一个kernel的报错, 一直在刷日志, 现在要把包含这条报错信息的内核日志丢弃:

    :msg, contains, "message want to be dropped" ~

或者更详细的:

    if $syslogfacility-text == 'kern' and ($msg contains 'message want to be dropped') then ~

参考: [Discarding unwanted messages](http://www.rsyslog.com/discarding-unwanted-messages/)

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
