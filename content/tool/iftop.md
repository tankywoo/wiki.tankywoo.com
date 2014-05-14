---
title: "iftop"
date: 2013-08-17 07:32
---


`iftop` - display bandwidth usage on an interface by host

## Display ##

Right Part:

	foo.example.com  =>  bar.example.com      1Kb  500b   100b
					 <=                       2Mb    2Mb    2Mb
					 
	The right part, indicates that 
	the rate at which data has been sent and received over the preceding 2, 10 and 40 second intervals


Bottom Part:

	TX:    cumm:   575KB   peak:   35.6Kb            rates:   9.61Kb  8.37Kb  5.83Kb
	RX:            120KB           3.78Kb                      688b   2.26Kb  1.45Kb
	TOTAL:         695KB           39.1Kb                     10.3Kb  10.6Kb  7.28Kb

TX is send, RX is receive  
comm is the total, peak is the top rate over last 40s  
rates indicate the rate average of 2s, 10s, 40s  


## Read More ##

* [Sysadmin's Toolbox: iftop](http://www.linuxjournal.com/content/sysadmins-toolbox-iftop|The)
* [Guide: Display Network Interface Bandwidth Usage on Linux](http://www.thegeekstuff.com/2008/12/iftop-guide-display-network-interface-bandwidth-usage-on-linux/|IFTOP)
* [Linux流量监控工具 - iftop](http://www.vpser.net/manage/iftop.html)

