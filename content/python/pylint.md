---
title: "Pylint"
date: 2014-08-26 09:04
---

[Pylint](http://www.pylint.org):

* 检查代码规范, 参考[PEP8](http://legacy.python.org/dev/peps/pep-0008/)
* 错误检查, 如模块是否导入等
* 自定义配置，根据个人习惯可以选择性的修改一些规范或忽略错误等
* 给予一些可以重构的提示
* 有配套的编辑器/IDE插件
* ...

pylint 的 `--help` 有简单的帮助，`--long-help` 或 man手册以及[官方文档](http://docs.pylint.org/)有更详细的解释.

官方的入门教程 [Pylint Tutorial](http://docs.pylint.org/tutorial.html)

## 配置文件 ##

默认没有配置文件, pylint会使用默认的配置.

通过`--generate-rcfile`生成一份简单的配置文件，然后在这基础上进行自定义修改.

通过`--rcfile`指定配置文件，如果没有指定，则会查找`~/.pylintrc`和`/etc/pylintrc`

**TODO** 自定义配置并托管到.dotfiles

## 原生的结果输出分析 ##

analysis message section 输出格式:

    MESSAGE_TYPE: LINE_NUM:[OBJECT:] MESSAGE

其中`MESSAGE_TYPE`的解释:

    * (C) convention, for programming standard violation
    * (R) refactor, for bad code smell
    * (W) warning, for python specific problems
    * (E) error, for probable bugs in the code
    * (F) fatal, if an error occurred which prevented pylint from doing further processing.

样例:

    tankywoo@gentoo-local::simiki/ (master) » pylint simiki/utils.py
    No config file found, using default configuration
    ************* Module simiki.utils
    W: 55, 0: TODO: OSError: [Errno 17] File exists: '/home/tankywoo/simiki/html/css' (fixme)
    C:  1, 0: Missing module docstring (missing-docstring)
    C: 11, 0: Invalid constant name "logger" (invalid-name)
    C: 28, 0: Missing function docstring (missing-docstring)
    C: 59, 8: Invalid variable name "s" (invalid-name)
    C: 70, 8: Invalid variable name "p" (invalid-name)
    C: 73,12: Invalid variable name "fp" (invalid-name)
    W: 78,19: Catching too general exception Exception (broad-except)
    W: 77,16: Specify string format arguments as logging function parameters (logging-not-lazy)


接下来是一些分析报表:

`Duplication`表显示了是否有重复的行，根据这个指标可以判断是否有可以抽离出来的部分，进行重构。这里有个key叫`nb duplicated lines`, 看了下源码，还是没找到这个`nb`是什么意思.

`Messages by category` 对上面的analysis message进行汇总，列出R, W, E, C的分别有多少.

`Messages` 根据 msg id进行汇总

`Global evaluation` 是对检查的代码进行评分，满分10分

`Raw metrics` 分析代码中的实际行数、文档字符串、注释、空行等分别有多少行，百分比是多少

`Statistics by type` 分析有多少个module, class, method, function

上面的一些tables中有`previous`，可以和前一次的做对比，这个数据是存在`~/.pylint.d/`, 由环境变量`PYLINTHOME`控制.

## 经验 ##

针对analysis message, 如果想要看详细的解释, 可以:

    pylint --help-msg=[方括号里的短语]

如:

    tankywoo@gentoo-local::simiki/ (master) » pylint simiki/utils.py --help-msg=missing-docstring
    No config file found, using default configuration
    :missing-docstring (C0111): *Missing %s docstring*
      Used when a module, function, class or method has no docstring.Some special
      methods like __init__ doesn't necessary require a docstring. This message
      belongs to the basic checker.

也可以在[这个页面](http://pylint-messages.wikidot.com/all-messages) 找到对应的MSG ID以及详细的说明.

对于`--include-ids`这个选项，可以输出MSG ID, 不过新版本不让用了...

report tables太长了，如果不关心这个，可以用`-rn`关闭.

`--output-format` 指定输出的格式, 默认是text, 可选:

* text
* parseable 可解析的格式, 这种方式已被弃用
* colorized 终端高亮显示
* msvs (visual studio) 已被弃用
* html 输出为html, 可重定向保存然后浏览器打开

`--msg-template` 可以修改输出信息的模板，默认见上面提到的. 可参考[页面](http://docs.pylint.org/output.html)

@TODO:

如果导入的第三方模块都是在`virtualenv`中安装，则`pylint`也应该在virtualenv中安装。

如果pylint是全局安装, 虽然进入了virtualenv, `sys.path`也有virtualenv安装模块的路径，但是依然会报Warning, 提示模块找不到.

## 其它类似工具 ##

@TODO, 待尝试.

PyChecker ?
[Pyflakes](https://pypi.python.org/pypi/pyflakes) 使用Vim插件, 对一些语法和运行时错误检查, 比较好用.
[PEP8](https://pypi.python.org/pypi/pep8) 针对PEP8的一些检查.
[Flake8](https://pypi.python.org/pypi/flake8) 是Pyflakes和PEP8的集合.
[Syntastic](https://github.com/scrooloose/syntastic) 听说很强大?

讨论:

* [PyLint, PyChecker or PyFlakes?](http://stackoverflow.com/questions/1428872/pylint-pychecker-or-pyflakes)
* [Static Code Analizers for Python](http://doughellmann.com/2008/03/01/static-code-analizers-for-python.html)
