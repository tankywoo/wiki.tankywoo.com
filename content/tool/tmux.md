---
title: "tmux"
date: 2013-10-16 16:24
update: 2015-10-22 14:22
---

[TOC]

# TMUX - terminal multiplexer #

前序: [布道 Tmux](http://www.wutianqi.com/?p=3676)

三个术语:

* session: 管理多个window的会话
* window: 一个window就是整个屏幕
* pane: 一个window可以被横向或纵向分割为多个pane, 也就是俗称的分屏

tmux有很多组合键, 类似screen, tmux的组合键前缀(prefix)默认是`C-b`, 如果习惯了screen的`C-a`, 可以修改prefix, 以下都用`C-b`表示前缀

## 快捷键 ##

### 基本操作 ###

* `C-b :` 进入tmux的命令行模式
* `C-b ?` 显示所有的bind-key
* `C-b [` 进入复制模式
* `C-b ]` 进入粘贴模式

如果有设置 `setw -g mode-keys vi` 的话，可按 vi 的按键模式操作。移动至待复制的文本处，按一下空格，结合 vi 移动命令开始选择，选好后按回车确认.

### session 操作 ###

* `C-b d` deattch当前的session
* `C-b C-z` 挂起当前的session
* `tmux attach [-t sessionname]` 恢复session
* `C-b $` 可以重命名当前的session
* `tmux ls` 显示tmux的所有session

### window 操作 ###

* `C-b c` 可以新建一个新的window
* `C-b &` 关闭当前的window
* `C-b ,` 可以重命名当前的window
* `C-b p` 切换到前一个window
* `C-b n` 切换到后一个window
* `C-b l` 切换到上一次的window
* `C-b number` 切换到指定编号的window, 默认从0开始
* `C-b w` 显示当前会话的window, 可以通过上下选择来切换
* `tmux neww -n tmux` 新建一个window, 名称是tmux

### pane 操作 ###

* `C-b "` 将当前window横向分割为两个pane
* `C-b %` 将当前window纵向分割为两个pane
* `C-b 方向键` 在当前window里移动到其他pane
* `C-b o` 切换到下一个pane
* `C-b Alt+方向键` 调整pane的大小
* `C-b q` 显示pane的编号
* `C-b x` 关闭当前的pane, 会有确认提示. 也可以直接C-d
* `C-b {` 把当前的pane移到左边
* `C-b }` 把当前的pane移到右边
* `C-b z` 把当前pane最大化/恢复. 感谢 yanyaoer 和 陈兴明Mingo 两位同学, tmux 升级到 1.8 后有这个特性了.
* `C-b Space` 切换到下一个布局(这个布局应该是系统默认的一些)

## 配置文件 ##

以下配置更新会有延迟, 最新配置见我的 [dotfiles](https://github.com/tankywoo/dotfiles)

```bash
set -g default-terminal "screen-256color"   # use 256 colors
set -g display-time 5000                    # status line messages display
set -g status-utf8 on                       # enable utf-8
set -g history-limit 100000                 # scrollback buffer n lines
setw -g mode-keys vi                        # use vi mode

# start window indexing at one instead of zero
set -g base-index 1

# set the prefix key and some key bindings to match GNU Screen
set -g prefix C-a
unbind-key C-b
bind-key C-a send-prefix

# key bindings for horizontal and vertical panes
unbind %
bind | split-window -h
unbind '"'
bind - split-window -v

# enable window titles
#set -g set-titles on

# window title string (uses statusbar variables)
set -g set-titles-string '#T'

# status bar with load and time
set -g status-bg '#4e4e4e'
set -g status-fg '#bbbbbb'
set -g status-left-fg '#55ff55'
set -g status-left-bg '#555555'
set -g status-right-fg '#55ff55'
set -g status-right-bg '#555555'
set -g status-left-length 90
set -g status-right-length 90
set -g status-left '[#(whoami)]'
set -g status-right '[#(date +" %m-%d %H:%M ")]'
set -g status-justify "centre"
set -g window-status-format '#I #W'
set -g window-status-current-format ' #I #W '
setw -g window-status-current-bg '#B3D9D9'
setw -g window-status-current-fg '#DDDDFF'

# pane border colors
set -g pane-active-border-fg '#55ff55'
set -g pane-border-fg '#555555'

# bind to reload config
bind r source-file ~/.tmux.conf

# add window to session
new -s tankywoo -n tankywoo
neww -n ops-dev
selectw -t 1

# scripting tmux
bind T source-file ~/.tmux/tanky
```

## 脚本化tmux ##

** 脚本化是 Tmux 的一大亮点 **

脚本化可以让我们自己定义一些脚本, 来构造自己的tmux布局

比如我写了一个分割三个pane的小脚本放在 ~/.tmux/tanky 里:

```bash
select-pane -t 0
split-window -h -p 60
select-pane -t 1
split-window -v -p 25
send-keys -t 0 'ipython' C-m
# The C-m at the end is interpreted by Tmux as the enter key.
select-pane -t 1
```

google搜出来的讲解tmux脚本化的E文不少, 不过没几个解释了 `C-m` 是干嘛的, 查看绑定键也没找到  
后来在[An Introduction to Scripting Tmux Key Bindings](http://spin.atomicobject.com/2013/04/11/tmux-key-binding-scripting/)上看到了解释.

> The C-m at the end is interpreted by Tmux as the enter key.

在 ~/.tmux.conf 里绑定快捷键: bind T source-file ~/.tmux/tanky

这样, 就可以通过快捷键 C-b S-t 一键初始化一个如下图的布局.
![Script Tmux](http://tankywoo-wb.b0.upaiyun.com/tmux_new.png)

另外, 还可以直接写shell脚本, 然后运行, 比如:

```bash
#!/bin/bash
# Tanky Woo@2013-06-19 10:51:15
# About:

tmux start-server

if ! $(tmux has-session -t 'tankywoo'); then
        tmux new-session -d -s 'tankywoo' -n 'tankywoo' # -d *
        tmux select-window -t 'tankywoo'
        tmux split-window -h -p 60
        tmux select-pane -t 1
        tmux split-window -v -p 25
        tmux send-keys -t 0 'ipython' C-m
        # The C-m at the end is interpreted by Tmux as the enter key.

        tmux new-window -n 'ops-dev'

        tmux select-window -t 'tankywoo'
        tmux select-pane -t 1
fi

tmux attach-session -d -t 'tankywoo'
```

下面这几个链接不错

* [Scripting Tmux Layouts](http://amjith.blogspot.com/2011/08/scripting-tmux-layouts.html)
* [TMUX SCRIPTING](http://blog.htbaa.com/news/tmux-scripting)
* [Scripting tmux](http://toastdriven.com/blog/2009/oct/09/scripting-tmux/)

## 技巧 ##

### 批量操作 ###

当需要在多个机器执行相同操作时, 可以考虑用`pdsh`等内容分发的工具, 而tmux也有它的一种强悍的方式. 在一个windows里打开多个pane, 每个pane登录一台服务器, 设置windows的选项, 在其中一个pane上操作时, 其它pane都会复制相同的操作.

在tmux的命令行里, 使用选项`set synchronize-panes on`即可.

### 在不同大小的屏幕打开一个session ###

** TODO **

比如在一个较小的桌面打开一个session, 然后又在一个较大的桌面也打开这个session:

	tmux attach -t session-name

则会发现在较大的桌面上, 也只会显示和小桌面同样大小的窗口, 其余部分被密密麻麻的小点扩充.

解决方法之一是:

	tmux attach -d -t session-name

即先强制 `detach` 掉小桌面的session, 然后再在较大桌面打开session.

另外, 看到很多帖子说可以设置:

	setw -g aggressive-resize on

但是我设置后还是没有成功.

参考:

* [Attach to different windows in session](http://unix.stackexchange.com/questions/24274/attach-to-different-windows-in-session)
* [Maximize window in tmux](http://superuser.com/questions/300251/maximize-window-in-tmux)
* [Practical Tmux](https://mutelight.org/practical-tmux)
* [Archlinux - Tmux](https://wiki.archlinux.org/index.php/Tmux)

### pane之间的移动 ###

	join-pane [-bdhv] [-l size | -p percentage] [-s src-pane] [-t dst-pane]
		(alias: joinp)
		Like split-window, but instead of splitting dst-pane and creating a new pane, split it and move src-pane into the space.  This can be used to reverse break-pane.  The -b option causes src-pane to be joined to left of or above dst-pane.

比如当前在window6上, 想将window7的pane2合并到当前window:

	joinp -s 7.2

如果只写的7则表示window7的当前活动pane.

关于 `session:window.pane`的详细表示, 可以看`man tmux`的`COMMANDS`这一大节.

参考:

* [Moving tmux window to pane](http://unix.stackexchange.com/questions/14300/moving-tmux-window-to-pane)

## 扩展 - tmux powerline ##

* [tmux-powerline项目](https://github.com/erikw/tmux-powerline) 官方说此项目现在只做维护, 不更新
* [powerline项目](https://github.com/Lokaltog/powerline) 这个是最新项目

## 其他资料 ##

* [screen and tmux](http://www.dayid.org/os/notes/tm.html) screen和tmux的操作对比
* [Tmux - ArchWIKI](https://wiki.archlinux.org/index.php/Tmux) 对tmux介绍的非常详细
* [TMUX – The Terminal Multiplexer (Part 1)](http://blog.hawkhost.com/2010/06/28/tmux-the-terminal-multiplexer/)
* [使用tmux](https://wiki.freebsdchina.org/software/t/tmux)
* [Using tmux](http://510x.se/notes/posts/Using_tmux/)
* [Practical Tmux](https://mutelight.org/practical-tmux)
* [tmux cheatsheet](https://gist.github.com/henrik/1967800)

---

# Tmuxinator #

[Tmuxinator](https://github.com/tmuxinator/tmuxinator) 是一个用Ruby写的管理tmux会话(session)的工具.

上面针对tmux, 可以写脚本来创建希望的布局, 但是比较麻烦.

而tmuxinator使用yaml来配置布局, 简单的配置就可以生成复杂的会话布局.

基本前提是安装tmux, 配置了`$EDITOR`和`$SHELL`. 可以通过doctor子命令来检查:

    $ tmuxinator doctor
    Checking if tmux is installed ==> Yes
    Checking if $EDITOR is set ==> Yes
    Checking if $SHELL is set ==> Yes

使用`new`子命令会使用配置的`$EDITOR`来创建并打开一个yaml会话配置. 默认保存在`~/.tmuxinator/`下.

因为的tmux设置了`set -g base-index 1`, 所以需要也设置pane-base-index:

    setw -g pane-base-index 1

否则创建pane报错:

    $ mux start sample
    can't find pane: 1
    arranging in: main-vertical
    can't find pane: 1
    [exited]

我设置pane-base-index后, 还是报错, 找了半天, 才发现是因为还有另外一个tmux在运行, tmux server不会重新加载pane-base-index, 需要全部退出后才行. 也可以用`bind-key q`来确认起始的pane index.

关于completion脚本, 我用的zsh, 直接配置上tmuxinator的plugin, 和官方提供的completion基本类似.
