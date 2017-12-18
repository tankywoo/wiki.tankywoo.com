---
title: "Wireshark"
date: 2017-03-05 15:20
collection: "网络(抓包/代理)"
---

[TOC]

[FROM](http://www.ttlsa.com/linux/wireshark-detailed/)

```
Wireshark基于libpcap on unix-like，winpcap on windows。Tcpdump同样基于libpcap实现。Libpcap来自于BPF
```


## 问题

### Mac下找不到网卡设备

打开 Wireshark，设备那一块报：*No interfaces found*。

原因是因为 **bpf** 设备权限不够，原来好像是 `0400`，从官网下载 DMG 安装包，点开始有一个 Read me first 文件，其中也提及这个问题。

Mac下，依赖额外的一个 `ChmodBPF` 工具（`brew info wireshark` 也可以通过 brew 来安装 Wireshark）：

> This creates an 'access_bpf' group and adds a launch daemon that changes the permissions of your BPF devices so that all users in that group have both read and write access to those devices.

预期如下所示：

```
$ ls -l /dev/bpf*
crw-rw----  1 root  access_bpf   23,   0 Mar  5 15:56 /dev/bpf0
crw-rw----  1 root  access_bpf   23,   1 Mar  5 15:56 /dev/bpf1
...
```


### pcapng vs pcap

PCAPNG：PCAP Next Generation Dump File Format，即PCAP下一代文件格式，后缀为.pacapng


## 待看

* [一站式学习Wireshark（一）：Wireshark基本用法](http://blog.jobbole.com/70907/)
* [Wireshark数据包分析(一)——使用入门](http://www.s0nnet.com/archives/wireshark-1)  系列
* [Wireshark入门与进阶系列一之基本使用](http://blog.csdn.net/qq_29277155/article/details/52059123) 系列
* [【存储入门必读】Wireshark入门：第一次亲密接触](http://bbs.ichunqiu.com/thread-5410-1-1.html)
