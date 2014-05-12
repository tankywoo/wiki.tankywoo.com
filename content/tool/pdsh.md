---
title: "pdsh"
date: 2014-04-28 14:57
---

TODO

[Pdsh](https://code.google.com/p/pdsh/)(Parallel Distributed Shell) 

> Pdsh is a high-performance, parallel remote shell utility. It uses a sliding window of threads to execute remote commands, conserving socket resources while allowing some connections to timeout if needed. It was originally written as a replacement for IBM's DSH on clusters at LLNL.

> The core functionality of pdsh is supplemented by many available dynamically loadable modules. The modules may implement a new connection protocol, target host filtering (e.g. removing hosts that are "down" from the target host list) and/or other host selection options (e.g. -a selects all hosts from a config file).

> The pdsh distribution also contains a parallel remote copy utility (pdcp - copy from local host to a group of remote hosts in parallel), reverse parallel remote copy (rpdcp, copy from a group of hosts to localhost in parallel), and a script dshbak for formatting and demultiplexing pdsh output.


dshgroup module options
The dshgroup module allows pdsh to use dsh (or Dancer's shell) style group files from /etc/dsh/group/ or ~/.dsh/group/.

-g groupname,...
Target nodes in dsh group file "groupname" found in either ~/.dsh/group/groupname or /etc/dsh/group/groupname.

-X groupname,...
Exclude nodes in dsh group file "groupname."


	pdsh -g group_name -l user "w" | dshbak -c
