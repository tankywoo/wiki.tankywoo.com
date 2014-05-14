---
title: "fastcgi"
date: 2013-08-17 07:36
---


## FastCGI ##

参考: [Nginx+FastCGI运行原理](http://book.51cto.com/art/201202/314840.htm)

## FastCGI介绍 ##

FastCGI是从CGI发展改进而来的。  
传统CGI接口方式的主要缺点是性能很差，因为每次HTTP服务器遇到动态程序时都需要重新启动脚本解析器来执行解析，然后将结果返回给HTTP服务器。  
这在处理高并发访问时几乎是不可用的。另外传统的CGI接口方式安全性也很差，现在已经很少使用了。

FastCGI接口方式采用C/S结构，可以将HTTP服务器和脚本解析服务器分开，同时在脚本解析服务器上启动一个或者多个脚本解析守护进程。  
当HTTP服务器每次遇到动态程序时，可以将其直接交付给FastCGI进程来执行，然后将得到的结果返回给浏览器。  
这种方式可以让HTTP服务器专一地处理静态请求或者将动态脚本服务器的结果返回给客户端，这在很大程度上提高了整个应用系统的性能。

维基百科上的解释：  
快速通用网关接口（Fast Common Gateway Interface／FastCGI）是一种重要的互联网技术，可以让一个客户端，从网页浏览器向执行在网页服务器上的程序请求数据。FastCGI是早期通用网关接口（CGI）的增强版本。  
FastCGI致力于减少网页服务器与CGI程序之间的互动，从而使服务器可以同时处理更多的网页请求。  
参考: [维基百科-FastCGI](http://zh.wikipedia.org/wiki/FastCGI)


## Nginx+FastCGI运行原理 ##

Nginx不支持对外部程序的直接调用或者解析，所有的外部程序（包括PHP）必须通过FastCGI接口来调用。  
FastCGI接口在Linux下是socket（这个socket可以是文件socket，也可以是ip socket）。  
为了调用CGI程序，还需要一个FastCGI的wrapper（wrapper可以理解为用于启动另一个程序的程序），  
这个wrapper绑定在某个固定socket上，如端口或者文件socket。  
当Nginx将CGI请求发送给这个socket的时候，通过FastCGI接口，wrapper接收到请求，然后派生出一个新的线程，  
这个线程调用解释器或者外部程序处理脚本并读取返回数据；  
接着，wrapper再将返回的数据通过FastCGI接口，沿着固定的socket传递给Nginx；  
最后，Nginx将返回的数据发送给客户端。这就是Nginx+FastCGI的整个运作过程。  
如图所示  

TODO
	{{/img/fastcgi_1.jpg}}

## spawn-fcgi与PHP-FPM ##

前面介绍过，FastCGI接口方式在脚本解析服务器上启动一个或者多个守护进程对动态脚本进行解析，这些进程就是FastCGI进程管理器，或者称之为FastCGI引擎  
spawn-fcgi与PHP-FPM就是支持PHP的两个FastCGI进程管理器。  
下面简单介绍spawn-fcgi与PHP-FPM的异同:  
spawn-fcgi是HTTP服务器lighttpd的一部分，目前已经独立成为一个项目，一般与lighttpd配合使用来支持PHP  
但是ligttpd的spwan-fcgi在高并发访问的时候，会出现内存泄漏甚至自动重启FastCGI的问题。

Nginx是个轻量级的HTTP server，必须借助第三方的FastCGI处理器才可以对PHP进行解析，因此Nginx+spawn-fcgi的组合也可以实现对PHP的解析，这里不过多讲述。

PHP-FPM也是一个第三方的FastCGI进程管理器，它是作为PHP的一个补丁来开发的，在安装的时候也需要和PHP源码一起编译  
也就是说PHP-FPM被编译到PHP内核中，因此在处理性能方面更加优秀；同时它在处理高并发方面也比spawn-fcgi引擎好很多  
因此，推荐Nginx+PHP/PHP-FPM这个组合对PHP进行解析。
 
FastCGI 的主要优点是把动态语言和HTTP Server分离开来  
所以Nginx与PHP/PHP-FPM经常被部署在不同的服务器上，以分担前端Nginx服务器的压力，使Nginx专一处理静态请求和转发动态请求  
而PHP/PHP-FPM服务器专一解析PHP动态请求。

## 关于php-cgi和php-fpm ##

CGI 是 Web Server 与 Web Application 之间数据交换的一种协议。  
FastCGI 同 CGI 是一种通信协议，但比  CGI 在效率上做了一些优化，同样 SCGI 协议与 FastCGI 类似。  
PHP-CGI 是 PHP （Web Application）对 Web Server 提供的 CGI 协议的接口程序。  
PHP-FPM 是 PHP（Web Application）对 Web Server 提供的 FastCGI 协议的接口程序，额外还提供了相信智能一些任务管理。  
参考：[请问CGI、PHP-CGI、PHP-FPM之间是什么关系?](https://groups.google.com/forum/?fromgroups=#!topic/shlug/d5hJKyFzI-g)
