---
layout: page
title: "Sphinx"
date: 2015-04-19 19:30
---

[TOC]

[Sphinx](http://sphinx-doc.org/)是一个Python文档构建工具, 使用的标记语言是[reStructuredText](http://docutils.sourceforge.net/rst.html).

安装:

    pip install Sphinx

当前版本: `Sphinx 1.3.1`

## 初始化文档项目 ##

使用自带的 `sphinx-quickstart` 命令快速构建文档项目, 相当于傻瓜式的安装指引, 把一些主要的配置根据个人定义写入`conf.py`.

其中:

    You have two options for placing the build directory for Sphinx output.
    Either, you use a directory "_build" within the root path, or you separate
    "source" and "build" directories within the root path.
    > Separate source and build directories (y/n) [n]:

这一步是选择文档的结构, 默认no是把源文件直接放在根目录下, 生成文件放在根目录下的`_build`目录:

    $  tree
    .
    ├── Makefile
    ├── _build
    ├── _static
    ├── _templates
    ├── conf.py
    └── index.rst

yes是把源文件和生成文件分两个目录存放:

    $  tree
    .
    ├── Makefile
    ├── build
    └── source
        ├── _static
        ├── _templates
        ├── conf.py
        └── index.rst

<!-- -->

    Inside the root directory, two more directories will be created; "_templates"
    for custom HTML templates and "_static" for custom stylesheets and other static
    files. You can enter another prefix (such as ".") to replace the underscore.
    > Name prefix for templates and static dir [_]:

* `_templates` 用于存放自定义HTML模板文件
* `_static` 用于存放静态文件, 如css文件等


    Sphinx has the notion of a "version" and a "release" for the
    software. Each version can have multiple releases. For example, for
    Python the version is something like 2.5 or 3.0, while the release is
    something like 2.5.1 or 3.0a1.  If you don't need this dual structure,
    just set both to the same value.
    > Project version: 0.1
    > Project release [0.1]:


TODO 这块应该有作用, 考虑下应用场景.


    If the documents are to be written in a language other than English,
    you can select a language here by its language code. Sphinx will then
    translate text that it generates into that language.

    For a list of supported codes, see
    http://sphinx-doc.org/config.html#confval-language.
    > Project language [en]: zh_CN

国际化的配置, 这里我选择了`zh_CN` 简体中文

Sphinx的 [Overview Tutorial](http://sphinx-doc.org/tutorial.html), 国内有翻译的[中文版](http://www.pythondoc.com/sphinx/tutorial.html) 或者 [中文版2](http://zh-sphinx-doc.readthedocs.org/en/latest/tutorial.html)


    One document is special in that it is considered the top node of the
    "contents tree", that is, it is the root of the hierarchical structure
    of the documents. Normally, this is "index", but if your "index"
    document is a custom template, you can also set this to another filename.
    > Name of your master document (without suffix) [index]:

索引文件, 默认是 `./index`

    A Makefile and a Windows command file can be generated for you so that you
    only have to run e.g. `make html' instead of invoking sphinx-build
    directly.
    > Create Makefile? (y/n) [y]:
    > Create Windows command file? (y/n) [y]:

Sphinx提供了Unix/Linux下的Makefile和Windows下的make.bat, 用于封装了一些常用的命令

---

## 主题 ##

官方提供了一些[内置主题](http://sphinx-doc.org/theming.html)可以选择.

直接修改`conf.py`的`html_theme`的选项.

部分主题有一些可定制的选项, 参考文档即可.

---

文档:

1. Overview Tutorial [官方](http://sphinx-doc.org/tutorial.html) | [中文1](http://www.pythondoc.com/sphinx/tutorial.html) | [中文2](http://zh-sphinx-doc.readthedocs.org/en/latest/tutorial.html)
2. [文档与笔记利器 reStructuredText 和 Sphinx](http://qixinglu.com/post/note_tools_restructuredtext_sphinx.html)
3. [A ReStructuredText Primer](http://docutils.sourceforge.net/docs/user/rst/quickstart.html)
4. [Quick reStructuredText](http://docutils.sourceforge.net/docs/user/rst/quickref.html)
5. [Markdown和reStructuredText语法比较](http://www.cnblogs.com/youxin/p/3597229.html)
6. [Markdown And RestructuredText](https://github.com/windfire-cd/note/blob/master/rst_mkd/rst_mkd.rst)
