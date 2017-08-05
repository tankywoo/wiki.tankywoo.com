---
title: "Python 的一些坑"
date: 2017-08-05 16:50
description: "踩踩更健康"
log: "初始"
---

[TOC]

总结平时自己注意到的一些陷阱。以后拿来当面试题也不错：）


## for 循环体的作用域

```python
def func():
    foo = 'aaa'

    bar = ['bbb']
    for foo in bar:
        pass
    print("foo: %s" % foo)

func()
```

输出多少？'aaa' 还是 'bbb'？

答案是 'bbb'，因为 Python 的循环体并不构成单独作用域，和 C/C++ 不一样。

写了好几年才发现这个问题……
