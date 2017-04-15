---
title: "ranger"
date: 2017-04-15 11:15
collection: "其它"
---

[TOC]

之前偶然在一个知乎专栏看到推荐 [MC](https://midnight-commander.org/)，一个终端文本模式的文件浏览/管理工具。觉得这类工具还是挺方便的，毕竟长期都是在终端下工作，有时目录太多或太深。

所以简单了解了下这方面的工具，除了上面的 MC，另外一个就是 [ranger](http://ranger.nongnu.org/)。

因为 ranger 支持 vim mode，所以选择了尝试下它，之前只限于安装后简单试试，今天看了下它的 man 手册，觉得功能/默认快捷键上还是挺符合我的习惯的。

ranger 默认会生成一些基本配置在 `~/.config/ranger/` 下，也可以通过 `ranger --copy-config=???` 来指定从默认配置目录中复制哪些文件。


## 快捷键

下面列出一些我觉得常用的快捷键，具体还是建议直接 man ：

移动：也是我选择的原因，支持 vim mode，比如 `h`、`j`、`k`、`l`、`gg`、`G` 等操作。

复制、剪切、粘贴、删除：`yy` 复制当前文件，还有相关的 `ya` 表示 copy mode 是 add file to copy buffer，`yr` 表示 copy mode 是 remove file from copy buffer。感觉 `yy` 和 `ya` 效果是一样 （也许 `yy` 是 copy 类操作的默认，也就是 add）。本地使用默认配色，`yy` 后，文件名颜色会改为黑色，`yr` remove 后恢复正常。`dd` 是剪切；`pp` 是粘贴，如果同级目录下有同名文件，则不覆盖，加了一个后缀，如果是 `po` 则覆盖。`dD` 是删除文件。

编辑文件：光标在指定文件直接 `E`，使用 `$EDITOR` 环境变量设置的编辑器打开，修改完后保存退出，会返回 ranger。

开启一个 Shell：在非 Tmux 的情况下，会 fork 一个 shell 子进程，进程退出后返回 ranger；在 Tmux 的情况下，会新建一个 Window。

书签：`mX` 即 `m` 后接一个字符（比如大小写字母、数字等），给当前所在目标打一个书签并给予一个书签名，后续可以 \`X （因为转义，就没用 code 标签了）来快速跳转到指定书签，和 jump 工具类似。标签是持久存储的，文件在 `~/.config/ranger/bookmarks`。

标记文件：使用 `Space` 空格，标记后背景高亮，但是注意这个是临时操作，退出 ranger 后就没了。

文件排序：`o`，方法和 mutt 一样。这个功能也非常赞，在工作中使用 mutt 处理报警邮件时，快速排序这个功能给了很大的帮助。

tab 页：也是类 vim mode 操作，`gn` 开启一个新标签页，标签页列表在右上角，`gt/gT` 前后换页，`gc` 关闭当前页。

终端刷新：有 `C-R` 和 `C-L`，`C-L` 是重绘窗口，`C-R` 是刷新所有。注意如果在其它地方新增、删除文件等，ranger 是会自动刷新的。

另外还支持 `:`、`!` 等操作。


## 其它

关于 colorscheme，有 4 个可选，可以临时修改或写在配置文件 `~/.config/ranger/rc.conf` 中。还可以自定义配置文件，放在 `~/.config/ranger/colorschemes/` 下。可参考 [colorschemes](https://github.com/ranger/ranger/blob/20f0f2ba96a4a9dcbb8beffbee957b42157d4efd/doc/colorschemes.txt)。

关于样式，建议开启 border，不然看起来好丑，`set draw_borders true`。
