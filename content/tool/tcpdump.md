---
title: "tcpdump"
date: 2013-09-06 10:24
update: 2015-11-14 16:00
---

TODO

tcpdump is a common packet analyzer that runs under the command line

## 语法 ##
Syntax: 
| Protocol | Direction | Host(s) | Value | Logical Operations | Other expression |

Example:
| tcp | dst | 10.1.1.1 | 80 | and | tcp dst 10.2.2.2 3128 |

== Protocol: ==
Values: ether, fddi, ip, arp, rarp, decnet, lat, sca, moprc, mopdl, tcp and udp.

If no protocol is specified, all the protocols are used. 

== Direction: ==
Values: src, dst, src and dst, src or dst

If no source or destination is specified, the "src or dst" keywords are applied. 

For example, "host 10.2.2.2" is equivalent to "src or dst host 10.2.2.2".

== Host(s): ==
Values: net, port, host, portrange.

If no host(s) is specified, the "host" keyword is used.

For example, "src 10.1.1.1" is equivalent to "src host 10.1.1.1". 

== Logical Operations: ==
Values: not, and, or.

Negation ("not") has highest precedence. Alternation ("or") and concatenation ("and") have equal precedence and associate left to right.

For example,

"not tcp port 3128 and tcp port 23" is equivalent to "(not tcp port 3128) and tcp port 23".

"not tcp port 3128 and tcp port 23" is NOT equivalent to "not (tcp port 3128 and tcp port 23)".

= Arguments =

== -A ==
print in ASCII

== -c ==
Specify the receive count 

== -D ==
Print the list of the network interfaces available on the system and on which tcpdump can capture packets

== -i ==
Listen on interface

== -l ==
>> tcpdump -l | tee dat

== -n ==
Don't convert addresses to names

== -v/-vv ==


= Read More =

* [The Easy Tutorial](http://openmaniak.com/tcpdump.php TCPDUMP)
* [Linux抓包工具tcpdump详解](http://www.ha97.com/4550.html)
* [Linux tcpdump命令详解](http://www.cnblogs.com/ggjucheng/archive/2012/01/14/2322659.html)
* [A tcpdump Tutorial and Primer](http://danielmiessler.com/study/tcpdump/)
* [12 Tcpdump Commands – A Network Sniffer Tool](http://www.tecmint.com/12-tcpdump-commands-a-network-sniffer-tool/)
* [wiki-tcpdump](http://en.wikipedia.org/wiki/Tcpdump)
http://www.alexonlinux.com/tcpdump-for-dummies
http://www.carnal0wnage.com/papers/TCPdumpBasics.pdf
http://science.hamptonu.edu/compsci/docs/iac/packet_sniffing.pdf
http://www.danielmiessler.com/study/tcpdump/


## ipv6 ##

for tcp ipv6

    sudo tcpdump -p -i any tcp and port 8000 and ip6

for tcp ipv4 or ipv6:

    sudo tcpdump -p -i any tcp and port 8000 and '(ip or ip6)'

for icmp ipv6

    sudo tcpdump -p -i any icmp6




= History =
Create 2013/01/13

Last modified 2013/01/13
