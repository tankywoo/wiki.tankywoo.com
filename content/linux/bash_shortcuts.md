---
title: "Bash Shortcuts"
date: 2013-08-17 07:23
---

## Ctrl ##

`Ctrl + a`  -  Jump to the start of the line # 如果使用screen，C-a可能会被占用，请使用C-a a

`Ctrl + e`  -  Jump to the end of the line

`Ctrl + k`  -  Delete from cursor to EOL # 从cursor处(包括光标)直接删除到行尾，很管用的命令

`Ctrl + u`  -  Delete backward from cursor # 从cursor处(不包括光标)直接前面所有，适合输错密码时用

`Ctrl + w`  -  Delete a word


`Ctrl + c`  -  Terminate the command

`Ctrl + d`  -  Delete char under the cursor


`Ctrl + b`  -  Move back a char

`Ctrl + f`  -  Move forward a char


`Ctrl + r`  -  Search the history backwards

`Ctrl + R`  -  Search the history with multi occurrence # ???还不明白这个和C-r的区别


`Ctrl + l`  -  Clear the screen

`Ctrl + z`  -  Suspend/Stop the command


# Bash Mode #

*TODO* 待具体研究

`set -o`		List all the modes

默认情况下，emacs mode是on，而vi mode是off，可以通过`set -o vi`改为vi mode

# Read More #

* [Bash Shortcuts](http://www.aboutlinux.info/2005/08/bash-shell-shortcuts.html)
* [Bash Shell 快捷键的学习使用](http://dbanotes.net/tech-memo/shell_shortcut.html) (此文是参考上文)
* [Bash Shortcuts For Maximum Productivity](http://www.skorks.com/2009/09/bash-shortcuts-for-maximum-productivity/)
* [让你提升命令行效率的 Bash 快捷键](http://linuxtoy.org/archives/bash-shortcuts.html)
* [Readline shortcuts](http://www.bigsmoke.us/readline/shortcuts)
* [Bash快捷键的思维导图](http://www.huangwei.me/blog/2010/10/27/bash_shortcuts_mindmap/)
* [高效操作Bash](http://ahei.info/bash.htm)
* [Bash Shell 快速鍵列表](http://blog.longwin.com.tw/2006/09/bash_hot_key_2006/)

