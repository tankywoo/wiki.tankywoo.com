# mdgen #

* 修改/添加/删除 的 日志功能
	+ 比如修改了一个.md, 则可以在首页显示 xxx 时间 修改了xxx.md
	+ 获取方式:
		- notipy (使用这种)
		- md5 变化
		- git log (更倾向这种)
		- github 接口
	+ daemon :
		- daemon tools (使用这种)
		- pyinotify 自带的 daemonize
* bug: 没有考虑更新 title 的情况


# wiki #

* x-windows.wiki还没有完成
* python built-in(python\_builtin.wiki)
* tool
	+ ethtool
	+ e2label
	+ dump2efs
	+ tune2fs
	+ pdsh
	+ pssh


# 其它 #

* 全局生成的脚本
* html 只考虑维护md文件和基本的html/css/js文件, 生成的html不再纳入版本库
