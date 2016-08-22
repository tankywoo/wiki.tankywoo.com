---
title: "CentOS"
date: 2016-05-01 23:00
updated: 2016-05-01 23:00
collection: "发行版"
log: "初始化"
---

[TOC]

## 基本 ##

### EPEL ###

Extra Packages for Enterprise Linux的简写，详细见[官方wiki](https://fedoraproject.org/wiki/EPEL)：

> EPEL is a Fedora Special Interest Group that creates, maintains, and manages a high quality set of additional packages for Enterprise Linux, including, but not limited to, Red Hat Enterprise Linux (RHEL), CentOS and Scientific Linux (SL), Oracle Linux (OL).

使用rpm安装相应版本的[epel源](https://dl.fedoraproject.org/pub/epel/):

	$ rpm -Uvh epel-release-X-Y.rpm
