---
title: "Gentoo"
date: 2014-08-30 16:29
---

[TOC]

## gentoo grub升级了 ##

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
