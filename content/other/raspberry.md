---
layout: page
title: "树莓派 Raspberry"
date: 2015-10-30 08:30
update: 2015-10-30 08:30
---

[TOC]

[树莓派](https://www.raspberrypi.org/)是一款基于arm架构的微型单片机电脑.

目前(2015-10-30)手头上使用的是几年前的1代B版, 700MHz CPU, 512M Ram. 刚换了一个[SanDisk 32G Class 10 Micro SD卡](http://item.jd.com/679773.html), 带卡托. 感觉速度上比原来的金士顿16G Class 10 SD卡有一些提升.

最开始装的Gentoo, 那叫一个无奈啊...

然后装的基于Debian6的Raspbian wheezy

最近刚换上基于Debian7的[Raspbian Jessie](https://www.raspberrypi.org/downloads/raspbian/)


## 安装镜像 ##

下载的Raspbian Jessie, zip包1.2G, 解压后是一个4.1G的img文件. Linux下使用`dd`直接写入SD卡. 不需要分区:

	tankywoo@gentoo-local ~ % sudo dd if=2015-09-24-raspbian-jessie.img of=/dev/sdb
	8448000+0 records in
	8448000+0 records out
	4325376000 bytes (4.3 GB) copied, 899.617 s, 4.8 MB/s

Win下好像使用的是win32diskimager这个工具.

## 初始账户密码 ##

	pi / raspberry

一定要改掉!!!

## 镜像源 ##

找了一圈, 发现国内 [清华mirror](http://mirrors.tuna.tsinghua.edu.cn/help/#raspbian) 支持Jessie.

	deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ jessie main non-free contrib
	deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ jessie main non-free contrib

更多的源列表见官方 [Raspbian Mirrors](https://www.raspbian.org/RaspbianMirrors)

## 初始扩容 ##

刚安装好后, 默认的根分区才3.9G:

	root@raspberrypi:~# df -lh
	Filesystem      Size  Used Avail Use% Mounted on
	/dev/root        3.9G  3.1G  491M  87% /
	/dev/mmcblk0p1   56M   20M   37M   36% /boot
	...

	root@raspberrypi:~# fdisk -l
	Disk /dev/mmcblk0: 29.7 GiB, 31914983424 bytes, 62333952 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: dos
	Disk identifier: 0xba2edfb9

	Device         Boot  Start     End Sectors Size Id Type
	/dev/mmcblk0p1        8192  122879  114688  56M  c W95 FAT32 (LBA)
	/dev/mmcblk0p2      122880 8447999 8325120   4G 83 Linux

初始就两个分区. 一个boot, 一个根分区. 需要扩容根分区.

	fdisk /dev/mmcblk0

记住分区2的起始扇区号, 按`d`删除分区2. 然后`n`重建分区, 起始需要和之前一致. 我这里配置的是分配25G空间 `+25G`. 然后`w`保存分区修改.

`partprobe`更新分区表, 然后`resize2fs`做online扩容:

	resize2fs /dev/mmcblk0p2

最后reboot.

因为根分区是ext4, 支持在线(online)扩容, 如不支持, 则需要reboot后再做resize2fs操作.

详细步骤可以参考:

* [How can I resize my / (root) partition?](http://raspberrypi.stackexchange.com/questions/499/how-can-i-resize-my-root-partition)
* [USING THE FULL SPACE ON YOUR SD CARD IN THE RASPBERRY PI](http://blog.retep.org/2012/06/19/using-the-full-space-on-your-sd-card/)

## Raspbian vim支持python ##

`apt-get`安装好vim后, 通过`vim --version`可以看到是不支持python扩展的.

不需要卸载自己编辑, 直接安装 `vim-nox` 即可:

    apt-get install vim-nox

## 其它 ##

* [树莓派实验室](http://shumeipai.nxez.com/)
* [Raspberry Pi 安裝心得、教學、簡介](https://wwssllabcd.github.io/blog/2013/01/31/how-to-setup-raspberry-pi/#安裝_OS)



