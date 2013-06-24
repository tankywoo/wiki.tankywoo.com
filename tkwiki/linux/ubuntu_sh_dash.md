# Ubuntu默认的sh是dash #

今天在执行一段shell脚本时，提示：
`let: not found`

我把代码提取关键部分加精简下：

	#!/bin/bash
	# test.sh
	a=10
	b=5

	let c="$a"-"$b"

	echo $c


然后

	tankywoo@linuxmint ~ $ sh test.sh
	test.sh: 6: test.sh: let: not found


网上查了下，原来是ubuntu下sh是指向dash，而dash不支持let命令


	tankywoo@linuxmint /bin $ whereis sh
	sh: /bin/sh.distrib /bin/sh /usr/share/man/man1/sh.1.gz

	tankywoo@linuxmint /bin $ cd /bin/

	tankywoo@linuxmint /bin $ ls -la | grep sh
	-rwxr-xr-x  1 root root  920788 Apr  3 23:58 bash
	-rwxr-xr-x  1 root root  100284 Mar 30 01:40 dash
	lrwxrwxrwx  1 root root       4 Jul 11 11:20 rbash -> bash
	lrwxrwxrwx  1 root root       4 Jul 11 11:20 sh -> dash
	lrwxrwxrwx  1 root root       4 Jul 11 11:20 sh.distrib -> dash
	lrwxrwxrwx  1 root root       7 Jul 11 11:20 static-sh -> busybox

	可以看到，sh是指向dash的


有两种解决方法:

* bash test.sh
* chmod +x test.sh; ./test.sh
