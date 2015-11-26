---
title: "Email相关"
date: 2013-08-17 07:36
description: "Mutt / Msmtp/ Exim"
---

[TOC]

## 基础 ##

首先得了解MUA，MTA的概念 (可参考鸟哥私房菜服务器篇)

* MUA(Mail User Agent): 主要用于接收、阅读、撰写邮件. 如thunderbird, 以为web的gmail, 或者简单的基于文本的mutt, mail命令(`mailx`)等.
* MTA(Mail Transfer Agent): 基于SMTP协议, 主要用于邮件的转发，如Postfix，Exim4, Sendmail, msmtp
* MDA(Mail Delivery Agent): 在邮件经过N个MTA达到目标的邮件服务器(local MTA)时, MDA将邮件放到相应的目录下.
* Mailbox: 信箱, linux下一般存在/var/spool/mail下

![mail process](http://tankywoo-wb.b0.upaiyun.com/mail-1.jpg)

(图片引用自[How a mail server works](http://xmodulo.com/how-mail-server-works.html))

更详细的基本概念:

* [How a mail server works](http://xmodulo.com/how-mail-server-works.html)
* [MTA, MDA what r they actually?](http://www.linuxquestions.org/questions/linux-software-2/mta-mda-what-r-they-actually-208129/)
* [Mail Server Components – MTA , MDA & MUA](http://www.nextstep4it.com/mail-server-components-mta-mda-mua/)
* [How email works (MTA, MDA, MUA)](http://ccm.net/contents/116-how-email-works-mta-mda-mua)

POP3 / IMAP / SMTP:

* POP3(Post Office Protocol 3): 用于邮件访问. 标准端口995(SSL)和110(非SSL)
* IMAP(Internet Mail Access Protocol): 交互式邮件存取协议. 用于邮件访问. 标准端口993(SSL)和143(非SSL)
* SMTP(Simple Mail Transfer Protocol): 简单邮件传输协议. 控制邮件的中转. 标准端口465/994(SSL)和25(非SSL)

POP3和IMAP的区别是前者本地的操作如删除不会同步到服务器. IMAP则是同步的.

## msmtp ##

负责smtp的功能

[主页](http://msmtp.sourceforge.net)

> msmtp is an SMTP client. In the default mode, it transmits a mail to an SMTP server which takes care of further delivery. To use this program with your mail user agent (MUA), create a configuration file with your mail account(s), and tell your MUA to call msmtp instead of /usr/sbin/sendmail.

在用户home目录新建一个.msmtprc配置文件

	account default
	host smtp.163.com	#邮件服务器，我用的是163的
	from xxx@163.com
	auth login
	user xxx@163.com	#账号
	password *******	#密码
	logfile /var/log/msmtp.log

因为这里涉及到了密码，所以建议把配置文件的权限改为600

测试:

	$ msmtp xxx@xx.com(收件人邮箱)

然后随便输入一些字符，按Ctrl+D退出，查看收件人邮箱是否有邮件

参考:

* [msmtp官方文档:Using msmtp with Mutt](http://msmtp.sourceforge.net/doc/mutt+msmtp.txt)

## mutt ##

[主页](http://www.mutt.org)

> Mutt is a small but very powerful text-based mail client for Unix operating systems.

在用户home目录新建一个.muttrc配置文件

	set sendmail="/usr/bin/msmtp"	#这里设置调用的MTA
	set use_from=yes
	set realname="XXX"				#发件人名称
	set editor="vim"				#调用的编辑器

测试:

	$ echo 'Hello World' | mutt -s 'Hi, Just a test!' xxx@xx.com

`w` 可以更改邮件的状态, 有:

* N: 新邮件
* O: 老邮件, 但未读
* r: 已读
* D: 将删除

关于 tmux下mutt没有重绘窗口的问题, 见我之前的[博客](http://blog.tankywoo.com/2015/10/24/tmux-mutt-not-redraw-problem.html)

关于邮件中的搜索, 有两种: `search` (按`/`) 和 `limit` (按`l`, 字母), 网上说后者比前者更强大, 不过暂时没感觉出来.

对于包含body content中的搜索, 模式是: `/~b xxx` 或者 `l~b xxx`, 前者是定位到第一个匹配的, 按`n`到第二个匹配; 而 limit搜索相当于filter, 只显示匹配的邮件, 如果想回到所有列表, 则`lall` (注意这里的/或者l都是上面提到的进入search/limit模式)

模式见文档 [mutt regex](http://www.mutt.org/doc/manual/manual-4.html#ss4.2)

另外在search时, 按`\`可以toggle关键词高亮.

删除指定日期的所有邮件:

	# 删除2015年12月1号的邮件
	l~d 01/12/2015
	^D

	# 删除2015/12/01 - 2015/12/06内的所有邮件
	l~d 01/12/2015+5d
	^D

参考:

* [Search for mail content with mutt](http://unix.stackexchange.com/questions/91046/search-for-mail-content-with-mutt)
* [mutt Pattern matching with regular expressions](http://mutt.blackfish.org.uk/searching/)
* [Gentoo文档:Mutt电子邮件快速入门指南](http://www.gentoo.org/doc/zh_cn/guide-to-mutt.xml?style=printable)
* [Arch - Mutt](https://wiki.archlinux.org/index.php/Mutt)
* [使用mutt作为email客户端](http://www.jianshu.com/p/bebbf2db2cd8)
* [Mutt cheat sheet](http://sheet.shiar.nl/mutt)
* [Mutt: limit or search by date](http://promberger.info/linux/2009/07/23/mutt-limit-or-search-by-date/)

## Exim ##

常用命令:

    # 输出邮件队列(queue)中的邮件数
    exim -bpc

    # 输出邮件队列中的邮件信息(time queued, size, message-id, sender, recipient)
    exim -bp

    # 输出邮件队列的摘要(count, volume, oldest, newest, domain, and totals)
    exim -bp | exiqsumm

    # exim当前状态
    exiwhat

    # 输出exim配置信息
    exim -bP

    # 删除邮件队列中指定的邮件
    exim -Mrm <message-id>

    # 删除邮件队列中所有的邮件(几种方法都行, 暂未全部尝试 XXX)
    exim -bp | exiqgrep -i | xargs exim -Mrm
    exiqgrep -i|xargs exim -Mrm
    exim -bp | awk '/^ *[0-9]+[mhd]/{print "exim -Mrm " $3}' | bash

参考:

* [Exim Cheatsheet](http://bradthemad.org/tech/notes/exim_cheatsheet.php)
* [Exim Remove All messages From the Mail Queue](http://www.cyberciti.biz/faq/exim-remove-all-messages-from-the-mail-queue/)
* [Quick way to remove all emails from the mail queue](http://crybit.com/remove-all-emails-from-queue/)
