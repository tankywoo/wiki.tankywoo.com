---
title: "vsftpd"
date: 2013-08-17 07:36
---


参考: [鸟哥私房菜](http://vbird.dic.ksu.edu.tw/linux_server/0410vsftpd.php)


三种群体：

* anonymous
* guest
* real user

关于设置real user，有三个设置：

	userlist_enable=YES
	userlist_deny=NO
	userlist_file=/etc/vsftpd/user_list

`userlist_enable`开启就是支持real user

在`userlist_file`设置user名，一个一行

如果`userlist_deny`设置为YES，则`userlist_file`中的用户被拒绝；

如果设置为NO，则只有`userlist_file`中的用户可以登录（系统用户除外？ *TODO* ）


`local_umask`设置新文件的掩码，推荐是022

我先开始这里设置了022，anonymous上传的文件权限就是600，所以自然就没法下载

在设置了`chroot_local_user=YES`后，用户限制在自己的home目录，但是登录会报错:

	500 OOPS: vsftpd: refusing to run with writable root inside chroot ()

Google了下，网上还是很常见的

对于`version > 3`的(网上讨论的结果，未确定)，添加

	allow_writeable_chroot=YES

即可解决问题，参考: [benscobie的Blog](http://www.benscobie.com/fixing-500-oops-vsftpd-refusing-to-run-with-writable-root-inside-chroot/)

如果是`2.x`的版本，[参考](http://blog.thefrontiergroup.com.au/2012/10/making-vsftpd-with-chrooted-users-work-again/)
