# 还原到某个版本 #

* svn up -r 版本号
* svn up -r 版本号 文件名

# 撤销修改 #

* svn revert

# diff比较 #

* svn diff					#将修改后和未修改的比较
* svn diff -r 5				#将本地代码和版本好为5的所有文件比较
* svn diff -r 5 a.txt		#将本地代码和版本号为5的a.txt文件比较
* svn diff -r 5:9			#将比较版本5和版本9之间所有文件比较
* svn diff -r 5:9 a.txt		#将版本5和版本9之间的a.txt文件比较

# 查看log #

* svn log			#查看所有的log信息
* svn log -r 5:9	#只查看版本5和版本9的日志信息
* svn log a.txt		#查看文件a.txt的日志修改信息;
* svn log -v dir	#查看目录的日志修改信息,需要加v;

# svn使用vimdiff #

在 [git](git.html) 里提到了git使用vimdiff替换默认的diff工具, svn也可以实现

首先可以写一个小脚本:

	#!/bin/sh
	# 配置你喜欢的diff程序路径
	DIFF="vimdiff"
	# SVN diff命令会传入两个文件的参数 
	LEFT=${6}
	RIGHT=${7}
	# 拼接成diff命令所需要的命令格式
	$DIFF $LEFT $RIGHT

可以把脚本放到/usr/bin/svndiff, 然后增加`x`权限

接着修改svn本地用户配置文件`~/.subversion/config`, 里面有这么一行:

	# diff-cmd = diff_program (diff, gdiff, etc.)

改为

	diff-cmd = /usr/bin/svndiff

然后就可以了

参考了:

* [更换svn diff为vimdiff](http://www.ccvita.com/445.html)
* [使用vimdiff作为svn diff的默认工具](http://www.blogjava.net/stone2083/archive/2011/05/24/350917.html)

# 修改历史 #

* 2013-06-25 : 增加了vimdiff方法
