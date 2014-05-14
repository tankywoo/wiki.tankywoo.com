---
title: "mount"
date: 2013-08-17 07:32
---


mount, 用于挂载分区到文件系统

`/etc/fstab` 是启动时读取的挂载列表, 挂载后的结果是存储在 `/proc/mounts` 里. 所以如果proc没有被挂载上, 则 `fdisk -l` 是看不到任何东西的.

具体可看/etc/fstab的注释和`man fstab`

`/etc/mtab` 是正在挂载的文件

## 常用操作 ##

### 挂载分区 ###

	mount -t type device dir

把 device 指定挂载格式挂载到 dir 上

### 查看已挂载分区 ###

	mount [-l] [-t type]

可以列出挂载列表中指定的类型

### 重新挂载 ###

	mount -o remount,rw device dir

最近遇到一个问题, fstab里都是以 `label` 挂载的, 但是 device 只用了uuid, 没有设置 label, 导致启动后挂载的权限是 ro, 最后在修改文件时一直无法保存, 还以为设置了 chattr, 后来才发现是这个地方导致的. 设置了 label 后, 重新挂载并设置 rw 权限就可以了.

### bind方式挂载 ###

	mount --bind olddir newdir

bind方式可以把一个已被挂载的目录再挂载到其他目录下

比如我的 /dev/sda5 已经挂载到 /home 目录下, 我可以把 /home 再挂载到 /mnt/home 下:

	mount --bind /home /mnt/home
	结果如下:
	/dev/sda5 on /home type ext4 (rw,noatime)
	/home on /mnt/home type none (rw,bind)

在挂载一个 livecd 来安装系统时(比如gentoo安装, 或rynsc安装linux), 就是先挂载根目录等, 然后以bind方式挂载 `sys`, `dev`, `proc`.



## 参考 ##

* [fstab and mtab](http://www.brunolinux.com/02-The_Terminal/Fstab_and_Mtab.html)
* [How to Mount and Unmount Filesystem / Partition in Linux](http://www.thegeekstuff.com/2013/01/mount-umount-examples/)

