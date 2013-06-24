# 查看现在使用的是哪一个shell #

	echo $0


# 修改login shell #

	chsh


# shell快捷键 #

	cd到错误路径时，返回上一个路径：`cd -`


# 关于export C #

	建议在脚本开始处加上export C
	且如果man手册乱码，也可以
	$ export C man xxx


# 查看本机最常用的10条命令 #

	history | awk '{a[$2]++}END{for(i in a){print a[i] " " i}}' | sort -rn | head


# 获取一个字符串的长度 #

	方法1: len#`expr length $str`
	方法2: echo ${str} | wc -L
	方法3: echo ${#str} # 推荐


# 统计当前目录下（包括子目录）以.py结尾文件的个数及总代码行数 #

	文件个数: find . -name "*.py" | wc -l
	单个文件代码行数及总行数: find . -name "*.py" | xargs wc -l


# 输出错误重定向 #

	ls 1>/dev/null 2>/dev/null
	ls >/dev/null 2>&1


# Show number of connections per remote IP #

	netstat -antu | awk '$5 ~ /[0-9]:/{split($5, a, ":"); ips[a[1]]++} END {for (ip in ips) print ips[ip], ip | "sort -k1 -nr"}'


# 以root身份执行上一条命令 #

	sudo !!


# 开启一个Web服务器(传输) #

	# -m 表示找到模块, 执行相应的.py文件
	# SimpleHTTPServer 是一个 Http Server 模块
	python -m SimpleHTTPServer


# 返回上一个目录 #

有时候移到一个目录, 想直接返回去

	cd -


# vim里强制保存 #

有时候, 一些文件编辑后, 才发现只有root可写

	:w !sudo tee %


# 替换上条命令的关键字并执行 #

	# 将上一条命令的pint换成traceroute
	^ping^traceroute^


# 复制一个备份文件 #

有时候, 为了测试, 为防止意外, 可能需要把 filename 在备份一个 filename.bak

	cp filename{,.bak}


# 搜索最近一条符合关键字的命令 #

比如上面执行过命令是ping wutianqi.com, 想再执行, 可以

	# p是关键字, 也可以 pi, pin, ping都行
	!p


# 给远程机器添加公钥认证 #

	ssh-copy-id user@host

	很多人喜欢生成公私钥后, 用scp传过去, 再登录上去设置
	其实完全没必要, ssh-copy-id会自动把公钥添加到~/.ssh/authorized_keys末尾
	如果 ssh-add -L 里面有内容，会优先使用里面的公钥
	其次，可以用 -i 指定要添加的公钥
	最后会用默认的 ~/.ssh/id_rsa.pub


# 把 Linux 桌面录制为视频 #

*TODO* 这个命令先记录一下, 还没尝试

	ffmpeg -f x11grab -s wxga -r 25 -i :0.0 -sameq /tmp/out.mpg


