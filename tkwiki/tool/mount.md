mount, 用于挂载到文件系统

常用操作：
mount -t type device dir

mount [-l] [-t type]
可以列出挂载列表中指定的类型


/etc/fstab是启动时读取的挂载列表

具体可看/etc/fstab的注释和`man fstab`

/etc/mtab是正在挂载的文件

参考：

* [fstab and mtab](http://www.brunolinux.com/02-The_Terminal/Fstab_and_Mtab.html)

# History #
Create 2013/01/27

Last modified 2013/01/27
