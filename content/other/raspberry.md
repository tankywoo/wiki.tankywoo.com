---
layout: page
title: "树莓派 Raspberry"
date: 2015-10-30 08:30
update: 2017-08-23 16:33
log: "更新树莓派wifi链接的参考链接"
---

[TOC]

[树莓派](https://www.raspberrypi.org/)是一款基于arm架构的微型单片机电脑.

目前(2015-10-30)手头上使用的是几年前的1代B版, 700MHz CPU, 512M Ram. 刚换了一个[SanDisk 32G Class 10 Micro SD卡](http://item.jd.com/679773.html), 带卡托. 感觉速度上比原来的金士顿16G Class 10 SD卡有一些提升.

最开始装的Gentoo, 那叫一个无奈啊...

然后装的基于Debian6的Raspbian wheezy

最近刚换上基于Debian7的[Raspbian Jessie](https://www.raspberrypi.org/downloads/raspbian/)

*（2017-04-13 补充）*

一些资源：

* [树莓派安装 Gentoo](https://wiki.gentoo.org/wiki/Raspberry_Pi)  算了，还是别自己遭罪了，最近刚买了一个 Deskmini，专门来跑 Gentoo
* [树莓派可以安装的Linux发行版有哪些？](https://www.zhihu.com/question/31632573)  看看大家都给出了哪些资源
* [官方下载页面](https://www.raspberrypi.org/downloads/) | [官方下载目录](https://downloads.raspberrypi.org/) 不折腾了，还是 Raspbian


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

<strike>找了一圈, 发现国内</strike> [清华mirror](http://mirrors.tuna.tsinghua.edu.cn/help/#raspbian) 支持Jessie.

	deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ jessie main non-free contrib
	deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ jessie main non-free contrib

还有 [LUG@USTC](https://lug.ustc.edu.cn/wiki/mirrors/help/raspbian)

更多的源列表见官方 [Raspbian Mirrors](https://www.raspbian.org/RaspbianMirrors)

## 初始扩容/新建分区 ##

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

初始只有两个分区, 个人习惯是将`/home`单独挂载到一个分区. 新增分区和Linux一样, 磁盘设备名是`/dev/mmcblk0`, 直接fdisk创建, partprobe同步分区.

详细步骤可以参考:

* [How can I resize my / (root) partition?](http://raspberrypi.stackexchange.com/questions/499/how-can-i-resize-my-root-partition)
* [USING THE FULL SPACE ON YOUR SD CARD IN THE RASPBERRY PI](http://blog.retep.org/2012/06/19/using-the-full-space-on-your-sd-card/)
* [Creating a seperate home partition (Raspberry Pi)](https://mike632t.wordpress.com/2014/02/10/resizing-partitions/)

## Raspbian vim支持python ##

`apt-get`安装好vim后, 通过`vim --version`可以看到是不支持python扩展的.

不需要卸载自己编辑, 直接安装 `vim-nox` 即可:

    apt-get install vim-nox

## 加密分区 ##

其实这个不是树莓派相关的内容, 不过刚在树莓派下试了, 顺便就先记录在这里.

以前经常手动安装ubuntu server时, 在分区这块记得好像是可以选择加密分区(好像centos 7安装时也遇到了), 不过都没有去尝试过. 现在树莓派作为一个备份机器, 有些重要数据是需要放在加密区, 于是搜了下.

首先安装 `cryptsetup` 包. 然后fdisk新建一个分区.

然后使用cryptsetup组件初始化待加密分区(注意这个会擦除重写分区, 如有资料需注意备份):

    # 这里的加密使用的是密码
    $ cryptsetup --verbose --verify-passphrase luksFormat /dev/mmcblk0p3

输入YES确认, 并输入密码. ok后需要打开加密分区, 映射到系统/var/mapper/下作为一个新的设备:

    # cryptsetup luksOpen <device> <name>
    $ cryptsetup luksOpen /dev/mmcblk0p3 mydisk

name是映射到/dev/mapper/下的设备名, 可以任意写

也可以使用open命令:

    $ cryptsetup open /dev/mmcblk0p3 mydisk

这时, fdisk -l 查看会看到多了一个新的磁盘.

第一次需要格式化这个磁盘, 不需要再分区, 直接格式化/新建文件系统整个磁盘即可:

    $ mke2fs -t ext4 /dev/mapper/mydisk

以后就不需要再建文件系统了, 直接mount挂载即可.

    $ mount /dev/mapper/mydisk /mnt/test/

还可以配置开机自动挂载, 这块就没去研究了, 还是先手动挂吧.

参考:

* [How to create an encrypted disk partition on Linux](http://xmodulo.com/how-to-create-encrypted-disk-partition-on-linux.html)
* [HowTo: Linux Hard Disk Encryption With LUKS [cryptsetup Command]](http://www.cyberciti.biz/hardware/howto-linux-hard-disk-encryption-with-luks-cryptsetup-command/)

## 禁止X Windows开机启动 ##

因为都是ssh直接登录, 也不需要桌面的支持, 所以完全没必要开机启动(`lightdm`)

最简单的关闭方式是使用raspbian提供的`raspi-config`命令, 选择3 Boot Options, 然后选择B1 Console  Text console, requiring user to login

看了下它的脚本内容:

    $ view `which raspi-config`
    ...
    if [ -e /etc/init.d/lightdm ]; then
      if [ $SYSTEMD -eq 1 ]; then
        systemctl set-default multi-user.target
        ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service
      else
        update-rc.d lightdm disable 2
        sed /etc/inittab -i -e "s/1:2345:respawn:\/bin\/login -f pi tty1 <\/dev\/tty1 >\/dev\/tty1 2>&1/1:2345:respawn:\/sbin\/getty --noclear 38400 tty1/"
      fi
    fi
    ;;
    ...

因为基于debian7, 使用的是systemd, 所以直接用systemctl管理即可. 当然后向兼容, 也可以通过upstarts来管理:

    $ update-rc.d lightdm stop

甚至remove也可以. 最后重启确认.


## 修改locale ##

发现默认的locale不知为何设置为`en_GB.UTF-8`, 导致使用mosh有问题, 使用export没法修改`LC_ALL`等.

没去具体看原因, 然后发现`raspi-config`里有对本地化的设置.(原因是 `en_US.UTF-8` 没有预生成)


## 开启 ssh ##

在 2016.11 的 release 中，ssh 默认开启给关闭了，开启很简单，具体参考官方文档 [REMOTE-ACCESS](https://www.raspberrypi.org/documentation/remote-access/ssh/)。

另外，开启 ssh server 后，连接报错：

```
$ ssh pi@192.168.1.200
Connection reset by 192.168.1.200
```

排查后，发现 `host_key_file` 有问题：

```
$ file /etc/ssh/ssh_host_*
/root/ssh.bak/ssh_host_dsa_key:         empty
/root/ssh.bak/ssh_host_dsa_key.pub:     empty
/root/ssh.bak/ssh_host_ecdsa_key:       empty
/root/ssh.bak/ssh_host_ecdsa_key.pub:   empty
/root/ssh.bak/ssh_host_ed25519_key:     empty
/root/ssh.bak/ssh_host_ed25519_key.pub: empty
/root/ssh.bak/ssh_host_key:             OpenSSH RSA1 private key, version 1.1
/root/ssh.bak/ssh_host_key.pub:         ASCII text, with very long lines
/root/ssh.bak/ssh_host_rsa_key:         empty
/root/ssh.bak/ssh_host_rsa_key.pub:     empty
```

ssh protocol 2 的相关 host key 文件都是空的，只有 protocol 1 的 key，但是 sshd_config 配置默认是 `Protocol 2`。

删掉这些空文件，然后重新生成：

```
$ dpkg-reconfigure openssh-server
```

这一块再继续深挖了一下：

目前稍微新一些的 OpenSSH 版本，`Protocol` 的版本默认都是2，如果要指定 1 和 2 混合，则显示写为 `Protocol 1,2`。默认的 `HostKey` 都是相应协议下的 host_key_file 文件名。

在 OpenSSH 6.7，`HostKey` 如果指定了相应的 host_key_file，比如只指定了 2 的，则哪怕写了协议是 1 和 2，客户端也无法用协议 1 登录。除非也写了协议 1 的 `HostKey`，或者全部注释使用默认。

在 OpenSSH 7.3，貌似不论怎么配置，客户端还是无法使用协议 1，这块就没有继续深究下去了。


## 配置 Wifi ##

参考 [SETTING WIFI UP VIA THE COMMAND LINE](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)，wpa-supplicant 默认是运行的，修改配置后，执行 `wpa_cli reconfigure` 重新加载配置即可。

更多参考：

* [树莓派连接WiFi](https://i.cmgine.net/archives/11053.html)
* [树莓派 Raspberry Pi 设置无线上网](http://www.jianshu.com/p/b42e8d3df449)


## 其它 ##

* [树莓派实验室](http://shumeipai.nxez.com/)
* [Raspberry Pi 安裝心得、教學、簡介](https://wwssllabcd.github.io/blog/2013/01/31/how-to-setup-raspberry-pi/#安裝_OS)



