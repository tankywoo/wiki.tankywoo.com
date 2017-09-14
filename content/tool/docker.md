---
title: "Docker"
date: 2015-11-08 12:34
updated: 2017-09-14 15:10
collection: "虚拟化"
log: "增加 docker hub 使用 mirror"
---

[TOC]

[Docker](https://www.docker.com/) Build, Ship, Run; An open platform for distributed applications for developers and sysadmins

## 前言 ##

下面5个链接是2014年的博客, 基于0.10.0, 当前是1.9.x (有些已经失效)

* [Docker 1 -- 开始](http://blog.tankywoo.com/docker/2014/05/08/docker-1-start.html)
* [Docker 2 -- 关于Dockerfile](http://blog.tankywoo.com/docker/2014/05/08/docker-2-dockerfile.html)
* [Docker 3 -- 自建Docker Registry](http://blog.tankywoo.com/docker/2014/05/08/docker-3-docker-registry.html)
* [Docker 4 -- 总结](http://blog.tankywoo.com/docker/2014/05/08/docker-4-summary.html)
* [Docker 网络桥接](http://blog.tankywoo.com/2014/12/22/docker-bridge-network.html)

入门参考:

* [Docker - Get Started](http://docs.docker.com/linux/started/)
* [Docker - Docs](https://docs.docker.com/)

其实以前入门时, 有一个Interactive commandline tutorial, 我觉得挺好的, 但是现在没了.

那个时候docker官网的域名还是docker.io, 现在已经把docker.com拿下了, 变化还是挺大的.

实践：

* [Dockerfile Best Practices](http://crosbymichael.com/dockerfile-best-practices.html) / [Dockerfile最佳实践](http://dockone.io/article/131)
* [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)

## 基础 ##

docker的分层镜像，支持devicemapper, aufs, btrfs。

目前本地1.11.0版本，默认是devicemapper

关于aufs，有两篇文章：

* [Docker基础技术：AUFS](http://coolshell.cn/articles/17061.html)
* [Docker容器和镜像存储机制](http://fengchj.com/?tag=aufs%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F)

另外关于devicemapper，在同步系统时遇到一个问题：

rsync同步时/var/lib/docker/devicemapper/devicemapper/data这个文件显示100G，已经超出机器存储的总大小。

第一感觉就是类似esxi的精简置备(thin provisioning)，网上搜了下，linux下叫[`sparse file`](https://en.wikipedia.org/wiki/Sparse_file)

> In computer science, a sparse file is a type of computer file that attempts to use file system space more efficiently when the file itself is mostly empty.

`ls`命令的`-s`参数可以看到实际使用大小:

	$ ls -alsh /var/lib/docker/devicemapper/devicemapper
	total 952M
	4.0K drwx------ 2 root root 4.0K Jul  6 17:12 .
	4.0K drwx------ 5 root root 4.0K Jul  6 19:14 ..
	950M -rw------- 1 root root 100G Jul  6 22:25 data
	2.0M -rw------- 1 root root 2.0G Jul  6 22:25 metadata

比如data文件，最前面是实际使用大小950M, 后面100G是最大分配的大小。但是rsync同步时是会按100G数据来同步的，并且这个也应该排除。

参考：

* [In Linux, how can I create thin-provisioned file so it can be mounted and a filesystem created on it?](http://serverfault.com/questions/344518/in-linux-how-can-i-create-thin-provisioned-file-so-it-can-be-mounted-and-a-file)
* [Finding sparse files?](http://unix.stackexchange.com/questions/86442/finding-sparse-files)


使用国内的 Docker Hub Mirror，编辑 `/etc/docker/daemon.json`，加上如使用 ustc：

```
{
	"registry-mirrors": ["https://docker.mirrors.ustc.edu.cn/"]
}
```

参考：

- [Docker Hub 源使用帮助](http://mirrors.ustc.edu.cn/help/dockerhub.html)
- [Ubuntu16.04安装Docker及配置镜像加速器](http://www.itfanr.cc/2017/01/14/ubuntu-install-docker-and-configure-mirror-accelerator/)


### CMD 与 ENTRYPOINT 的区别

简单的说：

* 两者都是在在container启动时执行，两者在Dockerfile总都只能有一条
* CMD的内容可以在`docker run <image> <your cmd>`时被your cmd覆盖
* ENTRYPOINT不会被覆盖，默认是`/bin/sh -c`
* ENTRYPOINT优先于CMD执行，所以两者可以配合

更详细可以看看这几篇，资源都不错：

* [Dockerfile reference - ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#/entrypoint)
* [Dockerfile里指定执行命令用ENTRYPOING和用CMD有何不同？](https://segmentfault.com/q/1010000000417103)
* [Dockerfile Best Practices](http://crosbymichael.com/dockerfile-best-practices.html) 5. CMD and ENTRYPOINT better together一节
* [What is the difference between CMD and ENTRYPOINT in a Dockerfile?](http://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile)
* [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#/entrypoint)

## 遇到的问题 ##

### loop module ###

Gentoo下安装docker后启动报错, 看日志:

> level=info msg="Listening for HTTP on unix (/var/run/docker.sock)"
> level=error msg="There are no more loopback devices available."
> level=fatal msg="Error starting daemon: error initializing graphdriver: loopback mounting failed"

原因是没有加载`loop`模块. 在`/etc/conf.d/modules` 中加入模块:

	$ cat /etc/conf.d/modules
	# You can define a list modules for a specific kernel version,
	# a released kernel version, a main kernel version or just a list.
	# The most specific versioned variable will take precedence.
	#modules_2_6_23_gentoo_r5="ieee1394 ohci1394"
	#modules_2_6_23="tun ieee1394"
	#modules_2_6="tun"
	#modules_2="ipv6"
	#modules="ohci1394"
	
	# You can give modules a different name when they load - the new name
	# will also be used to pick arguments below.
	#modules="dummy:dummy1"
	
	# Give the modules some arguments if needed, per version if necessary.
	# Again, the most specific versioned variable will take precedence.
	#module_ieee1394_args="debug"
	#module_ieee1394_args_2_6_23_gentoo_r5="debug2"
	#module_ieee1394_args_2_6_23="debug3"
	#module_ieee1394_args_2_6="debug4"
	#module_ieee1394_args_2="debug5"
	
	# You should consult your kernel documentation and configuration
	# for a list of modules and their options.
	modules="loop"

然后加载模块: `modprobe loop`

### 内核支持 ###

一个是iptables nat表, 编译内核时忘了打开nat支持了, 导致docker启动不了(docker开启不修改iptables选项应该就没事了).

打开内核选项:

	CONFIG_IP_NF_NAT

[can't initialize iptables table `nat'`](https://forums.gentoo.org/viewtopic-t-1009770.html?sid=7822e8eefcdb28edcedf9db7526b7b1e)

安装完docker顺便发现有如下提示:

	* Messages for package app-emulation/docker-1.10.0:
	
	*   CONFIG_IP_NF_TARGET_MASQUERADE:     is not set when it should be.
	*   CONFIG_CGROUP_HUGETLB:      is not set when it should be.
	*   CONFIG_CGROUP_NET_PRIO:     is not set when it should be.
	* Please check to make sure these options are set correctly.
	* Failure to do so may cause unexpected problems.

就顺便一起重新编译内核了.

官方也提供了内核参数检查的脚本 [docker/contrib/check-config.sh](https://github.com/docker/docker/blob/master/contrib/check-config.sh)

### docker hub 墙 ###

可以通过配置`HTTP_PROXY`来解决：

	HTTP_PROXY=http://127.1:8123 docker pull busybox

讨论帖：

* [set http/https proxy through command line](https://github.com/docker/docker/issues/11093)
* [please add support for socks5 proxy](https://github.com/docker/docker/issues/5989)

1.11版本好像支持socks5代理了


### 针对registry的搜索

基于registry v1，列出全部的镜像：

```bash
$ curl http://localhost:5000/v1/search 2>/dev/null | jq '.results[].name'
"library/mongodb"
"library/elasticsearch"
"library/python"
"library/golang"
```

搜索某个镜像仓库，`docker search`指定仓库url：

```bash
$ docker search http://localhost:5000/python
NAME             DESCRIPTION   STARS     OFFICIAL   AUTOMATED
library/python                 0
```

列出某个镜像仓库的所有tags，参考[官方registry api](https://docs.docker.com/v1.6/reference/api/registry_api/#tags)：

```bash
$ curl http://localhost:5000/v1/repositories/library/python/tags 2>/dev/null | jq '.'
{
  "2.7": "7a7d87336a3328623e3fb332a8752b940097aec03e4d39804721bfda2fa2a08d"
}
```

官方Registry即：

```bash
curl https://registry.hub.docker.com/v1/repositories/ubuntu/tags 2>/dev/null | jq '.[].name'
"10.04"
"12.10"
"13.04"
...
```

### docker stop vs. docker kill

具体看help和man

* `docker stop`会先发SIGTERM信号，等待默认10s后发SIGKILL信号 (graceful关闭)
* `docker kill`直接发送默认SIGKILL信号，也可以指定其它信号 (暴力关闭)


## Docker Registry

docker registry 最开始是 v1 版本，参见我三年前写的博客 [Docker 3 -- 自建Docker Registry](https://blog.tankywoo.com/2014/05/08/docker-3-docker-registry.html)，但是现在这个版本已经过时了，更多的是使用 v2 版本。

部署 docker registry 最简单的方法就是直接通过 docker 镜像来运行，docker hub 上的地址 [registry](https://hub.docker.com/_/registry/)。直接 pull 然后运行，不过运行前建议先看看 Dockerfile，比如 push 上去的镜像是放在 `/var/lib/registry`，所以建议将本地目录挂载到容器的这个目录，否则容器重启后数据就没了，具体的启动命令见：

```
docker run -d -p 5000:5000 --restart always --name registry \
        -v /home/registry/data:/var/lib/registry \
        registry:2
```

注意要指定为 v2 的版本。

推送到 registry 根据镜像的前缀确认推送的地址，所以需要给本地的镜像打一个额外的tag：

```
docker tag alpine:latest 127.0.0.1:5000/alpine
```

然后推送到本地的 registry。

可以通过如下查看目前有哪些镜像：

```
curl http://127.0.0.1:5000/v2/_catalog
```

关于认证，没有深入研究，直接使用了 registry 自带的 basic auth，参考 [native basic auth](https://docs.docker.com/registry/deploying/#native-basic-auth)：

```
# 创建一个 auth 目录，生成简单认证的用户密码对
$ mkdir auth
$ docker run \
        --entrypoint htpasswd \
        registry:2 -Bbn testuser testpassword > auth/htpasswd
```

当然如果安装了 `apache-tools` 也可以直接使用 `htpasswd` 命令生成：

```
htpasswd -bBn testuser testpassword > auth/htpasswd
```

注意 `-B` 参数，使用 bcrypt 加密。

新的启动命令：

```
docker run -d -p 5000:5000 --restart always --name registry \
        -v /home/registry/data:/var/lib/registry \
        -v /home/registry/auth:/auth \
        -e "REGISTRY_AUTH=htpasswd" \
        -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
        -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
        registry:2
```

然后通过 `docker login` 来登录，登录会话保存到 `~/.docker/config.json` 中，使用 `docker logout` 删除。通过 curl 访问：

```
curl -u testuser:testpassword --basic  http://127.0.0.1:5000/v2/_catalog
```

看到还有推荐 [cesanta/docker_auth](https://github.com/cesanta/docker_auth) 这个仓库，未尝试。


## Docker Compose

顾名思义，一个 `Dockerfile` 是针对于一个容器（服务），编排就是将项目所包含的一组服务组合起来，是更高一级的配置管理。

[Docker Compose](https://docs.docker.com/compose/) 安装参考官方 [Install Compose](https://docs.docker.com/compose/install/#install-compose)，官方直接提供了编译好的二进制程序，放到 `$PATH` 下即可，或者通过 `pip` 安装。

下面这两篇都给出了一样的例子，通过 flask web 配合 redis 做一个简单的demo：

- [Docker：容器编排利器Compose（起步篇）](https://lw900925.github.io/docker/docker-compose-getting-started.html)
- [使用docker-compose实现容器编排](https://www.centos.bz/2017/08/docker-compose-container-choreography/)

Docker Compose 会给里面定义的各服务做相应的 dns 记录，使一组服务之间方便互联。

其它参考：

- [Docker Compose 项目](https://yeasy.gitbooks.io/docker_practice/content/compose/)



## 一些链接 ##

* [Docker —— 从入门到实践](https://www.gitbook.com/book/yeasy/docker_practice/details)
* [国内daocloud的一些镜像](https://dashboard.daocloud.io/packages) 国内现在没找到什么好的仓库, 这个算一个, 就是镜像略少
