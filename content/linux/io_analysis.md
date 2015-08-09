---
title: "IO Analysis"
date: 2015-02-05 17:37
---

了解这个, 首先要对系统的基本原理比较了解.

另外, 这个是基于平时排查问题积累的, 后期会逐步完善和修正

---

Linux Wait IO 问题:

> Wait IO problem can be caused by several reasons, the basic road-map to find out is which process is "eating" your CPU first and then determine why. The main cause are those background processes with "D" status code which means "Uninterruptiable sleep". But the those processes with "D+" which means "Uninterruptible sleep foreground process" will generally not cause the serious problem as those background processes. In this example, the cause of Wait IO is the File System Journal, so the configuration of file system is the cause of the problem.   -- 摘自[Linux Wait IO Problem](http://www.chileoffshore.com/en/interesting-articles/126-linux-wait-io-problem)

确认负载(load):

最简单的就是`w`或者`uptime`, 前者已经包含了后者的输出

    $ uptime
     03:14:34 up 4 days, 12:08,  1 user,  load average: 0.00, 0.01, 0.05

    $ w
     03:14:34 up 4 days, 12:08,  1 user,  load average: 0.00, 0.01, 0.05
    USER     TTY        LOGIN@   IDLE   JCPU   PCPU WHAT
    tankywoo pts/1     Mon08    0.00s  0.41s  0.00s tmux -2

其次, 通过top等命令查看cpu的状态, 如us/sy/wa等

vmstat(Report virtual memory statistics) 用来输出ram, swap, io, cpu等信息.

最简单的就是后可接delay(输出间隔)和count(输出次数), 没有count则无限输出, 都没有则输出一次

另外vmstat不需要特殊权限

     $ vmstat 1 3
    procs -----------memory---------- ---swap-- -----io---- -system-- ----cpu----
     r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa
     0  0      0 197628 270232 245340    0    0     1    26   32   47  0  0 100  0
     0  0      0 197628 270232 245340    0    0     0    40   51   71  0  0 99  1
     0  0      0 197628 270232 245340    0    0     0     0   37   53  1  0 99  0

更复杂的专门看io的命令 iostat (Report Central Processing Unit (CPU) statistics and input/output statistics for devices and partitions); 输出cpu和io的信息.

默认输出基本的信息, `-c`只输出cpu信息, `-d`只输出硬盘信息, `-x`输出扩展信息

和vmstat一样, 最后接delay和count

    $ iostat -x 1 2
    Linux 3.7.10-gentoo-r1-ks (gentoo-local)        08/06/2015      _x86_64_        (1 CPU)

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.15    0.00    0.17    0.05    0.00   99.63

    Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sda               0.00     2.35    0.15    0.73     0.92    25.64    60.44     0.01    7.69    0.37    9.23   0.96   0.08
    dm-0              0.00     0.00    0.00    0.00     0.00     0.00     8.00     0.00    0.04    0.04    0.00   0.04   0.00

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.99    0.00    0.99    0.00    0.00   98.02

    Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
    sda               0.00     0.99    0.00    1.98     0.00    11.88    12.00     0.00    0.50    0.00    0.50   0.50   0.10
    dm-0              0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00

类似top, io也有相关的命令 iotop

参数也和top类似

    Total DISK READ :       0.00 B/s | Total DISK WRITE :       0.00 B/s
    Actual DISK READ:       0.00 B/s | Actual DISK WRITE:       0.00 B/s
      TID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN     IO>    COMMAND
        1 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % init [3]
        2 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [kthreadd]
    22022 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % sshd: tankywoo
    ...

另外, `man ps`可以看到进程状态的解释:

    PROCESS STATE CODES
      Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display to describe the state of a process:

        D    uninterruptible sleep (usually IO)
        R    running or runnable (on run queue)
        S    interruptible sleep (waiting for an event to complete)
        T    stopped, either by a job control signal or because it is being traced
        W    paging (not valid since the 2.6.xx kernel)
        X    dead (should never be seen)
        Z    defunct ("zombie") process, terminated but not reaped by its parent

查看进程状态是否有`D`, 表示进程在等待IO

    $ while true; do date; ps auxf | awk '{if($8=="S") print $0;}'; sleep 1; done

或者:

    $ for x in `seq 1 1 10`; do ps -eo state,pid,cmd | grep "^D"; echo "----"; sleep 1; done

还有一个比较强大的工具[dstat](http://dag.wiee.rs/home-made/dstat/), 集合了vmstat, iostat, ifstat等工具的功能, 并且输出是颜色高亮

其实工具都只是表层, 最底层的还是读取/proc下的文件, 具体在每个工具的man手册都有介绍.

---

其它:

找到cpu占用率最高的进程

一个是通过 [top/htop/atop](./top.html) 来查看.

另外可以通过ps:

    $ ps -auxf | sort -nr -k 3 | head -3

sort命令非常强大, 参数支持很多类别的排序, 具体可以man手册

比如内存使用率排序:

    $ ps -auxf | sort -nr -k 4 | head -3

另外, 可以看看相同名称进程的数量:

    $ ps aux | awk '{print $11}' | sort | uniq -c | sort -nk1 | tail -n5

或者某个用户在运行的进程数:

    $ ps aux | awk '{print $1}' | sort | uniq -c | sort -nk1 | tail -n5

---

参考资料:

* [Troubleshooting High I/O Wait in Linux](http://bencane.com/2012/08/06/troubleshooting-high-io-wait-in-linux/)
* [Isolating Linux High System Load](http://www.tummy.com/articles/isolating-heavy-load/)
* [Hack and / - Linux Troubleshooting, Part I: High Load](http://www.linuxjournal.com/magazine/hack-and-linux-troubleshooting-part-i-high-load?page=0,0)
* [Troubleshooting high load average on Linux](https://martincarstenbach.wordpress.com/2013/06/25/troubleshooting-high-load-average-on-linux/)
* [Linux Wait IO Problem](http://www.chileoffshore.com/en/interesting-articles/126-linux-wait-io-problem)
* [How to find out which process is consuming “wait CPU” (i.e. I/O blocked)](http://stackoverflow.com/questions/666783/how-to-find-out-which-process-is-consuming-wait-cpu-i-e-i-o-blocked)
