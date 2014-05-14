---
title: "markdown"
date: 2013-08-17 07:32
---


## MarkDown ##

## About ##

[Markdown](http://daringfireball.net/projects/markdown/) is written by [Perl](http://daringfireball.net/projects/markdown/)  
And there are some implementation by other languages, such as [Python](http://freewisdom.org/projects/python-markdown/), in Gentoo, it is `dev-python/markdown`

## Syntax ##

* [Official Doc](http://daringfireball.net/projects/markdown/syntax)
* [Markdown 语法说明](http://wowubuntu.com/markdown)
* [献给写作者的 Markdown 新手指南](https://reader.mx/p/6529)
* [Markdown语法示例](http://liufeiyu.cn/markdown/2012/12/28/markdown-learning.html)

## Markdown in VIM ##

* [offical-Markdown](http://www.vim.org/scripts/script.php?script_id=2882)
* [plasticboy/vim-markdown](https://github.com/plasticboy/vim-markdown)
* [hallison/vim-markdown](https://github.com/hallison/vim-markdown/tree/changes)

## CSS ##

* [Mou Theme](https://github.com/gcollazo/mou-theme-github2)
* [markdown-github.css](http://uedsky.com/static/css/markdown-github.css)
* [markdown-css](https://github.com/mrcoles/markdown-css)
* [markdowncss](http://kevinburke.bitbucket.org/markdowncss)

## 遇到的问题 ##

### code标签里使用` ###
在md语法里, 反引号(backtick quotes) 本身就是来定义一个 `<code>` 标签, 如果还需要使用它, 可以使用多个反引号来括住.

[官方文档](http://daringfireball.net/projects/markdown/syntax#code) 里给出的样例:

	To include a literal backtick character within a code span, you can use multiple backticks as the opening and closing delimiters:
	``There is a literal backtick (`) here.``

	which will produce this:
	<p><code>There is a literal backtick (`) here.</code></p>


PS: vimwiki好像没解决方法...

### 支持表格 ###
原生的md是不支持表格的, 但是很多第三方实现都已经支持了.

比如md的py实现 [python-markdown2](https://github.com/trentm/python-markdown2) 就可以实现. 可以参考 [官方wiki](https://github.com/trentm/python-markdown2/wiki/wiki-tables)

### 分隔两个pre ###
在md里, 使用 `Tab` 或 `4个空格` 来生成 `<pre>` 标签.  
但是就算中间有空行, 也依然会被放在同一个 pre 里.  

在list列表(ul)里, 如果紧接着pre, 则必须要空两个tab才行.

可以使用 html 的注释 `<!-- comment -->` 来分隔两个 pre

参考: [Separating consecutive code blocks](http://meta.stackoverflow.com/questions/152358/separating-consecutive-code-blocks)


