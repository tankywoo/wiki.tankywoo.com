# Linux Comamnds #

# About This Page #

	这里记录的是一些命令的常用方法
	有些强大的命令会单独放在Tools(Command)目录下单独总结
	看**man手册**等才是王道



# 文件传输命令 #

`scp`

	scp — secure copy (remote file copy program)
	-p参数	将每个副本的修改时间、权限等与源文件保持一致





# 系统磁盘管理命令 #

`mount`

[Linux的mount命令简介](http://www.blogjava.net/decode360/archive/2009/07/30/289072.html)

`df`

`du`


# 源 #

`apt`

`add-apt-repository`

	add-apt-repository 是由 python-software-properties 这个工具包提供的,只有ubuntu 09.10之后版本支持
	add-apt-repository - Adds a repository into the /etc/apt/sources.list or /etc/apt/sources.list.d or removes an existing one
	这个命令是在ubuntu10.04安装nginx时遇到的，用于添加最新的nginx源
	格式：add-apt-repository [OPTIONS] REPOSITORY
	man文档：
	REPOSITORY can be either a line that can be added directly to sources.list(5), or in the form ppa:<user>/<ppa-name> for adding Personal Package Archives.
	In the first form, REPOSITORY will just be appended to /etc/apt/sources.list.
	In the second form, ppa:<user>/<ppa-name> will be expanded to the full deb line of the PPA and added into a new file in the /etc/apt/sources.list.d/ directory. 
	执行命令后要记得apt-get update
	eg.sudo add-apt-repository ppa:nginx/stable

`equery`

	Gentoo的命令(Gentoo Package Query Tool)，用于查询Gentoo包的状态、文件、和USE标记


# 系统服务 #

`chkconfig`

`rc-update`




# 网络命令 #

`nc`

	netcat
	传输文件
	nc 192.168.2.100 8888 < test.txt
	nc -l 8888 > test.txt

	扫描主机的tcp端口
	nc -v -z -w2 localhost 20-30 #扫描20~30端口


`traceroute`

	print the route packets trace to network host
	在NAT模式下traceroute都返回* * *
	可以使用ICMP包，发送ICMP包需要有一定的权限，可以用root
	sudo traceroute -I 192.168.1.100


`route`


`iproute2`

	这是一个工具集


`ipcalc`

	计算给定IP地址的相关信息，包括掩码、广播地址等



`tcpdump`

`nscd`

	name service cache daemon
	nscd -i xx # Invalidate the specified cache


# 查找 #

`grep`

	在search_path路径下查找search_content内容
	grep search_content search_path -ri


# 其他 #

`convert`

	这个命令是在一次需要压缩图片时用到了
	e.g:
	convert -resize 50% input.jpg output.png


`chsh`

	Change login shell
	更改当前用户的login shell
	所以这里先开始我用
	sudo chsh -s /bin/fish
	导致没有变化，因为修改的是root的shell
	另外，通过cat /etc/passwd可以看见
	其实就是修改了/etc/passwd的最后一个字段（login shell）


`xargs`
[xargs: How To Control and Use Command Line Arguments](http://www.cyberciti.biz/faq/linux-unix-bsd-xargs-construct-argument-lists-utility/)

	从标准输入获取数据,然后对数据执行命令
	xargs从标准输入读取各个元素
	执行命令,默认是echo命令
	分隔符是空格或者换行符

	常用参数：
	-d 指定分隔符
	-t 在执行前将命令行打印到STDERR
	-I 非常常用的一个参数，用来指定替换符，例子：
	$ find . -name "*.bak" -print0 | xargs -0 -I {} mv {} ~/old.files


`pgrep`

	用于搜索服务的pid


# History #

begin at 2012/09/10
