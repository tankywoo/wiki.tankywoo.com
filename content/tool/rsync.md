---
title: "rsync"
date: 2013-08-17 07:36
---


## rsync ##

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
* 主机前加上`rsync://`, 后面直接使用`/`分隔主机和目录, 和目录结构一样

<!-- comment -->

	Pull: rsync [OPTION...] [USER@]HOST::SRC... [DEST]
	rsync [OPTION...] rsync://[USER@]HOST[:PORT]/SRC... [DEST]
	Push: rsync [OPTION...] SRC... [USER@]HOST::DEST
	rsync [OPTION...] SRC... rsync://[USER@]HOST[:PORT]/DEST

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
* `-X` - preserve extended attributes **TODO**
* `-A` - 保持ACL
* `--delete` - 删除src没有, 但dest存在的文件. 这是mirror方式需要的, 保持两边所有文件一致.
* `--stats` - 输出文件传输的状态
* `--progress` - 输出文件传输的进度
* `--exclude-from` - 从文件里读取排除在外的文件或目录
* `--numeric-ids` - 不映射uid/gid到user/group的名字

常用的mirror同步命令:

	rsync -hvaHEXA --delete --stats --progress --numeric-ids --exclude-from=/root/filter_file tankywoo::wiki /data

## 资料 ##

* [howtocn - rsync](http://www.howtocn.org/rsync)
