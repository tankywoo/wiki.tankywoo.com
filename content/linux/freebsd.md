---
title: "FreeBSD"
collection: "发行版"
date: 2016-09-15 17:00
updated: 2016-09-15 17:00
log: "初探"
---

[TOC]

## 基本

目前10.3是RELEASE版，11.0还是BETA

一般下载disc1.iso就可以，大概700MB；dvd1是比较齐全的，大概2个多G；memstick好像是写入U盘的，具体没试过，大小也是700M左右。

安装和基本使用参考[FreeBSD使用手册](https://www.freebsd.org/doc/zh_CN.UTF-8/books/handbook/index.html)就足够了。

其它参考：

* [FreeBSD 简明用户指南](http://bsdelf.github.io/posts/freebsd-brief-user-guide/)
* [freebsdchina](https://wiki.freebsdchina.org/start)
* [FreeBSD 9.0 安装入门教程.pdf](quiver-file-url/871494DBDDBEF4ABDF120C463796CB52.pdf)
* [FreeBSD Handbook](https://www.freebsd.org/doc/handbook/book.html)


修改源：

pkg源主页：[pkg.freebsd.org](http://pkg.freebsd.org/)

FreeBSD 10.x版本和之前貌似不同，需要修改`/etc/pkg/FreeBSD.conf`:

```bash
FreeBSD: {
  url: "pkg+http://pkg0.twn.freebsd.org/${ABI}/latest/",  # 这个源没被墙
  mirror_type: "srv",
  signature_type: "fingerprints",
  fingerprints: "/usr/share/keys/pkg",
  enabled: yes
}
```

额外参考：

* [freebsd10怎么修改pkg的源？](https://www.freebsdchina.org/forum/viewtopic.php?t=67003)

权限，普通用户需要属于组`wheel`才能使用`su`命令，否则报Sorry；直接修改`/etc/group`或者执行`pw user mod tankywoo -G wheel`

可以安装sudo工具。[参考](http://unix.stackexchange.com/questions/116470/whats-the-sudo-equivalent-for-freebsd)

> 通常情况下， 强烈建议不要去更改 root 用户的默认 Shell。原因是这些 Shell 没有包括在基本系统中，正常情况下它们会被安装到 /usr/local/bin 和 /usr/bin 目录下。万一某天 /usr/local/bin 和 /usr/bin 的文件系统不能被挂载， 这样情况下 root 将不能进入自己默认的 Shell，从而 root 将不能够登录进去。 鉴于这个原因，第二个系统管理员帐户 toor 创建时使用的是非默认的 Shell。 [来源](https://www.freebsd.org/doc/zh_CN/articles/linux-users/shells.html)

所以root还是使用csh，登录配置为`~/.cshrc`，增加以下几项：

```bash
alias ls        ls -G
alias ll        ls -al
alias rm        rm -i
alias mv        mv -i

set path = ($HOME/.local/bin /sbin /bin /usr/sbin /usr/bin /usr/games /usr/local/sbin /usr/local/bin $HOME/bin)  # 主要是增加~/.local/bin

setenv  EDITOR  vim
```

第二个系统管理用户改为bash，参考 [Freebsd下安装bash](http://linux.it.net.cn/m/view.php?aid=8444)。其中`/etc/shells`会自动更新。

make install后最后的提示不清楚有什么用：

```
Installing bash-4.3.46_1...
======================================================================

bash requires fdescfs(5) mounted on /dev/fd

If you have not done it yet, please do the following:

        mount -t fdescfs fdesc /dev/fd

To make it permanent, you need the following lines in /etc/fstab:

        fdesc   /dev/fd         fdescfs         rw      0       0

======================================================================
```

修改提示符在csh下是`prompt`环境变量：

```bash
set prompt = " # " 
```

主机名、网络配置在`/etc/rc.conf`里。

看内存：安装`freecolor`，执行`freecolor -m -o`；`swapinfo`看swap。

参考：[What is equivalent of Linux's 'free' command on FreeBSD v8.1](http://stackoverflow.com/questions/4093786/what-is-equivalent-of-linuxs-free-command-on-freebsd-v8-1) / [FreeBSD find out RAM size Including Total Amount of Free and Used Memory Size](http://www.cyberciti.biz/faq/freebsd-command-to-get-ram-information/)

折腾MOTD：`/etc/motd`，以及`cowsay`, `fortune`等。

参考：[Put a Talking Cow in Your Linux Message of the Day](https://www.linux.com/learn/put-talking-cow-your-linux-message-day) / [CUSTOMIZE YOUR MOTD](http://www.mewbies.com/how_to_customize_your_console_login_message_tutorial.htm)


## 安装/更新软件

参考：

* [How To Install and Manage Ports on FreeBSD 10.1](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-ports-on-freebsd-10-1)
* [How To Manage Packages on FreeBSD 10.1 with Pkg](https://www.digitalocean.com/community/tutorials/how-to-manage-packages-on-freebsd-10-1-with-pkg)

### pkg

FreeBSD 10.x 之前的命令貌似叫 `pkg_add`, `pkg_info`等，10.x 之后就`pkg`命令，`install`这些都是pkg的子命令。

这个是安装二进制包，所以没法定制，但是安装速度很快。

通过disc1安装的FreeBSD，默认没有`pkg`命令，第一次敲会提示安装，Yes确认即可。默认的源安装不上，可以按上面修改源地址。

```bash
$ pkg search python  # 搜索
$ pkg install python27-2.7.12  # 安装
$ pkg info python27-2.7.12  # 查看信息
$ pkg upgrade <pakcage>  # 升级软件
```

### ports

第一次使用ports需要更新

```bash
$ portsnap fetch extract
$ portsnap update
```

虽然执行了第一步，但是看`/usr/ports/`下有内容，可能只需要第二步就可以了。

安装软件：

```bash
$ whereis tmux
tmux: /usr/ports/sysutils/tmux

$ cd /usr/ports/sysutils/tmux
$ make
$ make install
```
更新软件:

```bash
$ make && make reinstall
```

中间会有一些安装包的选项提示(勾选)。

安装后二进制bin文件默认在`/usr/local/bin/`下：

```
$ whereis tmux
tmux: /usr/local/bin/tmux /usr/local/man/man1/tmux.1.gz /usr/ports/sysutils/tmux
```

安装`pip`和`setuptools`:

```bash
$ python -m ensurepip
Ignoring indexes: https://pypi.python.org/simple
Collecting setuptools
Collecting pip
Installing collected packages: setuptools, pip
Successfully installed pip-8.1.1 setuptools-20.10.1
```

参考 [How to install python3.4-pip in FreeBSD 10.1?](http://serverfault.com/questions/694665/how-to-install-python3-4-pip-in-freebsd-10-1)

### 查看哪些软件可以升级

`pkg version -v` 可以显示所有安装的软件以及哪些可以升级。

参考[使用Ports Collection](https://www.freebsd.org/doc/zh_CN.UTF-8/books/handbook/ports-using.html)

### 查看已安装的软件包是通过什么方式安装的

输出最后一栏如果是 FreeBSD则是二进制；unknown-repository则是ports安装

参考：<https://www.reddit.com/r/freebsd/comments/3mc0ss/list_of_installed_ports/>

```bash
$ pkg query --all '%o %n-%v $R'
```

## 遇到的问题

### make config配置

安装vim时，在make开始就会有config配置的ncurser窗口，让选择安装哪些，和Gentoo的USE类似，可以把X11去掉，改为console，只安装CUI版本。(其实不装X11等，编译安装还是很快的)

之前安装vim时，配置有问题，导致无法make:

```bash
make
====> You must select one and only one option from the UI single
*** Error code 1

Stop.
make[1]: stopped in /usr/ports/editors/vim
*** Error code 1

Stop.
make: stopped in /usr/ports/editors/vim
```

这时`make clean`无用，需要再次调出之前的ncurser窗口，执行`make config`重新配置；`make showconfig`查看配置；`make rmconfig`删除配置。

### cron任务

每天上午11点负载会莫名飙到3，甚至5。

排查后发现原来时区不对，`/etc/crontab`默认有个daily任务，每天3点进行日常维护，正好就是错误时区下的上午11点。（通过`md5`(unix下不是md5sum)确认时区文件/etc/localtime是Shanghai, zone文件也都在/usr/share/zoneinfo/下）。
