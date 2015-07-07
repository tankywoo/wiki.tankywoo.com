---
title: "grep"
date: 2013-08-17 07:32
---

格式:

	grep [OPTIONS] PATTERN [FILE...]

	grep [OPTIONS] [-e PATTERN | -f FILE] [FILE...]

`egrep`, `fgrep` 等都是 grep 的变种和扩展:

	egrep == grep -E
	fgrep == grep -F

## 参数 ##

` -e `
This can be used to specify multiple search patterns

` -f `
Obtain patterns from FILE, one per line.

` -i | --ignore-case` : 忽略大小写

` -v `
--invert-match

` -w `
--word-regexp

` -x `
--line-regexp

` -c `
print the match line number

` -m `

` -n, --line-number` : 打印行号

	TankyWoo@Mac-OS::tool/ (master*) » grep 'tankywoo' ssh.md
	                IdentityFile ~/.ssh/tankywoo     # tankywoo就是私钥文件
	TankyWoo@Mac-OS::tool/ (master*) » grep -n 'tankywoo' ssh.md
	42:             IdentityFile ~/.ssh/tankywoo     # tankywoo就是私钥文件

`-R | -r | --recursive` : 递归查询

`-l, --files-with-matches` : 只显示匹配的文件列表

`--include` : 只搜索匹配指定文件名模式的文件。

	# 在 souce/_posts 目录下, 在所有以.makrdown后缀文件里搜索含有tankywoo-wiki字符串的行
	grep -r --include *.markdown 'tankywoo-wiki' source/_posts


## Examples ##

	# The test.file is :
	root@gentoo-jl tmp # cat -n test.file
	     1  TankyWoo
	     2  tankywoo
	     3  tank
	     4  helloworld
	     5  say hello

	root@gentoo-jl tmp # grep -in 'tanky' test.file
	1:TankyWoo
	2:tankywoo

	root@gentoo-jl tmp # grep -in -e 'tanky' -e 'hello' test.file
	1:TankyWoo
	2:tankywoo
	4:helloworld
	5:say hello

	root@gentoo-jl tmp # grep -inv 'tanky' test.file
	3:tank
	4:helloworld
	5:say hello

	root@gentoo-jl tmp # grep -in -w 'sa' test.file
	root@gentoo-jl tmp # grep -in -w 'say' test.file
	5:say hello

	root@gentoo-jl tmp # grep -in -x 'say' test.file
	root@gentoo-jl tmp # grep -in -x 'say hello' test.file
	5:say hello

