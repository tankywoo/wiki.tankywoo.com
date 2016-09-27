---
title: "Python2 编码问题"
date: 2016-09-27 21:10
updated: 2016-09-27 21:10
log: ""
---

Python 2.X的编码问题，一直很令人恼火。

以前在博客写过一篇 [Python Encoding](https://blog.tankywoo.com/2015/01/21/python-encoding.html)，找个时间迁移过来。

今天(2016-09-27)看同事的一个代码时又遇到一个之间没注意的问题，说白了还是编码这块没完全弄透彻。

大致是这样：

```python
# python 2.7
for a, b, c in args:
    print a, b, c  # a is unicode, b/c is str
```

手动测试写stdout没问题；加到crontab写/dev/null就出现编码问题。

原因是stdout支持写utf-8，如果不支持也会报错。A subtle problem causing even print to fail is having your environment variables set wrong, eg. here LC_ALL set to "C" [参考](http://stackoverflow.com/a/20334767/1276501)

而如果要写文件的话，要么encode转为str，要么如使用`codecs.open("filename", "w", "utf-8")`打开文件句柄时指定编码方式，我在simiki项目也都是这么处理了。

一个不推荐的方法就是修改全局的默认编码(默认是ascii)：

```python
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
```

参考:

* [Python 2.7 Unicode HOWTO](https://docs.python.org/2.7/howto/unicode.html)
* [Overcoming frustration: Correctly using unicode in python2](https://pythonhosted.org/kitchen/unicode-frustrations.html) 
* [Unicode error when outputting python script output to file](http://stackoverflow.com/questions/10018271/unicode-error-when-outputting-python-script-output-to-file)
* [Setting the correct encoding when piping stdout in Python](http://stackoverflow.com/questions/492483/setting-the-correct-encoding-when-piping-stdout-in-python)
* [Why should we NOT use sys.setdefaultencoding(“utf-8”) in a py script?](http://stackoverflow.com/questions/3828723/why-should-we-not-use-sys-setdefaultencodingutf-8-in-a-py-script)
