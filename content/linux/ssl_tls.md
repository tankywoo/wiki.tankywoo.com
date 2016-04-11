---
title: "SSL/TLS相关"
date: 2016-04-07 09:50
#draft: true
id: AHK7TCr5
---

[TOC]

## 自建CA ##

环境:

* Gentoo
* OpenSSL 1.0.2g

当前环境下, 有关SSL证书的目录是 `/etc/ssl/`。

A certificate authority (CA) is an entity that signs digital certificates.

默认openssl配置: `/etc/ssl/openssl.cnf`， 定义openssl操作时的一些默认选项。

	####################################################################
	[ ca ]
	default_ca      = CA_default            # The default ca section

	####################################################################
	[ CA_default ]

	#dir            = ./demoCA              # Where everything is kept
	dir             = /etc/ssl/demoCA       # Where everything is kept
	certs           = $dir/certs            # Where the issued certs are kept
	crl_dir         = $dir/crl              # Where the issued crl are kept
	database        = $dir/index.txt        # database index file.
	#unique_subject = no                    # Set to 'no' to allow creation of
											# several ctificates with same subject.
	new_certs_dir   = $dir/newcerts         # default place for new certs.

	certificate     = $dir/cacert.pem       # The CA certificate
	serial          = $dir/serial           # The current serial number
	crlnumber       = $dir/crlnumber        # the current crl number
											# must be commented out to leave a V1 CRL
	crl             = $dir/crl.pem          # The current CRL
	private_key     = $dir/private/cakey.pem        # The private key
	RANDFILE        = $dir/private/.rand    # private random number file

其中:

* `default_ca` 配置默认使用的ca配置块，这里配置的是下面的「CA_default」块。
* `dir` 配置CA相关的根目录，默认是相对路径，因为涉及到在别的路径下操作，所以这里我改为绝对路径。
* `certs` / `crl_dir` 存放的是个人使用的相关的 cert / crl。具体讨论见: [What is “certs” in openssl.conf for?](http://serverfault.com/questions/360825/what-is-certs-in-openssl-conf-for)
* `database` / `serial` / `crlnumber` 都是维护的索引文件，编号可以自定义。
* `new_certs_dir` 存放通过ca签发的证书。
* `private_key` 是CA证书私钥。
* `certificate` 是CA证书。
* `crl` 是当前的CRL。

扩展这块还需要研究: TODO

	x509_extensions = usr_cert              # The extentions to add to the cert

匹配策略配置:

	# A few difference way of specifying how similar the request should look
	# For type CA, the listed attributes must be the same, and the optional
	# and supplied fields are just that :-)
	policy          = policy_match
	
	# For the CA policy
	[ policy_match ]
	countryName             = match
	stateOrProvinceName     = optional
	organizationName        = optional
	organizationalUnitName  = optional
	commonName              = supplied
	emailAddress            = optional

如果是 `match`, 则必须要一样的配置才行; 比如之前「organizationName 」是match, 而我签发证书时写的和CA的organizationName 不一样，导致报错:

	$ openssl ca -in www.tankywoo.com.csr -out www.tankywoo.com.crt
	Using configuration from /etc/ssl/openssl.cnf
	Check that the request matches the signature
	Signature ok
	The organizationName field needed to be the same in the
	CA certificate (myorg1) and the request (myorg2)


