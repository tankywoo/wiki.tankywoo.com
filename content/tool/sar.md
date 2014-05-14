---
title: "sar"
date: 2013-08-17 07:32
---

Sar commands comes with the sysstat package. Make sure sysstat is installed. If you don’t have sar installed on your system, get it from Sysstat project.

Sar is an excellent monitoring tool that displays performance data of pretty much every resource of the system including CPU, memory, IO, paging, networking, interrupts etc.,

Sar Collects, Reports (displays) and Saves the performance data.


直接使用 `sar` 命令会报错:

> Cannot open /var/log/sa/sa05: No such file or directory

开启 `sysstat` 服务解决, [参考](http://forums.gentoo.org/viewtopic-t-641960-view-next.html?sid=fd20b938e3904492b2f865039f250625)

	/etc/init.d/systat start




## 参考资料 ##

* [10 Useful Sar (Sysstat) Examples for UNIX / Linux Performance Monitoring](http://www.thegeekstuff.com/2011/03/sar-examples/)
* [Using sar to Monitor System Performance](http://www.hosting.com/support/linux/using-sar-to-monitor-system-performance)
* [Hack 96. Sar Command Examples](http://linux.101hacks.com/monitoring-performance/sar-command-examples/)
* [Using the Linux sar command](http://www.inmotionhosting.com/support/website/general-server-setup/using-the-linux-sar-command)
