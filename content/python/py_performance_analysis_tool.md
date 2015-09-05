---
title: "Python Performance Analysis Tool"
date: 2013-08-17 07:39
---


Python 性能分析工具

## timeit ##

timeit 模块提供了简单的接口来测量小段代码的执行时间.

    import timeit

    print 'timeit.timeit:'
    timeit.timeit(stmt="print 'main statement'", setup="print 'setup'", number=2)

    t = timeit.Timer("print 'main statement'", "print 'setup'")

    print '----------'
    print 'timeit.Timer.timeit:'
    print t.timeit(2)

    print '----------'
    print 'timeit.Timer.repeat:'
    print t.repeat(3, 2)

timeit可以简单的直接调用`timeit`/`repeat`函数, repeat就是重复调用timeit N次.

看源码就知道, timeit()实际就是:

    Timer(stmt, setup, timer).timeit(number)

timeit的Timer类接口分别是一个要执行的语句和初始化语句, timeit成员函数提供一个反复执行语句的次数(默认1000000次)和重复执行timeit的次数.

也支持命令行参数:

    $ python -m timeit -n <number> -r <repeat> -s <setup> <statement>

> If -n is not given, a suitable number of loops is calculated by trying successive powers of 10 until the total time is at least 0.2 seconds.

如果没有设置-n, 则会以10倍数尝试，直到总耗时超过0.2s

    $ python -m timeit  -r 2 -s "print 'setup'" pass
    repeat(None, 10)
    setup
    repeat(None, 100)
    setup
    repeat(None, 1000)
    setup
    repeat(None, 10000)
    setup
    repeat(None, 100000)
    setup
    repeat(None, 1000000)
    setup
    repeat(None, 10000000)
    setup
    repeat(None, 100000000)
    setup
    repeat(None, 100000000)
    setup
    repeat(None, 100000000)
    setup
    100000000 loops, best of 2: 0.0145 usec per loop

后面的pass语句可以不写，默认就是pass. repeat(None, xxx)这个是我在源码里添加的调试语句, 可以看出没有指定-n时的情况. -r没指定默认是3次, 这里指定了2次, 所以最后是best of 2.

更多:

* [timeit – Time the execution of small bits of Python code](https://pymotw.com/2/timeit/)
* [How to Time Small Pieces of Python Code with timeit](http://www.blog.pythonlibrary.org/2014/01/30/how-to-time-small-pieces-of-python-code-with-timeit/)

## profile ##

TODO

## pstats ##

TODO
