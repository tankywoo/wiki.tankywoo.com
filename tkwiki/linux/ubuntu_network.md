# Ubuntu网络配置 #

## 直接用ifconfig配置 ##

	设置网卡eth0的IP地址和子网掩码
	sudo ifconfig eth0 192.168.2.106 netmask 255.255.255.0
	设置网关
	sudo route add default gw 192.168.2.254
	配置DNS
	sudo vim /etc/resolv.conf
	重启网络


## 修改网络配置文件 ##

	sudo vim /etc/network/interfaces

	DHCP连接
	auto eth0
	iface eth0 inet dhcp

	手动配置静态ip
	auto eth0
	iface eth0 inet static
	address 192.169.2.106
	gateway 192.168.2.254
	netmask 255.255.255.0
	#network ?.?.?.?
	#broadcast ?.?.?.?

	#### dns设置
	# 我印象中重启后resolv.conf的内容会删除
	# 所以DNS服务器的配置也是在/etc/network/interfaces下
	dns-nameservers 8.8.8.8

