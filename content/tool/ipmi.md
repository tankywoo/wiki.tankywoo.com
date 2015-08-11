---
title: "ipmi"
date: 2015-08-10 21:33
---

IPMI(Intelligent Platform Management Interface) 智慧平台管理工具.

一般用于操作系统重启, 监控硬件如温度等.

工具是ipmitool.

---

首先在启动机器时, Dell一般是`Ctrl-E`进入IPMI配置:

![IPMI-1](http://tankywoo-wb.b0.upaiyun.com/ipmi-1.png)

配置`IPMI Over LAN`为`On`, 这块暂时没找到如何通过ipmitool来管理, 看到这个[帖子](http://serverfault.com/questions/676145/how-to-disable-ipmi-over-lan-using-ipmitool), 有时间再研究下.

![IPMI-2](http://tankywoo-wb.b0.upaiyun.com/ipmi-2.png)

另外, Common Settings中, NIC Selection设置为`Shared with Failover LOM2`, 这块涉及到网卡的使用, 因为配置的ip是内网, 和第一块网卡绑定, 如果配错了也不通. 之前遇到有时是LOM1, 通过插拔网线可以切换过去.

最后进入BIOS, 设置Serial Communication:

![IPMI-3](http://tankywoo-wb.b0.upaiyun.com/ipmi-3.png)

---

远程的话, 最常用的就是:

	$ ipmitool -H X.X.X.X -U root -P XXXX -I [lan|lanplus|open] power [on|off|reset|soft|status]

其中lan/lanplus分别是v1.5/v2.0的标准, 具体看主板的IPMI支持了.

open是默认的, 基于本地的操作可以不写.

因为IPMI是基于主板硬件上的, 所以即时服务器关机, 只要ipmi ip可通, 且插电, 就可以远程控制开机

下面记录一些本机上的命令操作. 环境Ubuntu 12.04.

首先查看是否支持IPMI:

	$ dmidecode |grep -C 5 IPMI
	...

	Handle 0x2600, DMI type 38, 18 bytes
	IPMI Device Information
			Interface Type: KCS (Keyboard Control Style)
			Specification Version: 2.0
			I2C Slave Address: 0x10
			NV Storage Device: Not Present
			Base Address: 0x0000000000000XXX (I/O)

加载指定模块:

	$ lsmod | grep ipmi
	ipmi_ssif              16256  0
	ipmi_devintf            8500  0
	ipmi_si                47731  0
	ipmi_msghandler        40979  3 ipmi_ssif,ipmi_devintf,ipmi_si

命令:

	# 查看本机的ipmi 通道1(channel)配置
	# -I open 可有可无
	$ ipmitool -I open lan print 1
	Set in Progress         : Set Complete
	Auth Type Support       : NONE MD2 MD5 PASSWORD
	Auth Type Enable        : Callback : MD2 MD5
							: User     : MD2 MD5
							: Operator : MD2 MD5
							: Admin    : MD2 MD5
							: OEM      :
	IP Address Source       : Static Address
	IP Address              : 192.168.0.100
	Subnet Mask             : 255.255.255.0
	MAC Address             : 78:2b:cb:8e:ab:90
	SNMP Community String   : public
	IP Header               : TTL=0x40 Flags=0x40 Precedence=0x00 TOS=0x10
	Default Gateway IP      : 192.168.0.1
	Default Gateway MAC     : 00:00:00:00:00:00
	Backup Gateway IP       : 0.0.0.0
	Backup Gateway MAC      : 00:00:00:00:00:00
	802.1q VLAN ID          : Disabled
	802.1q VLAN Priority    : 0
	RMCP+ Cipher Suites     : 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14
	Cipher Suite Priv Max   : aaaaaaaaaaaaaaa
							:     X=Cipher Suite Unused
							:     c=CALLBACK
							:     u=USER
							:     o=OPERATOR
							:     a=ADMIN
							:     O=OEM

	# 设置ipmi ip为静态ip
	$ ipmitool lan set 1 ipsrc static

	# 设置ipmi ip
	$ ipmitool lan set 1 ipaddr X.X.X.X

	# 设置ipmi掩码
	$ ipmitool lan set 1 netmask 255.255.255.0

	# 设置ipmi默认网关
	$ ipmitool lan set 1 defgw ipaddr X.X.X.X

	# 查看ipmi的用户列表
	$ ipmitool user list 1
	ID  Name             Callin  Link Auth  IPMI Msg   Channel Priv Limit
	2   root             true    true       true       ADMINISTRATOR
	3   tankywoo         true    true       true       ADMINISTRATOR

	# 对指定用户设置密码
	$ ipmitool user set password 2 XXXX

	# 新建用户
	$ ipmitool user set name 3 tankywoo

	# 给用户设置权限
	# 其中privilege可以运行ipmitool channel查看数字所代表的等级
	$ ipmitool channel setaccess 1 3 link=on ipmi=on callin=on privilege=4

	# 开启用户
	$ ipmitool user enable 3

	# 查看指定通道的指定用户权限
	$ ipmitool channel getaccess 1 3
	Maximum User IDs     : 10
	Enabled User IDs     : 2

	User ID              : 3
	User Name            : tankywoo
	Fixed Name           : No
	Access Available     : call-in / callback
	Link Authentication  : enabled
	IPMI Messaging       : enabled
	Privilege Level      : ADMINISTRATOR

	# 修改认证方式
	$ ipmitool lan set 1 auth USER MD5,MD2


## 参考 ##

* [Configuring IPMI under Linux using ipmitool](https://www.thomas-krenn.com/en/wiki/Configuring_IPMI_under_Linux_using_ipmitool)
* [ipmitool - utility for controlling IPMI-enabled devices](http://netkiller.github.io/monitoring/ipmitool.html)
* [IPMI SOL – Inexpensive Remote Console](http://www.alleft.com/sysadmin/ipmi-sol-inexpensive-remote-console/)
* [Managing Dell PowerEdge Servers Using IPMItool](http://www.dell.com/downloads/global/power/ps4q04-20040204-murphy.pdf)
