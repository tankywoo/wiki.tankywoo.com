---
title: "logrotate"
date: 2016-03-07 22:00
collection: "日志管理"
updated: 2016-08-03 22:03
log: "增加信号相关"
---

[TOC]

## 基础

关于logrotate分割日志后重新打开日志文件，一般发送`USR1`信号。

具体可以看看各个信号的作用`man 7 signal`。 延伸：

* [Why do many Unix programs use signals like USR1?](http://stackoverflow.com/questions/5350865/why-do-many-unix-programs-use-signals-like-usr1)
* [PHP-FPM signals for pool error_log rotation](http://serverfault.com/questions/444673/php-fpm-signals-for-pool-error-log-rotation)

## 参考

* man 8 logrotate
* [鸟哥的Linux私房菜](http://vbird.dic.ksu.edu.tw/linux_basic/0570syslog_3.php#rotate)
* [被遗忘的Logrotate](http://huoding.com/2013/04/21/246)
* [HowTo: The Ultimate Logrotate Command Tutorial with 10 Examples](http://www.thegeekstuff.com/2010/07/logrotate-examples/)
* [Understanding logrotate utility](https://support.rackspace.com/how-to/understanding-logrotate-utility/)
* [Managing Logs with Logrotate](https://serversforhackers.com/managing-logs-with-logrotate)
