---
title: "Ubuntu"
date: 2016-01-06 10:16
updated: 2016-09-03 17:45
collection: "发行版"
log: "更新配置timezone"
---

[TOC]

![Ubuntu Logo](http://design.ubuntu.com/wp-content/uploads/ubuntu-orange.gif)

* [Ubuntu官网](http://www.ubuntu.com/server)
* [Ubuntu Help](https://help.ubuntu.com/)

## 基本 ##

### apt-key ###

APT key管理工具

有时添加第三方的apt源，需要添加授权的key保证源是安全可信的。

比如添加salt源并操作`apt-get update`之前需要先添加key `apt-key add <key_file>`:

```bash
$ wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
```

列出已有的key `apt-key list`:

```bash
$ apt-key list
/etc/apt/trusted.gpg
--------------------

pub   2048R/DE57BFBE 2014-06-24
uid                  SaltStack Packaging Team <packaging@saltstack.com>
sub   2048R/17928113 2014-06-24
```

其中keyid是DE57BFBE

删除指定的key `apt-key del <keyid>`

```bash
$ apt-key del DE57BFBE
```


## 经验 ##

### remove vs purge ###

`apt-get` 的 `remove` 和 `purge` 区别:

* `remove`: 只删除软件包, 保留配置文件
* `purge`: 删除软件包和配置文件

这里的配置文件是指包添加的系统配置, 不包括用户自定义的配置.

参考:

* man apt-get
* [What is the Difference Between `apt-get purge` and `apt-get remove`?](http://askubuntu.com/questions/231562/what-is-the-difference-between-apt-get-purge-and-apt-get-remove)
* [What is the correct way to completely remove an application?](http://askubuntu.com/questions/187888/what-is-the-correct-way-to-completely-remove-an-application)

### 查询指定包的反向依赖 ###

即查看哪些包依赖指定的包.

    apt-cache rdepends <package>

showpkg也可以, 不过包含的内容更多一些:

    apt-cache showpkg <package>

查看哪些**已安装**的包依赖指定的包:

    apt-cache rdepends --installed <package>

更多可以`man 8 apt-cache`

参考:

* [How to list dependent packages](http://askubuntu.com/questions/128524/how-to-list-dependent-packages-reverse-dependencies)
* [Can I see why a package is installed?](http://askubuntu.com/questions/5636/can-i-see-why-a-package-is-installed)

### 更新 ###

	$ sudo apt-get update        # Fetches the list of available updates
	$ sudo apt-get upgrade       # Strictly upgrades the current packages
	$ sudo apt-get dist-upgrade  # Installs updates (new ones)

`update`负责更新可更新的软件列表，`upgrade`更新已装的包，`dist-upgrade`更新需要新安装的包。

比如在upgrade时，提示

	$ apt-get upgrade
	...
	The following packages were automatically installed and are no longer required:
	  linux-headers-4.4.0-21 linux-headers-4.4.0-21-generic linux-image-4.4.0-21-generic linux-image-extra-4.4.0-21-generic
	Use 'apt autoremove' to remove them.
	The following packages have been kept back:
	  linux-generic linux-headers-generic linux-image-generic
	The following packages will be upgraded:
	...

在dist-upgrade时，提示：

	$ apt-get dist-upgrade
	...
	The following packages were automatically installed and are no longer required:
	  linux-headers-4.4.0-21 linux-headers-4.4.0-21-generic linux-image-4.4.0-21-generic linux-image-extra-4.4.0-21-generic
	Use 'apt autoremove' to remove them.
	The following NEW packages will be installed:
	  linux-headers-4.4.0-28 linux-headers-4.4.0-28-generic linux-image-4.4.0-28-generic linux-image-extra-4.4.0-28-generic
	The following packages will be upgraded:
	  linux-generic linux-headers-generic linux-image-generic
	...

即更新linux-headers, linux-image等相关的包

参考：[How to install updates via command line?](http://askubuntu.com/questions/196768/how-to-install-updates-via-command-line)

### 安全更新 ###

和上面基本一样。

Ubuntu的包版本在当前发行版(如12.04)release出来后，版本号基本是不会变的，后期有安全更新，都是以patch形式增加。

比如openssl，经常爆出漏洞，虽然官方是建议建议到1.0.1t等当前最新版本，不过ubuntu下针对这些安全更新都增加了patch。

首先`apt-get update`更新软件包树，如果有更新一是`apt-get upgrade`会提示；另外还可以通过`source`来确认：

	$ apt-get source openssl

会将openssl的debian目录tar包等下载下来：

	# ls
	debian  // openssl_1.0.1-4ubuntu5.36.debian.tar.gz解压后的目录
	openssl_1.0.1-4ubuntu5.36.debian.tar.gz
	openssl_1.0.1-4ubuntu5.36.dsc
	openssl_1.0.1.orig.tar.gz

	$ ls debian/patches/CVE-2016-2107.patch

比如最近的安全漏洞CVE-2016-2107，目前就给出了修复patch, 版本是openssl_1.0.1-4ubuntu5.36

然后更新：

	apt-get install openssl
	apt-get install libssl1.0.0

注意，对于openssl，要更新libssl1.0.0, openssl只是相关的工具包，而libssl1.0.0才是动态库的更新。具体可以看debian/control文件。

更新完记得重启nginx。



## 问题 ##

### syntax error: unknown group 'ssl-cert' in statoverride file ###

安装某个包时遇到这个报错:

    $ apt-get install libffi-dev
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    The following NEW packages will be installed:
      libffi-dev
    0 upgraded, 1 newly installed, 0 to remove and 18 not upgraded.
    Need to get 0 B/96.1 kB of archives.
    After this operation, 356 kB of additional disk space will be used.
    dpkg: unrecoverable fatal error, aborting:
     syntax error: unknown group 'ssl-cert' in statoverride file
    E: Sub-process /usr/bin/dpkg returned an error code (2)

其实提示还是很清楚了, statoverride文件有一个未知的用户组ssl-cert.

这个组其实是Apache建立的. 个人猜测应该是在卸载Apache时, 用的remove而不是purge导致.

文件在/var/lib/dpkg/statoverride:

    $ cat /var/lib/dpkg/statoverride
    root mlocate 2755 /usr/bin/mlocate
    root ssl-cert 710 /etc/ssl/private
    root Debian-exim 640 /etc/exim4/passwd.client
    root stapusr 4750 /usr/bin/staprun
    root crontab 2755 /usr/bin/crontab

这个的作用可以[`man 8 dpkg-statoverride`](http://manpages.ubuntu.com/manpages/trusty/man8/dpkg-statoverride.8.html):

> override ownership and mode of files

> `stat overrides' are a way to tell dpkg(1) to use a different owner or mode for a path when a package is installed

### The following packages have unmet dependencies ###

	Reading package lists... Done
	Building dependency tree
	Reading state information... Done
	You might want to run 'apt-get -f install' to correct these:
	The following packages have unmet dependencies:
	 pack_1 : Depends: pack_2 but it is not going to be installed
	 E: Unmet dependencies. Try 'apt-get -f install' with no packages (or specify a solution).

之前dpkg安装包pack_1, 依赖pack_2;

未安装pack_2前先安装pack_1则出现这个问题, 不过安装pack_2就可以了.

但是pack_2之前是另外一个名称, 导致改名后的deb安装不了.

尝试:

	apt-get -f install
	apt-get purge pack_2_origin_name

都不行.

后来发现`dpkg --purge package` 可以删除老的包.

参考: [How To Overwrite Existing Files From A Removed Package in Ubuntu and Debian](http://linuxg.net/how-to-overwrite-existing-files-from-another-package-in-ubuntu-and-debian/)

### files list file for package 'xxx' is missing final newline ###

报错:

	(Reading database ... 95%dpkg: unrecoverable fatal error, aborting:
	  files list file for package 'xxx' is missing final newline
	  E: Sub-process /usr/bin/dpkg returned an error code (2))

通过`apt-get purge`或`dpkg -P`都无法卸载包。

参考[这篇回答](http://askubuntu.com/a/350508/434496), 发现是 `/var/lib/dpkg/info` 下那个包的文件损坏了, 文件内容有乱码导致, 删掉即可.

### 配置timezone(时区) ###

```bash
$ dpkg-reconfigure tzdata
```

基本和Gentoo的方式一样，通过/etc/timezone的配置，修改/etc/localtime。执行命令时会显示一个交互式的窗口，更新会同时写入/etc/timezone和/etc/localtime。可以直接写文件而不进入交互方式：

```bash
$ dpkg-reconfigure -u tzdata
```
