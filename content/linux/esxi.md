---
title: "ESXi 5.x 命令行操作"
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

## 控制虚拟机开关机 ##

To power on a virtual machine from the command line:

List the inventory ID of the virtual machine with the command:

	vim-cmd vmsvc/getallvms |grep <vm name>

Note: The first column of the output shows the vmid.

Check the power state of the virtual machine with the command:

	vim-cmd vmsvc/power.getstate <vmid>

Power-on the virtual machine with the command:

	vim-cmd vmsvc/power.on <vmid>

关机就是把 `power.on` 改为 `power.off` 就可以了.

参考: [Powering on a virtual machine from the command line when the host cannot be managed using vSphere Client](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1038043)

另外还有一种方法, 只能控制关机:

Get a list of **running** virtual machines, identified by World ID, UUID, Display Name, and path to the .vmx configuration file, using this command:

	esxcli vm process list # 只显示开机的虚拟机列表

Power off one of the virtual machines from the list using this command:

	esxcli vm process kill --type=[soft,hard,force] --world-id=WorldNumber

Notes: 
Three power-off methods are available. Soft is the most graceful, hard performs an immediate shutdown, and force should be used as a last resort.

Alternate power off command syntax is: 

	esxcli vm process kill -t [soft,hard,force] -w WorldNumber

参考:

* [Powering off a virtual machine on an ESXi host](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1014165)
* [How to shutdown a virtual machine on ESXi5 over an ssh terminal session?](http://serverfault.com/questions/321909/how-to-shutdown-a-virtual-machine-on-esxi5-over-an-ssh-terminal-session)
