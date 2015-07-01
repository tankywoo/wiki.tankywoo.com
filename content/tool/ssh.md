---
title: "ssh"
date: 2013-09-13 10:48
---


我们老大上次提到了一句话非常好，他说他每安装一个工具，都要 `equery files toolname` 来查看这个工具到底会带有多少小工具.  
就像我没有执行 equery 查询，我也不会发现，原来 ssh 自带了这么多好用的工具！

* /usr/bin/scp
* /usr/bin/sftp
* /usr/bin/slogin
* /usr/bin/ssh
* /usr/bin/ssh-add
* /usr/bin/ssh-agent
* /usr/bin/ssh-copy-id
* /usr/bin/ssh-keygen
* /usr/bin/ssh-keyscan

### RTFM ###

	man ssh
	man sshd
	man ssh_config
	man sshd_config


## 关于ssh config ##

ssh\_config 有两个文件：`~/.ssh/config` 和 `/etc/ssh/config`

	config文件的格式：

	空行和#开头的是注释文件
	用Host指定特定的主机，*表示默认的
	具体可以参考/etc/ssh/config样例

	比如可能有多个私钥文件，其中对于所有网站，要用私钥A。而对于某一个网站，必须用私钥B
	则可以配置：
	Host xxx
		IdentityFile ~/.ssh/tankywoo     # tankywoo就是私钥文件

	Host name还可以用匹配，具体可以man ssh_config


## ssh-agent ##

ssh-agent 是一个ssh私钥的认证代理工具，类似于 windows 下的 [Pageant](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)

这类 authentication agent 适合于特别多私钥需要管理，或者私钥有密码等情况

思想是 ssh-agent 启动一个会话(X-session/login session)，然后其他程序在这个会话里使用ssh时，都会通过使用agent的环境变量自动加载私钥来认证

ssh-agent 后可以接一些参数和命令，一般接shell名称就可以启动一个新的加载ssh-agent环境变量的会话，如:

	ssh-agent zsh

然后就可以用ssh-add加载私钥了，加载后可以用 `ssh-add -l` 查看当前会话加载了哪些私钥。

通过 ssh-agent 启动一个会话，然后用 `ssh-add` 加载私钥，以后使用ssh就无需关心私钥的事情了。

## Github: 'Error: Key already in use' 问题 ##

2013-07-28 补充:

今天在给 Github 上的一个 repo 添加公钥时, 提示 `Error: Key already in use`

**TODO** 我是记得这个 公钥 给同一个账户下的另外一个 repo 添加过, 但是没想到居然会冲突, 看来要么加成`全局公钥`, 要么一个公钥只能指定到一个 **特定** repo

搜到 [官方的Help](https://help.github.com/articles/error-key-already-in-use) 有讲到这个问题:

	$ ssh -T -i ~/.ssh/id_rsa git@github.com
	# Connect to github.com using a specific ssh key
	# Hi username! You've successfully authenticated, but GitHub does not
	# provide shell access.

通过 `-i` 指定 密钥, 然后通过输出的 `username` 可以知道是哪个 repo 在使用这个密钥.

## ssh卡住如何退出 ##

2013-09-13 补充:

有时因为网络或其他原因, ssh远程登录其他机器时, 会卡住, 但是又没有自动退出, ctrl-c 也没用.

其实 `man ssh` 里已经讲了解决方法了.

查看 `ESCAPE CHARACTERS` 这一块:

	~.      Disconnect.

## 其它 ##

获取公钥的fingerprint, 比如将公钥加到github后台, 会有一个fingerprint id, 有时在不通帐号添加的公钥都是用的同一个邮箱名, 不知道对应的是哪个公钥, 本地对公钥:

    $ ssh-keygen -lf /path/to/ssh/key.pub

如果有一个私钥, 可以重新生成找到公钥:

    $ ssh-keygen -y -f /path/to/ssh/key
