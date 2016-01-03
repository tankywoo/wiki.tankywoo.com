---
title: "rsync"
date: 2013-08-17 07:36
updated: 2016-01-03 11:28
---

[TOC]

rsync - a fast, versatile, remote (and local) file-copying tool

广泛用于`备份(backup)`和`镜像(mirror)`

支持本地或远程复制, 有`shell`和`rsync daemon`两种方式

* remote shell
	+ via ssh or rsh
	+ the source or destination path contains a single colon (:) separator after a host specification
* rsync daemon
	+ via TCP
	+ the source or destination path contains a double colon (::) separator after a  host  specification
	+ OR  when  an rsync://  URL  is  specified

## 使用方式 ##

	Local:
		rsync [OPTION...] SRC... [DEST]

	Access via remote shell:
		Pull: rsync [OPTION...] [USER@]HOST:SRC... [DEST]
		Push: rsync [OPTION...] SRC... [USER@]HOST:DEST

	Access via rsync daemon:
		Pull: rsync [OPTION...] [USER@]HOST::SRC... [DEST]
			  rsync [OPTION...] rsync://[USER@]HOST[:PORT]/SRC... [DEST]
		Push: rsync [OPTION...] SRC... [USER@]HOST::DEST
			  rsync [OPTION...] SRC... rsync://[USER@]HOST[:PORT]/DEST

	Usages with just one SRC arg and no DEST arg will list the source files instead of copying.

### 本地同步 ###

	rsync [OPTION...] SRC... [DEST]

### remote shell方式 远程同步 ###

使用一个冒号`:`分隔主机和目录

	Pull: rsync [OPTION...] [USER@]HOST:SRC... [DEST]
	Push: rsync [OPTION...] SRC... [USER@]HOST:DEST

可以使用`ssh`或`rsh`方式传输

举例:

	# 使用ssh方式, 端口为1234. 传输主机tankywoo的/data目录到本地的/tmp/backup下
	rsync -e 'ssh -p 1234' root@tankywoo:/data /tmp/backup/


### rsync daemon方式 远程同步 ###

有两种方式:

* 使用两个冒号`::`分隔主机和目录

		Pull: rsync [OPTION...] [USER@]HOST::SRC... [DEST]
		Push: rsync [OPTION...] SRC... [USER@]HOST::DEST

* 主机前加上`rsync://`, 后面直接使用`/`分隔主机和目录, 和目录结构一样

		Pull: rsync [OPTION...] rsync://[USER@]HOST[:PORT]/SRC... [DEST]
		Push: rsync [OPTION...] SRC... rsync://[USER@]HOST[:PORT]/DEST

## 常用参数 ##

* `-a` - archive mode; 相当于 `-rlptgoD`
* `-r` - 递归. 和`cp`的 -r 参数一样
* `-l` - 复制软链接
* `-p` - 保持权限不变
* `-t` - 保持修改时间不变
* `-g` - 保持group组不变
* `-o` - 保持owner不变
* `-D` - 等价于`--devices --specials`, 分别是同步设备文件和特殊文件
* `-b` - backup. 配合`--backup-dir`来用.
* `-n` - 这个非常有用. 在同步前可以先测试来查看会由哪些变化, 但不实际修改. 类似gentoo emerge时的`-pv`
* `-v` - 更详细的输出信息
* `-h` - 以human-readable的方式输出数字格式
* `-H` - 复制硬链接
* `-E` - 保持可执行权限一致
* `-X` - 保持扩展属性(extended attributes), 如`setattr`配置的属性
* `-A` - 保持ACL
* `--delete` - 删除src没有, 但dest存在的文件. 这是mirror方式需要的, 保持两边所有文件一致.
* `--stats` - 输出文件传输的状态
* `--progress` - 输出文件传输的进度
* `--exclude-from` - 从文件里读取排除在外的文件或目录
* `--numeric-ids` - 不映射uid/gid到user/group的名字
* `--list-only` - 只列出文件列表, 不同步. 这个和同步时加上`-n`做pretend有点类似

列出可用modules(只有module未配置`list = no`的才会被列出):

	rsync 192.168.1.100::

查看文件列表:

	rsync --list-only bob@192.168.1.100::mymodule

常用的mirror同步命令:

	rsync -hvaHEXA --delete --stats --progress --numeric-ids --exclude-from=/root/filter_file tankywoo::wiki /data

rsyncd 可以配置多个modules, 如:

```
[mymodule]
    uid = root
    gid = root
    path = /home/test/
    numeric ids = yes
    list = no
    exclude from = /path/to/file
    ignore errors
    auth users = bob
    secrets file = /etc/rsyncd.secrets
    hosts allow = 192.168.1.101
    comment = "for rsyncd test"
```


## 经验 ##

### 关于 hosts allow 和 hosts deny ##

如果只设置了`hosts allow`, 则不符合的都会拒绝连接(reject).

如果同时设置了`hosts allow`和`hosts deny`, 则首先会判断是否符合allow列表, 如果符合则连接, 否则判断deny连接, 如果符合则拒绝, 剩下的都允许连接.

另外, 这两个配置项都可以是全局级的.

逻辑上有点绕, 所以感觉这个如果没有仔细看文档和尝试的话, 容易造成安全问题.

这里也可以使用通配符(wildcards) `*`.

### 关于认证用户和密码 ###

`auth users` 和 `secrets file` 控制.

前者列出允许连接module的用户, 后者管理用户和密码.

普通的设置只是简单的帐号密码匹配, 这套用户密码体系和本地用户(`/etc/passwd`)是无关的.

也可以配置`groupname matching`, 组名使用`@`前缀, 此时认证用户必须是本地系统上存在的真实用户, 且是这个组下的成员.

### 关于 filter, exclude, exclude from 等 ###

排除的文件路径, 始终是**相对路径**, 相对于path的路径.

`exclude` 配置排除的模式

`exclude from` 配置排除文件, 包含多行排除模式/文件, 一个module只能配置一个此配置项, 配置多个的话以最后一个为主. 但是客户端命令可以指定多个`--exclude-from`, 且都生效.

> Only one "exclude from" parameter can apply to a given module; if you have multiple exclude-from files, you can specify them as a merge file in the "filter" parameter.

排除模式可以使用`-`和`+`来显示的指定`exclude`和`include`.

关于filter和exclude from的区别:

* filter 必须指定 `-` 和 `+`, 而exclude from里的模式默认都是`-`

这里还有些疑惑的地方:

如果配置了`use chroot = yes`, 那么感觉`exclude from` 以及 `filter` 指定的文件都应该是相对路径, 相对于path, 但是实际还是要配置绝对路径, 否则报错.

不过, filter是可以显式配置为相对:

	filter = : .rsync-filter

这样就是相对了path配置的路径下的.rsync-filter文件.

另外就是关于:

> you can specify them as a merge file in the "filter" parameter

这里不清楚怎么使用?  **TODO**

## 关于权限问题 ##

同步时会看到有些文件报 `failed: Permission denied`, `uid` 选项给出了说明:

> The default when run by a super-user is to switch to the system’s "nobody" user.  The default for a non-super-user is to not try to change the user.

所以需要配置 `uid = root` (或其它足够的权限)


## Troubleshoot ##

> rsync: didn't get server startup line

测试时配置的`exclude from`是一个无效路径, 导致这个错误

> auth failed on module xxx

见 [rsync auth failed on module xxx 问题总结](http://blog.tankywoo.com/linux/2013/12/07/rsync-auth-failed-on-module-xxx.html)
