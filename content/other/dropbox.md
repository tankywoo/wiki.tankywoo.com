---
title: "网盘 Dropbox"
date: 2017-08-25 15:56
log: ""
---

## Linux 命令行管理

考虑到 Mac 和 Linux（终端）下的同步，之前用过 `dropbox-cli`，不过忘了，现在又折腾了一下，顺便记录起来。

系统 Gentoo，portage 里已经有 `net-misc/dropbox` 和 `net-misc/dropbox-cli` 两个工具了，这两个都需要安装，前者是 Dropbox 守护进程，后者是 Dropbox 的管理工具。当然功能上还是比较弱，肯定没法和 GUI 版本比。

首先安装 `net-misc/dropbox`，根据 `SRC_URI` 从 dropbox 官网下载编译好的tar包，不过因为被墙了，所以可以手动将 tar 包下载下来放到 `/usr/portage/distfiles/` 下，emerge 会先查看这个目录下是否已经有下载过的tar包，如果有就不会再下载了。

程序会解压并放到 `/opt/dropbox/` 下并将其中的 dropboxd 做软链接到 `/opt/bin/dropbox`。

还是因为被墙的原因，直接执行 `dropbox` 是没用的，需要先配置 `http_proxy/https_proxy`：

```
export http_proxy="127.0.0.1:8123"
export https_proxy="127.0.0.1:8123"
```

启动 `dropbox` 后会有如下提示：

```
$ dropbox
This computer isn't linked to any Dropbox account...
Please visit https://www.dropbox.com/cli_link_nonce?nonce=HASH-STRING to link this device.
```

复制这个链接在浏览器访问并授权即可，登录等信息会存储在 `$HOME/.dropbox/` 下。并会将 `/opt/dropbox/` 下的文件在 `$HOME/.dropbox-dist/` 下放一份，通过 `ps` 可以看出最终是使用这个的文件。

最后安装 `net-misc/dropbox-cli`，提供的管理比较简单，就是查看文件状态，dropbox同步情况，停掉进程等。

还有一个问题是 dropbox 守护进程启动后会自动 Kill，然后子进程的父进程会变为 init 进程，可能是程序的 bug导致。

参考：

* [How To Install Dropbox Client as a Service on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-install-dropbox-client-as-a-service-on-ubuntu-14-04)
* [Dropbox Install - Linux](https://www.dropbox.com/install-linux)
