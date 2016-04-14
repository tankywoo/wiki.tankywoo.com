---
title: "nscd"
date: 2016-04-05 14:50
updated: 2016-04-05 14:50
collection: "DNS工具"
log: "新增文档"
---

[TOC]

nscd是一个dns解析相关的缓存守护进程。

之前有遇到过个别域名无法解析的情况, name server都是ok的, 没有具体排查, 只知道是nscd的原因。

停掉nscd服务后解析正常。

不过看到一篇文章: [How to really flush the various nscd caches](https://stijn.tintel.eu/blog/2012/05/10/how-to-really-flush-the-various-nscd-caches), 里面指出停掉nscd服务但是缓存文件还是会在本地存放, 所以停掉并不能解决问题, 需要强制去指定清除缓存:

	nscd -i <table_name>  # 或者 nscd --invalidate=<table_name>

一般是hosts表:

	nscd -i hosts

TODO 这个问题下次再遇到验证下, 本地还没看到这个缓存问题, 暂时不去分析了.
