---
title: "Go 资源汇总"
date: 2017-08-10 14:50
updated: 2017-09-12 18:30
description: "包括资源、文章、问题"
log: "新增pkg manage资源"
---

## 资源/文章

### 全面型

- [The Go Programming Language Specification](https://golang.org/ref/spec)
- [a8m/go-lang-cheat-sheet](https://github.com/a8m/go-lang-cheat-sheet)


## 入门练手项目

* [gobyexample](https://gobyexample.com/)
* [初学Go语言，哪类小项目适合练手](https://segmentfault.com/q/1010000002481792)  介绍 [swapview](https://github.com/lilydjwg/swapview) 查看系统每个进程的 swap 使用情况
* [go语言值得学习的开源项目推荐](http://www.cnblogs.com/baiyuxiong/p/4309934.html)  提到 Go 在 Github 上维护的一个 [Go 优秀项目列表](https://github.com/golang/go/wiki/Projects)
* [有什么适合 Go 语言初学者的 Starter Project？](https://www.zhihu.com/question/33241133)


### import 包

- [What does an underscore in front of an import statement mean in Golang?](https://stackoverflow.com/questions/21220077/what-does-an-underscore-in-front-of-an-import-statement-mean-in-golang)
- [What does the '.' (dot or period) in a Go import statement do?](https://stackoverflow.com/questions/6478962/what-does-the-dot-or-period-in-a-go-import-statement-do)


### json 相关

- [What is the usage of backtick in golang structs definition?](https://stackoverflow.com/questions/30681054/what-is-the-usage-of-backtick-in-golang-structs-definition)


### 命令行参数

- [Golang-使用命令行参数](http://www.nljb.net/default/Golang-%E4%BD%BF%E7%94%A8%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%8F%82%E6%95%B0/)
- [golang 命令行处理](http://studygolang.com/articles/2878)

### json 处理

- [Go 处理 JSON](http://n.thepana.com/2015/10/21/go-json/)
- [astaxie/build-web-application-with-golang](https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/07.2.md)
- [golang - 解析复杂json](https://segmentfault.com/q/1010000000583211)
- [golang解析创建复杂嵌套的json数据](http://xiaorui.cc/2016/03/06/golang%E8%A7%A3%E6%9E%90%E5%88%9B%E5%BB%BA%E5%A4%8D%E6%9D%82%E5%B5%8C%E5%A5%97%E7%9A%84json%E6%95%B0%E6%8D%AE/)

### yaml 处理

- [A tour of YAML parsers for Go](http://sweetohm.net/article/go-yaml-parsers.en.html)
- [golang使用yaml格式解析构建配置文件](http://xiaorui.cc/2016/03/20/golang%E4%BD%BF%E7%94%A8yaml%E6%A0%BC%E5%BC%8F%E8%A7%A3%E6%9E%90%E6%9E%84%E5%BB%BA%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6/)
- [The right way to handle YAML in Go](http://ghodss.com/2014/the-right-way-to-handle-yaml-in-golang/)

### Go包依赖管理

- [官方给出的这类工具列表](https://github.com/golang/go/wiki/PackageManagementTools)
- [govendor](https://github.com/kardianos/govendor)
- [glide](https://github.com/Masterminds/glide)
- [Go Vendoring Tools 使用总结](http://www.grdtechs.com/2016/05/24/comparison-of-Go-Vendoring-Tools/)
- [大家推荐哪种golang包管理方式？](https://gocn.io/question/9)  讨论
- [Should I add "vendor" directory into .gitignore if I am using tools like glide or godep ?](https://www.reddit.com/r/golang/comments/6b9817/should_i_add_vendor_directory_into_gitignore_if_i/)  讨论

最后一个问题，需要将 vendor 目录加入 git 中吗？包括参考了 [github上一些大的golang项目](https://github.com/search?l=&p=1&q=language%3AGo+stars%3A%3E1000+forks%3A%3E50&ref=advsearch&type=Repositories&utf8=%E2%9C%93)，有的项目压根不存 vendor，有的只存了 `vendor/vendor.json`，也有的将整个 vendor 目录都加入 git 中了。

虽然帖子里有提到都是文本不会很大，但是实际并不是这样，比如我用了 `github.com/mattn/go-sqlite3` 这个包，里面有一个 sqlite3-binding.c 占了 6.8M。

## Q&A

### Go get 被 X 的解决

```
http_proxy=127.0.0.1:8123 https_proxy=127.0.0.1:8123 go get -u ...
```

注意有些地址是 https 的，所以将两个都配置了。

参考：

* [GoGetProxyConfig](https://github.com/golang/go/wiki/GoGetProxyConfig)
* [Set proxy when executing “go get” command](http://nanxiao.me/en/set-proxy-when-executing-go-get-command/)


### 关于单引号和双引号

如果是单引号，'b'，则输出98
如果是双引号，"b"，则输出b

参考<http://stackoverflow.com/a/34691123/1276501>:

> In Go, `'⌘'` represents a single character (called a Rune), whereas `"⌘"` represents a string containing the character `⌘`. 
> This is true in many programming languages where the difference between strings and characters is notable, such as C++.
> Check out the "Code points, characters, and runes" section in the [Go Blog on Strings](https://blog.golang.org/strings)
