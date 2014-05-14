---
title: "tig"
date: 2013-09-06 11:35
---


> Tig is an ncurses-based text-mode interface for git. It functions mainly as a Git repository browser, but can also assist in staging changes for commit at chunk level and act as a pager for output from various Git commands.

[Tig](http://jonas.nitro.dk/tig/) 官网的介绍.

`Tig` 使用 `vi` 的快捷键模式, 加上和 `Git` 的完美配合, 非常强大.

现在才知道这个工具挺惭愧的, 而且这么优秀的工具, 在国内外的Giter中, 知道也并不是很多, 感觉有点匪夷所思.

## Pager Mode ##

使用 git 的命令, 标准输出使用管道(pipe)重定向到stdin流给tig, 则 tig 可以调用其 pager mode 来显示.

	git show | tig




## 更多资料 ##

* [Tig 官网](http://jonas.nitro.dk/tig/)
* [Tig 官网手册](http://jonas.nitro.dk/tig/manual.html)
* [Tig Github](https://github.com/jonas/tig)
* [git? tig!](http://blogs.atlassian.com/2013/05/git-tig/)
* [Using Tig: A Text Interface for Git](http://ericjmritz.wordpress.com/2013/05/16/using-tig-a-text-interface-for-git/)
* [tig, the ncurses front-end to Git](http://gitready.com/advanced/2009/07/31/tig-the-ncurses-front-end-to-git.html)
