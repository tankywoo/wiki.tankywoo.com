---
title: "SUID / SGID / Sticky Bit"
date: 2015-11-03 20:36
---

[TOC]

## SUID ##

即 Set User IDentification, 更详细说是Set owner User ID on execution.

> is a special type of file permissions given to a file. Normally in Linux/Unix when a program runs, it inherits access permissions from the logged in user. SUID is defined as giving temporary permissions to a user to run a program/file with the permissions of the file owner rather that the user who runs it. **In simple words users will get file owner’s permissions as well as owner UID and GID when executing a file/program/command**.

用户在执行程序/命令时, 会临时拥有此程序的属主权限.

使用场景:

* Where root login is required to execute some commands/programs/scripts.
* Where you don’t want to give credentials of a particular user, but want to run some programs as the owner.
* Where you don’t want to use SUDO command, but want to give execute permission for a file/script etc.

针对目标一般是文件

最常见的就是`passwd`命令:

    $ ls -alh /bin/passwd
    -rws--x--x 1 root root 42K Sep 17  2012 /bin/passwd

    $ ls -alh /etc/{passwd,shadow}
    -rw-r--r-- 1 root root 1.8K Nov  3 05:28 /etc/passwd
    -rw-r----- 1 root root  854 Nov  3 05:28 /etc/shadow

执行passwd命令会修改如上面的文件, 但是设置了suid, 则在执行命令时effective uid则是root.

设置suid的两种方式:

    $ chmod u+s xxx.file
    $ chmod 4644 xxx.file

注意user权限一栏的x是`s`. 如果`S`(captial), 则表示没有设置可执行权限(`x`).

[虽然有人说这样会导致suid无效, 不过我测试是没问题]

suid也可以给目录设置, 不过没什么用.

测试例子:

    #include <stdio.h>
    #include <unistd.h>

    int main(int argc, char** argv) {
        printf("%d", geteuid());
        return 0;
    }

执行:

    $ ./test_suid
    1000

    $ sudo chmod u+s test_suid

    $ ./test_suid
    0

另外, 脚本设置suid是无效的:

    $ cat a.sh
    #!/bin/bash

    echo '> effective id: ' `id -u`
    echo '> real id: ' `id -u -r`
    echo -e '\n---------------------\n'

    touch /opt/xxxxx

    $ ls -al a.sh
    -rwsr-xr-x 1 root tankywoo 129 Nov  3 06:27 a.sh

    $ ./a.sh
    > effective id:  1000
    > real id:  1000

    ---------------------

    touch: cannot touch ‘/opt/xxxxx’: Permission denied

可以通过C代码做一个wrapper来实现. 具体的原因和方法见:

> Linux ignores the setuid¹ bit on all interpreted executables (i.e. executables starting with a #! line). The [comp.unix.questions FAQ](http://www.faqs.org/faqs/unix-faq/faq/part4/section-7.html) explains the security problems with setuid shell scripts. These problems are of two kinds: shebang-related and shell-related

* [Allow setuid on shell scripts](http://unix.stackexchange.com/questions/364/allow-setuid-on-shell-scripts)
* [Using the setuid bit properly](http://unix.stackexchange.com/questions/166817/using-the-setuid-bit-properly)
* [Can I make a script always execute as root?](http://superuser.com/questions/440363/can-i-make-a-script-always-execute-as-root)

## SGID ##

和SUID类似. Set Group ID up on execution.

> is a special type of file permissions given to a file/folder. Normally in Linux/Unix when a program runs, it inherits access permissions from the logged in user. SGID is defined as giving temporary permissions to a user to run a program/file with the permissions of the file group permissions to become member of that group to execute the file. **In simple words users will get file Group’s permissions when executing a Folder/file/program/command**.

使用场景:

* 保持子文件/子目录和父目录一个数组

针对目标一般是目录

设置sgid的两种方式:

    $ chmod g+s directory
    $ chmod 2755 directory

注意group权限一栏的x是`s`. 如果`S`(captial), 则表示没有设置可执行权限(`x`).

默认情况下, 用户创建文件的数组是自身的primary group, 通过sgid可以改变这个特性:

    # 设置sgid前
    $ ll file1
    -rw-r--r-- 1 tankywoo tankywoo 0 Nov  3 06:54 file1         # <--- group是tankywoo
    $ id
    uid=1000(tankywoo) gid=1000(tankywoo) groups=1000(tankywoo),10(wheel),16(cron)

    # 设置sgid
    $ mkdir test_gid
    $ sudo chmod g+s test_gid
    $ chgrp mygroup test_gid
    $ ls -ald test_gid
    drwxr-sr-x 2 tankywoo mygroup 4096 Nov  3 06:54 test_gid
    $ cd test_gid
    $ touch file2
    $ ll file2
    -rw-r--r-- 1 tankywoo mygroup 0 Nov  3 06:56 file2          # <--- group是mygroup

## Sticky Bit ##

即 粘滞位

> is mainly used on folders in order to avoid deletion of a folder and its content by other users though they having write permissions on the folder contents. If Sticky bit is enabled on a folder, the folder contents are deleted by only owner who created them and the root user. No one else can delete other users data in this folder(Where sticky bit is set). This is a security measure to avoid deletion of critical folders and their content(sub-folders and files), though other users have full permissions.

使用场景即作用, 一个公共目录, 大家(other)都可以写文件, 这时自然大家也都可以删文件; 粘滞位就是保护这些文件

设置sticky bit的三种方式:

    $ chmod o+t directory
    $ chmod +t directory
    $ chmod 1777 directory

最常见的就是`/tmp` 目录:

    $ ll -d /tmp
    drwxrwxrwt 14 root root 4096 Nov  3 07:12 /tmp

针对目标一般是目录

    $ chmod 1777 test_sticky
    $ ls -ald test_sticky
    drwxrwxrwt 2 root root 4096 Nov  3 07:17 test_sticky

    # 用户shen创建一个文件
    shen $ touch xxx.txt

    # 用户tankywoo删除此文件
    tankywoo % rm xxx.txt
    rm: cannot remove ‘xxx.txt’: Operation not permitted

    # 去掉sticky bit权限
    $ chmod o-t test_sticky
    $ ls -ald test_sticky
    drwxrwxrwx 2 root root 4096 Nov  3 07:18 test_sticky

    # 正常删除
    tankywoo $ rm  xxx.txt
    tankywoo $ 

## 参考 ##

非常详细的一系列三篇文章:

* [What is SUID and how to set SUID in Linux/Unix?](http://www.linuxnix.com/suid-set-suid-linuxunix/)
* [What is SGID and how to set SGID in Linux?](http://www.linuxnix.com/sgid-set-sgid-linuxunix/)
* [What is a sticky Bit and how to set it in Linux?](http://www.linuxnix.com/sticky-bit-set-linux/)
