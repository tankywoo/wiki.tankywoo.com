---
title: "screen"
date: 2013-09-06 10:22
---

## .screenrc ##

`info screen "String Escapes"`  

* [How do I change the colors in the hardstatus line in GNU Screen?](http://superuser.com/questions/31047/how-do-i-change-the-colors-in-the-hardstatus-line-in-gnu-screen)
* [Screen status bar to display current directory for zsh/bash shell](http://unix.stackexchange.com/questions/28430/screen-status-bar-to-display-current-directory-for-zsh-bash-shell)
* [What are useful .screenrc settings?](http://serverfault.com/questions/3740/what-are-useful-screenrc-settings)
* [How can I change screen's hardstatus color based on the logged in user?](http://unix.stackexchange.com/questions/62842/how-can-i-change-screens-hardstatus-color-based-on-the-logged-in-user)

## Tricks ##

### 同步显示同一个screen ###
A打开一个screen, B可以登录这个screen,同步显示A的操作;B也可以在上面操作.

	A 打开一个叫tankywoo的会话
	screen -S tankywoo
	B 使用`-x`参数登入这个会话
	screen -x tankywoo
