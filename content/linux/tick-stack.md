---
title: "TICK技术栈"
date: 2017-08-24 10:28
log: ""
---

TICK 是由 InfluxData 开发的一套运维工具栈，由 Telegraf, InfluxDB, Chronograf, Kapacitor 四个工具的首字母组成。

这一套组件将 收集数据和入库、数据库、绘图、告警四者囊括了。

结构如下（[图片来源](https://www.influxdata.com/time-series-platform/)）：

![TICK Stack](https://www.influxdata.com/wp-content/uploads/InfluxData_TICK.png)

## InfluxDB

时序数据库工具。

详见另外一篇wiki：[InfluxDB](/database/influxdb.html)


## Telegraf

是一个数据收集和入库的工具。提供了很多 input 和 output 插件，比如收集本地的 cpu、load、网络流量等数据，然后写入 InfluxDB 或者 Kafka 等。

我们已经在几年前开发了一个性能数据收集工具，不过这个也简单了解过，感觉是目前 TICK 四大组件中也就这个和 InfluxDB 两者比较成熟了，使用用户也多一些。


## Chronograf

绘图工具，有点是绑定了 Kapacitor，缺点是难用。

所以我选择了成熟很多的 [Grafana](https://grafana.com/)。


## Kapacitor

[Kapacitor](https://docs.influxdata.com/kapacitor/) 是 InfluxData 家的告警工具，通过读取 InfluxDB 中的数据，根据 DLS 类型配置 TickScript 来进行告警。

说实话，Kapacitor 并没有给我什么感觉，应该目前依靠 Nagios 被动告警已经可以做到很好，而 Kapacitor 的 KickScript 则相对比较复杂，且目前这个工具还是不够成熟。

但是不妨碍我花点时间简单研究了解下，以作为以后告警的一个备选。

目前市面上没有看到有价值的文档，要么都是简介，实际例子没有，所以只看官方文档和它自带的例子吧，虽然我感觉写的比较简陋。

下面是 [Getting Started](https://docs.influxdata.com/kapacitor/v1.3/introduction/getting_started/) 的一个简单小结（目前的研究版本是 v1.3）：

总得来说，Kapacitor 的依赖就 InfluxDB，文档说也可以不用 InfluxDB，不过没看出还支持哪些。

`kapacitord` 生成配置并适当修改，启动，监听 http://0.0.0.0:9092，并主动向配置的 InfluxDB 配置订阅，通过 `SHOW SUBSCRIPTIONS` 可以看到增加的订阅信息，这样 InfluxDB 新接收的数据就会发送到 Kapacitor 上。

`kapacitor` 是 Kapacitor 提供的管理工具，根据 http api 操作 Kapacitor，比如新增任务等。

Kapacitor 的认为分两种，一种是 `stream`，一种是 `batch`。`stream` 方式相当于 Kapacitor 一直接收 InfluxDB 传递过来的数据并做相应分析和告警；而 `batch` 则是自动定义查询间隔和周期，对数据做一些聚合计算后再告警。

简单的例子如：

```
# InfluxDB 创建数据库
CREATE DATABASE mydb

# 编写 tick 脚本
$ cat tick/load_alert.tick
stream
    |from()
        .measurement('load')
    |alert()
        .warn(lambda: "value" > 3.2)
        .crit(lambda: "value" > 3.5)
        .log('/tmp/alerts.log')

# 定义这个任务，指定名称，tick脚本，db和rp
kapacitor define load_alert -type stream -tick tick/load_alert.tick -dbrp mydb.autogen

# 在启用这个任务前，先截取当前的数据测试下，发现告警泛滥
# record 会生成一个 recording id
kapacitor record stream -task load_alert -duration 20s
# replay 回放时根据这个 id 来回放
kapacitor replay -recording <id> -task load_alert

# 确认 /tmp/alert.log，如果告警预期，则可以考虑开启任务
kapacitor enable load_alert

# 任何时候如果更新了 tick 脚本，只需要再次执行 define 语句即可
# 可以在修改并define后，执行 replay 看看此时告警情况
```
