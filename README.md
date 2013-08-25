# 关于 #

这是我个人的 wiki 文档, 使用 `vim` 和 `markdown` 来记录. 生成器和监控器等都是用 `Python` 写的.

如果大家喜欢, 也可以把这个基本框架拿去用, 我在下面写了详细的使用方法.

# 结构 #

最基本的结构:

	.
	├── html
	│   ├── template
	│   │   └── markdown.tpl    # wiki 的 基本模板, .md文件转换的内容会嵌入这个模板
	│   └── tkwiki
	│       ├── index.html    # 控制页面展示的页面, 包括注册要显示的目录
	│       ├── about.html    # 首页, 这个可以在 index.html 里指定具体用哪个页面当首页
	│       ├── css    # wiki 的 css 目录
	│       ├── js     # wiki 的 js 目录
	│       └── img    # 存放 .md 中使用到的图片的位置, 我暂时直接使用了又拍云(upyun)
	├── tkwiki
	│   ├── python     # 此处不是基本结构, 只是举例如何分目录存放 *
	│   ├── ...
	│   └── tool
	└── tools
		├── comm.py        # 其他脚本用到的一些公共函数等
		├── configs.py     # 注册文件, 设置 wiki 使用到的一些目录路径等
		├── __init__.py
		├── mdgen_all.py   # 把所有的 .md 文件都转换成 .html 文件
		├── mdgen.py       # .md文件生成器. 对指定文件转换成 .html 文件. 具体可以 `-h` 查看使用方法
		└── monitor.py     # wiki 的监控脚本. 用于对修改后的 .md 文件自动生成 .html

wiki 分为三个主目录:

* `tkwiki` -- markdown wiki 文件的目录. 此目录存放的是分类的`子目录`, 所有 .md 文件都存放在自己定义的相应的子目录中
* `html` -- 包括模板, 一些必须的.html文件, 以及markdown 生成的 html 文件的目录
* `tools` -- 里面都是 wiki 的一些工具, 包括 `生成器`, `监控器` 等

# 使用 #

我现在尽量在对 `mdgen.py` 这个 wiki 生成器做优化和改进, 保证大家可以简单的移植过去, 当作自己的 wiki 来使用.

## wiki 结构详细介绍 ##

首先了解下上面介绍的 wiki 结构, 其中 `tkwiki` 是用来分`目录`存放 .md 文件的.

`html` 目录下, `template` 下的 `markdown.tpl` 文件是基本的 html 模板, 大家可以自己定制, 只要别修改其中的 `{{ title  }}` 和 `{{ content  }}` 这两个就行了, 这两个是 mdgen.py 生成器用来嵌套 html 用的.

`html/tkwiki` 是用来存放 css, js, index.html 和生成的 html. 生成的 html 也会同 markdown 文件一样, 存放在同样的目录下. 比如 `tkwiki/tool/tmux.md`, 生成的 html 会放在 `html/tkwiki/tool/tmux.html`.

## 使用介绍 ##

在 `tkwiki` 下建立目录文件夹, 把相应的 .md 文件放在合适的目录里. 写完后, 用生成器生成就可以了, 不需要做额外的操作.

现在首页使用了 [Pagify](https://github.com/cmpolis/Pagify) 这个 jQuery 写的插件, 如果想在首页上显示目录, 必须要在`html/tkwiki/index.html`里注册进去.

注册方法(修改两个地方):

![注册目录](http://wutianqi-wiki.b0.upaiyun.com/wiki_readme_1.png)

![增加目录](http://wutianqi-wiki.b0.upaiyun.com/wiki_readme_2.png)

## 注意点 ##

关于 .md 的格式, 只有一个地方要注意, 首行 **必须** 填写`标题`, 为了方便, mdgen.py 是通过 .md 的首行获取标题的. 格式如下:

	<!-- title : The wiki title -->

这是 html 的注释格式, 所以页面是看不到的, `title` 和 `:` 必须写上, 生成器会做判断, 没有就报错, 冒号后面就是要写的标题, 标题在首页的目录页面会使用到.

其它的地方都是遵循标准的 Markdown 语法, 如有一些无法实现的格式, 如 `table`, 可以直接写 html.

这个地方我改进了很多, 原来的 文件和标题 对应关系, 我是单独维护在一个 .py 文件里, 生成器调用来获取标题, 并且目录的文章列表页面也是手动维护, 现在这里全优化成自动获取并生成了.

关于生成的目录页面, 因为生成器会自动生成, 所以大家不要做其它改动, 生成器对这一块的容错还没写完, 所以如果改了格式, 可能会发生错误操作.

## 依赖 ##

生成器使用 `Python` 写的, 会有一些模块的依赖.

### Python 模块 ###

* argparse : 这个在 `Python2.7` 以后会自带, 如果低于此版本, 需要额外安装. Python 3.x 的我还没测试过, 暂不知道有没有问题.
* markdown2 : markdown 生成引擎, [项目主页](http://github.com/trentm/python-markdown2)
* pyinotify : inotify 是监控文件系统变化的工具. [项目主业](https://github.com/seb-m/pyinotify).

上面可以使用 `pip` (当然首先得安装pip) 或 从各自的`linux发行版的源`里搜索安装(gentoo源测试ok).

	pip install package_name

**Note** : `pyinotify` 是对 `inotify` 封装的 Python 接口. `inotify` 是 Linux内核从 2.6.13 开始引入. 要判断内核是否开启 `inotify` 的支持, 可以看看我总结的 [inotify wiki](http://wiki.wutianqi.com/linux/inotify.html).

### 第三方工具 ###

* daemontools : 一个服务集合的管理工具. 用于监控和管理监控脚本.

## 配置wiki ##

### Nginx 配置 ###

因为都是静态页面, 所以配置非常简单, 给个最简单的样例, 其它优化比如图片和 css/js 的 expires 可以自己设置:

	server
	{
		listen 80;
		server_name wiki.wutianqi.com;
		index index.html index.htm default.html default.htm;
		root /path/to/wiki/html/tkwiki;
	}

### 生成器使用和配置 ###

为了方便, 可以把 mdgen.py 和 mdgen_all.py 放在 `/usr/bin` 下

	sudo ln -s /path/to/mdgen.py /usr/bin/mdgen
	sudo ln -s /path/to/mdgen_all.py /usr/bin/mdgen_all


* 生成 html 文件 : `mdgen -f mdfile`
* html只输出到屏幕 : `mdgen -f mdfile --debug`

其它可以 `mdgen -h` 看, 暂时还没其它功能.

大家如果有兴趣, 可以看看 mdgen.py, 如果有功能改进或逻辑问题, 都可以发 issue 或 email.

### 监控器配置 ###

#### Gentoo ####

安装好 `daemontools` 后会自动在 `根分区` 下建一个 `/service` 目录.

	$ cd /service
	$ mkdir wiki_monitor

	$ vim run # 新建一个叫run的脚本
	#!/bin/sh
	pushd /path/to/wiki/tools
	exec sudo ./monitor.py

	$ rc-update add svscan default

#### Ubuntu ####

TODO

## 截图 ##

![截图](http://wutianqi-wiki.b0.upaiyun.com/wiki_readme_3.png)

给 Sublime Text 2 装过 markdown 预览插件的童鞋肯定看出来了, 这个效果和它基本类似. 

因为我的CSS有一部分引用它的了, 样式非常小清新.


# 站点 #

http://wiki.wutianqi.com

# Email #

	me#tankywoo.com
