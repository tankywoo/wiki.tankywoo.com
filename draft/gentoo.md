---
title: "Gentoo"
date: 2014-08-30 16:29
---

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
