# SSH Tunnel #


## 本地绑定端口从ssh转发出去 #

可以让未加密的数据, 全部通过 ssh端口 **转发** 出去

`-D [bind_address:]port`

例如想让 8080 端口的数据, 全部从 ssh端口传到远程主机, 可以:

	ssh -D 8080 user@host

TODO : 这么做, 远程如何区别 ssh 连接的包 和 转发的包?

## 本地端口转发 ##

假设有 A, B, C 三台主机, A 和 B 因为某种原因(比如GFW), 无法直接从 A 访问 B.

但是 A 和 C 可以互联, 且 B 和 C 也可以互联.

这时就可以通过 C 做 **跳板** , 从而从 A 访问 C.

ssh 翻墙就是这么做的.

在主机 A 上执行命令:

	ssh -L 8080:host_B:80 [user_C@]host_C

语法: `-L [bind_address:]port:host:hostport`

`-L` 表示 Local(L), 即本地转发.

执行命令后, 相当于通过 localhost:8080, 就可以访问主机 B 的 80 端口资源.

## 远程端口转发 ##

依然假设是上面 A, B, C 三台主机.

A 和 B 无法互联, 而 C 是一台内网主机, 可以访问 A, 但是 A 无法访问 C.

这时可以在主机 C 上, 做端口转发, 这样 A 就依然可以通过 C 访问 B 了.

在主机 C 上执行命令:

	ssh -R 8080:host_B:80 [user_A@]host_A

语法: `-R [bind_address:]port:host:hostport`

`-R` 表示 Remote(R), 即远程转发

这时命令中的第一个端口是远程主机(相对于C, A就是远程主机)的端口.

相当于在主机 C 上, 建立一个反向隧道, 在主机 A 访问本地端口 8080 时, 相当于访问主机 B 的 80 端口.

# putty #

# 参考资料 #

* [SSH原理与运用（二）：远程操作与端口转发](http://www.ruanyifeng.com/blog/2011/12/ssh_port_forwarding.html) *
* [Ssh隧道技术](http://emmoblin.github.io/blog/2013/02/19/ssh-tunnel/)
* [SSH隧道与端口转发及内网穿透](http://blog.creke.net/722.html) *
* [Linux下建立SSH隧道做Socket代理](http://gnailuy.com/2011/08/02/linux%E4%B8%8B%E5%BB%BA%E7%AB%8Bssh%E9%9A%A7%E9%81%93%E5%81%9Asocket%E4%BB%A3%E7%90%86/)
* [三种不同类型的ssh隧道](http://codelife.me/blog/2012/12/09/three-types-of-ssh-turneling/) *
* [SSH tunnel tips](http://blog.pluskid.org/?p=369) *

# 修改历史 #

* 2013-07-29 : 创建
