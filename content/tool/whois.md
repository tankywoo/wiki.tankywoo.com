---
title: "whois"
date: 2015-11-01 15:21
---

[TOC]

## 简介 ##

[whois][0] 是一个基于tcp的query/response协议, 使用端口43, 用于查询域名的相关信息.

本地Gentoo上使用的whois客户端是 Debian GNU/Linux whois 5.1.5

> whois searches for an object in a RFC 3912 database.
>
> This version of the whois client tries to guess the right server to ask for the specified object. If no guess can be made it will connect to whois.networksolutions.com for NIC handles or whois.arin.net for IPv4 addresses and network names.

图片阐述了域名注册各部分的职能, 来源 [Domain Name Registration Process](http://whois.icann.org/en/domain-name-registration-process):

![domain registry process](http://tankywoo-wb.b0.upaiyun.com/Registry-Process-Large-FINALgif)


## 术语 ##

[TLD][1]: Top-level domain. 顶级域名, 如.com, .net, .org等.

[NIC][2] 相关:

`domain name registry`, 域名注册局 是一个维护所有顶级域名域名及相关注册信息的数据库.

> A domain name registry is a database of all domain names and the associated registrant information in the top level domains of the Domain Name System (DNS) of the Internet that allow third party entities to request administrative control of a domain name. Most registries operate on the top-level and second-level of the DNS.

`registry operator` 注册操作者, 即NIC(Network Information Centre, 网络信息中心), 维护了域名的数据, 生成包含域名/ip对应关系的zone文件.

> A registry operator, sometimes called a network information center (NIC) maintains all administrative data of the domain and generates a zone file which contains the addresses of the nameservers for each domain.

每一个registry都是一个组织, 管理相关域名的注册.

[Domain name registrar][3] 域名注册商. 是一个商业实体或组织, 它们由互联网名称与数字地址分配机构(ICANN)或者一个国家性的国家代码顶级域名(ccTLD)域名注册局委派, 以在指定的域名注册数据库中管理互联网域名, 向公众提供此类服务.

> is an organization or commercial entity that manages the reservation of Internet domain names. A domain name registrar must be accredited by a generic top-level domain (gTLD) registry and/or a country code top-level domain (ccTLD) registry.

[NIC handle][4]:

> is a unique alphanumeric character sequence that represents an entry in the databases maintained by Network Information Centres. When a new domain name is registered with a domain name registrar, a NIC handle is assigned by the registrar to the particular set of information associated with that domain name (such as who registered it and a contact e-mail address). Once a domain name has been registered, its NIC handle can be used to search for that record in the database.

[ICANN][5] (The Internet Corporation for Assigned Names and Numbers) 互联网名称与数字地址分配机构. 是一个集合了全球网络界商业、技术及学术各领域专家的非营利性国际组织，负责在全球范围内对互联网唯一标识符系统及其安全稳定的运营进行协调, 包括互联网协议(IP)地址的空间分配、协议标识符的指派、通用顶级域名(gTLD)以及国家和地区顶级域名(ccTLD)系统的管理、以及根服务器系统的管理. 这些服务最初是在美国政府合同下由 互联网号码分配当局(Internet Assigned Numbers Authority, IANA) 以及其它一些组织提供. 现在, ICANN行使IANA的职能.

Referral URL: TODO

## 使用 ##

`--verbose`可以看到更详细的查询相关信息.

比如查询我的域名:

    $ whois --verbose tankywoo.com
    Using server whois.verisign-grs.com.                # look here 1

    Whois Server Version 2.0

    Domain names in the .com and .net domains can now be registered
    with many different competing registrars. Go to http://www.internic.net
    for detailed information.

       Domain Name: TANKYWOO.COM
       Registrar: ENOM, INC.
       Sponsoring Registrar IANA ID: 48
       Whois Server: whois.enom.com
       Referral URL: http://www.enom.com
       ...
       Creation Date: 06-dec-2010

    >>> Last update of whois database: Sun, 01 Nov 2015 06:24:11 GMT <<<

    For more information on Whois status codes, please visit
    https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en.
    Using server whois.enom.com.                        # look here 2
    Query string: "tankywoo.com"

    Domain Name: TANKYWOO.COM
    Registrar WHOIS Server: whois.enom.com
    Registrar URL: www.enom.com
    ...
    Registrar: ENOM, INC.
    Reseller: NAMECHEAP.COM
    Registrant Name: WHOISGUARD PROTECTED
    Registrant Organization: WHOISGUARD, INC.
    Registrant Street: P.O. BOX 0823-03411
    Registrant City: PANAMA
    ...

这里先查询whois.verisign-grs.com这个whois server. verisign是一个registry operator, 负责操作.com和.net的注册. 在本地使用的whois实现里, 维护了一个tld_serv_list列表, 对每个顶级域首先使用相应的whois server来查询, 获取代理的whois server, 再在这个whois server中查询获取更详细的信息. 如上所示, 进而查询的whois server是whois.enom.com.

另外, 有些域名直接查询registry opeartor(nic) 即可获取详细信息, 如.me


  [0]: https://en.wikipedia.org/wiki/WHOIS 'whois'
  [1]: https://en.wikipedia.org/wiki/Top-level_domain 'Top-level domain'
  [2]: https://en.wikipedia.org/wiki/Domain_name_registry 'NIC'
  [3]: https://en.wikipedia.org/wiki/Domain_name_registrar 'Domain name registrar'
  [4]: https://en.wikipedia.org/wiki/NIC_handle 'NIC handle'
  [5]: https://en.wikipedia.org/wiki/ICANN 'ICANN'
