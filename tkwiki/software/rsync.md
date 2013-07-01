# rsync #

rsync - a fast, versatile, remote (and local) file-copying tool

Usages with just one SRC arg and no DEST arg will list the source files instead of copying.

广泛用于`备份(backup)`和`镜像(mirror)`

支持本地或远程复制, 有`shell`和`rsync daemon`两种方式

* remote shell
	+ via ssh or rsh
	+ the source or destination path contains a single colon (:) separator after a host specification
* rsync daemon
	+ via TCP
	+ the source or destination path contains a double colon (::) separator after a  host  specification
	+ OR  when  an rsync://  URL  is  specified
