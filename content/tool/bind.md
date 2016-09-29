---
title: "BIND"
date: 2016-09-29 14:50
updated: 2016-09-29 14:50
collection: "DNS工具"
---

[TOC]

### 历史

BIND是目前最常用的一个DNS实现工具。

之前由伯克利分校(UCB)开发维护，最后一个版本是BIND9。

2009年后开始由Internet Software Consortium (ISC)开发新版BIND10

所以目前官方是 <https://www.isc.org/downloads/bind/>

摘自 [维基百科](https://en.wikipedia.org/wiki/BIND)


## 工具

bind配置、zone文件等如果出问题，会导致bind服务异常，印象中以前zone文件出现过一个语法错误。

好在bind包提供了一些工具集：

`named-checkconf`用于检查bind配置。

如果没问题，则不会有任何输出，否则报错：

```bash
$ named-checkconf /etc/bind/named.conf
/etc/bind/named.conf:125: unknown option 'inclxude'
```

`named-checkzone`用于检查zone文件：

```bash
# named-checkzone <zonename> <filename>
$ named-checkzone intra.example.com /etc/bind/ks/intra.example.com.zone
zone intra.example.com/IN: loaded serial 2016092801
OK
```
