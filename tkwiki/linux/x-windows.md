# X-Windows安装记录 #

参考: [X服务器配置指南](http://www.gentoo.org/doc/zh_cn/xorg-config.xml)

先在 `/etc/make.conf` 添加相应配置

后来发现emerge -pv xorg-server后，有很多问题，于是

    emerge -pv xorg-server > /tmp/xorg-server.log 2>&1


查看 `emerge -pv` 日志

    !!! Your current profile is deprecated and not supported anymore.
    !!! Use eselect profile to update your profile.
    !!! Please upgrade to the following profile if possible:
      default/linux/amd64/13.0


解决:  
`eselect profile list`  
原来是`no-multilib`，然后`eselect profile set [number]`选择desktop就行了

然后再次emerge -pv查看，有很多Blocks：

    [blocks B      ] sys-apps/kmod ("sys-apps/kmod" is blocking sys-apps/module-init-tools-3.16-r1)
    [blocks B      ] sys-apps/module-init-tools ("sys-apps/module-init-tools" is blocking sys-apps/kmod-12-r1)
    [blocks B      ] <sys-kernel/genkernel-3.4.25 ("<sys-kernel/genkernel-3.4.25" is blocking sys-fs/udev-197-r4)
    [blocks B      ] <sys-apps/openrc-0.9.9 ("<sys-apps/openrc-0.9.9" is blocking sys-fs/udev-197-r4)

    Total: 97 packages (6 upgrades, 90 new, 1 reinstall), Size of downloads: 235,887 kB
    Conflict: 4 blocks (4 unsatisfied)

    !!! Multiple package instances within a single package slot have been pulled
    !!! into the dependency graph, resulting in a slot conflict:

    dev-libs/libxml2:2

      (dev-libs/libxml2-2.8.0-r3::gentoo, ebuild scheduled for merge) pulled in by
        dev-libs/libxml2[python] required by (media-libs/mesa-9.0.1::gentoo, ebuild scheduled for merge)

      (dev-libs/libxml2-2.8.0-r2::gentoo, installed) pulled in by
        (no parents that aren't satisfied by other packages in this slot)

    sys-apps/hwids:0

      (sys-apps/hwids-20121119::gentoo, installed) pulled in by
        (no parents that aren't satisfied by other packages in this slot)

      (sys-apps/hwids-20130114::gentoo, ebuild scheduled for merge) pulled in by
        >=sys-apps/hwids-20130114[udev] required by (sys-fs/udev-197-r4::gentoo, ebuild scheduled for merge)

    sys-libs/zlib:0

      (sys-libs/zlib-1.2.5.1-r2::gentoo, installed) pulled in by
        (no parents that aren't satisfied by other packages in this slot)

      (sys-libs/zlib-1.2.7::gentoo, ebuild scheduled for merge) pulled in by
        >=sys-libs/zlib-1.2.6 required by (sys-apps/kmod-12-r1::gentoo, ebuild scheduled for merge)


    It may be possible to solve this problem by using package.mask to
    prevent one of those packages from being selected. However, it is also
    possible that conflicting dependencies exist such that they are
    impossible to satisfy simultaneously.  If such a conflict exists in
    the dependencies of two different packages, then those packages can
    not be installed simultaneously.

    For more information, see MASKED PACKAGES section in the emerge man
    page or refer to the Gentoo Handbook.


    !!! The following installed packages are masked:
    - dev-python/pysqlite-2.6.3::gentoo (masked by: package.mask)
    /usr/portage/profiles/package.mask:
    # Michał Górny <mgorny@gentoo.org>
    # Unmaintained and replaced by built-in sqlite3 module in Python.
    # Masked for removal in 30 days, bug 452122.

    For more information, see the MASKED PACKAGES section in the emerge
    man page or refer to the Gentoo Handbook.


     * IMPORTANT: 5 news items need reading for repository 'gentoo'.
     * Use eselect news to read news items.


针对第一步libxml2进行了升级：

    emerge -u dev-libs/libxml2:2

逐个update

关于Masked的文档，可以参考：
[Portage入门](http://www.gentoo.org/doc/zh_cn/handbook/handbook-x86.xml?part=2&chap=1)

    你也可能会遇到某些特定版本的包被屏蔽的情况，比如<media-video/mplayer-bin-1.0_rc1-r2。在这种情况下，升级到一个更新的版本就能解决问题


# 自动成成xorg配置 #

    root@gentoo profiles # Xorg -configure

    X.Org X Server 1.13.1
    Release Date: 2012-12-13
    X Protocol Version 11, Revision 0
    Build Operating System: Linux 3.4.9-gentoo x86_64 Gentoo
    Current Operating System: Linux gentoo-jl 3.4.9-gentoo #1 SMP Thu Nov 29 01:18:03 Local time zone must be set--see zic  x86_64
    Kernel command line: root=/dev/ram0 real_root=/dev/sda3
    Build Date: 12 February 2013  09:40:50PM

    Current version of pixman: 0.26.0
            Before reporting problems, check http://wiki.x.org
            to make sure that you have the latest version.
    Markers: (--) probed, (**) from config file, (==) default setting,
            (++) from command line, (!!) notice, (II) informational,
            (WW) warning, (EE) error, (NI) not implemented, (??) unknown.
    (==) Log file: "/var/log/Xorg.0.log", Time: Tue Feb 12 22:03:54 2013
    List of video drivers:
            nvidia
    modprobe: ERROR: could not insert 'nvidia': No such device
    No devices to configure.  Configuration failed.
    Server terminated with error (2). Closing log file.





x11-misc/Xorgautoconfig


gentoo portage

masked

slot

# 网上找的Linux X相关术语解释 #
TODO:

这个比较乱，需要再整理

    linux图形界面基本知识（X、X11、Xfree86、Xorg、GNOME、KDE之间的关系）

    LINUX初学者经常分不清楚linux和X之间，X和Xfree86之间，X和KDE，GNOME等之间是什么关系，常常混淆概念。
    本文以比较易于理解的方式来解释X，X11，XFREE，WM，KDE，GNOME等之间的关系。

    一、linux本身没有图形界面，linux现在的图形界面的实现只是linux下的应用程序实现的。
    图形界面并不是linux的一部分，linux只是一个基于命令行的操作系统
    linux和Xfree的关系就相当于当年的DOS和 WINDOWS3.0一样，windows3.0不是独立的操作系统，
    它只是DOS的扩充，是DOS下的应用程序级别的系统，不是独立的操作系统，
    同样 XFree只是linux下的一个应用程序而已，不是系统的一部分。但是X的存在可以方便用户使用电脑。
    WINDOWS95及以后的版本就不一样了，他们的图形界面是操作系统的一部分，图形界面在系统内核中就实现了，没有了图形界面windows就不成为windows了
    但linux却不一样，没有图形 界面linux还是linux，很多装linux的WEB服务器就根本不装X服务器.这也WINDOWS和linux的重要区别之一。

    二、X是协议，不是具体的某个软件。
    X 是协议，就像HTTP协议，IP协议一样.这个概念很多初学者甚至学习LINUX有一定时间的人都混淆
    一个基于X的应用程序需要运行并显示内容时他就联 接到X服务器，开始用X协议和服务器交谈。
    比如一个X应用程序要在屏幕上输出一个圆那么他就用X协议对X服务器说：
    喂!我需要在屏幕上画一个圆.X应用程序只负责告诉X服务器在屏幕的什么地方用什么颜色画一个多大的圆，
    而具体的"画"的动作，比如这个圆如何生成，用什么显卡的驱动程序去指挥显卡完成等等工 作是由X服务器来完成的。
    X服务器还负责捕捉键盘和鼠标的动作，假设X服务器捕捉到鼠标的左键被按下了，他就告诉X应用程序：
    亲爱的应用程序先生，我发现 鼠标被按下了，您有什么指示吗?如果X应用程序被设计成当按下鼠标左健后再在屏幕上画一个正方形的话，
    X应用程序就对X服务器说：请再画一个正方形，
    当然 他会告诉服务器在什么地方用什么颜色画多大的正方形，但不关心具体怎么画--那是服务器的事情。
    那么协议是需要具体的软件来实现的，这就是下面我要讲的:

    三、X和XFree86的关系.
    有了协议就需要具体的软件来实现这个协议.就好比我们有了交通法规就需要交警去根据法规维护交通秩序一样.
    Xfree86就是这样一个去根据法规实现协议的 "交警".他按照X协议的规定来完成X应用程序提交的在屏幕上显示的任务.
    当然不仅仅是某个特定的交警才可以去维护和实现这个法规，比如还可以由交通协管员来实现交通法规，
    必要的时候警察也可以介入，当然前提是他们都要懂得交通法规，也就是要懂得协议.
    所以实现X协议的软件也并不只有 XFree86，XFree86只是实现X协议的一个免费X服务器软件.
    商业上常用MOTIF，现在还有XORG，还有很多很小的由爱好者写的小的X服务 器软件.
    甚至可以在WINDOWS上有X服务器运行，这样你可以在linux系统上运行一个X应用程序然后在另一台windows系统上显示.多么神奇. 
    你可以用google找到这样的X服务器软件.只不过在LINUX上最常用的是XFree86.(现在的linux发行版都用Xorg了)顺便说一句，
    苹果电脑的图形界面用的也是X协议，而且被认为是做的最好的X协议图形界面，
    并且他对X协议的实施是做在系统内核里的，所以性能明显好很多，这就是为什么很 多大型三维图形设计软件都是在苹果平台上的原因.
    为了便于理解拿HTTP协议来比较:

    协议是HTTP (hyper text transmission protocol)
    实现这个协议的常用服务器有:apache IIS 等
    请求这些服务器传输文件的客户有:IE ，MOZILLA ，NETSCAPE等.
    协议是X
    实现这个协议的常用服务器有Xfree86 ，Xorg ，Xnest等
    请求这些服务器来完成显示任务的客户:所有的X应用程序.

    四、X和X11R6又是什么关系?
    不知道初学者有没有注意到/usr/X11R6这个目录，这是XFree的默认安装目录
    X11R6 实际上是 X Protocol version 11 Release 6
    (X协议第11版第六次发行)的意思，就是说目前用的X协议是第11版的，然后经过了6次小的修正.不同版本的X协议是不能通信的.就象我们现在IPV4和IPV6不能通信一样，不过不用担心，现在的X服务器软件和X应用程序都遵循X11R6.
    另外XFree86 3.3.6 XFree86 4.3.6 等这些版本是实现X协议的软件XFree86的版本号.这是初学者经常高混淆的概念.
    协议版本和实现协议的软件的版本--这两个概念的区别你分清楚了吗?

    五、X服务器和WM(window manager 窗口管理器)之间是什么关系.
    平时大家起动图形界面是怎么启动的呢?
    如果你是一开己就进入图形界面那就太遗憾了.应为你错过了了解X服务器起动过程的好时机.不过没关系.你打开一个XTERM输入:
    init 3
    就可以安全的回到字符界面.
    好了，等做完以下实验你就完全明白X和WM(window manager 窗口管理器)之间是什么关系了.
    先输入以下命令:
    #startx
    起动图形界面，你看到的是一个和平时使用一样的完整的图形界面操作环境.
    你可以最大化，最小化，移动，关闭窗口等.
    按ctrl+alt+backspace反回字符界面.
    输入:
    #xinit
    再次启动图形界面，你看到了什么，你看到一个XTERM.而且不能移动.但是你可以在这个XTERM中输入命令打开X应用程序，如果我输入:
    #mozilla
    打开浏览器，你看到的浏览器和平时有什么不同吗?他在屏幕中间，不能移动，不能最小化，不能最大化，没有边框.
    为什么同样一个X应用程序会有这样的不同呢?因为我们用startx起动图形界面的时候同时也启动了一个WM(即窗口管理器)，
    如果你用KDE就起动了KDE，如果你用GNOME就起动了GNOME.但是你用xinit起动图形界面的时候却没有起动WM.
    现在你明白窗口管理器的作用了吗?他的作用就是最大化，最小化，移动，关闭窗口等.而这些不是X服务器来负责完成的.
    如果你用xinit起动图形界面并在xterm中输入twm，看看会有什么?
    xterm被加上了一个边框，你可以通过这个边框移动，最大化，最小化这个xterm，
    twm就是XFree86中自带的窗口管理器，是一个比较简陋的最简单的窗口管理器，但是他具有窗口管理器的全部特征.
    如果你不输入twm而输入gnome-session就可以起动GNOME
    或者输入startkde起动KDE.
    通过以上的实验你就可以清楚的明白他们之间的关系.

    六、关于KDE和GNOME
    KDE 和GNOME是LINUX里最常用的图形界面操作环境，他们不仅仅是一个窗口管理器那么简单，
     KDE是K Desktop Environment 的缩写.他不仅是一个窗口管理器，还有很多配套的应用软件和方便使用的桌面环境，比如任务栏，开始菜单，桌面图标等等.
    GNOME是GNU Network Object Model Environment 的缩写.和KDE一样，也是一个功能强大的综合环境.
    另外在其它UNIX系统中，常常使用CDE作为这样一个环境.
    其它的小型窗口管理器有:
    window maker，after step，blackbox，fvwm，fvwm2，等等都是常用的优秀窗口管理器.
    REDHAT9中有 window maker 但是默认不安装，大家可以装来试试.只要xinit再wmaker&就可以用windowmaker了.

    七、linux图形界面层次关系总结
    linux本身-->X服务器<-[通过X协议交谈]->窗口管理器(综合桌面环境)-->X应用程序.
    Xfree86服务器的实现包括两个部分，一部分是和显卡直接打交道的低层，一部分是和X应用程序打交道的上层。
    上层负责接收应用程序的请求和鼠标 键盘的动作。
    而和显卡直接打交道的底层负责指挥显卡生成图形，其实就是显卡驱动。
    上层接收到应用程序的请求后，将请求内容做适当处理，然后交给显卡驱动来 指挥 显卡完成画图的动作.
    另外，上层的捕捉键盘和鼠标动作的部分会向应用程序提供鼠标和键盘的状态信息，应用程序接收到这些信息后决定是否再有相应的动作.
    平时说的VESA，VGA ，fbdev等其实就是针对不同模式显卡的驱动程序.
    VESA(Video Electronics Standards Association)
    VGA (Video Graphics Array)
    fbdev (FrameBuffer Device)
    等都是不同的显卡标准，不过这些标准都已经很老了.现在的显卡都兼容这几种模式.

更多参考：
[X Window 配置介绍](http://vbird.dic.ksu.edu.tw/linux_basic/0590xwindow.php)


# Read More #

* [Upgrading old Gentoo installations](http://www.ogalik.ee/upgrading-old-gentoo/)
* [emerge user guide](http://linuxreviews.org/gentoo/emerge/)	*
