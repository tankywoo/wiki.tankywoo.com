# 关于 #

这是我个人的 wiki 文档, 使用 `vim` 和 `markdown` 来记录.

如果大家喜欢, 也可以把这个基本框架拿去用, 我在下面写了详细的使用方法.

# 结构 #

最基本的结构:

	.
	├── html
	│   ├── template
	│   │   └── markdown.tpl
	│   └── tkwiki
	│       ├── css
	│       │   └── style.css
	│       ├── img
	│       ├── index.html
	│       └── js
	│           ├── jquery.js
	│           └── pagify.js
	├── README.md
	├── tkwiki
	│   ├── python(此处不是基本结构, 只是举例如何分目录存放)
	│   ├── ...
	│   └── tool
	└── tool.py

* `tkwiki` -- markdown wiki 文件的目录
* `html` -- markdown 生成的 html 文件的目录
* `template` -- html 模板目录, 生成的 html 嵌套进这个模板
* `tool.py` -- markdown2html 生成器

# 使用 #

我现在尽量在对 `tool.py` 这个 wiki 生成器做优化和改进, 保证大家可以简单的移植过去, 当作自己的 wiki 来使用.

## wiki 结构详细介绍 ##

首先了解下上面介绍的 wiki 结构, 其中 `tkwiki` 是用来分`目录`存放 .md 文件的.

`html` 目录下, `template` 下的 `markdown.tpl` 文件是基本的 html 模板, 大家可以自己定制, 只要别修改其中的 `{{ title  }}` 和 `{{ content  }}` 这两个就行了, 这两个是 tool.py 生成器用来嵌套 html 用的.

`html/tkwiki` 是用来存放 css, js, index.html 和生成的 html. 生成的 html 也会同 markdown 文件一样, 存放在同样的目录下. 比如 `tkwiki/tool/tmux.md`, 生成的 html 会放在 `html/tkwiki/tool/tmux.html`.

## 使用介绍 ##

在 `tkwiki` 下建立目录文件夹, 把相应的 .md 文件放在合适的目录里. 写完后, 用生成器生成就可以了, 不需要做额外的操作.

现在首页使用了 [Pagify](https://github.com/cmpolis/Pagify) 这个 jQuery 写的插件, 如果想在首页上显示目录, 必须要在`html/tkwiki/index.html`里注册进去.

注册方法(修改两个地方):

![注册目录](http://wutianqi-wiki.b0.upaiyun.com/wiki_readme1.png)

![增加目录](http://wutianqi-wiki.b0.upaiyun.com/wiki_readme2.png)

## 注意点 ##

关于 .md 的格式, 只有第一个地方要注册, 首行 *必须* 填写`标题`, 为了方便, tool.py 是通过 .md 的首行获取标题的. 格式如下:

	<!-- title : The wiki title -->

这是 html 的注释格式, 所以页面是看不到的, `title` 和 `:` 必须写上, 生成器会做判断, 没有就报错, 冒号后面就是要写的标题, 标题在首页的目录页面会使用到.

其它的地方都是遵循标准的 Markdown 语法, 如有一些无法实现的格式, 如 `table`, 可以直接写 html.

这个地方我改进了很多, 原来的 文件和标题 对应关系, 我是单独维护在一个 .py 文件里, 生成器调用来获取标题, 并且目录的文章列表页面也是手动维护, 现在这里全优化成自动获取并生成了.

关于生成的目录页面, 因为生成器会自动生成, 所以大家不要做其它改动, 生成器对这一块的容错还没写完, 所以如果改了格式, 可能会发生错误操作.

## 依赖 ##

生成器使用 `Python` 写的, 会有一些模块的依赖.

* argparse : 这个在 `Python2.7` 以后会自带, 如果低于此版本, 可能需要额外安装. Python 3.x 的我还没测试过, 暂不知道有没有问题.
* markdown2 : markdown 生成引擎, [项目主页](http://github.com/trentm/python-markdown2)

## wiki 生成器使用方法 ##

为了方便, 可以把 tool.py 放在 `/usr/bin` 下

	sudo ln -s /path/to/tool.py /usr/bin/mdgen

我取名是叫 mdgen, 这个可以随便设置

* 生成 html 文件 : `mdgen -f mdfile`
* html只输出到屏幕 : `mdgen -f mdfile --debug`

其它可以 `mdgen -h` 看, 暂时还没其它功能.

大家如果有兴趣, 可以看看 tool.py, 如果有功能改进或逻辑问题, 都可以发 issue 或 email.

## Nginx 的配置 ##

因为都是静态页面, 所以配置非常简单, 给个最简单的样例, 其它优化比如图片和 css/js 的 expires 可以自己设置:

	server
	{
		listen 80;
		server_name wiki.wutianqi.com;
		index index.html index.htm default.html default.htm;
		root /path/to/wiki;
	}

# 站点 #

http://wiki.wutianqi.com

# Email #

	echo bWVAdGFua3l3b28uY29tCg== | base64 -d
