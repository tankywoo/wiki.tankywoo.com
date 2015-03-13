---
title: "Python Debug"
date: 2013-08-17 07:39
---


## PDB (The Python Debug) ##

Python自带的调试器, 常用的几种调用方法:

命令行调用模块:

    python -m pdb myscript.py

如果代码异常退出, pdb会自动进入`post-mortem debugging`

交互模式下:

    >>> import pdb
    >>> import mymodules
    >>> pdb.run('mymodules.test()')

临时插入断点:

    import pdb
    pdb.set_trace()

检查一个崩溃的代码:

    >>> import pdb
    >>> import test_pdb
    >>> test_pdb.fun(100, 'hello pdb')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "test_pdb.py", line 9, in fun
        print(2/0)
    ZeroDivisionError: integer division or modulo by zero
    >>> pdb.pm()
    > /Users/TankyWoo/dev_env/debug/test_pdb.py(9)fun()
    -> print(2/0)
    (Pdb) a
    var1 = 100
    var2 = hello pdb
    (Pdb)

`pdb.pm()` 会根据`sys.last_traceback`寻找最近一次的traceback对象, 并进入`post-mortem debugging`.

`pdb.post_mortem([traceback])和`pdb.pm()`类似，但是需要把traceback作为参数, 为空则认为是当前处理的exception.


`post-mortem debugging`: 事后调式, 如果程序发生异常, 不会退出程序, 而是保存之前的环境并进入调式模式. 不需要设置断点, 可以方便的到异常代码，进行调试.

关于debug时的交互式命令, 按`h(elp)`会列出所有命令, 有些命令是同一个, 只是一个全称、一个简称. `h(elp) command`可以查看命令的详细说明.

* `c`/`cont`/`continue`: 执行代码, 直到一个断点处. 在post-mortem debugging下, 会自动停在异常代码处.
* `a`/`args`: 打印当前函数的参数值
* `l`/`list`: 列出当前调试行前后共11行代码, 也可以指定起始、终止的代码行数
* `n`/`next`: 在当前函数内逐行执行
* `s`/`step`: 逐行执行, 如果调用其它函数, 会进入相应函数
* `b`/`break`: 设置断点, 后接行号(1开始)或函数名, 不接则显示所有的断点
* `cl`/`clear`: 清除断点, 后者 文件名:行号 或者 断点号, 都可以通过`b`看到
* ... TODO

推荐文档:

* [pdb官方文档](https://docs.python.org/2/library/pdb.html)
* [PyMOTW - pdb](http://pymotw.com/2/pdb/)
* [常用的 Python 调试工具](http://blog.jobbole.com/51062/?replytocom=42831)

知乎的这个[帖子](http://www.zhihu.com/question/21572891)和[像老大一样调试Python](http://blog.jobbole.com/52171/)还推荐到了`pudb`和`ipdb`.

这两个都是非常强大好用的调试工具.

[`pudb`](https://pypi.python.org/pypi/pudb) 风格上类似vi, 多窗口操作, 方便一边看代码, 一遍调试, 还可以执行调用相关的交互解释器, 这些都可以通过`Ctrl-P`配置. UI上感觉像当年用过的Turbo C.

[`ipdb`](https://pypi.python.org/pypi/ipdb)更像是`pdb`的加强版, ipython和pdb的结合体, 可以直接取代pdb来使用.


