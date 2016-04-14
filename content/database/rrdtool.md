---
title: "rrdtool"
date: 2013-08-17 07:36
---


## RRDtool ##


## 简介 ##

RRDtool(Round Robin Database Tool)

效果图

## 安装 ##

参考: [RRDtool简体中文教程(ChinaUnix)](http://bbs.chinaunix.net/thread-2150417-1-1.html)

## 新建RRD ##
[Offical Doc - rrdcreate](http://oss.oetiker.ch/rrdtool/doc/rrdcreate.en.html)

	rrdtool create filename [--start|-b start time] [--step|-s step] [--no-overwrite] \
			[DS:ds-name:DST:dst arguments] \
			[RRA:CF:cf arguments]

	* filename
	rrd的名称. 默认以.rrd结尾

	* --start
	设置rrd的起始时间, rrd不接收比这个时间靠前的数据. 默认是当前时间前10s

	* --step
	设置时间步长. 默认是300s


### DS ###

DS - Data Source

一个RRD可以接受多个DS. 比如入口流量和出口流量分别作为各作为一个DS存在一个RRD里.

* `ds-name`: DS的名称, 长度为1~19个字符(Note)
* `DST`: Data Source Type, DS的类型, 有GAUGE, COUNTER, DERIVE, ABSOLUTE, COMPUTE

		DS:ds-name:GAUGE | COUNTER | DERIVE | ABSOLUTE:heartbeat:min:max
		DS:ds-name:COMPUTE:rpn-expression
			
		* GAUGE: 直接把值存入RRD
		* COUNTER: 用于记录持续增长的计数器. 适合一个率的计算，如流量增长率.
		* DERIVE: 和COUNTER类似. 但是可以计算增长或减少的率.
		* ABSOLUTE: 它假设每次前一个interval的值都是0, 再计算平均值. (没用过)
		* COMPUTE: 引用其他RRD中的DS来计算某个值. (没用过)

		`heartbeat`: 心跳. 定义两次更新间最大的秒数. 长于这个时间未获取到数据的, 则为 Unknown
		`min`,`max`: 定义期望数据的范围. 如果超出其中，则会被当作`UNKNOWN`. 如果不知道或不关心这个，可以设置为`U`
		`rpn-expression`: 逆波兰表达式


### RRA ###

RRA - Round Robin Archives

RRD的目的就是把数据存入RRA中. 一个RRA由许多数据值组成.

CF: Consolidation Function. 有AVERAGE, MIN, MAX, LAST类型.

在新建RRD的时候, 定义了step(一个interval的时间, 比如一分钟就是60s), 每个step都会有一个PDP(Primary Data Point).

在RRA中的steps表示这个RRA的CDP(Consolidation Data Point)使用上面的几个step, 比如要一分钟获取一个就写1

然后RRA会根据CF来计算PDP, 最后合并出CDP.

详细的RRA定义:

	RRA:AVERAGE | MIN | MAX | LAST:xff:steps:rows

	xff - 是一个比例值, 表示一个CDP中有超过xff的PDP为空值, 则这个值就回UNKNOWN
	steps - 上面提到了, 定义这个RRA使用几个step
	rows - 表示记录的CDP的个数, 比如上面选择一分钟一个CDP, 要记录1小时, row就是60


例子:

	11:06 tankywoo@gentoo-gs /home/tankywoo/rrd
	% rrdtool create test.rrd -s 60 \
	> DS:testds:GAUGE:120:0:U \
	> RRA:AVERAGE:0.5:1:60 \
	> RRA:AVERAGE:0.5:1:1440

	11:06 tankywoo@gentoo-gs /home/tankywoo/rrd
	% rrdtool info test.rrd
	filename = "test.rrd"
	rrd_version = "0003"
	step = 60
	last_update = 1370142396
	header_size = 792
	ds[testds].index = 0
	ds[testds].type = "GAUGE"
	ds[testds].minimal_heartbeat = 120
	ds[testds].min = 0.0000000000e+00
	ds[testds].max = NaN
	ds[testds].last_ds = "U"
	ds[testds].value = 0.0000000000e+00
	ds[testds].unknown_sec = 36
	rra[0].cf = "AVERAGE"
	rra[0].rows = 60
	rra[0].cur_row = 51
	rra[0].pdp_per_row = 1
	rra[0].xff = 5.0000000000e-01
	rra[0].cdp_prep[0].value = NaN
	rra[0].cdp_prep[0].unknown_datapoints = 0
	rra[1].cf = "AVERAGE"
	rra[1].rows = 1440
	rra[1].cur_row = 339
	rra[1].pdp_per_row = 1
	rra[1].xff = 5.0000000000e-01
	rra[1].cdp_prep[0].value = NaN
	rra[1].cdp_prep[0].unknown_datapoints = 0


## 更新RRD ##
[Offical Doc - rrdupdate](http://oss.oetiker.ch/rrdtool/doc/rrdupdate.en.html)

	rrdtool {update | updatev} filename
			[--template|-t ds-name[:ds-name]...]
			[--daemon address] [--]
			N|timestamp:value[:value...]
			at-timestamp@value[:value...]
			[timestamp:value[:value...] ...]


`updatev` : 是 `update` 的 verbose版, 会描述返回信息.

`--template|-t ds-name[:ds-name]...` :   
默认情况下, update希望数据是按DS定义的顺序来更新的. 但是有可能会弄错顺序, 导致传入的数据错误.  
template函数允许指定更新DS的顺序  

`N|timestamp:value[:value...]` :  
更新DS的数据要有一个指定的时间戳. 如果使用 `N`, 则使用当前时间.  
如果时间是负数, 则使当前时间减去指定的时间. 此时要用 `--` 来分隔选项和数据, 否则数据会被当作参数传进去.  
如果使用 `@` 代替 `:`, 则限定结束时间.  
*TODO*

	# 下面写了一个 Python 传入随机数据来更新 RRD
	# 我放到 crontab 里面每分钟调用一次

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-

	import rrdtool
	import random

	v = random.randint(1, 100)
	rrdtool.updatev('test.rrd', 'N:%d' % v)


## 画图 ##
[Offical Doc - rrdgraph](http://oss.oetiker.ch/rrdtool/doc/rrdgraph.en.html)

	rrdtool graph|graphv filename [option ...] 
			[data definition ...] 
			[data calculation ...] 
			[variable definition ...] 
			[graph element ...] 
			[print element ...]

	# 其中以下三个分别是data definition, data calculation, variable definition的格式
	DEF:vname=rrdfile:ds-name:CF[:step=step][:start=time][:end=time]

	CDEF:vname=RPN expression

	VDEF:vname=RPN expression


rrdtool graph 需要数据提供以画图. 它并不局限于单个RRD, 可以收集多个rrd的数据画图.  
从 RRA 里 fetch 出来数据, 然后合并(consolidated)它们, 所以图上一个像素一个数据点(data point).  
有时数据的格式并不是我们想要的. 在合并数据后, 强大的 `RPN` 命令集可以实现它们.  

`graphv` 与 `graph` 的关系类似 `updatev` 和 `update`. 可以获取相信的画图信息.

### options的一些参数 ###

`[-s|--start time] [-e|--end time] [-S|--step seconds]` :  
设置了画图的起始时间和结束时间, 一般使用结束时间减去需要监控的时间段范围就行.

`[-t|--title string] [-v|--vertical-label string]` :  
分别是: 图片顶部的横坐标label 和 左边纵坐标的label

`[-w|--width pixels] [-h|--height pixels] [-j|--only-graph] [-D|--full-size-mode]` :  
设置图片的宽度和高度
--only-graph 和  --full-size-mode
*TODO*

`[-u|--upper-limit value] [-l|--lower-limit value] [-r|--rigid]` :  
可以限制上限值和下限值

	DEF:vname=rrdfile:ds-name:CF[:step=step][:start=time][:end=time]
	DEF是画图的定义, 一般至少需要一个DEF, 用来定义使用的DS, 使用的CF函数, 步长等

	CDEF:vname=RPN expression
	前面提到的, 可能DEF获取的值在格式上无法满足需求, 这时可以使用CDEF用逆波兰表达式来生成需要的变量. 比如求网络流量单位是bit, 就可以用CDEF定义乘以8.

	VDEF:vname=RPN expression


在上面更新RRD的代码里增加画图代码:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-

	import rrdtool
	import random
	import time

	v = random.randint(1, 100)
	ret = rrdtool.updatev('test.rrd', 'N:%d' % v)

	now = int(time.time())
	onehour = str(now - 3600)
	ret = rrdtool.graphv('test.png',
	        '--start', str(onehour),
	        'DEF:v=test.rrd:testds:AVERAGE',
	        'AREA:v#00008B',
	        '-w 400 -h 100')


效果图:  
![效果图](http://tankywoo-wb.b0.upaiyun.com/rrd1.png)



## 资料 ##

* [RRDtool Tutorail(Offical)](http://oss.oetiker.ch/rrdtool/tut/)
* [RRDtool Documentation(Offical)](http://oss.oetiker.ch/rrdtool/doc/index.en.html)
* [RRDtool简体中文教程(ChinaUnix)](http://bbs.chinaunix.net/thread-2150417-1-1.html)
