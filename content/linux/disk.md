---
title: "磁盘相关"
date: 2016-10-01 11:00
updated: 2017-08-23 16:37
log: ""
---

[TOC]


FROM: <http://unix.stackexchange.com/questions/5085/how-to-see-disk-details-like-manufacturer-in-linux>

```text
lshw -class disk
  *-disk:0
       description: SCSI Disk
       product: PERC H710
       vendor: Winbond Electronics
       physical id: 2.0.0
       bus info: scsi@0:2.0.0
       logical name: /dev/sda
       version: 3.13
       serial: 00d6621b0483fd451f00f570dce03f08
       size: 278GiB (299GB)
       capabilities: partitioned partitioned:dos
       configuration: ansiversion=5 signature=48992565
  *-disk:1
       description: SCSI Disk
       product: PERC H710
       vendor: Winbond Electronics
       physical id: 2.1.0
       bus info: scsi@0:2.1.0
       logical name: /dev/sdb
       version: 3.13
       serial: 00954bd7048ffd451f00f570dce03f08
       size: 278GiB (299GB)
       capabilities: partitioned partitioned:dos
       configuration: ansiversion=5 signature=4ea89616

```

显示是PERC H710的Raid 控制器(PowerEdge RAID Controller)。


FROM <http://serverfault.com/questions/381177/megacli-get-the-dev-sd-device-name-for-a-logical-drive>

```text
ls -l /dev/disk/by-path/
total 0
lrwxrwxrwx 1 root root  9 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:0:0 -> ../../sda
lrwxrwxrwx 1 root root 10 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:0:0-part1 -> ../../sda1
lrwxrwxrwx 1 root root  9 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:1:0 -> ../../sdb
lrwxrwxrwx 1 root root 10 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:1:0-part1 -> ../../sdb1
lrwxrwxrwx 1 root root  9 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:2:0 -> ../../sdc
lrwxrwxrwx 1 root root 10 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:2:0-part1 -> ../../sdc1
lrwxrwxrwx 1 root root  9 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:3:0 -> ../../sdd
lrwxrwxrwx 1 root root 10 Sep 28 20:27 pci-0000:02:00.0-scsi-0:2:3:0-part1 -> ../../sdd1
```

FROM: <http://www.cyberciti.biz/faq/linux-checking-sas-sata-disks-behind-adaptec-raid-controllers/>

```text
$ lspci | grep -i raid
02:00.0 RAID bus controller: LSI Logic / Symbios Logic MegaRAID SAS 2208 [Thunderbolt] (rev 05)
```

FROM: <https://www.thomas-krenn.com/en/wiki/Smartmontools_with_MegaRAID_Controller#cite_note-1>

smartctl provides integrated support for MegaRAID controller. Access is made in the following manner:

```text
# Where <N> stands for the device ID on the RAID controller.
$ smartctl -a -d megaraid,N  /dev/sdX
```

FROM `man smartctl`:

> megaraid,N - [Linux only] the device consists of one or more SCSI/SAS disks connected to a MegaRAID controller. The non-negative integer N (in the range of 0 to 127 inclusive) denotes which disk on the controller is monitored.  Use syntax such as:
>
> smart supported raid control: <https://www.smartmontools.org/wiki/Supported_RAID-Controllers>


```text
# 查找raid控制器的型号
$ lspci -nn | grep -i raid
02:00.0 RAID bus controller [0104]: Hewlett-Packard Company Smart Array Gen8 Controllers [103c:323b] (rev 01)

# 根据 https://www.smartmontools.org/wiki/Supported_RAID-Controllers
# 使用cciss类型

# 可以使用hpacucli工具, http://www.thegeekstuff.com/2014/07/hpacucli-examples/
$ smartctl -a -d cciss,0 /dev/sda

## 如果是LSI MegaRAID SAS Controller
$ lspci -nn | grep -i raid
84:00.0 RAID bus controller [0104]: LSI Logic / Symbios Logic MegaRAID SAS 2108 [Liberator] [1000:0079] (rev 05)

# 根据以下获取N
$ megacli -AdpAllInfo -aAll
Number of Backend Port: 8
Port  :  Address
0        5000c5007ef85205
1        5000c5007e988439
2        5000c5007ef86209
3        5000c5007e9868b1
4        0000000000000000
5        0000000000000000
6        0000000000000000
7        0000000000000000

$ megacli -PDList -Aall | egrep 'Device Id|SAS Address'
Device Id: 11
SAS Address(0): 0x5000c5007e9868b1
SAS Address(1): 0x0
Device Id: 10
SAS Address(0): 0x5000c5007ef86209
SAS Address(1): 0x0
Device Id: 9
SAS Address(0): 0x5000c5007e988439
SAS Address(1): 0x0
Device Id: 8
SAS Address(0): 0x5000c5007ef85205
SAS Address(1): 0x0
```



## 更多

* [官网](https://www.smartmontools.org/)
* [Linux Raid For Admins](https://wiki.debian.org/LinuxRaidForAdmins)
* [LSI Raid Controller](https://wiki.hetzner.de/index.php/LSI_RAID_Controller/en)
