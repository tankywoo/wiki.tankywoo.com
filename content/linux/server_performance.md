---
title: "Server Performance Analysis"
date: 2013-08-17 07:23
---

[TOC]

服务器性能用到的知识:

* Load
* CPU
* Memory
* 磁盘I/O
* 网络I/O

## Load ##

系统负载指运行队列的平均长度，也就是等待CPU的平均进程数

可以通过`cat /proc/loadavg` `w` `top`等命令获取

推荐一篇文章[[http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages|Understanding Linux CPU Load]]

## CPU ##

`top` `atop` `htop`
获取CPU信息`cat /proc/cpuinfo`

其中%wa指CPU等待磁盘写入完成的时间

`vmstat` `sar` `iostat`

## Memory ##

`free` `vmstat` `top` `cat /proc/meminfo`

### Swap ###

From [Linux.com](https://www.linux.com/news/software/applications/8208-all-about-linux-swap-space)

> Linux divides its physical RAM (random access memory) into chucks of memory called pages. Swapping is the process whereby a page of memory is copied to the preconfigured space on the hard disk, called swap space, to free up that page of memory. The combined sizes of the physical memory and the swap space is the amount of virtual memory available.
>
> Swapping is necessary for two important reasons. First, when the system requires more memory than is physically available, the kernel swaps out less used pages and gives memory to the current application (process) that needs the memory immediately. Second, a significant number of the pages used by an application during its startup phase may only be used for initialization and then never used again. The system can swap out those pages and free the memory for other applications or even for the disk cache.

排查哪个进程占用swap过高:

1 读取`/proc/*/status`或`/proc/*/smaps`文件, 具体可以`man 5 proc`. [脚本来源](http://stackoverflow.com/a/7180078)

    #!/bin/bash
    # Get current swap usage for all running processes
    # Erik Ljungstrom 27/05/2011
    # Modified by Mikko Rantalainen 2012-08-09
    # Pipe the output to "sort -nk3" to get sorted output
    # Modified by Marc Methot 2014-09-18
    # removed the need for sudo

    SUM=0
    OVERALL=0
    for DIR in `find /proc/ -maxdepth 1 -type d -regex "^/proc/[0-9]+"`
    do
        PID=`echo $DIR | cut -d / -f 3`
        PROGNAME=`ps -p $PID -o comm --no-headers`
        for SWAP in `grep VmSwap $DIR/status 2>/dev/null | awk '{ print $2 }'`
        do
            let SUM=$SUM+$SWAP
        done
        if (( $SUM > 0 )); then
            echo "PID=$PID swapped $SUM KB ($PROGNAME)"
        fi
        let OVERALL=$OVERALL+$SUM
        SUM=0
    done
    echo "Overall swap used: $OVERALL KB"

简短的命令就如下, 不过wild match应该只匹配数字, 所以这里会把一些其它文件包含进来, [脚本来源](http://www.cyberciti.biz/faq/linux-which-process-is-using-swap/):

    for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | sort -k 2 -n -r | less


2 `top`命令, 好像3.2的版本是`Op`, 3.3的版本是`fp`来调出swap并排序. 具体查看help.

3 `smem`命令, 要装的东西太多了, 所以还没装.

参考:

* [how to find out which processes are swapping in linux?](http://stackoverflow.com/questions/479953/how-to-find-out-which-processes-are-swapping-in-linux)
* [Find Out What Is Using Your Swap](http://northernmost.org/blog/find-out-what-is-using-your-swap/)
* [Linux: Find Out What Process Are Using Swap Space](http://www.cyberciti.biz/faq/linux-which-process-is-using-swap/)
* [Linux: Total swap used = swap used by processes +?](http://unix.stackexchange.com/questions/71714/linux-total-swap-used-swap-used-by-processes)


## 磁盘I/O ##

`iostat`

## 网络I/O ##

`netstat`

## Read More ##

* [Linux服务器性能小结](http://blog.chinaunix.net/uid-27127953-id-3333176.html)
* [linux wa%过高，iostat查看io状况](http://www.cnblogs.com/mfryf/archive/2012/03/12/2392000.html)
