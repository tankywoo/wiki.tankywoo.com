---
title: "Gentoo"
date: 2014-08-30 16:29
updated: 2015-12-27 12:23
---

[TOC]

![Gentoo Logo](https://1b9a50f4f9de4348cd9f-e703bc50ba0aa66772a874f8c7698be7.ssl.cf5.rackcdn.com/site-logo.svg)

* [Gentoo官网](https://www.gentoo.org/)
* [Gentoo Handbook](https://wiki.gentoo.org/wiki/Handbook:Main_Page)

## Architecture ##

[Handbook-MainPage](https://wiki.gentoo.org/wiki/Handbook:Main_Page) 介绍了什么是架构:

> An architecture is a family of CPUs (processors) who support the same instructions. The two most prominent architectures in the desktop world are the x86 architecture and the x86_64 architecture (for which Gentoo uses the amd64 notation). But many other architectures exist, such as sparc, ppc (the PowerPC family), mips, arm, etc...
> 
> A distribution as versatile as Gentoo supports many architectures. For that reason, you'll find that our Gentoo Handbooks are offered for many of the supported architectures. However, that might lead to some confusion as not all users are aware of the differences. Some are only aware of the CPU type or name that their system is a part of (like i686 or Intel Core i7). Below you will find a quick summary of the supported architectures and the abbreviation used in Gentoo. However, most people that do not know the architecture of their system are mostly interested in x86 or amd64.

---

## Stage ##

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

## Portage ##

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

添加第三方的ebuilds, 以前总结过 [Gentoo Overlays and Layman](http://blog.tankywoo.com/gentoo/2013/09/18/gentoo-overlays-and-layman.html)

参考:

* [Gentoo - Portage](https://wiki.gentoo.org/wiki/Portage)
* [Gentoo Handbook - Portage](https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Portage)
* [Gentoo Handbook - Installation](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/About)
* man portage
* man make.conf

## Gentoo grub升级到grub2 ##

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

## Gentoo 升级相关 ##

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


## world 和 @world ##

> @ indicates a package set. In portage-2.1 there are only @world and @system. In portage-2.2 there are more (emerge --list-sets). In both cases world and system are aliases for the correspnding sets, which means there is no difference. Other sets don't have such aliases.

参考:

* [@world versus world...what's the difference?](https://forums.gentoo.org/viewtopic-t-899878-start-0.html)
* [World set (Portage)](https://wiki.gentoo.org/wiki/World_set\_(Portage))

## 升级后更新系统配置文件 ##

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

## dependency graph slot conflict ##

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

## Perl相关 ##

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

## 编译报错 ##

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

## dev-python/python-exec 问题 ##

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

## 卸载python2.6 ##

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

## gcc 升级 ##

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


## 卸载X11相关 ##

还未操作, 先记录:  [How to remove X11](https://forums.gentoo.org/viewtopic-p-6667611.html)


## 清理 /usr/portage/{distfiles,packages} ##

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

## 磁盘分区限制 ##

摘自[Gentoo Handbook - Installation](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks)

> Each partition is limited to 2 TB in size (due to the 32-bit identifiers). Also, the MBR setup does not provide any backup-MBR, so if an application or user overwrites the MBR, all partition information is lost.

> For completeness, the BIOS boot partition is needed when GPT partition layout is used with GRUB2, or when the MBR partition layout is used with GRUB2 when the first partition starts earlier than the 1 MB location on the disk.

之前一直弄错了, 以为mbr分区最大的磁盘限制是2T, 应该是分区限制是2T.


## 其它资源 ##

* [emerge 中文手册](http://www.jinbuguo.com/gentoo/emerge.html)
* [gentoo 日常维护命令备忘](https://javran.wordpress.com/2011/02/18/gentoo-commands/)
* [Gentoo Quick Guide](http://www.tamabc.com/article/60785.html)
* [Gentoo Troubleshooting](https://wiki.gentoo.org/wiki/Troubleshooting)
* [Portage入门](https://gentoo-handbook.lugons.org/doc/zh_cn/handbook/handbook-x86.xml?part=2&chap=1&style=printable)
