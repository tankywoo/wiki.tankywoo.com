---
title: "InfluxDB"
date: 2016-09-21 10:40
updated: 2017-08-07 18:00
logs: "增加几个参考链接"
---

[TOC]

InfluxDB是一个Go写的时序数据库(Time-Series Database)。

[官网](https://www.influxdata.com/time-series-platform/influxdb/) / [Github](https://github.com/influxdata/influxdb) / [文档](https://docs.influxdata.com/influxdb/latest/)


## 基本

环境：Gentoo

目前版本V1.0，没有提供官方的ebuild，不过`go-overlay`有别人写好的：<https://github.com/gentoo-mirror/go-overlay/tree/master/dev-db/influxdb>

也可以直接下载tar包，里面是Go编译好的，包括二进制工具，配置文件和目录等。

tar包里的配置有详细注释，默认的比如数据存储路径都是`/etc`下。

也可以手动生成配置。手动生成的配置默认存储路径等在$HOME/.influxdb/，且注释相对少一些：

```bash
$ cp ./etc/influxdb/influxdb.conf{,bak}
$ ./usr/bin/influxd config > ./etc/influxdb/influxdb.conf
```

启动influxdb：

```text
$ ./usr/bin/influxd run --config ./etc/influxdb/infludb.conf
```

默认会全局监听三个端口：

* 8083: Web admin管理服务的端口, <http://localhost:8083>
* 8086: HTTP API的端口
* 8088: 集群端口(目前还不是很清楚, 配置在全局的bind-address，默认不配置就是开启的)

官方给出的硬件配置是，[参考](https://docs.influxdata.com/influxdb/v1.0/introduction/installation#hardware)：

* 两块SSD。一块存储influxdb/wal，一块存储influxdb/data
* 最少8G内存

另外就是注意启动时的进程权限以及存储目录权限问题了。


### 核心概念

Influxdb是一个时序数据库，数据都是一些可度量的值，比如cpu load或者温度等。

写入是一行行的数据，称为`Point`：

```text
<measurement>[,<tag-key>=<tag-value>...] <field-key>=<field-value>[,<field2-key>=<field2-value>...] [unix-nano-timestamp]
```

由`time`(时间戳), `measurement`(比如cpuload), 至少一个k/v对`field`(measured value，比如value=0.6), 0个或多个k/v对`tags`(一些元信息metadata, 如host=server01, region=us)

官方给的例子：

```text
cpu,host=serverA,region=us_west value=0.64
payment,device=mobile,product=Notepad,method=credit billed=33,licenses=3i 1434067467100293230
stock,symbol=AAPL bid=127.46,ask=127.48
temperature,machine=unit42,type=assembly external=25,internal=37 1434067467000000000
```

和MySQL做类比，InfluxDB的`measurement`类似于表，主索引永远是time, tags是被索引的，fields不是；Point就是一行行的数据，只不过表名是在Point中。


### 常用操作

```text
# -----------------------------------------------------------------------------
# Query Language列表:
# <https://docs.influxdata.com/influxdb/v1.0/query_language/spec/>
# -----------------------------------------------------------------------------

# 创建数据库
> create database mydb

# 查看有哪些数据库, 在配置了认证的情况下，只有admin权限的用户可以看
> show databases;
name: databases
---------------
name
_internal  # <-- 这个是内置的，用于存储一些influxdb元信息
mydb

# 选择使用的数据库
> use mydb
Using database mydb

# 插入数据
> INSERT cpu,host=serverA,region=us_west value=0.62

# 查询数据
# 需要用 **双引号**
# 也可以 **都** 不用双引号
# ref: https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_tutorial/#quoting
> SELECT "host", "region", "value" FROM "cpu"
name: cpu
---------
time                    host    region  value
1474442747173411091     serverA us_west 0.62

# 插入多个数据(fields)
> INSERT temperature,machine=unit42,type=assembly external=25,internal=37

# 除了glob匹配，InfluxQL还支持Go-Style的正则
> SELECT * FROM 'cpu'
ERR: error parsing query: found cpu, expected identifier at line 1, char 14
> SELECT * FROM "cpu"
name: cpu
---------
time                    host    region  value
1474442747173411091     serverA us_west 0.62

# 显示所有的measurements
> show measurements
name: measurements
------------------
name
cpu


# 删除操作
# https://docs.influxdata.com/influxdb/v1.0/query_language/database_management/
# 看了下v1.0和v0.9的文档，这块变化还是不少
# 目前这块几种的具体区别还没弄明白 TODO

## drops the series from index
## FROM或WHERE至少存在一个
> DROP SERIES FROM "cpu" WHERE host='serverA'

## Unlike DROP SERIES, it does not drop the series from the index and it supports time intervals in the WHERE clause.
> DELETE FROM "cpu" WHERE host='serverA'

## The DROP MEASUREMENT query deletes all data and series from the specified measurement and deletes the measurement from the index.
> DROP MEASUREMENT "cpu"


# 其它
# 查询时时间显示，使用rfc3339格式时间(默认是时间戳)
# https://docs.influxdata.com/influxdb/v1.0//tools/shell/#influx-arguments
> precision rfc3339

```


### 用户认证和权限

文档：[Authentication and Authorization](https://docs.influxdata.com/influxdb/v1.0/query_language/authentication_and_authorization/)

开启用户认证，首先创建admin权限用户和相应数据库的普通用户：

```text
# 默认没有用户
> show users;
user    admin  # 这里admin是一个boolean值

# 创建一个admin权限的用户
> create user admin with password '********' with all privileges
> show users;
user    admin
admin   true

# 创建一个普通权限的用户
> create user tankywoo with password '********'
> show users;
user       admin
admin      true
tankywoo   false

# 给普通用户赋予某个数据库的权限
> grant all on mydb to tankywoo

# 查看某个用户的权限
> show grants for tankywoo
database        privilege
mydb            ALL PRIVILEGES

# 删除用户
> drop user tankywoo
```

配置文件的`[http]`块：

```text
[http]
  enable = true
  bind-address = ":8086"
  auth-enabled = true  # 开启认证
  ...
```

重启influxd，下次使用influx cli时需要认证：

```text
# influx cli认证
# 然后进入交互输入用户名和密码
> auth
username: tankywoo
password:
```

## Retention Policy 和 Continuous Query

* Retention Policy(RP): 保留策略, 控制数据存储的周期，超过duration的自动删除
* Continuous Query(CQ): 连续查询, 配合RP，自动对数据downsample(降低采样率)并存入其它measurement

类似于rrdtool中的rra的概念，可以控制不同的存储时长有不同的数据采样粒度。

关于RP, 默认是autogen, 表示永久存储. 默认配置下对每一个DB会自动创建, 可以通过修改配置`retention-autocreate`来控制不自动创建.

可以修改其它RP为默认RP:

```
# 如新建一个one_hour的RP, 并设置为默认的RP
> show retention policies on mydb
name            duration        shardGroupDuration      replicaN        default
autogen         0               168h0m0s                1               false
one_hour        1h0m0s          1h0m0s                  1               true
one_day         24h0m0s         1h0m0s                  1               false
```

关于对其它RP的写入和查询, 格式和普通的稍微有些区别, 之前没看清楚文档, 结果被折腾了半天:

```text
# 写入
> INSERT INTO [<database>.]<retention_policy> <line_protocol>

# 查询
> SELECT * FROM "<database>"."<retention_policy>"."<measurement>"
```

注意写入是有个`INTO`子句. [How do I write to a non-DEFAULT retention policy with InfluxDB’s CLI?](https://docs.influxdata.com/influxdb/v1.0/troubleshooting/frequently-asked-questions/#how-do-i-write-to-a-non-default-retention-policy-with-influxdb-s-cli)

比如:

```
> insert into one_hour load 1=1.0,5=2.0,15=3.0

> select * from one_hour.load
```

还有个地方需要注意:

> Note that once you specify a retention policy with INSERT INTO, influx automatically writes data to that retention policy. This occurs even for later INSERT entries that do not include an INTO clause. Restarting the CLI will revert to using the DEFAULT retention policy. [来源](https://docs.influxdata.com/influxdb/v1.0/tools/shell/#write-data-to-influxdb-with-insert)

```text
> insert into one_day mem value=2
Using retention policy one_day
```

如上可以看到, 说有使用`one_day`这个RP, 后续如果直接`insert mem value=3`，则依然是写入`one_day`这个RP. 要么重新`insert into`指定, 要么重新登录cli client.

如果需要清空 RP 里的数据，则直接删掉 RP 即可。

目前这块没法针对 RP 中的某个 measurement 单独删除，因为 `drop measurement "xxx"` 是没法指定 RP 的，以前这样会导致将默认RP的 measurement 删掉，现在会有提示（在 Issue 上看到的，没具体尝试）。

构建CQ:

```
> create continuous query "cq_5m" on "mydb" begin select mean("value") into "one_day"."load" from "load" group by time(5m) end

# 查看
> show continuous queries
```

关于这块，两点需要注意：

1 `GROUP BY` 后面如果没有接指定的 **tags** （逗号分隔），则生成的 RP 数据中，这些 tags 的值都是空的。

2 在我使用的情况，一个 db 里 N 个 measurements，一个 measurement 中 N 个 fields。全部按上面来添加，会累晕的，后来有支持 [Automatically downsample a database with backreferencing](https://docs.influxdata.com/influxdb/v1.0/query_language/continuous_queries/#example-3-automatically-downsample-a-database-with-backreferencing)，但是有个蛋疼的地方，比如用 `mean()`，它会将所有的 field 的名字都改为 *mean_field*，优点就是一个 CQ 就解决了所有 measurements 的问题，而且后面的 tags 也可以省略。不过最后我还是选择写个脚本生成20多个 CQ……

```
CREATE CONTINUOUS QUERY "cq_basic_br" ON "transportation"
BEGIN
  SELECT mean(*) INTO "downsampled_transportation"."autogen".:MEASUREMENT FROM /.*/ GROUP BY time(30m),*
END
```

参考文档:

* [Downsampling and Data Retention](https://docs.influxdata.com/influxdb/v1.0/guides/downsampling_and_retention/)
* [Continuous Queries](https://docs.influxdata.com/influxdb/v1.0/query_language/continuous_queries/)
* [InfluxDB学习之InfluxDB数据保留策略](http://www.linuxdaxue.com/retention-policies-in-influxdb.html)


## 关于 GROUP BY 语句

GROUP BY 语句用于筛选数据，最常见的是 `GROUP BY time(interval)`，除了这个外，还有 `GROUP BY tag`。

之前有个需求，机器外网流量的 points 有 location、if_name、host 几个字段，现在 Grafana 要画出同一个 location 的每个节点流量：

初始的写法是：

```
SELECT non_negative_derivative(mean("out"), 1s) * 8 as wan FROM "net" WHERE location = '$idc' AND "if_name" = 'wan' GROUP BY time($interval) fill(null)
```

但是这样画出来的所有数据是在一个数据里，无法区别同一个机房的每一台机器，且画出来的数据因为是混合的 derivative 操作，所以总数据也是错误的。

后来看文档发现还有 `GROUP BY tag` 的用法，可以将数据按指定的 tag 分开，适合这样的场景。

改正后的 metric 语句：

```
SELECT non_negative_derivative(mean("out"), 1s) * 8 as wan FROM "net" WHERE location = '$idc' AND "if_name" = 'wan' GROUP BY host, time($interval) fill(null)
```

参考：[The GROUP BY clause](https://docs.influxdata.com/influxdb/v1.2/query_language/data_exploration/#the-group-by-clause)


## 其它

### 关于 point 的唯一性

一个 Point 由 timestamp 和 tag 唯一识别。

所以要覆盖一个 Point 时，即修改这个 Point 的某些 value，只需要插入时指定相应的 timestamp 和 tag 即可：

```
> insert load,host=server1 value=0.00 1488435842307330152
> select * from load
name: load
---------
time                    host    value
1488435842307330152     server1 0

# 插入一条相同的
> insert load,host=server1 value=0.00 1488435842307330152
> select * from load
name: load
---------
time                    host    value
1488435842307330152     server1 0

# 插入一条值修改后的
> insert load,host=server1 value=0.01 1488435842307330152
> select * from load
name: load
---------
time                    host    value
1488435842307330152     server1 0.01
```


### 关于单双引号

总是忘了哪里改用单引号，哪里该用双引号，还是直接看文档吧：

* [When should I single quote and when should I double quote in queries?](https://docs.influxdata.com/influxdb/v1.2/troubleshooting/frequently-asked-questions/#when-should-i-single-quote-and-when-should-i-double-quote-in-queries)
* [TL;DR InfluxDB Tech Tips – Using Single Quotes vs Double Quotes Within InfluxQL](https://www.influxdata.com/tldr-influxdb-tech-tips-july-21-2016/)
* [InfluxQL Reference](https://docs.influxdata.com/influxdb/v1.2/query_language/spec/) 搜关键字 `quote`


## 术语

* InfluxQL: Influx Query Language
* Series: 序列, 是由一项指标(measurement)和一组标签键值对(tag)组成的


## 其它

* [influxdb-handbook](https://www.gitbook.com/book/xtutu/influxdb-handbook/details)
* [python-influxdb](http://influxdb-python.readthedocs.io/en/latest/index.html)
* [influxdata/telegraf](https://github.com/influxdata/telegraf)  The plugin-driven server agent for collecting & reporting metrics.
* [时间序列数据库调研之InfluxDB](http://blog.fatedier.com/2016/07/05/research-of-time-series-database-influxdb/)
* [mark-rushakoff/awesome-influxdb](https://github.com/mark-rushakoff/awesome-influxdb) awesome 系列之 influxdb 篇
* [influxdata/chronograf](https://github.com/influxdata/chronograf) influxdata 自家的画图工具，不过感觉比 grafana 差太多……
* [使用 Kapacitor 对 InfluxDB 数据进行统计处理](http://hugoren.iteye.com/blog/2312979) influxdata 自家的数据预警工具
