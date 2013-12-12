---
title: "ESXi"
date: 2013-08-14 18:09
---


## 网络 ##

很多命令的 `-h` 都包含了详细的例子

`esxcli network`:

这是一个命令集, 包含了很多子命令

* `esxcli network nic list` 查看网卡信息
* `esxcli network ip route ipv4 list` 查看路由(ipv4)
* `esxcli network ip dns server list` 查看 dns
* `esxcli network ip interface ipv4 get` 查看ip配置(ipv4)

`esxcfg-route`:

* `esxcfg-route` 查看默认路由

`esxcfg-nics`:

* `esxcfg-nics` 等价 `esxcli network nic list`

`tcpdump-uw`:

类似于Linux下的 tcpdump, 是 ESX 的抓包工具

`vsish`

## ESXi命令行修改密码 ##

通过 ssh 登录到 ESXi 系统后, 可以通过 passwd root 来修改密码

参考 [Changing ESXi Root Password](http://vmwaresupportguy.com/2011/12/changing-esxi-root-password/) , 里面还说明了如何开启 ESXi ssh 登录.

## ESXi 的 authorized\_keys ##

For ESXi 5.0, the location of authorized\_keys is: `/etc/ssh/keys-<username>/authorized_keys`

参考: [Allowing SSH access to ESX hosts with public/private key authentication](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1002866)
