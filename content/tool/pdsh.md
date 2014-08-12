---
title: "pdsh"
date: 2014-04-28 14:57
---

[Pdsh](https://code.google.com/p/pdsh/)(Parallel Distributed Shell) 

> Pdsh is a high-performance, parallel remote shell utility. It uses a sliding window of threads to execute remote commands, conserving socket resources while allowing some connections to timeout if needed. It was originally written as a replacement for IBM's DSH on clusters at LLNL.

> The core functionality of pdsh is supplemented by many available dynamically loadable modules. The modules may implement a new connection protocol, target host filtering (e.g. removing hosts that are "down" from the target host list) and/or other host selection options (e.g. -a selects all hosts from a config file).

> The pdsh distribution also contains a parallel remote copy utility (pdcp - copy from local host to a group of remote hosts in parallel), reverse parallel remote copy (rpdcp, copy from a group of hosts to localhost in parallel), and a script dshbak for formatting and demultiplexing pdsh output.

常用参数:

`-w TARGETS,...` : 指定主机列表, 以逗号分隔(中间不能有空格).

`-x host,host,...` : 排除指定主机

`-l user` : 指定登录用户

配置主机组:

> dshgroup module options
> The dshgroup module allows pdsh to use dsh (or Dancer's shell) style group files from /etc/dsh/group/ or ~/.dsh/group/.
> 
> -g groupname,...
> Target nodes in dsh group file "groupname" found in either ~/.dsh/group/groupname or /etc/dsh/group/groupname.
> 
> -X groupname,...
> Exclude nodes in dsh group file "groupname."

将主机组列表文件放在 `/etc/dsh/group/` 或 `~/.dsh/group/` 下, 主机组名就是文件名, 主机一行一个.

    $ more ~/.dsh/group/myhosts
    192.168.1.12
    192.168.1.13
    $ pdsh -g myhosts -l root uptime
    192.168.1.13:  10:47:12 up 38 days, 14:37,  0 users,  load average: 0.04, 0.06, 0.05
    192.168.1.12:  10:47:12 up 10 days, 23:53,  5 users,  load average: 0.22, 0.26, 0.28


因为pdsh需要配置好公私钥后才可以使用，而配置了公私钥后，如果从未登录过某台机器，第一次登录时默认交互式的确认Yes或No来将ECDSA签名写入`~/.ssh/known_hosts`文件. 这是如果用pdsh执行命令会失败. 可以通过批量执行`ssh -o StrictHostKeyChecking=no`来将这个签名写入文件, 并执行命令.

    $ pdsh -R exec -g myhosts ssh -o StrictHostKeyChecking=no -l root %h uptime
    host1: Warning: Permanently added 'host1,192.168.1.12' (ECDSA) to the list of known hosts.
    host2: Warning: Permanently added 'host2,192.168.1.13' (ECDSA) to the list of known hosts.
    host1:  10:34:01 up 38 days, 14:24,  0 users,  load average: 0.02, 0.06, 0.05
    host2:  10:34:02 up 10 days, 23:40,  5 users,  load average: 0.12, 0.22, 0.25

注意这里的 `-l root` 是 ssh 的参数选项, 不是 pdsh 的.

### dshbak ###

dshbak 是 pdsh 的一个配套工具, 用于格式化输出结果.

一般使用 `dshbak -c` 将输出结果归类, 相同结果不会重复输出, 方便查看差异结果:

    $ pdsh -g myhosts -l root whoami | dshbak -c
    ----------------
    192.168.1.[12-13]
    ----------------
    root

### pdcp ###

pdcp 是一个批量传输的工具，也是pdsh工具集中的一个，还有一个反向的`rpdcp`

比如要传一个目录到/home目录下:

    pdcp -r -l root -g myhosts /dir /home/


