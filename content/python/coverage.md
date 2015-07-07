---
title: "coverage"
date: 2014-06-14 15:00
---

[文档](http://nedbatchelder.com/code/coverage/) | [项目主页](https://pypi.python.org/pypi/coverage)

> Measure, collect, and report on code coverage in Python programs.

主要用于测试代码覆盖率，收集统计生成报表。

安装:

	pip install coverage


常用的一些操作:

执行统计:

	coverage run setup.py -q nosetests

会生成一个`.coverage`的统计文件。然后可以配合其它子命令如`report`显示统计结果。

选项`--branch`, 增加分支覆盖率, 见[文档](http://nedbatchelder.com/code/coverage/branch.html#branch).

清除统计数据：

上面的run命令会生成统计文件，使用`coverage erase`可以清除生成的文件。

生成统计报表:

通过`coverage run`生成的统计文件，显示出统计结果：

	coverage report

coverage也可以将结果生成为html，并且点击html里各个模块的文件名，还可以看到此模块详细的覆盖范围，哪些没有被覆盖到。

	coverage html

还可以转为xml格式

其它命令可参考[Coverage command line usage](http://nedbatchelder.com/code/coverage/cmd.html#cmd)

配置:

coverage的配置文件默认是`.coveragerc`，放在项目根目录下就行，coverage测试时会寻找当前目录下的此配置文件。[文档](http://nedbatchelder.com/code/coverage/config.html#config)

相关项目: [coveralls](https://github.com/coagulant/coveralls-python)

[coveralls.io](https://github.com/coagulant/coveralls-python) 是一个在线显示代码覆盖率统计的服务。
[Code coverage](http://en.wikipedia.org/wiki/Code_coverage)
[代码覆盖率浅谈](http://www.cnblogs.com/coderzh/archive/2009/03/29/1424344.html)
