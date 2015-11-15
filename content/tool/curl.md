---
title: "curl"
date: 2013-08-17 07:32
update: 2015-11-14 16:00
---

[TOC]

## Argument ##

* `-o` - output to file
* `-O` - output to file named the same with the remote name
* `-i` - Include the HTTP-header in the output
* `-I` - only get the HTTP-header
* `-u`

## Example ##

	# get the file source and output to the STDOUT
	curl http://wiki.wutianqi.com/index.html

	# download the file
	curl -o myindex.html http://wiki.wutianqi.com/index.html
	curl -O http://wiki.wutianqi.com/index.html

	# get the HTTP-header only
	curl -I http://wiki.wutianqi.com/index.html


## IPv6 ##

curl ipv6 localhost:8000, 注意要加`-g`和`-6`, url要用方括号(bracket):

    curl -g -6 'http://[::1]:8000'

参考: [How can I use curl with ::1 for ipv6 based loopback?](http://superuser.com/a/885757/251495)

## Read More ##

* [15 Practical Linux cURL Command Examples](http://www.thegeekstuff.com/2012/04/curl-examples/)
* [curl tutorial with examples of usage](http://www.yilmazhuseyin.com/blog/dev/curl-tutorial-examples-usage)
* [curl网站开发指南](http://www.ruanyifeng.com/blog/2011/09/curl.html)

