---
title: "Gentoo"
date: 2014-08-30 16:29
updated: 2016-06-23 19:15
log: "增加禁用新网卡命名的方式"
collection: "发行版"
---

[TOC]

![Gentoo Logo](https://1b9a50f4f9de4348cd9f-e703bc50ba0aa66772a874f8c7698be7.ssl.cf5.rackcdn.com/site-logo.svg)

* [Gentoo官网](https://www.gentoo.org/)
* [Gentoo Handbook](https://wiki.gentoo.org/wiki/Handbook:Main_Page)


## 基本 ##

### Architecture ###

[Handbook-MainPage](https://wiki.gentoo.org/wiki/Handbook:Main_Page) 介绍了什么是架构:

> An architecture is a family of CPUs (processors) who support the same instructions. The two most prominent architectures in the desktop world are the x86 architecture and the x86_64 architecture (for which Gentoo uses the amd64 notation). But many other architectures exist, such as sparc, ppc (the PowerPC family), mips, arm, etc...
> 
> A distribution as versatile as Gentoo supports many architectures. For that reason, you'll find that our Gentoo Handbooks are offered for many of the supported architectures. However, that might lead to some confusion as not all users are aware of the differences. Some are only aware of the CPU type or name that their system is a part of (like i686 or Intel Core i7). Below you will find a quick summary of the supported architectures and the abbreviation used in Gentoo. However, most people that do not know the architecture of their system are mostly interested in x86 or amd64.

---

### Stage ###

stage3 是Gentoo的最小系统:

> A stage3 tarball is an archive containing a minimal Gentoo environment, suitable to continue the Gentoo installation using the instructions in this manual. Previously, the Gentoo Handbook described the installation using one of three stage tarballs. While Gentoo still offers stage1 and stage2 tarballs, the official installation method uses the stage3 tarball. If you are interested in performing a Gentoo installation using a stage1 or stage2 tarball, please read the Gentoo FAQ on How do I Install Gentoo Using a Stage1 or Stage2 Tarball?

> Stage3 tarballs can be downloaded from releases/amd64/autobuilds/ on any of the official Gentoo mirrors and are not provided by the installation CD.

一般情况下是安装的stage3:

> Instructions on using a stage1 or stage2 tarball are now available in the [Gentoo FAQ](https://wiki.gentoo.org/wiki/Handbook:Main_Page). A stage3 installation is the only supported installation as of now.

[wikipedia](https://en.wikipedia.org/wiki/Gentoo_Linux#Stages)的解释:

Before October 2005, installation could be started from any of three base stages:

* Stage1 begins with only what is necessary to build a toolchain (various compilers, linkers, and libraries necessary to compile all other software) for the target system; this is known as bootstrapping the system.
* Stage2 begins with a bootstrapped system and requires the compilation of all other base system software.
* Stage3 begins with a partially configured (but not yet bootable) base system.

Since October 2005, only the stage3 installations have been officially supported. Tarballs for stage1 and stage2 were distributed for some time after this, although the instructions for installing from these stages had been removed from the handbook and moved into the Gentoo FAQ.

As of September 2015, only the supported stage3 tarballs are publicly available. However, if desired so, a user may rebuild the toolchain or reinstall the base system software after completing a stage3 installation.


参考:

* [Gentoo](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Media)
* [Wikipedia - Stage](https://en.wikipedia.org/wiki/Gentoo_Linux#Stages)
* [How do I install Gentoo using a stage1 or stage2 tarball?](https://wiki.gentoo.org/wiki/FAQ#How_do_I_install_Gentoo_using_a_stage1_or_stage2_tarball.3F)

---

### Portage ###

Portage是一个Python和Shell写的软件包管理系统, 维护了一个软件包树

> Portage is the official package management and distribution system for Gentoo.

> Portage, the package maintenance system which Gentoo uses, is written in Python, meaning the user can easily view and modify the source code.

只升级安装的软件包:

	$ emerge --update --ask @world

Portage will then search for newer version of the applications that are installed. However, it will only verify the versions for the applications that are explicitly installed (the applications listed in `/var/lib/portage/world`) - it does not thoroughly check their dependencies. To update the dependencies of those packages as well, add the --deep option:

	$ emerge --update --deep @world

主动安装的包列表在`/var/lib/portage/world`里

Portage的默认配置文件在 `/var/share/portage/config/make.globals`

每一个架构下都有一系列的profile, 不同的profile管理的系统配置不一样:

	$ eselect profile list
	Available profile symlink targets:
	  [1]   default/linux/amd64/13.0 *
	  [2]   default/linux/amd64/13.0/selinux
	  [3]   default/linux/amd64/13.0/desktop
	  [4]   default/linux/amd64/13.0/desktop/gnome
	  [5]   default/linux/amd64/13.0/desktop/gnome/systemd
	  [6]   default/linux/amd64/13.0/desktop/kde
	  [7]   default/linux/amd64/13.0/desktop/kde/systemd
	  [8]   default/linux/amd64/13.0/desktop/plasma
	  [9]   default/linux/amd64/13.0/desktop/plasma/systemd
	  [10]  default/linux/amd64/13.0/developer
	  [11]  default/linux/amd64/13.0/no-multilib
	  [12]  default/linux/amd64/13.0/systemd
	  [13]  default/linux/amd64/13.0/x32
	  [14]  hardened/linux/amd64
	  [15]  hardened/linux/amd64/selinux
	  [16]  hardened/linux/amd64/no-multilib
	  [17]  hardened/linux/amd64/no-multilib/selinux
	  [18]  hardened/linux/amd64/x32
	  [19]  hardened/linux/musl/amd64
	  [20]  hardened/linux/musl/amd64/x32
	  [21]  default/linux/uclibc/amd64
	  [22]  hardened/linux/uclibc/amd64

Profile管理了一些系统的配置, 见`/etc/portage/make.profile`, 指向的就是配置的profile目录

当需要修改Portage配置, 不建议直接修改系统的默认配置文件. 可以复制Gentoo提供的sample文件, 默认用户自定义的portage配置文件在`/etc/portage/make.conf`:

	cp /usr/share/portage/config/make.conf.example /etc/portage/make.conf  # copy and edit this file

`make.conf` 也可以是一个目录, 按alphabetical顺序读取里面的配置.

> As noted previously, Portage is configurable through many variables which should be defined in /etc/portage/make.conf or one of the subdirectories of /etc/portage/. Please refer to the make.conf and portage man pages for more and complete information:

这里好像有问题, 并不会读取/etc/portage/下子目录, 测试建立一个子目录, 配置GENTOO_MIRRORS, 但是并没有覆盖.

用户定制的配置:

`/etc/portage/`下，有几个文件负责不同的功能:

* `package.mask` which lists the packages that Portage should never try to install
* `package.unmask` which lists the packages Portage should be able to install even though the Gentoo developers highly discourage users from emerging them
* `package.accept_keywords` which lists the packages Portage should be able to install even though the package hasn't been found suitable for the system or architecture (yet)
* `package.use` which lists the USE flags to use for certain packages without having the entire system use those USE flags

这四个不一定必须是文件, 也可以是目录, 里面一个package一个文件, 这样便于管理维护.

`PORTDIR` 管理Portage Tree的路径, 默认是`/usr/portage`, 因为python包是一个分级的结构, 如python是`dev-lang/python`, portage树存储的也是这个结构, 如python相关的元信息以及ebuild都在/usr/portage/dev-lang/python/下

`PKGDIR` 管理预编译二进制(prebuilt binary)包的路径, 默认是`/usr/portage/packages`. 默认情况下python是源码安装管理的, 不过也支持二进制包的安装.

`DISTDIR` 控制程序源码包下载存放的地址, 默认是 `/usr/portage/distfiles`. 默认是wget下载下来后安装. 如果空间不是很缺的话，建议保留这个目录下的源码压缩包，比如有时新版本有问题，而老版本已经从portage树中移除，这个可以方便的直接通过源码压缩包安装回退到老版本.

Portage数据库(存储系统的状态, 如哪些包已经安装，哪些文件属于哪些包) 在 `/var/db/pkg`. 不建议动, 否则会悲剧.

Portage cache(修改时间, virtuals, 依赖关系等) 存在 `/var/cache/edb`. 这个文件是可以清理掉的, 不过也不大, 请不清理没意义.

`PORTAGE_TMPDIR`管理portage的临时文件, 默认是 `/var/tmp/`下. Portage编译时, 每个包一个目录, 在 `/var/tmp/portage/`下, 由`BUILD_PREFIX`控制.

如果软件包的配置文件升级, `CONFIG_PROTECT`用于设置需要保护的配置目录. 这时此目录下的配置文件不会被覆盖, 新的配置会存放在此目录. `CONFIG_PROTECT_MASK` 用于设置保护目录下不需要保护的子目录.

	$ ack PROTECT /etc/portage/make.conf
	# Minimal CONFIG_PROTECT
	CONFIG_PROTECT="/etc"
	CONFIG_PROTECT_MASK="/etc/env.d"

	# 或者使用 emerge
	$ emerge --info | ack 'PROTECT'
	CONFIG_PROTECT="/etc /usr/share/gnupg/qualified.txt /var/bind"
	CONFIG_PROTECT_MASK="/etc/ca-certificates.conf /etc/env.d /etc/gconf /etc/gentoo-release /etc/php/apache2-php5.6/ext-active/ /etc/php/cgi-php5.6/ext-active/ /etc/php/cli-php5.6/ext-active/ /etc/revdep-rebuild /etc/sandbox.d /etc/terminfo"

后面输出多一些, 暂时还不清楚是哪里插入的?

当需要的信息/数据在本地系统不存在(比如安装某个软件)时, Portage会通过网络下载相应的数据:

* `GENTOO_MIRRORS` 定义一系列的server, 用于下载源码包(distfiles)
* `PORTAGE_BINHOST` 指定二进制包的server

`/etc/portage/repos.conf`或者这个目录下的子文件, 用于配置Portage树更新(同步)的配置:

* `sync-type` 定义同步类型, 默认是通过`rsync`来同步更新Portage树
* `sync-uri` 定义从一个server来更新Portage树

`GENTOO_MIRRIOS`, `sync-type`, `sync-uri` 可以通过 `mirrorselect` 来自动获取

当Portage下载(fetch)源码包时, 默认的方式是`wget`. 可以通过修改`FETCHCOMMAND`来修改下载方式

当更新Portage树时, 可以定制 `rsync` 的选项. `PORTAGE_RSYNC_OPTS` 定义了默认的选项, 不建议修改. `PORTAGE_RSYNC_EXTRA_OPTS` 用户定义一些用户定制扩展的选项. `PORTAGE_RSYNC_RETRIES` 控制重试次数, 默认是3次.

Gentoo的分支(branch)是指相应架构的软件包分支, 包括稳定(stable)和测试(testing)分支. 通过`ACCEPT_KEYWORDS`来管理. 默认是稳定分支.

比如amd64架构下, 默认是:

	ACCEPT_KEYWORDS="amd64"

如果想全局改为使用测试分支，则在 架构名 前加上 `~`：

	# /etc/portage/make.conf
	ACCEPT_KEYWORDS="~amd64"

也可以在全局是稳定分支的情况下, 指定某些特定的包是测试分支. `/etc/portage/package.accept_keywords`文件或目录下添加指定包名:

	$ cat /etc/portage/package.accept_keywords
	#required by dev-db/mongodb (argument)
	=dev-db/mongodb-2.2.0-r1 ~amd64

一般被mask的软件包(`profiles/default/linux/amd64/package.use.mask`)是没法安装, 不过可以通过添加unmask来安装, 同上类似, 文件或目录是`/etc/portage/package.unmask`:

	$ more /etc/portage/package.unmask
	# required by @preserved-rebuild (argument)
	# /usr/portage/profiles/package.mask:
	# Hans de Graaff <graaff@gentoo.org> (11 Oct 2015)
	# Ruby 1.9 is no longer maintained upstream since January
	# 2015, bug 536852.
	# Masked for removal in 30 days.
	=dev-lang/ruby-1.9.3_p551-r1

同样也可以指定mask某个包:

	$ more /etc/portage/package.mask
	=dev-python/python-exec-10000.2

mask是除了keyword外额外的一个限制安装的功能，keyword针对的是架构，mask是针对的整个包。

参考:

* [Gentoo - Portage](https://wiki.gentoo.org/wiki/Portage)
* [Gentoo Handbook - Portage](https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Portage)
* [Gentoo Handbook - Installation](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/About)
* [Unmasking a package](https://wiki.gentoo.org/wiki/Knowledge_Base:Unmasking_a_package)
* man portage
* man make.conf

---

### Overlay and Layman ###

最初的需求是13年时，想安装一个包，但是Gentoo官方Portage中没有，于是了解到Overlay。

添加第三方的ebuilds, 以前总结过 [Gentoo Overlays and Layman](http://blog.tankywoo.com/gentoo/2013/09/18/gentoo-overlays-and-layman.html)

去年Gentoo官方Portage中移除了Python2.6，后来本地一个项目支持py2.6，为了单元测试，所以本地考虑装回Python2.6。

解决方案就是本地建立Local Overlay，手动维护一个个人的Portage。

> A local repository aka local overlay

**What Are Overlays?**

> "Overlays" are package trees for Portage. They contain additional ebuilds for Gentoo. They are maintained by Gentoo developers and projects but distributed separately from the main Portage tree.

From [Gentoo Overlays: Users' Guide](http://www.gentoo.org/proj/en/overlays/userguide.xml)


**Why call it Overlays?**

> Within Gentoo Linux, users already have one "main" package repository, called the Portage tree. This main repository contains all the software packages (called ebuilds) maintained by Gentoo developers. But users can add additional repositories to the tree that are "layed over" the main tree - hence the name, overlays.

From [Gentoo Wiki: Overlay](http://wiki.gentoo.org/wiki/Overlay)

操作比较简单(部分步骤直接copy的官方文档):

	# 官方portage放在/usr/portage下，这里个人的放在/usr/local/portage
	# 最基本的就是两个子目录 metadata, profiles
	$ mkdir -p /usr/local/portage/{metadata,profiles}
	# NameOfYourOverlay自定义，和下面repos.conf中的名称一致
	$ echo 'NameOfYourOverlay' > /usr/local/portage/profiles/repo_name
	$ echo 'masters = gentoo' > /usr/local/portage/metadata/layout.conf
	$ chown -R portage:portage /usr/local/portage

然后增加repos配置:

	$ more /etc/portage/repos.conf/*.conf
	# 这个是默认的官方portage配置
	::::::::::::::
	/etc/portage/repos.conf/gentoo.conf
	::::::::::::::
	[DEFAULT]
	main-repo = gentoo
	
	[gentoo]
	location = /usr/portage
	sync-type = rsync
	sync-uri = rsync://mirrors.163.com/gentoo-portage
	auto-sync = yes

	# 这个是个人的overlay
	::::::::::::::
	/etc/portage/repos.conf/local.conf
	::::::::::::::
	[NameOfYourOverlay]
	location = /usr/local/portage
	masters = gentoo
	auto-sync = no

`/etc/portage/make.conf`最下面添加 (**TODO**: 这块具体目的/用途还得再研究下):

	PORTDIR_OVERLAY='/usr/local/portage'

这样最基本的local overlay就搭建好了，接下来就是增加自己维护的ebuilds了。

ebuilds文件存放的目录结构，和官方portage保持一致，即`/usr/local/portage/<type>/<name>/`，目录里存放具体的ebuild `name-version.ebuild`等。

放置相关的ebuils和一些依赖文件后，就是签名生成清单了，如:

	# digest和manifest子命令等价, 前者已过时
	$ ebuild dev-lang/python/python-2.6.8.ebuild manifest
	>>> Creating Manifest for /usr/local/portage/dev-lang/python

或者文档里推荐:

	$ pushd /usr/local/portage/dev-lang/python
	$ repoman manifest
	$ popd

`ebuild`命令虽然指定了版本号的文件，但是实际会扫描这个ebuild所在目录，所有相关的文件(以及其它版本)都会写入Manifest文件。

目前我的local overlay目录结构如下:

	$ tree /usr/local/portage
	/usr/local/portage
	├── dev-lang
	│   └── python
	│       ├── files
	│       │   ├── pydoc.conf
	│       │   ├── pydoc.init
	│       │   └── python-2.5-tcl86.patch
	│       ├── Manifest
	│       ├── python-2.6.8.ebuild
	│       └── python-2.6.9.ebuild
	├── dev-python
	│   └── python-docs
	│       ├── Manifest
	│       ├── python-docs-2.6.8.ebuild
	│       └── python-docs-2.6.9.ebuild
	├── metadata
	│   └── layout.conf
	└── profiles
	    └── repo_name
	
	7 directories, 11 files

ebuild和tar包可以在官网源或其它可信站点里找，比如我在[这里](https://sources.gentoo.org/cgi-bin/viewvc.cgi/gentoo-x86/dev-lang/python/?hideattic=0)找的。

然后就可以`emerge`正常安装了。

*遇到的问题：*

在安装Python2.6.x时遇到一个问题，找的python-2.6.9和python2.6.8-r3的ebuild，发现在安装时又依赖python2.6的解释器，具体是ebuild编译时有如下的内容:

	...
	SLOT="2.6"
	...
	python_export python${SLOT} EPYTHON PYTHON PYTHON_SITEDIR

不确定为何python-2.6.9.ebuild会依赖这个，其它版本只在`-rX`的小版本会依赖，大版本(不带`-rX`)的不会依赖python2.6的解释器。具体可以看看我之前在Gentoo论坛的[提问](https://forums.gentoo.org/viewtopic-p-7867700.html#7867700)

还有一个问题就是python2.6.9的EAPI是2, 导致ebuild有些函数指定不了:

	die "python_do* and python_new* helpers are banned in EAPIs older than 4."

改为`EAPI="4"`即可。

参考:

* [Project:Overlays/User Guide](https://wiki.gentoo.org/wiki/Project:Overlays/User_Guide)
* [Overlay/Local overlay](https://wiki.gentoo.org/wiki/Overlay/Local_overlay)
* [Handbook - Adding unoffical ebuilds](https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Portage#Adding_unofficial_ebuilds)
* [初探 ebuild](https://segmentfault.com/a/1190000003819421) 总结的也挺不错的
* [Gentoo Portage](https://packages.gentoo.org/)
* [Gentoo Overlays](https://overlays.gentoo.org/)
* [Gentoo Layman](https://wiki.gentoo.org/wiki/Layman)

---

### world 和 @world ###

> @ indicates a package set. In portage-2.1 there are only @world and @system. In portage-2.2 there are more (emerge --list-sets). In both cases world and system are aliases for the correspnding sets, which means there is no difference. Other sets don't have such aliases.

参考:

* [@world versus world...what's the difference?](https://forums.gentoo.org/viewtopic-t-899878-start-0.html)
* [World set (Portage)](https://wiki.gentoo.org/wiki/World_set\_(Portage))

---

### world / system / selected ###

针对这个问题:

	Would you like to add these packages to your world favorites? [Yes/No]

参考:

* [World set](https://wiki.gentoo.org/wiki/World_set_(Portage))
* [System set](https://wiki.gentoo.org/wiki/System_set_(Portage))
* [Selected set](https://wiki.gentoo.org/wiki/System_set_(Portage))

里面介绍的已经非常详细了

---

### emerge ##

安装包后做基本配置, 如:

	emerge --config =dev-db/mariadb-10.0.23

---

### Eix ###

[eix](https://wiki.gentoo.org/wiki/Eix) 通过增加一个portage树本地索引库, 快速的查询软件包，比「emerge」方便了很多。

	# 搜索软件，用于替代emerge -S
	eix <package_name>

	# 更新portage树, 等价于 emerge --sync
	eix-sync

	# 更新本地索引库缓存, 否则有时更新了portage树, eix搜到的还是老的
	eix-update

---

### EAPI ###

关于EAPI的介绍:

* [EAPI Usage and Description](https://devmanual.gentoo.org/ebuild-writing/eapi/)
* [EAPI 用途及描述](https://www.gentoo.org.cn/devmanual/ebuild-writing/eapi/index.html) 上面的中文版, 只更新到EAPI5
* [EAPI](https://wiki.gentoo.org/wiki/EAPI)
* [初探 ebuild](https://segmentfault.com/a/1190000003819421)
* [ebuild文件阅读和撰写方法简介](http://tieba.baidu.com/p/2255141345?see_lz=1)

大致就是portage提供的一些现成的函数, 让编写ebuild的工作更简单。我估计EAPI应该是 Ebuild API 的简称(虽然官方没看到有这个说明。。。)

---

### SLOT ###

SLOT, 即「槽」, 和具体某个包相关的概念, 是Gentoo实现多版本共存的基础。

`0` 是默认的slot名, 表示没有使用slot;

slot名是空字符串表示彻底禁止使用slot;

带有slot的包, 包名后面会有`:`冒号分隔, 并带上slot, 如:

	dev-python/dnspython-1.12.0-r200:py2
	dev-python/dnspython-1.12.0-r300:py3

表示dnspython这个包分别有py2和py3两个slot。

相关的一些命令:

`eix` 可以直接查看包的所有slot:

	$ eix dnspython
	* dev-python/dnspython
		 Available versions:
		 (py2)  1.12.0-r200
		 (py3)  1.12.0-r300
		   {examples test PYTHON_TARGETS="python2_7 python3_3 python3_4"}
		 Homepage:            http://www.dnspython.org/ https://pypi.python.org/pypi/dnspython
		 Description:         DNS toolkit for Python

`equery list -p`:

	$ equery l -po dnspython
	 * Searching for dnspython ...
	[-P-] [  ] dev-python/dnspython-1.12.0-r200:py2
	[-P-] [  ] dev-python/dnspython-1.12.0-r300:py3
	[-P-] [ ~] dev-python/dnspython-1.12.0-r301:py3

`equery keywords`:

	$ equery keywords dnspython
	Keywords for dev-python/dnspython:
				|                                 | u     |
				| a a   a         n   p r     s   | n     |
				| l m   r h i m m i   p i s   p   | u s   | r
				| p d a m p a 6 i o p c s 3   a x | s l   | e
				| h 6 r 6 p 6 8 p s p 6 c 9 s r 8 | e o   | p
				| a 4 m 4 a 4 k s 2 c 4 v 0 h c 6 | d t   | o
	------------+---------------------------------+-------+-------
	1.12.0-r200 | + + + ~ + + o o o + + o ~ ~ + + | o py2 | gentoo
	------------+---------------------------------+-------+-------
	1.12.0-r300 | + + + ~ + + o o o + + o ~ ~ + + | o py3 | gentoo
	1.12.0-r301 | ~ ~ ~ ~ ~ ~ o o o ~ ~ o ~ ~ ~ ~ | o     | gentoo

参考:

* [Slotting](https://devmanual.gentoo.org/general-concepts/slotting/)
* [Sub-slots and Slot-Operators](https://wiki.gentoo.org/wiki/Sub-slots_and_Slot-Operators)
* [List *ALL* Slot for a Given Package](https://forums.gentoo.org/viewtopic-t-824052-start-0.html)


### Hardened Gentoo ###

参考:

* 加固的Gentoo [en](https://wiki.gentoo.org/wiki/Hardened_Gentoo) / [zh](https://wiki.gentoo.org/wiki/Hardened_Gentoo/zh-cn)

### Preserved libs ###

比如手动更新masked的czmq，导致需要rebuild：

	!!! existing preserved libs:
	>>> package: net-libs/zeromq-4.1.4
	 *  - /usr/lib64/libzmq.so.3
	 *  - /usr/lib64/libzmq.so.3.0.0
	 *      used by /usr/bin/makecert-czmq (net-libs/czmq-3.0.2)
	 *      used by /usr/lib64/libczmq.so.3.0.0 (net-libs/czmq-3.0.2)
	 *      used by /usr/lib64/rsyslog/imzmq3.so (app-admin/rsyslog-8.16.0-r1)
	 *      used by /usr/lib64/rsyslog/omzmq3.so (app-admin/rsyslog-8.16.0-r1)
	>>> package: net-libs/czmq-3.0.2
	 *  - /usr/lib64/libczmq.so.1
	 *  - /usr/lib64/libczmq.so.1.1.0
	 *      used by /usr/lib64/rsyslog/imzmq3.so (app-admin/rsyslog-8.16.0-r1)
	 *      used by /usr/lib64/rsyslog/omzmq3.so (app-admin/rsyslog-8.16.0-r1)
	Use emerge @preserved-rebuild to rebuild packages using these libraries

可以rebuild依赖这个的包：

root@gentoo-local ~ % emerge -p @preserved-rebuild

	These are the packages that would be merged, in order:

	Calculating dependencies... done!
	[ebuild   R   ~] net-libs/czmq-3.0.2
	[ebuild   R    ] app-admin/rsyslog-8.16.0-r1

参考：[preserve-libs](https://wiki.gentoo.org/wiki/Preserve-libs)


## 问题 ##

### Gentoo grub升级到grub2 ###

world file: `/var/lib/portage/world`

example:

	2013-10-14-grub2-migration
	  Title                     GRUB2 migration

	A newer version of GRUB (sys-boot/grub) is now stable. There are now
	two available slots:

	sys-boot/grub:0 - Known as "GRUB Legacy"
	sys-boot/grub:2 - Known as "GRUB2"

	GRUB2 uses a different configuration format, and requires a manual
	migration before your system will actually use it. A guide [1] is
	available on the gentoo.org website, and the Gentoo wiki [2][3] has
	additional information.

	If you would prefer not to migrate at this time, you do not need to
	take any action: GRUB Legacy will remain functional in /boot. To
	prevent any associated files (documentation) from being removed, add
	sys-boot/grub:0 to your world file. For example:

	emerge --noreplace sys-boot/grub:0

	References:

	[1] http://www.gentoo.org/doc/en/grub2-migration.xml
	[2] https://wiki.gentoo.org/wiki/GRUB2_Quick_Start
	[3] https://wiki.gentoo.org/wiki/GRUB2

### Gentoo 升级相关 ###

更新portage树

    $ emerge --sync 或者 eix-sync

更新eix缓存:

	$ sudo eix-update
	Reading Portage settings ..
	Building database (/var/cache/eix/portage.eix) ..
	[0] "gentoo" /usr/portage/ (cache: metadata-md5-or-flat)
		 Reading category 161|161 (100%) Finished
	Applying masks ..
	Calculating hash tables ..
	Writing database file /var/cache/eix/portage.eix ..
	Database contains 18239 packages in 161 categories.

升级python/portage

    $ sudo emerge -auv python portage

升级完python后:

> python-updater -- Find & rebuild packages broken due to a Python upgrade

	$ python-updater -p -v
	 * Starting Python Updater...
	 * Main active version of Python:    2.7
	 * Active version of Python 2:       2.7
	 * Active version of Python 3:       3.3
	 * Globally supported Python ABIs in installed repositories:
	 *   gentoo:                         2.4 2.5 2.6 2.7 3.1 3.2 3.3 2.5-jython 2.7-jython 2.7-pypy-1.7 2.7-pypy-1.8 2.7-pypy-1.9 2.7-pypy-2.0
	 * Check "manual" enabled.
	 * Check "need_rebuild" enabled.
	 * Check "pylibdir" enabled.
	 * Check "PYTHON_ABIS" enabled.
	 * Check "shared_linking" enabled.
	 * Check "static_linking" enabled.
	 *   Adding to list: app-admin/webapp-config:0
	 *     check: PYTHON_ABIS [ Previous Python ABIs: 2.7, new Python ABIs: 2.7 3.3 ]
	 *   Adding to list: app-portage/gentoolkit:0
	 *     check: PYTHON_ABIS [ Previous Python ABIs: 2.7 3.2, new Python ABIs: 2.7 3.3 ]
	...
	*   Adding to list: www-servers/tornado:0
	 *     check: PYTHON_ABIS [ Previous Python ABIs: 2.7 3.2, new Python ABIs: 2.7 3.3 ]
	 *   Adding to list: www-servers/uwsgi:0
	 *     check: PYTHON_ABIS [ Previous Python ABIs: 2.7 3.2, new Python ABIs: 2.7 3.3 ]
	 * emerge -Dv1 --keep-going -p app-admin/webapp-config:0 app-portage/gentoolkit:0 dev-python/bpython:0 dev-python/chardet:0 dev-python/feedparser:0 dev-python/html2text:0 dev-python/ipy:0 dev-python/pep8:0 dev-python/pyflakes:0 dev-python/pymongo:0 dev-python/pysqlite:2 dev-python/virtualenv:0 dev-util/scons:0 dev-vcs/subversion:0 net-analyzer/rrdtool:0 net-dns/bind:0 net-misc/dropbox:0 sys-libs/libcap-ng:0 www-servers/tornado:0 www-servers/uwsgi:0

	These are the packages that would be merged, in order:

	Calculating dependencies... done!

	emerge: there are no ebuilds to satisfy "dev-python/pysqlite:2".

	 * IMPORTANT: 19 news items need reading for repository 'gentoo'.
	 * Use eselect news read to view new items.

清除孤立的包, 需要在升级系统之后, 否则报错:

	 * Have you forgotten to do a complete update prior to depclean? The
	 * most comprehensive command for this purpose is as follows:
	 *
	 *   emerge --update --newuse --deep --with-bdeps=y @world
	 *
	 * Note that the --with-bdeps=y option is not required in many
	 * situations. Refer to the emerge manual page (run `man emerge`)
	 * for more information about --with-bdeps.

    $ emerge -avuDN @world

清除不需要(孤立)的包:

    $ emerge -av --depclean

检查系统包的依赖关系是否都ok:

    $ revdep-rebuild

更新系统配置文件:

    $ dispatch-conf

参考:

* [Gentoo系统全面升级记录](http://blog.chinaunix.net/uid-8874157-id-3763893.html)
* [Optimal procedure to upgrade Gentoo Linux?](http://serverfault.com/questions/9936/optimal-procedure-to-upgrade-gentoo-linux)
* [Gentoo Cheat Sheet](https://wiki.gentoo.org/wiki/Gentoo_Cheat_Sheet)
* [sys-apps/portage-2.2.16 发布，支持多种同步方式](http://www.gentoo-cn.info/article/new-portage-plug-in-sync-system/)
* [Portage/Sync](https://wiki.gentoo.org/wiki/Project:Portage/Sync)
* [升级GCC](https://wiki.gentoo.org/wiki/Upgrading_GCC/zh-cn)
* [内核/升级](https://wiki.gentoo.org/wiki/Kernel/Upgrade/zh-cn)


### 升级后更新系统配置文件 ###

初试, 所以了解的不是很全.

一般`emerge --sync`或者`eix-sync`更新portage树后, 会有这种提示:

    * IMPORTANT: 9 config files in '/etc' need updating.
    * See the CONFIGURATION FILES section of the emerge
    * man page to learn how to update config files.

    * IMPORTANT: 18 news items need reading for repository 'gentoo'.
    * Use eselect news read to view new items.

提示已经很清楚了, 看`man emerge`的`CONFIGURATION FILES`一节.

根据`CONFIG_PROTECT`的配置, 默认比如`/etc/`下的配置文件, 当软件更新时, 相应的配置是不会覆盖当前的, 而在本地生成一个`._cfg000_*`的文件, 为更新后的默认配置.

通过`dispatch-conf`可以来处理这些情况, 可以丢弃新的配置文件, 或者合并两者等等.

参考: [Portage附加工具](https://gentoo-handbook.lugons.org/doc/zh_cn/handbook/handbook-arm.xml?part=3&chap=4)

### dependency graph slot conflict ###

如下:

    $ emerge -auv dev-python/pygments

    These are the packages that would be merged, in order:

    Calculating dependencies... done!
    ...

    Total: 4 packages (2 upgrades, 2 new), Size of downloads: 4,387 KiB

    !!! Multiple package instances within a single package slot have been pulled
    !!! into the dependency graph, resulting in a slot conflict:

    dev-python/setuptools:0

      (dev-python/setuptools-18.4:0/0::gentoo, ebuild scheduled for merge) pulled in by         # <--- 依赖新版本
    ...
    target_pypy(-),-python_single_target_pypy3(-)] required by (dev-python/pygments-2.0.2-r1:0/0::gentoo, ebuild scheduled for merge)

    ...
    target_pypy(-),-python_single_target_pypy3(-)] required by (dev-python/certifi-2015.9.6.2:0/0::gentoo, ebuild scheduled for merge)


      (dev-python/setuptools-2.2:0/0::gentoo, installed) pulled in by                           # <--- 依赖老版本
    ...
    _python3_3(-),-python_single_target_pypy(-)] required by (dev-python/pip-1.4.1:0/0::gentoo, installed)

    ...
    _python3_3(-),-python_single_target_python3_4(-),-python_single_target_pypy(-)] required by (dev-python/logilab-common-0.61.0:0/0::gentoo, installed)

    ...
    python_single_target_python3_3(-),-python_single_target_python3_4(-),-python_single_target_pypy(-)] required by (dev-python/meld3-1.0.0:0/0::gentoo, installed)

解决:

把老的版本以及相应依赖同时升级:

    $ emerge -avu dev-python/setuptools dev-python/pip dev-python/logilab-common dev-python/pygments

参考: [Gentoo - Troubleshooting](https://wiki.gentoo.org/wiki/Troubleshooting#Dependency_graph_slot_conflicts)

### Perl相关 ###

好像perl-core和virtual/xxx合并了, 很多perl的依赖, 可以执行`perl-cleaner -v --modules`重新编译一些较老的库.

期间会遇到一些提示, 说明卡在哪, 处理掉相应的包, 然后重新执行perl-cleaner.

都是一些perl-core的包, 安装相应的virtual/perl-xxx包, 然后`emerge -C`清理掉这些包, 直到perl-cleaner可以执行.

    $ emerge --depclean -pv
    ...
    Calculating dependencies... done!
     * Dependencies could not be completely resolved due to
     * the following required packages not being installed:
     *
     *   dev-lang/perl:0/0=[-build(-)] pulled in by:
     *     dev-perl/Net-SMTP-SSL-1.10.0-r1
     *
     *   dev-lang/perl:0/0=[-build(-)] pulled in by:
     *     dev-perl/PlRPC-0.202.0-r2
     *
     *   dev-haskell/old-locale:= pulled in by:
     *     dev-haskell/data-default-instances-old-locale-0.0.1
     *
     *   sys-block/thin-provisioning-tools pulled in by:
     *     sys-fs/lvm2-2.02.97-r1
     *
    ...
     *   dev-lang/perl[-build] pulled in by:
     *     dev-perl/Locale-gettext-1.50.0
     *
     *   dev-lang/perl:0/0=[-build(-)] pulled in by:
     *     dev-perl/Authen-SASL-2.160.0-r1
    ...

    $ perl-cleaner -v --modules

参考: [gentoo forums](https://forums.gentoo.org/viewtopic-t-987896.html)

### 编译报错 ###

升级pip/lxml时遇到编译报错.

    >>> Failed to emerge dev-python/lxml-3.4.4, Log file:

    >>>  '/var/tmp/portage/dev-python/lxml-3.4.4/temp/build.log'

     * Messages for package dev-python/lxml-3.4.4:

     * ERROR: dev-python/lxml-3.4.4::gentoo failed (compile phase):
     *   (no error message)
     *
     * Call stack:
     *     ebuild.sh, line   93:  Called src_compile
     *   environment, line 3878:  Called distutils-r1_src_compile
     *   environment, line 1036:  Called _distutils-r1_run_foreach_impl 'python_compile'
     *   environment, line  315:  Called python_foreach_impl 'distutils-r1_run_phase' 'python_compile'
     *   environment, line 3339:  Called multibuild_foreach_variant '_python_multibuild_wrapper' 'distutils-r1_run_phase' 'python_compile'
     *   environment, line 2447:  Called _multibuild_run '_python_multibuild_wrapper' 'distutils-r1_run_phase' 'python_compile'
     *   environment, line 2445:  Called _python_multibuild_wrapper 'distutils-r1_run_phase' 'python_compile'
     *   environment, line  635:  Called distutils-r1_run_phase 'python_compile'
     *   environment, line 1029:  Called python_compile
     *   environment, line 2947:  Called distutils-r1_python_compile
     *   environment, line  908:  Called esetup.py 'build'
     *   environment, line 1518:  Called die
     * The specific snippet of code:
     *       "${@}" || die
     *
     * If you need support, post the output of `emerge --info '=dev-python/lxml-3.4.4::gentoo'`,
     * the complete build log and the output of `emerge -pqv '=dev-python/lxml-3.4.4::gentoo'`.
     * The complete build log is located at '/var/tmp/portage/dev-python/lxml-3.4.4/temp/build.log'.
     * The ebuild environment file is located at '/var/tmp/portage/dev-python/lxml-3.4.4/temp/environment'.
     * Working directory: '/var/tmp/portage/dev-python/lxml-3.4.4/work/lxml-3.4.4-python2_7'
     * S: '/var/tmp/portage/dev-python/lxml-3.4.4/work/lxml-3.4.4'

可以选择直接删掉或者`emerge -C`先清理掉这些包, 然后重新安装.

    rm -r /usr/lib64/python2.7/site-packages/pip*

参考: [dev-python/pip fail to emerge](https://forums.gentoo.org/viewtopic-p-7842512.html?sid=933da6a4a2d0e85f87614965a7e3d34d)

### dev-python/python-exec 问题 ###

有bug被移除的是`dev-python/python-exec`, 保留的是`dev-lang/python-exec`.

注意清理时不要把`dev-lang/python-exec`给卸载了, 否则emerge就用不了了.

首先查看`dev-python/python-exec`的依赖有哪些, 逐步清理, 该升级的升级, 该移除的移除

    emerge --verbose --depclean =dev-python/python-exec-10000.1

升级相应的包

    emerge --oneshot <packages used python-exec>

或者移除

    emerge -C <packages used python-exec>

直到可以清理`emerge --verbose --depclean =dev-python/python-exec-10000.1`

参考: [masking & removal of dev-python/python.exec-10000.1](https://forums.gentoo.org/viewtopic-p-7512702.html)

    $ emerge --verbose --depclean "=dev-python/python-exec-10000.1"

    Calculating dependencies... done!
      dev-python/python-exec-10000.1 pulled in by:
        app-portage/layman-2.0.0 requires dev-python/python-exec:0/0=[python_targets_python2_7(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-),-python_single_target_pypy2_0(-)]
        dev-python/beautifulsoup-4.1.3-r1 requires dev-python/python-exec[python_targets_python2_7(-),python_targets_python3_2(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-),-python_single_target_python3_1(-),-python_single_target_python3_2(-),-python_single_target_python3_3(-)]
        dev-python/imaging-1.1.7-r2 requires dev-python/python-exec[python_targets_python2_7(-),-python_single_target_python2_5(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-)]
        dev-python/lxml-3.0.1 requires dev-python/python-exec[python_targets_python2_7(-),python_targets_python3_2(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-),-python_single_target_python3_1(-),-python_single_target_python3_2(-),-python_single_target_python3_3(-)]
        dev-python/markdown-2.2.1-r1 requires dev-python/python-exec[python_targets_python2_7(-),python_targets_python3_2(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-),-python_single_target_python3_1(-),-python_single_target_python3_2(-),-python_single_target_pypy1_9(-),-python_single_target_pypy2_0(-)]
        dev-python/markdown2-2.1.0-r1 requires dev-python/python-exec[python_targets_python2_7(-),-python_single_target_python2_5(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-),-python_single_target_pypy1_9(-),-python_single_target_pypy2_0(-)]
        dev-python/psycopg-2.4.6-r1 requires dev-python/python-exec[python_targets_python2_7(-),python_targets_python3_2(-),-python_single_target_python2_5(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-),-python_single_target_python3_1(-),-python_single_target_python3_2(-)]
        virtual/python-argparse-1 requires dev-python/python-exec[python_targets_python2_7(-),python_targets_python3_2(-),-python_single_target_python2_5(-),-python_single_target_python2_6(-),-python_single_target_python2_7(-),-python_single_target_python3_1(-),-python_single_target_python3_2(-),-python_single_target_python3_3(-),-python_single_tar
    get_pypy1_9(-),-python_single_target_pypy2_0(-)]

    >>> No packages selected for removal by depclean
    Packages installed:   612
    Packages in world:    189
    Packages in system:   44
    Required packages:    612
    Number removed:       0

    $ emerge --verbose --depclean "=dev-python/python-exec-10000.1"

    Calculating dependencies... done!
    >>> Calculating removal order...

     dev-python/python-exec
        selected: 10000.1
       protected: none
         omitted: 10000.2

    All selected packages: =dev-python/python-exec-10000.1

    >>> 'Selected' packages are slated for removal.
    >>> 'Protected' and 'omitted' packages will not be removed.

    >>> Waiting 5 seconds before starting...
    >>> (Control-C to abort)...
    >>> Unmerging in: 5 4 3 2 1
    >>> Unmerging (1 of 1) dev-python/python-exec-10000.1...
    ...

有些甚至可能是已经被移除的, 都可以清理掉, 如遇到的这个:

    (dev-db/sqlite-3.8.10.2:3/3::gentoo, ebuild scheduled for merge) conflicts with
      >=dev-db/sqlite-3.3.8:3[extensions] required by (dev-lang/python-3.2.3-r2:3.2/3.2::gentoo, installed)
                              ^^^^^^^^^^
      >=dev-db/sqlite-3.3.8:3[extensions] required by (dev-python/pysqlite-2.6.3:2/2::gentoo, installed)
                            ^^^^^^^^^^

其中dev-lang/python-3.2.3-r2已经从portage中移除了, 所以可以先检查没有依赖就删掉`emerge --verbose --depclean "=dev-lang/python-3.2.3-r2"`

### 卸载python2.6 ###

python2.6在gentoo下已经从portage中移除.

    $ emerge -av @preserved-rebuild

     * IMPORTANT: 18 news items need reading for repository 'gentoo'.
     * Use eselect news read to view new items.


     * IMPORTANT: 4 config files in '/etc/portage' need updating.
     * See the CONFIGURATION FILES section of the emerge
     * man page to learn how to update config files.

    These are the packages that would be merged, in order:

    Calculating dependencies... done!

    emerge: there are no ebuilds to satisfy "dev-lang/python:2.6".
    (dependency required by "@preserved-rebuild" [argument])

同上面, 清理掉:

    emerge --verbose --depclean "=dev-lang/python2.6.8-r1"

具体版本号可以通过`emerge -c -pv "dev-lang/python"`看到.

### gcc 升级 ###

gcc升级后, 如果老版本被卸载, 需要运行`gcc-config`配置到新的版本.

    # 查看当前配置的版本的profile, 此处因为老的被卸载, 所以报错
    # 并且也显示了可配置的列表
    $ gcc-config -c
     * gcc-config: Active gcc profile is invalid!

     [1] x86_64-pc-linux-gnu-4.9.3

    # 查看可选的版本的profile, 此处因为老的被卸载, 所以报错
    $ gcc-config -l
     * gcc-config: Active gcc profile is invalid!

     [1] x86_64-pc-linux-gnu-4.9.3

    # 配置到相应版本
    $ gcc-config x86_64-pc-linux-gnu-4.9.3
     * Switching native-compiler to x86_64-pc-linux-gnu-4.9.3 ...
    >>> Regenerating /etc/ld.so.cache...                                                                                                                                   [ ok ]

     * If you intend to use the gcc from the new profile in an already
     * running shell, please remember to do:

     *   . /etc/profile

    $ gcc-config -c
    x86_64-pc-linux-gnu-4.9.3


### 卸载X11相关 ##A

还未操作, 先记录:  [How to remove X11](https://forums.gentoo.org/viewtopic-p-6667611.html)


### 清理 /usr/portage/{distfiles,packages} ###

默认情况下, 源文件在`/usr/portage/distfiles`目录, 二进制文件在`/usr/portage/packages`. 这些都可以删除.

不过保留下来以后可以方便的降级.

使用`eclean`命令可以方便的删除过时/废弃的文件. 而保留有用的.

	$ eclean [global-option] ... <action> [action-option] ...
	$ eclean-dist [global-option, distfiles-option] ...
	$ eclean-pkg [global-option, packages-option] ...

`eclean distfiles`等价于`eclean-dist`

参考:

* [Gentoolkit](https://wiki.gentoo.org/wiki/Gentoolkit)
* [eclean](https://wiki.gentoo.org/wiki/Eclean)
* [Gentoo FAQ: Source tarballs are collecting in /usr/portage/distfiles/. Is it safe to delete these files?](https://wiki.gentoo.org/wiki/FAQ#Source_tarballs_are_collecting_in_.2Fusr.2Fportage.2Fdistfiles.2F._Is_it_safe_to_delete_these_files.3F)

### 磁盘分区限制 ###

摘自[Gentoo Handbook - Installation](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks)

> Each partition is limited to 2 TB in size (due to the 32-bit identifiers). Also, the MBR setup does not provide any backup-MBR, so if an application or user overwrites the MBR, all partition information is lost.

> For completeness, the BIOS boot partition is needed when GPT partition layout is used with GRUB2, or when the MBR partition layout is used with GRUB2 when the first partition starts earlier than the 1 MB location on the disk.

之前一直弄错了, 以为mbr分区最大的磁盘限制是2T, 应该是分区限制是2T.


### Gentoo下Perl的一些问题 ###

> 插播一句, 最近被这个问题折腾的蛋疼, 然后看到某个Github Issues上有人评价了一句: Perl in Gentoo is the pain in the ass.

最近一个新的Gentoo系统, Perl刚从5.18升级到5.20。但是执行 `perl-cleaner --all` 失败。

首先一个是 `app-text/po4a` 这个玩意, 忘了是哪里需要, 但是后面的依赖很多, 有些是不能删的, 看这玩意碍事, 就`-C`不管依赖强制删除了。

另外一个是 `virtual/perl-CPAN-Meta`, 这个在执行时总是让perl升级到5.22, 而5.22又是非稳定版。后来我看了下portage文件:

	$ cat /usr/portage/virtual/perl-CPAN-Meta/perl-CPAN-Meta-2.150.1.ebuild

	DESCRIPTION="Virtual for ${PN#perl-}"

	RDEPEND="
			|| ( =dev-lang/perl-5.22* ~perl-core/${PN#perl-}-${PV} )
			>=virtual/perl-CPAN-Meta-YAML-0.11.0
			>=virtual/perl-JSON-PP-2.271.30
			>=virtual/perl-Parse-CPAN-Meta-1.441.400
	"

根据RDEPEND的意思, 我查了下相关文档:

* [Dependencies](https://devmanual.gentoo.org/general-concepts/dependencies/)
* [Quickstart Ebuild Guide](https://devmanual.gentoo.org/quickstart/)

RDEPEND就是运行时依赖, 第一行依赖的意思就是这是一个 **或** 的关系, 要么存在 `=dev-lang/perl-5.22*` (前面的等号是强制的), 要么存在 `perl-core/CPAN-Meta-${PV}`, 即相同版本.

而`2.143.240`这个版本两者都有, 虽然是masked, 但是只需要perl-5.20, 所以我先unmask, 然后安装:

	emerge -auv '=virtual/perl-CPAN-Meta-2.143.240' '=perl-core/CPAN-Meta-2.143.240'

然后就可以再升级到最新版本:

	emerge -auv perl-core/CPAN-Meta virtual/perl-CPAN-Meta

(才发现前面有一个perl的问题了... [链接](/linux/gentoo.html#perl))


### masked by EAPI ###

eix看本地git最新稳定版是2.7.3, 但是默认不给安装, 强制指定版本后报:

	$ emerge -auv '=dev-vcs/git-2.7.3-r1'

	These are the packages that would be merged, in order:

	Calculating dependencies... done!

	!!! All ebuilds that could satisfy "=dev-vcs/git-2.7.3-r1" have been masked.
	!!! One of the following masked packages is required to complete your request:
	- dev-vcs/git-2.7.3-r1::gentoo (masked by: EAPI 6)

	The current version of portage supports EAPI '5'. You must upgrade to a
	newer version of portage before EAPI masked packages can be installed.
	For more information, see the MASKED PACKAGES section in the emerge
	man page or refer to the Gentoo Handbook.

提示很清楚了, 当前的portage版本不支持EAPI6。更新 `sys-apps/portage` 软件即可。


### hard blocking ###

更新samba时遇到的阻塞问题:

	[ebuild     U  ] net-fs/samba-4.2.9::gentoo [3.6.25::gentoo] ...
	[blocks B      ] <net-fs/samba-4.1.7 ("<net-fs/samba-4.1.7" is hard blocking sys-libs/ntdb-1.0-r1)

关于ntdb的ebuild内容:

	DEPEND="!!<net-fs/samba-4.1.7
			${RDEPEND}
			${PYTHON_DEPS}
			app-text/docbook-xml-dtd:4.2"

`!!`表示hard block, 需要用户自己来处理这个关系; 这里表示安装ntdb前samba必须>=4.1.7版本.(参考[dependencies](https://devmanual.gentoo.org/general-concepts/dependencies/))

目前的解决办法就是先卸载掉samba-3.x, 再直接安装samba-4.x (参考[samba hard blocking ntdb](https://forums.gentoo.org/viewtopic-p-7639846.html))


### 内核升级 ###

* [Kernel/Upgrade](https://wiki.gentoo.org/wiki/Kernel/Upgrade)
* [Kernel/Configuration](https://wiki.gentoo.org/wiki/Kernel/Configuration#Build)
* [Kernel/Removal](https://wiki.gentoo.org/wiki/Kernel/Removal)

基于旧的`.config`文件, 转为适应新内核选项的配置文件:

	# 选择新的内核
	# 其实是修改/usr/src/linux的符号链接
	$ eselect kernel set xxx

	# 把当前运行的(老内核)的配置放到新内核源码文件目录下
	$ zcat /proc/config.gz > /usr/src/linux/.config

	# 将旧的内核配置转为新的内核配置
	$ cd /usr/src/linux
	$ make olddefconfig

然后就是编译内核和initramfs了。


### 禁用新网卡命名方式 ###

Gentoo采用新网卡命名方式(应该是从udev-197下一个版本开始)，称为 [Predictable Network Interface Names](https://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/)。

具体的命名规则没去看，基本就是各种enp0s5, enp5s0, ens32等等方式。

这个新方式是可以禁用的。

最可靠的方式就是内核启动选项加上：

	net.ifnames=0

还可以通过udev rules来禁用。

udev-208之前是增加软链接`/etc/udev/rules.d/80-net-name-slot.rules`，指向`/dev/null`；udev-208之后是增加软链接 `/etc/udev/rules.d/80-net-setup-link.rules`，指向 `/dev/null`

参考：

* [Udev/Upgrade Guide](https://wiki.gentoo.org/wiki/Udev/Upgrade_Guide)
* [Upgrading udev to version >=200](https://www.gentoo.org/support/news-items/2013-03-29-udev-upgrade.html)


## 其它资源 ##

* [emerge 中文手册](http://www.jinbuguo.com/gentoo/emerge.html)
* [gentoo 日常维护命令备忘](https://javran.wordpress.com/2011/02/18/gentoo-commands/)
* [Gentoo Quick Guide](http://www.tamabc.com/article/60785.html)
* [Gentoo Troubleshooting](https://wiki.gentoo.org/wiki/Troubleshooting)
* [Portage入门](https://gentoo-handbook.lugons.org/doc/zh_cn/handbook/handbook-x86.xml?part=2&chap=1&style=printable)
* [Equery](https://wiki.gentoo.org/wiki/Equery)
* [Gentoo Cheat Sheet](https://wiki.gentoo.org/wiki/Gentoo_Cheat_Sheet)
