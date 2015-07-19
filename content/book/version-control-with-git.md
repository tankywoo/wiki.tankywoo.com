---
title: "Version Control with Git"
date: 2014-04-28 23:31
---

[TOC]

* First Edition, 2009, 英文影印版
* 第二版, 2015, 中文版

*注*: 在 [@e2c89f10](https://github.com/tankywoo/wiki.tankywoo.com/commit/e2c89f107421c1bc668185298946cc33d969e441?short_path=031a497#diff-031a497c22aeea7eabd1a48496833702) 这个提交及之前, 因为看的是影印版(看了3年才只看了8章...), 所以很多笔记都是英文的. 5月份第二版中文版出了, 立马买了一本, 所以后续会逐步改为中文笔记, 部分原话及术语保留英文.

## 3. 起步 ##

查看帮助:

	# For a complete list of git subcommands
	$ git help --all

	# document for git subcommand
	$ git help <subcommand>
	$ git <subcommand> --help

命令行中的`双破折号`(double dash):

> About `bare double dash` (`--`), in shell, it indicate the end of the command options; The same as in git, it seperate the option and the path.
[ref 1](http://unix.stackexchange.com/questions/11376/what-does-double-dash-mean-also-known-as-bare-double-dash)
[ref 2](http://unix.stackexchange.com/questions/52167/what-does-mean-in-linux-unix-command-line)
[ref 3](http://stackoverflow.com/questions/1192180/deleting-a-badly-named-git-branch/1192194#1192194)
[ref 4](http://stackoverflow.com/questions/13321458/meaning-of-git-checkout-double-dashes)

查看某个特定提交的详细信息 `git show`:

	# show the details of the most recent commit
	$ git show

	# To see more detail about a particular commit
	$ git show <commit number>

查看所有分支的整体情况 `git show-branch`:

	$ git show-branch --more=10

更详细的可以看看[GitGuys](http://www.gitguys.com/topics/git-show-branch-to-see-branches-and-their-commits/?lang=zh)上的图解.

---

## 4.基本的Git概念 ##

**注意**: 这章太重要了, 字字都是珠玑, 真想把整篇都copy过来.

在版本库中, Git维护两个主要的数据结构: `对象库(object store)` 和 `索引(index)`. 所有这些版本库数据存放在工作目录根目录下的`.git`的隐藏目录中.

索引是**暂时**的信息, 对版本库来说是**私有**的, 并且可以在需要的时候按需求进行创建和修改.

对象库是git版本库实现的核心. 包含了原始数据文件和所有日志信息、作者信息、日期, 以及其它用来重建项目任意版本或分支的信息.

### 对象库(Object Store) ##

Git对象库中的对象**只有**四种类型: 块(blog), 目录树(tree), 提交(commit)和标签(tag). 这四种原子对象构成Git高层数据结构的基础.

* `块 (Blob)` : 

    文件的每一个版本都表示为一个块(blob). blob 是`二进制大对象(binary large object)`的缩写. 一个blob保存一个文件的数据, 但不包含任何关于这个文件的元数据, 甚至没有文件名.

* `树 (Tree)` :

    一个目录树(tree)对象代表一层目录信息. 它记录blob标识符, 路径名和在一个目录下所有文件的一些元数据. 它可以递归引用其它目录树或子树对象, 从而建立一个包含文件和子目录的完整层次结构.

* `提交 (Commit)` :

    一个提交(commit)对象保存版本库中每一次变化的元数据, 包括作者、提交者、提交日期和日志消息. 每一个提交对象指向一个目录树对象, 这个目录树对象在一张完整的快照中捕获提交时版本库的状态.

* `标签 (Tag)` :

    一个标签对象分配一个任意的且human readable的名字给一个特定对象, 通常是一个提交对象.

对象库会随着项目的开发一直变化和增长, 为了有效利用磁盘空间和网络带宽, Git把对象压缩并存储在`打包文件(pack file)`里, 这些文件也在对象库里.


### 索引(Index) ###

索引, 又称`暂存区(Stage)`, 是一个临时的、动态的二进制文件.

    $ file .git/index
    .git/index: data

它捕获项目在某个时刻的整体结构的一个版本.


下面是一个简单的git object内部dag图, 经过两次的提交, 非常清晰(摘自书上图4-2):

![Figure 4-2. Git objects after a second commit](http://tankywoo-wb.b0.upaiyun.com/git-4-2.png!small)


### 可寻址内容名称 ###

Git对象库被组织及实现成一个内容可寻址的存储系统. 对象库中每个对象都有一个唯一的名称, 这个名称是向对象的内容应用sha1得到的`sha1散列值`, sha1值是一个160位的数, 通常表示为一个40位的十六进制数.

### Git追踪内容 ###

Git不仅是一个VCS, 还是一个内容追踪系统(content tracking system). 主要表现为两个方式:

* Git的对象库基于其对象内容的散列计算的值, 而不是基于用户的原始文件布局的文件名或目录的设置.

    Git追踪的是内容而不是文件, 如果两个文件的内容完全一样, 无论是否在相同的目录, Git在对象库里只保存一份blob形式的内容副本.

* 当文件从一个版本变到下一个版本时, Git的内部数据库有效地存储每个文件的每个版本, 而不是他们的差异.

### 打包文件(pack file) ###

之前提到的, git 会存储每个文件的每一个版本.

但是, 这个并不是绝对的, 比如一个大文件, 每次只修改其中一行, 那么, 经过多次修改后, 这个文件的各个blob会占用非常大的空间.

实际上git不会这么笨的, git有一个有效的存储机制, 叫做 `打包文件(pack file)`.

git 往磁盘保存对象时默认使用的格式叫松散对象 (loose object) 格式

git 时不时地将这些对象打包至一个叫 packfile 的二进制文件以节省空间并提高效率.

经过打包后, git会存储文件的最新版本, 其余的版本都以差异形式存储(`delta`)

例子:

	$ git init
	$ echo 'hello' > hello.txt; git add hello.txt; git commit -m 'add hello.txt'

	$ tree .git/objects
	.git/objects
	├── 0b
	│   └── 9d7dbd4e9e2b8be42ebe043083937acd52fccf
	├── aa
	│   └── a96ced2d9a1c8e72c56b253a0e2fe78393feb7
	├── ce
	│   └── 013625030ba8dba906f756967f9e9ca394464a
	├── info
	└── pack

	5 directories, 3 files

	# 将Python自带的BaseHTTPServer.py加到仓库里
	$ git add BaseHTTPServer.py; git commit -m 'add BaseHTTPServer.py'

	$ wc -l BaseHTTPServer.py
		 603 BaseHTTPServer.py

	# mac os 下 du 没有 -b 参数
	$ stat -f%z BaseHTTPServer.py
	22461

	$ tree .git/objects
	.git/objects
	├── 04
	│   └── 0fc62ff827be04d5def454bfef3ef8c49ea488
	├── 0b
	│   └── 9d7dbd4e9e2b8be42ebe043083937acd52fccf
	├── 25
	│   └── fc7b5d264c24fed7f7a843fbe9ae3224a07de8
	├── aa
	│   └── a96ced2d9a1c8e72c56b253a0e2fe78393feb7
	├── ce
	│   └── 013625030ba8dba906f756967f9e9ca394464a
	├── de
	│   └── af2f960b83c76b38b0c494db91202c70886833
	├── info
	└── pack

	8 directories, 6 files

	# 找到blob id是 deaf2f960b83c76b38b0c494db91202c70886833
	# 显示的大小是字节, 这个是经过压缩的大小
	$ stat -f%z .git/objects/de/af2f960b83c76b38b0c494db91202c70886833
	8569

	# 添加一行
	$ echo 'a new line' >> BaseHTTPServer.py; git commit -m 'add a new line' BaseHTTPServer.py

	$ find .git/objects -type f
	.git/objects/04/0fc62ff827be04d5def454bfef3ef8c49ea488
	.git/objects/0b/9d7dbd4e9e2b8be42ebe043083937acd52fccf
	.git/objects/25/fc7b5d264c24fed7f7a843fbe9ae3224a07de8
	.git/objects/28/5fb1a7ab0bcfe01588ad548ac96187366e8c74
	.git/objects/3b/119f80b81e4483b12812eb72ebb2df338adbc5
	.git/objects/95/16bba0fea3fb039a6e028fb975bb35d158626f
	.git/objects/aa/a96ced2d9a1c8e72c56b253a0e2fe78393feb7
	.git/objects/ce/013625030ba8dba906f756967f9e9ca394464a
	.git/objects/de/af2f960b83c76b38b0c494db91202c70886833

	# 新的blob id是 9516bba0fea3fb039a6e028fb975bb35d158626f
	$ stat -f%z .git/objects/95/16bba0fea3fb039a6e028fb975bb35d158626f
	8575

	$ git gc
	Counting objects: 9, done.
	Delta compression using up to 4 threads.
	Compressing objects: 100% (7/7), done.
	Writing objects: 100% (9/9), done.
	Total 9 (delta 1), reused 0 (delta 0)

	$ tree .git/objects
	.git/objects
	├── info
	│   └── packs
	└── pack
		├── pack-dde2d3ff207bb65df9a3a3d2f4f6e088a18622ad.idx
		└── pack-dde2d3ff207bb65df9a3a3d2f4f6e088a18622ad.pack

	2 directories, 3 files

	$ more .git/objects/info/packs
	P pack-dde2d3ff207bb65df9a3a3d2f4f6e088a18622ad.pack

	$ stat -f%z .git/objects/pack/pack-dde2d3ff207bb65df9a3a3d2f4f6e088a18622ad.idx
	1324
	$ stat -f%z .git/objects/pack/pack-dde2d3ff207bb65df9a3a3d2f4f6e088a18622ad.pack
	8334

	$ git verify-pack -v .git/objects/pack/pack-dde2d3ff207bb65df9a3a3d2f4f6e088a18622ad.idx
	3b119f80b81e4483b12812eb72ebb2df338adbc5 commit 221 155 12
	25fc7b5d264c24fed7f7a843fbe9ae3224a07de8 commit 228 163 167
	0b9d7dbd4e9e2b8be42ebe043083937acd52fccf commit 172 125 330
	9516bba0fea3fb039a6e028fb975bb35d158626f blob   22472 7596 455
	ce013625030ba8dba906f756967f9e9ca394464a blob   6 15 8051
	285fb1a7ab0bcfe01588ad548ac96187366e8c74 tree   82 90 8066
	040fc62ff827be04d5def454bfef3ef8c49ea488 tree   82 90 8156
	deaf2f960b83c76b38b0c494db91202c70886833 blob   9 20 8246 1 9516bba0fea3fb039a6e028fb975bb35d158626f
	aaa96ced2d9a1c8e72c56b253a0e2fe78393feb7 tree   37 48 8266
	non delta: 8 objects
	chain length = 1: 1 object
	.git/objects/pack/pack-dde2d3ff207bb65df9a3a3d2f4f6e088a18622ad.pack: ok

`git verify-pack`是用于验证pack文件的, 查看man手册里输出格式说明:

	When specifying the -v option the format used is:

	   SHA-1 type size size-in-pack-file offset-in-packfile

	for objects that are not deltified in the pack, and

	   SHA-1 type size size-in-packfile offset-in-packfile depth base-SHA-1

对比上面的输出, 可以看到, BaseHTTPServer.py的第一个版本就是 @deaf2f96, 它的base-SHA-1是 @9516bba0, 且 @deaf2f96 的大小只有9bytes, pack中的压缩后大小是20, 而新的blob在pack中的大小是22472字节. pack中的大小是7596

第二个版本是完整保存文件内容的对象, 而第一个版本是以差异方式保存的, 这是因为大部分情况下需要快速访问文件的最新版本.

git 自动定期对仓库进行重新打包以节省空间. 也可以手工运行 git gc 命令来这么做.

参考:

* Pro Git: Git Internals - Packfiles [zh](https://git-scm.com/book/zh/v1/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-Packfiles) | [en](https://git-scm.com/book/en/v2/Git-Internals-Packfiles)
* Git Community Book [zh](http://gitbook.liuhui998.com/7_5.html) | [en](https://schacon.github.io/gitbook/7_the_packfile.html)

另外, 在 pro git那一章还学到一个命令:

	$ git cat-file -p master^{tree}

和下面效果一样:

	$ git ls-tree master

### 底层命令例子 ###

以下例子使用的基本都是Git的底层命令, 在实际使用中, 有更简单的命令封装了这些底层命令, 不过通过底层命令, 可以更清晰的了解Git的工作流程.

* `git cat-file`
* `git write-tree`
* `git commit-tree`
* `git rev-parse`
* `git ls-files`

初始化的Git仓库:

	# An initial git repo
	$ find .git/objects
	.git/objects
	.git/objects/info
	.git/objects/pack

新建一个文件a.txt, 内容是 'hello', sha1值 ce013625030ba8dba906f756967f9e9ca394464a, 使用`git cat-file`查看散列的内容:

	$ echo 'hello' > a.txt
	$ git add a.txt
	$ find .git/objects
	.git/objects
	.git/objects/ce
	.git/objects/ce/013625030ba8dba906f756967f9e9ca394464a
	.git/objects/info
	.git/objects/pack

	$ git cat-file -p ce013625030ba8dba906f756967f9e9ca394464a
	hello

使用`git ls-files`查看staged信息:

    $ git ls-files -s
    100644 ce013625030ba8dba906f756967f9e9ca394464a 0       a.txt

捕获索引状态并保存到一个树对象:

	$ git write-tree
	2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1

	$ git cat-file -p 2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt

现在增加文件b.txt, 内容和a.txt一样, 可以看到, 两个使用同一个blob:

	$ echo 'hello' > b.txt
	$ git add b.txt

	$ git write-tree
	b5b0cccf7401633f12e0fafc6b85731251b86850

	$ git cat-file -p b5b0cccf7401633f12e0fafc6b85731251b86850
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    b.txt

现在改变文件a.txt内容, b.txt还是指向原来的blob:

	$ echo 'world' >> a.txt
	$ git add a.txt

	$ git write-tree
	579c3877d5f450e34ea642b3a29d2d01dcf8e392

	$ git cat-file -p 579c3877d5f450e34ea642b3a29d2d01dcf8e392
	100644 blob 94954abda49de8615a048f8d2e64b5de848e27a1    a.txt
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    b.txt

添加一个子目录, 里面也放一个a.txt, 内容一样:

    $ mkdir subdir
    $ cp a.txt subdir/
    $ tree
    .
    ├── a.txt
    └── subdir
        └── a.txt

    1 directory, 2 files
    $ git add subdir/a.txt

    $ git ls-files -s
    100644 ce013625030ba8dba906f756967f9e9ca394464a 0       a.txt
    100644 ce013625030ba8dba906f756967f9e9ca394464a 0       subdir/a.txt

    $ git write-tree
    ec518d6bb3cabb8e88b5458cf18d862aa0514622

    $ git cat-file -p ec518d6bb3cabb8e88b5458cf18d862aa0514622
    100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt
    040000 tree 2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1    subdir

可以看到, subdir这个tree对象的sha1 id和之前父目录是一样的.

现在a.txt的blob已经有了, 树对象也有了, 接着就是提交:

    $ echo -n 'commit a file' | git commit-tree ec518d6bb3cabb8e88b5458cf18d862aa0514622
    7dc4ee9984a52278b3b67480feb712e36ea5a64c

    $ git cat-file -p 7dc4ee9984a52278b3b67480feb712e36ea5a64c
    tree ec518d6bb3cabb8e88b5458cf18d862aa0514622
    author Tanky Woo <me@tankywoo.com> 1431832347 +0800
    committer Tanky Woo <me@tankywoo.com> 1431832347 +0800

    commit a file%

`author` vs `committer`(引用 [Pro Git](http://git-scm.com/book/ch2-3.html))

> The author is the person who originally wrote the patch, whereas the committer is the person who last applied the patch. So, if you send in a patch to a project and one of the core members applies the patch, both of you get credit — you as the author and the core member as the committer.

更详细的[解释](http://stackoverflow.com/a/18754896/1276501)

打标签:

    $ git tag -m 'add tag v1.0' v1.0 7dc4ee9984a52278b3b67480feb712e36ea5a64c

    $ git rev-parse v1.0
    76a2a639a517e26a6c79fdcd09c0a5ffec97e099

    $ git cat-file -p v1.0
    object 7dc4ee9984a52278b3b67480feb712e36ea5a64c
    type commit
    tag v1.0
    tagger Tanky Woo <me@tankywoo.com> 1431832535 +0800

    add tag v1.0

    $ git cat-file -p 76a2a639a517e26a6c79fdcd09c0a5ffec97e099
    object 7dc4ee9984a52278b3b67480feb712e36ea5a64c
    type commit
    tag v1.0
    tagger Tanky Woo <me@tankywoo.com> 1431832535 +0800

    add tag v1.0

---

## 5. 文件管理和索引 ##

关于文件管理, 与其它版本管理系统类似, 不过Git在`工作目录(working directory)`与`版本库(repository)`之间, 增加了一个`Index(Stage)`层, 称为`索引(暂存)`目录. 在工作目录下编辑, 在索引中积累修改, 然后把索引中积累的修改作为一次性的变更来进行提交.

![Git process](https://marklodato.github.io/visual-git-guide/basic-usage-2.svg)

(图片引用 [图解Git](https://marklodato.github.io/visual-git-guide/index-zh-cn.html))

![The lifecycle of the status of your files](http://tankywoo-wb.b0.upaiyun.com/git-5-lifecycle.png!small)

(图片引用 [Pro Git - 2.2](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository))

> Linus Torvalds 在git mailing list里提到，如果不先理解Index的目的，就无法理解和领会Git的强大.

Git 的Index不存放任何文件的内容，它只简单的记录准备提交的文件，当运行`git commit`时，git 会检查Index而不是工作目录.

Git 把文件分为三个大类: `已追踪(Tracked)`, `未追踪(Untracked)`和`被忽略(Ignored)`，其中`Tracked`又可以分为`暂存(Staged)` 和 `未暂存(Unstaged)`，在工作目录下修改Tracked的文件是Unstaged，经过`git add`后变为Staged.


`git ls-files --stage` 可以查看stage中的文件的`sha1`值:

	$ git ls-files --stage  # 或 git ls-files -s
	100644 8d0e41234f24b6da002d962a26c2495ea16a425f 0       fa

`git hash-object`可以计算文件的`sha1`值并输出:

	$ git hash-object fa
	8d0e41234f24b6da002d962a26c2495ea16a425f

简单的说是文件fa已经在 索引(index) 中了，本质是文件在 对象库(object store) 中，Index指向它.

关于 `--all` 在 `git add` 和 `git commit`中有点区别，文件必须要经过add才会被tracked，`git add --all` 会把所有tracked 和 untracked的文件都add，但是`git commit --all`只会add所有tracked的文件并提交.

关于`git rm`，如果tracked中的文件被修改了，则可以通过`git rm --cached`来从git库中移除，并在本地保存为untracked的，也可以通过`-f`强制删除.

对于被误删的文件，如果在Index中，如下:

	$ git status
	# On branch master
	# Changes to be committed:
	#   (use "git reset HEAD <file>..." to unstage)
	#
	#       deleted:    fa
	#

可以通过如下方式之一来返回:

	$ git checkout HEAD -- fa

	# 或者

	$ git reset HEAD fa
	$ git checkout -- fa

如果是移除被提交，则可以通过`git reset HEAD^`或rebase来取回.

关于`git mv`，等价于:

	$ mv fa fb
	$ git rm fa
	$ git add fb

Git 把文件fa改为fb，会在`object store`中保存原始的文件内容，然后把文件名(路径名path)重新关联到这个内容:

	$ git ls-files --stage
	100644 15acaeb140c2805acdbb2d0dbdedeeea6bb73b06 0       fa

	$ git mv fa fb
	$ git ls-files --stage
	100644 15acaeb140c2805acdbb2d0dbdedeeea6bb73b06 0       fb

把fa改为fb后，sha1值并没变.

经过mv操作后，使用`git log fb`只会看到变更后的提交(包括变更的那个提交)，即关联内容并为fb文件的历史，可以通过`--follow`选项来查看关联这段内容的完整历史:

	$ git log --follow fb

关于 `.gitignore` 文件, 简单语法:

* 忽略空行, `#` **开头** 作为注释, 如果跟在其它文本后面, 则不是注释
* 简单的字符文件名匹配任何目录下的同名文件或**目录**
* 目录名由反斜线`/`结尾, 表示只匹配同名的目录, 不匹配文件和软链接
* `*`作为通配符, 类似shell
* 感叹号`!`表示对改行其余部分的模式取反

Git版本库中任何目录下都可以有.gitignore文件, 且只影响当前目录及子目录. 作用规则是**级联**的, 可以覆盖父级以上的规则.

另外Git有多个地方可以影响ignore文件, 所以有优先级关系(从高到低):

* 命令行中指定的模式
* 当前目录下.gitignore文件中的模式
* 父级以上目录中.gitignore文件中的模式
* `.git/info/exclude`文件中的模式
* 环境配置`core.excludedfile`指定文件中的模式

A Detailed View of Git’s Object Model and Files 一节对 Git中对象模型和文件的详细视图, 把一次从 干净->编辑->add->commit 的原理图画出来了, 讲得非常好:

Figure 5-1. Initial files and objects:

![Figure 5-1. Initial files and objects](http://tankywoo-wb.b0.upaiyun.com/git-5-1.png!small)

Figure 5-2. After editing file1:

![Figure 5-2. After editing file1](http://tankywoo-wb.b0.upaiyun.com/git-5-2.png!small)

Figure 5-3. After git add:

![Figure 5-3. After git add](http://tankywoo-wb.b0.upaiyun.com/git-5-3.png!small)

Figure 5-4. After git commit:

![Figure 5-4. After git commit](http://tankywoo-wb.b0.upaiyun.com/git-5-4.png!small)

关于索引, 更多可以参考:

* [Git权威指南](http://www.worldhello.net/2010/11/30/2166.html)
* [Git Community Book](http://gitbook.liuhui998.com/7_4.html)
* [GitGuys - 什么是Git Index?](http://www.gitguys.com/topics/whats-the-deal-with-the-git-index/?lang=zh)
* [图解Git](https://marklodato.github.io/visual-git-guide/index-zh-cn.html)
* [git - 简明指南](http://rogerdudler.github.io/git-guide/index.zh.html)

---

## 6. 提交 ##

当提交时, Git会记录索引的快照并把快照放进对象库.

Git可以通过显示引用(explicit ref)或隐式引用(implied ref)来表示提交. 散列id(sha1)是显示引用, HEAD等是隐式引用.

引用(ref)是一个sha1散列值, 指向Git对象库中的对象.

符号引用(symref) 是一个指向引用的引用(指针), 间接的指向git对象. 有点类似C语言里指针的指针? 和Linux的软链接(soft link)也有点类似?

本地特性分支名, 远程跟踪分支名, 标签名都是引用.

每一个<strike>符号</strike>引用都有一个以 refs/ 开始的明确名称, 并且都分层存储在版本库的`.git/refs/` 目录中. 基本分为三种:

* refs/heads/<ref> 代表本地分支
* refs/remotes/<ref> 代表远程跟踪分支
* refs/tags/<ref> 代表标签

**注**(2015-07-19更新):

书上说:

> Each symbolic ref has an explicit, full name that begins with refs/ and each is stored hierarchically within the repository in the .git/refs/ directory.

我查了文档, 并且看了`git symbolic-ref`的man手册, 发现这里的解释是**错误**的

首先, 关于master, 即 .git/refs/heads/master:

	$ more .git/refs/heads/master
	f35f166562045569095169d340fec0d16eaef73b

存储的也是sha1 id, 所以它不是一个符号引用, 而只是一个引用.

另外用`git symbolic-ref`也可以看到说这不是一个符号引用:

	$ git symbolic-ref master
	fatal: ref master is not a symbolic ref

那么, 哪些是符号引用? 暂时只知道默认的有HEAD:

	$ git symbolic-ref HEAD
	refs/heads/master

	$ more .git/HEAD
	ref: refs/heads/master

接着, 符号引用有什么特征? 还是`git symbolic-ref`的man手册, 写的很清楚:

	A symbolic ref is a regular file that stores a string that begins with `ref: refs/`. For example, your .git/HEAD is a regular file whose contents is `ref: refs/heads/master`.

很显然, HEAD符合这个特征.

符号引用也可以自己创建, 还是用上面的命令:

	$ git symbolic-ref TANKYWOO refs/heads/master
	$ git rev-parse TANKYWOO
	f35f166562045569095169d340fec0d16eaef73b
	$ git rev-parse master
	f35f166562045569095169d340fec0d16eaef73b
	$ more .git/TANKYWOO
	ref: refs/heads/master
	$ git symbolic-ref TANKYWOO
	refs/heads/master

(2015-07-19更新 结束)

比如本地分支dev, 就是 refs/heads/dev 的缩写:

	$ git show dev
	commit e31b74d259b83af0f69683b9b12a29ebb3946748
	Merge: 12e3223 5488c82
	Author: Tanky Woo <wtq1990@gmail.com>
	Date:   Fri Apr 10 19:11:27 2015 +0800

		Merge branch 'project-tools' into dev

	$ git show refs/heads/dev
	commit e31b74d259b83af0f69683b9b12a29ebb3946748
	Merge: 12e3223 5488c82
	Author: Tanky Woo <wtq1990@gmail.com>
	Date:   Fri Apr 10 19:11:27 2015 +0800

		Merge branch 'project-tools' into dev

	$ more .git/refs/heads/dev
	e31b74d259b83af0f69683b9b12a29ebb3946748

Git 有几个特殊<strike>符号</strike>引用(除了HEAD, 其余都不是符号引用):

* `HEAD`
* `ORIG_HEAD`
* `FETCH_HEAD`
* `MERGE_HEAD`

`HEAD`: `.git/HEAD`, 总是指向当前分支的最后一次提交, 当分支改变，HEAD也会变

	$ more .git/HEAD
	ref: refs/heads/master

`ORIG_HEAD`: `.git/ORIG_HEAD`, 一些操作, 如`merge`或`reset`, 会记录操前的commit(HEAD). 作为一个保护措施，使操作可以回溯.

比如最近三个commits 以及 此时的ORIG_HEAD(存储的是之前某一个的commit id):

	* d46546a - (HEAD, master) update d (42 seconds ago) <Tanky Woo>
	* 8ed2d79 - update f (76 seconds ago) <Tanky Woo>
	* 75b09c2 - (tag: v0.1) Merge branch 'dev' (3 days ago) <Tanky Woo>

	$ more .git/ORIG_HEAD
	015b5b99f5c9973e840f29c9f6e6b936c99b92a5

做一次reset操作:

	$ git reset --soft HEAD^

查看`ORIG_HEAD`, 会指向之前的HEAD:

	$ more .git/ORIG_HEAD
	d46546a5192b7e1c834947b612e3401a6f7729c7

这样就可以回溯到reset之前的版本:

	$ git reset ORIG_HEAD

然后 `ORIG_HEAD` 又指向 @8ed2d79 这个id

`HEAD` vs `ORIG_HEAD` [HEAD and ORIG_HEAD in Git](http://stackoverflow.com/questions/964876/head-and-orig-head-in-git)

`FETCH_HEAD`: `.git/FETCH_HEAD`, 当使用远程库时, git fetch 命令将所有抓取分支的头记录到这个文件中, 是最近fetch的分支HEAD的简写.

	$ git fetch origin
	$ more .git/FETCH_HEAD
	f35f166562045569095169d340fec0d16eaef73b                branch 'master' of https://example.com/tankywoo/git-test-symref

`MERGE_HEAD`: 当一个合并操作正在进行时, 其它分支的头暂时记录在 `MERGE_HEAD` 中. 即是正在合并进HEAD的提交.

`git symbolic-ref` 操作符号引用:

	(master*) $ git symbolic-ref HEAD
	refs/heads/master

详细可以参考[progit-9.3](http://git-scm.com/book/en/Git-Internals-Git-References)

sha1 id是绝对提交名, 通过`~`和`^`则可以代表相对提交名.

* `^ (caret)` 同一代提交中, 用来选择不同的父提交(比如合并时有多个父提交)
* `~ (tilde)` 某个提交的父提交或更上一/N代提交

使用前面讲到的`git show-branch`可以看到每个提交的相对提交名.

例子:

	*   75b09c2 - (HEAD, master) Merge branch 'dev' (4 seconds ago) <Tanky Woo>
	|\
	| * 0aab100 - (dev) Add d (26 seconds ago) <Tanky Woo>
	| * 6a9379e - Add c (31 seconds ago) <Tanky Woo>
	* | 015b5b9 - Add f (14 seconds ago) <Tanky Woo>
	|/
	* 545851d - Add b (59 seconds ago) <Tanky Woo>
	* 1509ece - Add a (80 seconds ago) <Tanky Woo>

第一个父提交:

	$ git log -1 --pretty=oneline --abbrev-commit -p master^1
	015b5b9 Add f

第二个父提交, 这是从dev分支合并进master的分支:


	$ git log -1 --pretty=oneline --abbrev-commit -p master^2
	0aab100 Add d

使用波浪号(~):

	$ git log -1 --pretty=oneline --abbrev-commit -p master~1
	015b5b9 Add f

`master^1` 等价于 `master~1`

组合使用:

	$ git log -1 --pretty=oneline --abbrev-commit -p master^2~1
	6a9379e Add c


### 查看提交历史 ###

`git log` 默认就是 `git log HEAD`

使用`-p/--patch` 可以查看提交的修改补丁:

	$ git log -1 -p HEAD

这个等价于:

	$ git show HEAD

`git show` 还可以查看某个文件的blob内容:

	$ git diff fa
	diff --git a/fa b/fa
	index 89b24ec..7bba8c8 100644
	--- a/fa
	+++ b/fa
	@@ -1 +1,2 @@
	 line 1
	+line 2

	$ git show :fa
	line 1

fa在历史库中只有line 1这一行, 在unstaged中增加了line 2.

还可以查看远程追踪分支中某文件的blob内容, 如:

	$ git show origin/master:setup.py

使用`git log <start>..<end>` **两个dot** 语法来查看某一段历史, 表示 "结束" 的提交可到达 且 "开始" 的提交不可到达的一组提交. 如:

	# 查看master~11, master~10, 但是不包括 master~12
	$ git log master~12..master~10

如图:


![Figure 6-9. Interpreting ranges as set subtraction](http://tankywoo-wb.b0.upaiyun.com/git-6-9.png!small)

实际也就是:

	$ git log ^X Y

**TODO** 这块看图6-11, 6-12, 6-13

`<start>..<end>` 的范围表示集合的减法运算, 而 `<A>...<B>` **三个dot** 表示A和B的对称差(symmetric difference), 也就是 A或B可达 且又 不同时在 A和B的并集 中.

比如 dev 是从master的init这个提交衍生出来的, 随后master和dev各增加一个提交:

	# master: init -> add fc
	# dev:	init -> add fb

	(master) $ git log master...dev --oneline
	52bdb27 add fc
	20d2444 add fb

下面这个命令效果是一致(**TODO**):

	(master) $ git rev-list --abbrev-commit master...dev --not $(git merge-base --all master dev)
	52bdb27
	20d2444


### 查找提交 ###

`git bisect` 二分法查找. 一般用于查找某次坏提交造成的问题.

`git blame` 用于查看一个文件中的没一行最后是最提交以及commit id:

	$ git blame CHANGELOG.rst
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  11) v1.3 (2015-03-04)
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  12) ===================
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  13)
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  14) 1. Add `site.time` variable, the generated time.
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  15) 2. Improve encoding
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  16) 3. Add `--update-them` when generate to improve generation speed
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  17) 4. Fix #36, add attach directory to put attachments.
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  18) 5. Fix #33, only show color logging message on Linux/MacOS
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  19)
	7a6a703b (Tanky Woo         2015-03-04 11:47:40 +0800  20)
	211a6669 (Tanky Woo         2014-12-23 12:35:59 +0800  21) v1.2.4 (2014-12-23)
	211a6669 (Tanky Woo         2014-12-23 12:35:59 +0800  22) ===================
	211a6669 (Tanky Woo         2014-12-23 12:35:59 +0800  23)
	211a6669 (Tanky Woo         2014-12-23 12:35:59 +0800  24) * Fix #31 encode/decode problems
	211a6669 (Tanky Woo         2014-12-23 12:35:59 +0800  25) * Fix image overflow in simple themes
	211a6669 (Tanky Woo         2014-12-23 12:35:59 +0800  26)
	211a6669 (Tanky Woo         2014-12-23 12:35:59 +0800  27)

`git log -S` 用于根据给定的关键字搜索出现在历史差异中的提交, 也成为pickaxe

但是需要注意: 如果某个提交 添加 和 删除 相同数量含关键词的行, 则这个提交不会被查找出来; 提交必须有添加和删除数量上的变化才能计数.

如:

	line 1       line 1
	row  2   ->  line 3
	line 3       row  3

则无法搜出这次提交.


## 7. 分支 ##

为了支持可扩展和分类组织, 可以创建一个带层次的分支名, 类似于Unix的路径名, 如

    # fix bug的分支集
    bug/pr-1
    bug/pr-2

    # 特性分支集
    feature/smt-1
    feature/smt-2

这样也例子筛选分支:

    $ git show-branch 'bug/*'

分支名的一些限制:

* 不能以斜线`/`结尾
* 不能以减号`-`开头
* 斜线分隔的分支名不能以点`.`开头, 如 feature/.new
* 分支名任何地方不能包含两个连续的点`..`
* 不能包含任何空格和空白字符
* 不能包含在Git中有特殊含义的字符, 如`~`, `^`, `:`, `?`, `*`, `[`
* ascii控制字符, 即小于`\040`的字符以及DEL符`\178`

使用`git merge-base` 可以找到两个点的共同祖先, 如master和dev分支:

    $ git merge-base master dev

新建分支时, 默认是从当前分支的最近一个点衍生出新分支, 也可以指定分支或某个sha1 id:

    $ git branch feature/new master
    $ git branch feature/new 7a6a703b

上面命令只新建, 不切换分支, `git checkout -b xxx`是新建且切换.

`git show-branch` 和 `git branch`的参数类似, 支持`-r` (远程分支), `-a` (所有分支).

关于`git show-branch`输出的解释, 之前几章多次用到这个命令, 这里终于有详细的解释了:

    (master*) $ git show-branch master dev category-index
    * [master] Release v1.3
     ! [dev] Merge branch 'project-tools' into dev
      ! [category-index] Merge branch 'project-tools' into dev
    ---
     -- [dev] Merge branch 'project-tools' into dev
     ++ [dev^2] Makefile add tox and covhtml section
     ++ [dev^2^] Update Makefile clean section
     ++ [dev^2~2] Add arguments for `nosetests` command
     ++ [dev~10] rename class InitSite to Initiator and refactor
     ++ [dev~11] rename initsite.py to initiator.py
     -- [dev~12] Merge branch 'support-draft' into dev
     ++ [dev~12^2] Add tester for draft
     ++ [dev~13] Add tag after release
    *++ [master] Release v1.3

默认情况下(不带参数), 会显示所有的本地分支,  我这里为了方便, 只显示3个分支, 且删除了中间很多提交.

输出被一排破折号分为两部分, 破折号长度与分支数有关.

破折号上方显示分支名, 每个分支名一行:

* 括号内是分支名
* 分支名后面是此分支最近的一次提交信息
* 分支名前面, `*` 表示当前分支; `!` 表示其它分支
* 每个分支一列, 后面讲到

破折号下面是提交信息:

* 起始的`+`表示提交在一个分支中, `*`突出表示当前分支的提交, `-` 表示是一个合并
* 中间显示的是每个sha1 id的相对引用, 这个在前面介绍过, 也可以用`--sha1-name`显示sha1 id.
* 后面显示相应提交的commit message

列表会显示到所有分支(活指定的所有分支)的公共祖先那个点, 也可以加`--more`来多显示一些commit.

关于checkout切换分支有冲突的情况, 比如某个文件同一块地方在两个分支都有改变, 默认无法切换, 除非`-f`强制切换, 一般的解决方法:

* git stash 暂存
* git checkout -m 做一个合并

试了下第二种方法, 比较麻烦, 一般习惯还是用stash


## 8. Diff ##

Unix/Linux 中的 `diff` 命令:

* `-u` 产生一个合并格式的差异(unified diff)
* `-r` 遍历整个目录
* `---` 表示原始文件, `+++` 表示新文件
* `@@ -1,2 +1 @@`部分, -表示原始文件, 1表示第1行, 4表示连续4行, 即第1行开始连续4行; +表示新文件, 1表示第一行, 后面没有指定连续行表示默认的1行

<!-- -->

	$ diff -u -r dir1 dir2
	diff -u -r dir1/fa dir2/fa
	--- dir1/fa     2015-05-24 12:16:11.000000000 +0800
	+++ dir2/fa     2015-05-24 12:15:54.000000000 +0800
	@@ -1,2 +1 @@
	-1-fa
	-1-fa
	+2-fa
	diff -u -r dir1/sub_dir/fb dir2/sub_dir/fb
	--- dir1/sub_dir/fb     2015-05-24 12:10:37.000000000 +0800
	+++ dir2/sub_dir/fb     2015-05-24 12:11:02.000000000 +0800
	@@ -1 +1 @@
	-1-fb
	+2-fb


`git diff`的效果类似`diff -u -r dir1 dir2`

四种基本比较:

* `git diff`: 工作目录和索引之间的差异
* `git diff <commit>`: 工作目录与给定commit之间的差异
* `git diff --cached <commit>`: 索引与给定提交之间的差异, 默认是HEAD. 1.6.1版本后可以用`--staged`代替`--cached`
* `git diff <commit1> <commit2>` : 两个commit之间的差异

还有一些常用的选项:

* `-M`: 针对重命名(rename, `git mv <file1> <file2>`), 只显示简单的结果, 而不是显示先删除再添加的内容
* `-w/--ignore-all-space`: 忽略空白字符
* `--stat`: 显示一个统计结果, 多少行发生变化, 添加多少, 删除多少

<!-- -->

    $ git mv log.py log2.py
    $ git diff --cached -M
    diff --git a/simiki/log.py b/simiki/log2.py
    similarity index 100%
    rename from simiki/log.py
    rename to simiki/log2.py

关于git diff中的提交范围, 和git log是不一样的, 首先明确两点:

* git diff不关心文件的历史，也不关心分支
* git log关注一个文件是如何变味另外一个(历史).

另外以下两个是等价的:

    $ git diff master..dev
    $ git diff master dev

如这个历史数:

          A---B---C topic
         /
    D---E---F---G master

    $ git diff master..topic    # A,B,C,F,G
    $ git diff master...topic   # A,B,C

这块网上有几篇讲得不错的:

* [dots in diff](https://matthew-brett.github.io/pydagogue/git_diff_dots.html), [dots in log](https://matthew-brett.github.io/pydagogue/git_log_dots.html#git-log-dots) 不过这里有个错误, `git log master topic`和`git log master..topic`是不等价的
* [Git "range" or "dot" syntax](https://wincent.com/wiki/Git_%22range%22_or_%22dot%22_syntax)
* [What are the differences between double-dot “..” and triple-dot “…” in Git diff commit ranges?](http://stackoverflow.com/questions/7251477/what-are-the-differences-between-double-dot-and-triple-dot-in-git-dif) 一图胜千言

git diff 还可以限制路径:

	# 限制在某个目录下
	git diff <some_directory>

	# 现在在某个文件中
	git diff <some_file>

如`-S`在git log中, `git diff`也有-S参数:

	# 在master分支最近50个提交中搜索包含指定字符串的变更
	git diff -S "octopus" master~50


## 9. 合并 ##

Git支持同时合并三个、四个或多个分支. 但是大多数情况下, 一次合并只结合两个分支.

> 作为一般规则, 每次合并都从干净的工作目录和索引开始, 那么Git的操作会变得容易很多

关于合并冲突的详解:

配置好环境:

	$ git show-branch
	! [alt] one world
	 * [master] all worlds
	--
	 * [master] all worlds
	+  [alt] one world
	+* [master^] init

两个分支, 一个文件hello

master分支和alt分支基于一个初始提交, 第二个提交分别是:

master:

	 hello
	+worlds
	+Yay!

alt:

	 hello
	+world
	+Yay!

master上合并alt, 产生冲突:

	$ git merge alt
	Auto-merging hello
	CONFLICT (content): Merge conflict in hello
	Automatic merge failed; fix conflicts and then commit the result.

	$ git status
	On branch master
	You have unmerged paths.
	  (fix conflicts and run "git commit")

	Unmerged paths:
	  (use "git add <file>..." to mark resolution)

			both modified:   hello

	no changes added to commit (use "git add" and/or "git commit -a")

	$ cat hello
	hello
	<<<<<<< HEAD
	worlds
	=======
	world
	>>>>>>> alt
	Yay!

现在hello这个文件的状态是`unmerged`. Git在处理合并冲突时, 会对冲突的文件标记为`冲突的(conflicted)`或`未合并的(unmerged)`.

	$ git diff hello
	diff --cc hello
	index e63164d,562080a..0000000
	--- a/hello
	+++ b/hello
	@@@ -1,3 -1,3 +1,7 @@@
	  hello
	++<<<<<<< HEAD
	 +worlds
	++=======
	+ world
	++>>>>>>> alt
	  Yay!

对于有冲突的文件,`git diff`会比较特殊, 之前说的默认情况下是比较当前工作目录与索引的差异, 这里显示的是两个服版本作的差异, 第一个是HEAD版本, 第二个是alt版本, 第二个又称`MERGE_HEAD`.

另外这里的+-号不再是一列了, 而是两列, 第一列表示相对当前版本的修改, 第二列是相对另一个版本的修改. 这个输出有点类似`show-branch`的结果.

	$ git diff HEAD
	diff --git a/hello b/hello
	index e63164d..1f2f61c 100644
	--- a/hello
	+++ b/hello
	@@ -1,3 +1,7 @@
	 hello
	+<<<<<<< HEAD
	 worlds
	+=======
	+world
	+>>>>>>> alt
	 Yay!

	$ git diff --ours
	* Unmerged path hello
	diff --git a/hello b/hello
	index e63164d..1f2f61c 100644
	--- a/hello
	+++ b/hello
	@@ -1,3 +1,7 @@
	 hello
	+<<<<<<< HEAD
	 worlds
	+=======
	+world
	+>>>>>>> alt
	 Yay!

这种就是正常的HEAD和工作目录的diff. `git diff HEAD` 等价于 `git diff --ours`

	$ git diff MERGE_HEAD
	diff --git a/hello b/hello
	index 562080a..1f2f61c 100644
	--- a/hello
	+++ b/hello
	@@ -1,3 +1,7 @@
	 hello
	+<<<<<<< HEAD
	+worlds
	+=======
	 world
	+>>>>>>> alt
	 Yay!

	$ git diff --theirs
	* Unmerged path hello
	diff --git a/hello b/hello
	index 562080a..1f2f61c 100644
	--- a/hello
	+++ b/hello
	@@ -1,3 +1,7 @@
	 hello
	+<<<<<<< HEAD
	+worlds
	+=======
	 world
	+>>>>>>> alt
	 Yay!

`git diff MERGE_HEAD` 等价于 `git diff --theirs`

	$ git diff $(git merge-base HEAD MERGE_HEAD)
	diff --git a/hello b/hello
	index ce01362..1f2f61c 100644
	--- a/hello
	+++ b/hello
	@@ -1 +1,7 @@
	 hello
	+<<<<<<< HEAD
	+worlds
	+=======
	+world
	+>>>>>>> alt
	+Yay!

	$ git diff --base
	* Unmerged path hello
	diff --git a/hello b/hello
	index ce01362..1f2f61c 100644
	--- a/hello
	+++ b/hello
	@@ -1 +1,7 @@
	 hello
	+<<<<<<< HEAD
	+worlds
	+=======
	+world
	+>>>>>>> alt
	+Yay!

`merge-base`会显示两个版本的公共祖先. 上面两条命令也是等价

接着做一些改动, 处理冲突, 删除三方合并标记线, 但是先不add, 还是保留unmerged状态:

	$ more hello
	hello
	worlds xxx			# 随便添加些字符
	Yay!
	$ git diff
	diff --cc hello
	index e63164d,562080a..0000000
	--- a/hello
	+++ b/hello
	@@@ -1,3 -1,3 +1,3 @@@
	  hello
	- worlds
	 -world
	++worlds xxx
	  Yay!

	$ more hello
	hello
	worlds  # 使用 --ours版本
	Yay!
	$ git diff
	diff --cc hello
	index e63164d,562080a..0000000
	--- a/hello
	+++ b/hello

	$ more hello
	hello
	world  # 使用 --theirs版本
	Yay!
	$ git diff
	diff --cc hello
	index e63164d,562080a..0000000
	--- a/hello
	+++ b/hello

后两者都没有diff, 这是git diff又一个特殊的地方: 对于有冲突的文件, git diff只显示真正有冲突的部分, 如果只有一边有变化, 这部分就不显示.

	$ git add hello
	$ git status
	On branch master
	All conflicts fixed but you are still merging.
	  (use "git commit" to conclude merge)

	Changes to be committed:

			modified:   hello

	$ git diff --cached
	diff --git a/hello b/hello
	index e63164d..562080a 100644
	--- a/hello
	+++ b/hello
	@@ -1,3 +1,3 @@
	 hello
	-worlds
	+world
	 Yay!

如果解决冲突并add后, 就可以看到实际diff了.

在解决冲突的过程中, 可以使用git log快速找到变更的地方:

	$ git log --merge --left-right -p
	commit < 944b769511d84455382a53c947f262db97dcbb09
	Author: Tanky Woo <wtq1990@gmail.com>
	Date:   Tue Jun 30 22:11:42 2015 +0800

		add master

	diff --git a/hello b/hello
	index ce01362..e63164d 100644
	--- a/hello
	+++ b/hello
	@@ -1 +1,3 @@
	 hello
	+worlds
	+Yay!

	commit > 4e2d91547b64b9ee2f26de286175819502d8c262
	Author: Tanky Woo <wtq1990@gmail.com>
	Date:   Tue Jun 30 09:35:05 2015 +0800

		one world

	diff --git a/hello b/hello
	index ce01362..562080a 100644
	--- a/hello
	+++ b/hello
	@@ -1 +1,3 @@
	 hello
	+world
	+Yay!

`--merge`会使用`MERGE_HEAD`来找到两者的差异.

`git ls-files -u` 可以查看工作树中未合并的文件:

	$ git ls-files -u
	100644 ce013625030ba8dba906f756967f9e9ca394464a 1       hello
	100644 e63164d9518b1e6caf28f455ac86c8246f78ab70 2       hello
	100644 562080a4c6518e1bf67a9f58a32a67bff72d4f00 3       hello

分别是1. base, 2. ours, 3. theirs

	$ git cat-file -p ce013625030ba8dba906f756967f9e9ca394464a
	hello

	$ git cat-file -p e63164d9518b1e6caf28f455ac86c8246f78ab70
	hello
	worlds
	Yay!

	$ git cat-file -p 562080a4c6518e1bf67a9f58a32a67bff72d4f00
	hello
	world
	Yay!

git diff支持在这两个版本之间互相diff:

	$ git diff :1:hello :3:hello
	diff --git a/:1:hello b/:3:hello
	index ce01362..562080a 100644
	--- a/:1:hello
	+++ b/:3:hello
	@@ -1 +1,3 @@
	 hello
	+world
	+Yay!

合并冲突的回退. 如果在冲突过程中想要回退, 可以:

	$ git reset --hard HEAD

如果在冲突解决后想到放弃, 回退(或终止), 可以:

	$ git reset --hard ORIG_HEAD

如果在解决冲突时解决方案失败, 比如弄得非常乱, 想重新回到冲突的原始状态, 重新解决, 可以:

	$ git checkout -m

交叉合并(criss-cross merge), 是指修改在分支间来回合并.

TODO 给出例子

Degenerate merge(退化合并)(中文翻译真蛋疼, 还是原词好理解一些), 就是指merge后不引入一个合并提交:

* 已经是最新的(already up-to-date)
* 快进合并 (fast-forward)

关于合并的策略, 用`-s`参数指定. 有5种(man git-merge, 见`MERGE STRATEGIES`一节):

* resolve (解决)
* recursive (递归)
* octopusd (章鱼)
* ours (我们的)
* subtree (子树)

resolve 曾经是Git的默认策略, 现已改为recursive. 处理针对两个分支合并的情况, 定义两个分支的共同祖先, 然后进行三路合并(3-way merge algorithm)

recursive 是默认的策略. 和resolve类似, 也是针对两个分支合并的情况. 可以处理多个共同祖先的情况, 进行三路合并. 在Linux的开发历史上, 此策略证明会比resolve导致更少的冲突而没有故障. 此策略还有很多策略选项, 用`-X`来指定, 常用的有`ours`和`theirs`.

octopusd 针对合并两个分支以上的情况. 当超过两个分支以上合并时, 这个是默认策略

ours 可以合并任意数量的分支. 但它实际是丢弃了其它分支的修改, 只使用当前分支的修改. 结果是和当前HEAD一样, 只是会标记其它分支也是父提交. 注意这个和recursive的-X ours策略选项不一样.

subtree 这个不理解 TODO

关于策略ours和recuresive的策略选项ours, theirs, 在我之前的博客有总结到: [Git merge strategy - ours and theirs](http://blog.tankywoo.com/git/2014/05/20/git-merge-strategy-ours-and-theirs.html)

用到现在, 策略这块基本就是用的默认策略, 其它复杂的情况还没用过, 也没有更多的体会...


## 10. 更改提交 ##

更改历史的哲学 TODO

一般原则, 只要没有其它开发人员获取到你的版本库副本, 那么可以任意的修改历史. 但是如果已经被他人同步过, 则不应该重写或修改历史. 不然对其他人来说是个灾难 :(

最常用的改写历史的应该是:

	$ git commit --amend

经常用这个来修改最后一次提交, 或其提交日志, 提交作者等.

其次就是reset操作, 调整HEAD引用指向给定的提交.

	$ git reset

它有三个选项:

* --sotf
* --mixed (默认方式)
* --hard

`--soft`软重置, 是副作用最小的, 只变化了HEAD引用, 比如:

	$ git reset --soft HEAD^

会重置到上一次提交, 并把最后一次提交的修改移到索引, 原先索引和未暂存的内容不会有影响

`--mixed` 副作用中等. 会影响索引的内容. 比如:

	$ git reset HEAD^

会重置到上一次提交, 并把最后一次提交的修改移到未暂存区, 且如果索引原先有修改, 也会被移到未暂存区.

`--hard`是杀伤力最大的. 影响到了工作目录的内容. 如:

	$ git reset --hard HEAD^

会重置到上一次提交, 并把最后一次提交的修改删除, 且如果索引和暂存区原来有修改, 都会删除.

前阵子在这里吃了一个大亏, wiki库有些修改积压了一阵子, 没提交(甚至都没add到索引, 不然还可以通过reflog找回...), 一个误操作用了--hard, 一夜回到解放前...

另外, 这里有一个有用的引用`ORIG_HEAD`, 在git reset时, git会把原始的HEAD存到ORIG_HEAD, 这样如果误操作后想返回到原来的版本, 可以:

	$ git reset --hard ORIG_HEAD

接着是`cherry-pick`, 将指定的commit应用到当前分支.

比如开发分支dev有个修复bug的提交dev~2, 现在需要临时引入到master分支应用上, 就可以用cherry-pick来操作:

	# 当前在master分支上
	$ git cherry-pick dev~2

cherry-pick还可以重建一系列提交, 比如一个分支的某两个提交想互换顺序, 可以引入一个新分支, 通过cherry-pick按预计顺序引入到新分支.

`revert` 和 cherry-pick 类似, 不过它的作用是应用指定提交的逆过程. 一般用于修复某个有问题的提交, 通过撤销来修复.

比如master分支上的某个提交master~3的修改有问题, 现在想撤销, 如果是线上公布的分支, 不建议rebase, 可以通过revert撤销:

	$ git revert master~3

这是引入一个新的提交, 是master~3的逆修改, 添加的就删除, 删除的就添加.

`rebase`(中文"变基", 很操蛋的翻译) 是用来改变一串提交以什么为基础.

> Forward-port(向前移植) local commits to the updated upstream head

常见的调用git rebase的两个命令(简化了来自man git-rebase的语法):

	$ git rebase [-i | --interactive] [options] [--onto <newbase>] [<upstream> [<branch>]]
	$ git rebase --continue | --skip | --abort | --edit-todo

首先最常用的功能, 是保持当前开发分支相对另一个分支是最新的.

比如一个多人协作的仓库, master分支是公共分支, 个人分支mydev, 如果mydev因一些事情耽搁几天, 这是master有了一些新提交, mydev需要用到, 可以将mydev移到master上最新的点分叉出来, 这样也可以保证分支图不会拉的太长, 简单步骤就是:

	$ git checkout mydev
	$ git rebase master

或者:

	$ git rebase master mydev

这也是上面第一条命令的语法, 最少需要指定某个上游, 基于此上游迁移. 默认是对当前分支做迁移

如, 原始的提交DAG图是:

	(master) $ git log --graph --branches --all --decorate --oneline
	* 00698e1 (HEAD, master) update master_file
	* d07ac54 add master_file
	| * 07e33e5 (mydev) update mydev_file
	| * dceb4d8 add mydev_file
	|/
	* a8923b3 master 1
	* 942c6af init

现在我要将mydev分支移从d07ac54分叉, 作了rebase后:

	(master) $ git rebase master~1 mydev
	First, rewinding head to replay your work on top of it...
	Applying: add mydev_file
	Applying: update mydev_file

	(mydev) $ git log --graph --branches --all --decorate --oneline
	* 8756814 (HEAD, mydev) update mydev_file
	* d88bae4 add mydev_file
	| * 00698e1 (master) update master_file
	|/
	* d07ac54 add master_file
	* a8923b3 master 1
	* 942c6af init

现在8756814 和d88bae4是mydev分支的两个提交, 和以前的sha-1 id不同了, 因为基于的历史树不一样.

注意指定branch后, 执行rebase后会checkout到那个分支.

通过`--onto`参数, 可以把一条分支上的开发线整个移到另一个分支:

	(another_dev) $ git log --graph --branches --all --decorate --oneline
	* 9b81f22 (HEAD, another_dev) update another_dev_file
	* e32f75f add another_dev_file
	| * 00698e1 (master) update master_file
	| * d07ac54 add master_file
	| | * 07e33e5 (mydev) update mydev_file
	| |/
	|/|
	* | dceb4d8 add mydev_file
	|/
	* a8923b3 master 1
	* 942c6af init

	(another_dev) $ git rebase master
	First, rewinding head to replay your work on top of it...
	Applying: add mydev_file
	Applying: add another_dev_file
	Applying: update another_dev_file

	(another_dev) $ git log --graph --branches='*dev' --all --decorate --oneline
	* d632eb3 (HEAD, another_dev) update another_dev_file
	* 824c829 add another_dev_file
	* 98f4d44 add mydev_file
	* 00698e1 (master) update master_file
	* d07ac54 add master_file
	| * 07e33e5 (mydev) update mydev_file
	| * dceb4d8 add mydev_file
	|/
	* a8923b3 master 1
	* 942c6af init

经过常规的rebase后, 可以看到, 原先在mydev上的两个提交现在有了两次. 改为--onto方式:

	(another_dev) $ git rebase --onto master mydev~1 another_dev
	First, rewinding head to replay your work on top of it...
	Applying: add another_dev_file
	Applying: update another_dev_file

	(another_dev) $ git --no-pager log --graph --branches='*dev' --all --decorate --oneline
	* 6e661ce (HEAD, another_dev) update another_dev_file
	* 870b906 add another_dev_file
	* 00698e1 (master) update master_file
	* d07ac54 add master_file
	| * 07e33e5 (mydev) update mydev_file
	| * dceb4d8 add mydev_file
	|/
	* a8923b3 master 1
	* 942c6af init

如果rebase过程中发生了冲突, 则需要用到最开始说的第二条命令了.

遇到冲突时, rebase会在冲突的提交点挂起, 等待处理冲突

* 冲突完成后, `git rebase --continue`恢复rebase
* 如果不想要这个提交, 则可以`git rebase --skip`跳过这个提交
* 如果不想进行rebase, 则`git rebase --abort`中止rebase

`git rebase -i` 以交互式的方式处理指定范围的rebase操作, 常用于修改以前某次的提交.

一般找到需要需要处理的某个点, 比如abcdef, 则:  TODO

	$ git rebase -i abcdef~1

此时会进入编辑器, 然后对每个commit 指定操作, 默认是pick, 显示如:

	pick d07ac54 add master_file
	pick 00698e1 update master_file

	# Rebase a8923b3..00698e1 onto a8923b3 (2 command(s))
	#
	# Commands:
	# p, pick = use commit
	# r, reword = use commit, but edit the commit message
	# e, edit = use commit, but stop for amending
	# s, squash = use commit, but meld into previous commit
	# f, fixup = like "squash", but discard this commit's log message
	# x, exec = run command (the rest of the line) using shell
	#
	# These lines can be re-ordered; they are executed from top to bottom.
	#
	# If you remove a line here THAT COMMIT WILL BE LOST.
	#
	# However, if you remove everything, the rebase will be aborted.
	#
	# Note that empty commits are commented out

提示内容非常详细, 如果要对某个commit进行指定操作, 则修改pick为其它即可, 可以用简写或全称, 如e 或 edit都是编辑修改

* pick: 默认操作, 使用原来的commit, 没变化
* record: 使用原来的commit, 但是修改提交日志
* edit: 修改, 到指定点停下, 可以通过--amend修复
* squash: 和前一次提交进行融合, 并将两次提交日志合在一起打开编辑器让用户编辑后确认
* fixup: 和squash类似, 但是直接使用前一次提交的日志
* exec: 指定shell命令.

exec这个简单试了下, 不是基于某个commit id, 而是在预期的位置做一些shell操作, 如:

	pick 8cc5fcb addxxx master_file
	exec touch xxx
	pick ac7a580 update master_file

看了下官方的man手册, 在针对每个版本都做测试时非常有用, 如:

	pick 5928aea one
	exec make test
	pick 04d0fda two
	exec make test
	pick ba46169 three
	exec make test
	pick f4593f9 four
	exec make test

另外, git rebase -i进入编辑器后的注释提示信息相当详细, 除了介绍上面的几个操作命令, 还有其它说明:

* 可以重新排序, git rebase是从上至下执行的
* 甚至可以删除某个commit, 这样这个提交点就会丢失
* 如果编辑器里除了注释外的内容为空, 则中止rebase, 和 git rebase --abort 一样

另外, rebase是把当前分支历史(带合并)线性化到了指定分支. 所以如果移动范围有合并提交, 默认会被线性化, 通过参数`-p/--preserve-merges`可以保留合并提交. 不然历史树就和以前有较大出入.

rebase后, 如果后悔了, 可以:

	$ git reset --hard ORIG_HEAD


## 11. 储藏和引用日志 ##

储藏(stash)是一个很常用的功能, 工作目录有一些修改时, 如:

* 此时需要紧急修复一个bug, 可以stash储藏之前的修改, 然后开始修复bug
* 需要临时切换分支去修改一些东西, 因为一些冲突导致无法切换过去, 也可以先stash起来
* 需要pull更新本地, 但是有冲突导致pull失败, 可以stash起来, pull后在pop解决冲突

直接执行`git stash`则储藏当前的修改, 默认是save子命令

	$ git stash
	Saved working directory and index state WIP on master: 7f63cf0 update master file
	HEAD is now at 7f63cf0 update master file

这里WIP是work in process的缩写

stash的数据结构是一个`栈`, 即先进后出FILO(first in, last out), 相应的还原最近一个储藏则是:

	$ git stash pop

查看stash栈:

	$ git stash list
	stash@{0}: WIP on master: 7f63cf0 update master file
	stash@{1}: WIP on master: 7965691 master

这里储藏时是用的默认的信息, 指出了分支, 当前sha1 id.

`stash@{0}`是储藏的编号, 根据FILO的原则, 0表示最新的一个储藏

也可以手动输入信息:

	$ git stash save 'do a stash'
	Saved working directory and index state On master: do a stash
	HEAD is now at 7965691 master
	$ git stash list
	stash@{0}: On master: do a stash

stash也是一个引用指针(`refs/stash`), 所以也可以使用这个引用来查看:

	$ git show-branch stash
	[stash] On master: do a stash

另外, 要注意, git stash并不是把最近一次储藏替换当前文件, 而是会做一个合并的操作, 这个是非常智能的.

git stash pop时, 如果成功, 则会删除相应储藏, 如果失败, 如产生冲突, 则会保留储藏.

删除储藏, 默认删除最近一个, 也可以手动指定某个储藏:

	$ git stash drop

因为stash pop成功后会清掉, 可以使用apply只做应用还原, 但是不清理, 和drop一样, 也可以指定某个储藏:

	$ git stash apply

查看储藏的内容, 不加`-p`则只显示stat信息:

	$ git stash show -p stash@{1}

也可以

	$ git show stash@{1}

一些常用的选项:

* `-u/--include-untracked`: 本地某个untracked的文件导致pull冲突失败时, 可以使用此选项把untracked文件也stash
* `-p/--patch`: 选择部分储藏, 和git add -p一样
* `-k/--keep-index`: 只储藏unstaged部分, 保留索引中的修改, 默认是全部都储藏
* `--index`: pop的选项, 当储藏包括staged和unstaged部分时, pop会全还原未unstaged, 次选项会按照原来的格局恢复

储藏是本地的操作, 所以储藏的object是不会提交到远程的

储藏还有一个给力的功能, 转化为分支:

	$ git stash branch <branch name> stash@{5}

因为某个stash后可能有增加了很多大的修改, 这是可以单拉一个分支来处理.

不过stash和branch还是要区别使用, stash更多是针对一个临时的操作, 最好不要积压太久, 随时保持储藏栈清理; 所以相应也不要过多的将stash转为一个branch. 至少至今为止我还没有做过这样的操作...

引用日志(reflog)

有时, 一些危险的操作, 会导致本地丢失一些提交, 如没有push到远程仓库前误操作执行了git reset HEAD^.

使用引用分支可以恢复丢失的提交.

修改引用或更改分支头的Git操作都会记录引用日志:

* 复制
* 推送
* 新提交
* 修改/创建分支
* rebase
* reset
* ...

默认情况下, 引用日志在非裸版本库是弃用的, 在裸版本库(bare)中是禁用的. 可以通过如下开启:

    $ git config core.logAllRefUpdates true

查看引用日志:

    $ git reflog [show]
    7f63cf0 HEAD@{0}: reset: moving to HEAD@{1}
    3dd62fb HEAD@{1}: merge mod: Fast-forward
    7f63cf0 HEAD@{2}: checkout: moving from master to master
    7f63cf0 HEAD@{3}: checkout: moving from master to master
    7f63cf0 HEAD@{4}: checkout: moving from mod to master
    3dd62fb HEAD@{5}: commit: update file in mod
    ...
    73ed934 HEAD@{12}: commit: dev
    38d4a3d HEAD@{13}: checkout: moving from master to dev
    38d4a3d HEAD@{14}: commit (initial): add file

子命令show可有可无, 默认输出的引用是HEAD, 所以在上面也可以看到都是HEAD@{X}

因为分支名也是引用, 所以后接分支名可以查看某个分支的引用日志

    $ git reflog show master
    3dd62fb master@{0}: reset: moving to ORIG_HEAD
    7f63cf0 master@{1}: reset: moving to HEAD^

或者:

    $ git reflog show refs/heads/master
    3dd62fb refs/heads/master@{0}: reset: moving to ORIG_HEAD
    7f63cf0 refs/heads/master@{1}: reset: moving to HEAD^

针对输出结果, 第一列的sha1 id和第二列的别名是对应的, 第三列只出相应的操作类型和操作内容

`HEAD@{0}` 始终指向当前的HEAD, 这里可以看到`HEAD@{14}`是第一次提交

例子:

    $ git ll
    * 3dd62fb - (HEAD, mod, master) update file in mod (17 hours ago) <Tanky Woo>
    * 7f63cf0 - update master file (3 days ago) <Tanky Woo>
    ...

    $ git reflog | head -n 1
    3dd62fb HEAD@{0}: checkout: moving from mod to master

    (master) $ git reset --hard HEAD^
    HEAD is now at 7f63cf0 update master file

    $ git reflog | head -n 2
    7f63cf0 HEAD@{0}: reset: moving to HEAD^
    3dd62fb HEAD@{1}: checkout: moving from mod to master

现在本地执行了一次reset, 如果发现是误操作, 想要返回, 但是本地的修改没有推送到远程, 这是可以通过reflog撤回:

    $ git reset --hard HEAD@{1}
    HEAD is now at 3dd62fb update file in mod

表明要重置到老的HEAD版本.

当然, 这种情形下还有一个方法, 使用`ORIG_HEAD`:

    $ git reset --hard ORIG_HEAD
    HEAD is now at 3dd62fb update file in mod

如`HEAD@{1}`, 如果使用形式`@{X}`, 则表示当前分支:

    $ git show @{0}
    commit 3dd62fb79377c7d0419ca12183db780489287731
    Author: Tanky Woo <wtq1990@gmail.com>
    Date:   Sat Jun 20 21:56:27 2015 +0800

    ...

    $ git reflog show @{0}
    3dd62fb refs/heads/master@{0}: reset: moving to ORIG_HEAD
    7f63cf0 refs/heads/master@{1}: reset: moving to HEAD^
    ...

另外, reflog的花括号内还可以指定时间限定符, 如:

    TankyWoo $ /tmp/test/ (master) $ git reflog 'HEAD@{1 hours ago}'
    3dd62fb HEAD@{Sat Jun 20 22:00:12 2015 +0800}: reset: moving to HEAD@{1}
    3dd62fb HEAD@{Sat Jun 20 21:56:47 2015 +0800}: merge mod: Fast-forward
    7f63cf0 HEAD@{Sat Jun 20 21:56:38 2015 +0800}: checkout: moving from master to master

还支持如:

* 2 days ago
* 1 hour ago
* 1 minute ago
* yesterday
* last saturday
* 2015-01-01
* ...

这里注意以下是等价的:

    $ git log 'HEAD@{2 days ago}'
    $ git log HEAD@{2.days.ago}
    $ git log HEAD@{2-days-ago}

注意第一个的单引号, 否则shell报错.

对于可达或不可达的引用日志, 都有一个默认的过期时限.

也可以手动设置过期时间:

    $ git reflog expire --expire='1 day ago' --all
    $ git gc
    Counting objects: 15, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (4/4), done.
    Writing objects: 100% (15/15), done.
    Total 15 (delta 1), reused 15 (delta 1)

还可以通过`git reflog delete`删除指定的条目

内部细节:

引用日志都是存储在 `.git/logs` 下

    $ tree .git/logs/
    .git/logs/
    ├── HEAD
    └── refs
        └── heads
            ├── master
            └── mod

引用日志也是一个本地概念, 和stash一样, 是不会被推送到远程, 也不会在克隆时被复制下来.

一篇不错的文章: [Git Tip of the Week: Reflogs](http://alblue.bandlem.com/2011/05/git-tip-of-week-reflogs.html)


## 12. 远程版本库 ##

远程版本库(remote)是一个引用或句柄, 通过文件系统或网络指向另外一个版本库. 可以使用远程版本库作为简称, 代替又长又复杂的Git URL.

TODO

* 远程追踪分支(remote-tracking branch)
* 本地追踪分支

Git版本库分为:

* 裸(bare)版本库. 是分布式开发的权威焦点, 内容基本就是.git目录
* 非裸(nonbare)版本库.用于日常开发的仓库

在git clone时, 原始版本库的本地开发分支refs/heads/xxx, 会成为新克隆版本库的远程分支refs/remotes/xxx. 原始版本库的远程分支不会克隆过来.

clone下来默认的远程版本库名称是origin, 可以通过`--origin`改为其它的.


针对远程版本库的操作, 有常用的`git pull`, `git fetch`, `git push`, 还有`git remote`, `git ls-remote` 列出远程版本库的引用列表.(相对的 `git show-ref`显示本地的引用列表)

关于`git remote`, 这个是我比较常用的一个命令, 介绍一下一些功能:

最简单的查看远程仓库的URL:

	$ git remote -v

添加一个上游版本库(upstream repo):

	$ git remote add upstream <git url>

添加上游版本库后, 我想防止误操作把提交push到这个仓库, 可以修改push url:

	$ git remote set-url --push origin 'do not pushing'

查看远程版本库的详细内容(这个操作会访问远程仓库, 而不是直接基于本地配置):

	$ git remote -v show origin
	* remote origin
	  Fetch URL: git@github.com:tankywoo/simiki.git
	  Push  URL: git@github.com:tankywoo/simiki.git
	  HEAD branch: master
	  Remote branches:
		dev              tracked
		jinja-extensions tracked
		master           tracked
		project-tools    tracked
	  Local branches configured for 'git pull':
		dev              merges with remote dev
		jinja-extensions merges with remote jinja-extensions
		master           merges with remote master
		project-tools    merges with remote project-tools
	  Local refs configured for 'git push':
		dev              pushes to dev              (up to date)
		jinja-extensions pushes to jinja-extensions (up to date)
		master           pushes to master           (up to date)
		project-tools    pushes to project-tools    (up to date)

虽然很多操作都可以直接修改`.git/config`, 但是就像修改/etc/sudoers使用visudo命令, 而不是直接vi /etc/sudoers一样, 命令的可靠性要大于手动.

git支持的传输协议有本地文件系统,git原生协议,http/https协议,rsync协议等. 以前http/https协议效率很多, 不过在1.6.6版本后,效率已经和git原生协议的效率差不多了.

查看`.git/config`, 可以看到fetch refspec配置, 默认是:

	[remote "origin"]
			url = git@github.com:tankywoo/simiki.git
			fetch = +refs/heads/*:refs/remotes/origin/*

refspec语法:

	[+]source:destination

source表示源引用, destination表示目标引用, 两者用冒号(:)分隔. 前面的加号(+)是可选的, 有加号表示不会在传输过程中进行正常的快进安全检查. 星号(`*`)表示通配符匹配

git fetch 和 git push 都用到refspec, refspec的源和目标是依赖于执行的操作:

	操作		源					目标
	push		推送的本地引用		更新的远程引用
	fetch		抓去的远程引用		更新的本地引用

这里有个很多人都没注意到的地方, push 的对立面不是 pull, 而是 fetch. 很多人可能因为命令名以及上手就学的push/pull, 而在这里有了错误的认识.

TODO


## 13. 版本库管理(略) ##


## 14. 补丁 ##

虽然Git协议非常方便, 但是还是有些理由来使用补丁(patch)的: 1. 防火墙限制, 比如有些公司不允许做推送操作. 2. 将补丁发到公共邮箱(mailing list), 方便同行评审.

关于补丁的一系列操作从生成补丁到发送补丁最后到应用补丁:

* git format-path 生成email形式的补丁
* git send-mail通过SMTP协议发送Git补丁
* git am 应用补丁

`git format-patch` 命令以邮件消息的形式生成一个补丁. 常用的生成方式(参数)有几种方式:

* 特定提交数; 如-2, 表示生成2个patch
* 提交范围; 如 master~4..master~2, 表示生成master~3, master~2这两个patch(不包括master~4), 和diff, log指定范围类似
* 某次特定提交; 如master~1, 其实表示是范围master~1..HEAD

git diff 是 git format-patch的核心, 不过还是有些区别, git diff 生成单个的差异合集, 而git format-match是为每个提交都生成单个patch; 二是git diff不带邮件头等信息.

git format-patch 和 git log -p --pretty=email的输出基本一致, 前者多了一个--stats信息, 以及最后的Git版本号(这里是2.3.5):

    (master) % git format-patch -1
    0001-D.patch

    (master*) % more 0001-D.patch
    From 50e7530441d9836b8643e3a3134b9072c7763e60 Mon Sep 17 00:00:00 2001
    From: Tanky Woo <wtq1990@gmail.com>
    Date: Tue, 7 Jul 2015 07:45:38 +0800
    Subject: [PATCH] D

    ---
     file | 1 +
     1 file changed, 1 insertion(+)

    diff --git a/file b/file
    index b1e6722..8422d40 100644
    --- a/file
    +++ b/file
    @@ -1,3 +1,4 @@
     A
     B
     C
    +D
    --
    2.3.5

    (master*) % git log -p -1 --pretty=email
    From 50e7530441d9836b8643e3a3134b9072c7763e60 Mon Sep 17 00:00:00 2001
    From: Tanky Woo <wtq1990@gmail.com>
    Date: Tue, 7 Jul 2015 07:45:38 +0800
    Subject: [PATCH] D

    diff --git a/file b/file
    index b1e6722..8422d40 100644
    --- a/file
    +++ b/file
    @@ -1,3 +1,4 @@
     A
     B
     C
    +D


例子, 首先创造环境:

    (master) % git init
    (master) % echo A > file ; git add file ; git ci -mA
    (master) % echo B >> file ; git ci -mB file
    (master) % echo C >> file ; git ci -mC file
    (master) % echo D >> file ; git ci -mD file

    (master) % git log --graph --oneline --decorate master
    * 50e7530 (HEAD, master) D
    * 1f0c2fd C
    * 2d1b9ed B
    * d900590 A

首先 -X 指定提交数:

    (master*) % git format-patch -2
    0001-C.patch
    0002-D.patch

    (master*) % git format-patch -3
    0001-B.patch
    0002-C.patch
    0003-D.patch

默认情况下, git为每个补丁生成单独的文件, 用一序列数字加上提交日志消息为其命令.

指定提交范围:

    (master) % git format-patch master~3..master~1
    0001-B.patch
    0002-C.patch

指定某次提交:

    (master*) % git format-patch master~3
    0001-B.patch
    0002-C.patch
    0003-D.patch

    # 如果要包含提交A, 即首次提交:
    (master*) % git format-patch --root master~3
    0001-A.patch

    # 全部提交, 带上 --root 参数
    (master*) % git format-patch --root master
    0001-A.patch
    0002-B.patch
    0003-C.patch
    0004-D.patch

几种方式还可以互相配合:

    (master*) % git format-patch --root master -2
    0001-C.patch
    0002-D.patch

复杂的例子:

    (master) % git checkout -b alt master~2
    (alt) % echo X >> file ; git ci -mX file
    (alt) % echo Y >> file ; git ci -mY file
    (alt) % echo Z >> file ; git ci -mZ file

    # 这里使用 --all 可以画出全部分支的ASCII图
    (alt) % git log --graph --oneline --decorate --all master
    * fb5c9a0 (HEAD, alt) Z
    * f67540b Y
    * b50d656 X
    | * 50e7530 (master) D
    | * 1f0c2fd C
    |/
    * 2d1b9ed B
    * d900590 A

接着合并alt分支, 处理冲突, 再增加一个新提交:

    (alt) % git checkout master
    (master) % git merge alt
    # ... 处理冲突 ...
    (master) % echo F >> file ; git ci -mF file

现在的结构:

    (master) % git log --graph --oneline --decorate --all master
    * bfad1bc (HEAD, master) F
    *   1dd3011 Merge branch 'alt'
    |\
    | * fb5c9a0 (alt) Z
    | * f67540b Y
    | * b50d656 X
    * | 50e7530 D
    * | 1f0c2fd C
    |/
    * 2d1b9ed B
    * d900590 A

    (master) % git show-branch --more=10
    ! [alt] Z
     * [master] F
    --
     * [master] F
    +* [alt] Z
    +* [alt^] Y
    +* [alt~2] X
     * [master~2] D
     * [master~3] C
    +* [master~4] B
    +* [master~5] A

生成master~2..master范围的补丁:

    (master) % git format-patch master~2..master
    0001-X.patch
    0002-Y.patch
    0003-Z.patch
    0004-F.patch

注意: 合并提交本身是不会生成补丁.

关于范围解析, TODO P250

邮件补丁 TODO

git有两条命令来应用补丁:

* git am 高层命令
* git apply 底层命令

基础最开始的A-D的提交图, 增加一个新提交E, 设成patch:

    (master) % echo E >> file ; git ci -mE file
    (master) % git format-patch -1
    0001-E.patch

    (master) % git log --graph --oneline --decorate --all master
    * 022cb18 (HEAD, master) E
    * 50e7530 D
    * 1f0c2fd C
    * 2d1b9ed B
    * d900590 A

    # 重新构建A-D的提交历史, 或者直接reset撤回D

    (master*) % more 0001-E.patch
    From 022cb1861d3ae5a500c5152464cece0d3e0082b0 Mon Sep 17 00:00:00 2001
    From: Tanky Woo <wtq1990@gmail.com>
    Date: Tue, 7 Jul 2015 08:46:22 +0800
    Subject: [PATCH] E

    ---
     file | 1 +
     1 file changed, 1 insertion(+)

    diff --git a/file b/file
    index 8422d40..8fda00d 100644
    --- a/file
    +++ b/file
    @@ -2,3 +2,4 @@ A
     B
     C
     D
    +E
    --
    2.3.5

    (master*) % git am 0001-E.patch
    Applying: E

    commit b98a9b55f6952f21ea64b28a478e0936744f8039
    Author: Tanky Woo <wtq1990@gmail.com>
    Date:   Tue Jul 7 08:46:22 2015 +0800

        E

    diff --git a/file b/file
    index 8422d40..8fda00d 100644
    --- a/file
    +++ b/file
    @@ -2,3 +2,4 @@ A
     B
     C
     D
    +E

git am后会生成新的提交

如果使用 `git apply`, 则会把修改保留在工作目录, 但是不会提交:

    (master*) % git reset --hard HEAD^
    HEAD is now at 50e7530 D

    (master*) % git apply 0001-E.patch

    (master*) % git diff
    diff --git a/file b/file
    index 8422d40..8fda00d 100644
    --- a/file
    +++ b/file
    @@ -2,3 +2,4 @@ A
     B
     C
     D
    +E

有时在仓库里作了一些修改没有提交, 也可以用git diff生成一个patch文件, 然后传给别人, 对象可以直接应用上这个patch:

    $ git apply patch.file

在没有git的情况下, 可以使用`patch`命令:

    $ patch -p1 < patch.file

参考:

* [How do you take a git diff file, and apply it to a local branch that is a copy of the same repository?](http://stackoverflow.com/questions/12320863/how-do-you-take-a-git-diff-file-and-apply-it-to-a-local-branch-that-is-a-copy-o)
* [How to apply `git diff` patch without Git installed?](http://stackoverflow.com/questions/3418277/how-to-apply-git-diff-patch-without-git-installed)

关于复杂的情况, 如之前A-Z的情况, 中间有个分支alt从B点分出去, 再重复贴一次图:

    (master) % git log --graph --oneline --decorate --all master
    * bfad1bc (HEAD, master) F
    *   1dd3011 Merge branch 'alt'
    |\
    | * fb5c9a0 (alt) Z
    | * f67540b Y
    | * b50d656 X
    * | 50e7530 D
    * | 1f0c2fd C
    |/
    * 2d1b9ed B
    * d900590 A

    (master) % git show-branch --more=10
    ! [alt] Z
     * [master] F
    --
     * [master] F
    +* [alt] Z
    +* [alt^] Y
    +* [alt~2] X
     * [master~2] D
     * [master~3] C
    +* [master~4] B
    +* [master~5] A

生成除A以外的patches:

    (master) % git format-patch -o /tmp/patches master~5
    /tmp/patches/0001-B.patch
    /tmp/patches/0002-C.patch
    /tmp/patches/0003-D.patch
    /tmp/patches/0004-X.patch
    /tmp/patches/0005-Y.patch
    /tmp/patches/0006-Z.patch
    /tmp/patches/0007-F.patch

现在回到提交A, 然后应用这些patches:

    (master) % git reset --hard HEAD~5
    HEAD is now at d900590 A

    (master) % git am /tmp/patches/*
    Applying: B
    Applying: C
    Applying: D
    Applying: X
    error: patch failed: file:1
    error: file: patch does not apply
    Patch failed at 0004 X
    The copy of the patch that failed is found in:
       /path/to/myrepo/.git/rebase-apply/patch
    When you have resolved this problem, run "git am --continue".
    If you prefer to skip this patch, run "git am --skip" instead.
    To restore the original branch and stop patching, run "git am --abort".

    (master) % more .git/rebase-apply/patch
    ---
     file | 1 +
     1 file changed, 1 insertion(+)

    diff --git a/file b/file
    index 35d242b..7f9826a 100644
    --- a/file
    +++ b/file
    @@ -1,2 +1,3 @@
     A
     B
    +X
    --
    2.3.5

    (master) % git status
    On branch master
    You are in the middle of an am session.
      (fix conflicts and then run "git am --continue")
      (use "git am --skip" to skip this patch)
      (use "git am --abort" to restore the original branch)

    nothing to commit, working directory clean

    (master) % git show-branch --more=4
    ! [alt] Z
     * [master] D
    --
     * [master] D
     * [master^] C
     * [master~2] B
    +  [alt] Z
    +  [alt^] Y
    +  [alt~2] X
    +  [alt~3] B
    +* [master~3] A

执行am失败了, 并且给了一些有用的提示操作. 不过这里失败了就是失败了, 没有类似合并冲突的解决的脏数据遗留下来.

.git/rebase-apply/patch文件还保留了失败时修改的内容, 老版本git在.dotest目录下. 这个文件是要清理掉的, 不然后续执行am会报错.

    The copy of the patch that failed is found in:
       /path/to/myrepo/.git/rebase-apply/patch


这时使用`-3/-3way`三路合并的方式来解决这个问题:

    (master) % git reset --hard HEAD~3
    HEAD is now at d900590 A

    # 这里如果没清理 .git/rebase-apply/ 目录的话就会报错
    (master) % git am -3 /tmp/patches/*
    previous rebase directory /path/to/myrepo/.git/rebase-apply still exists but mbox given.

    (master) % rm -rf .git/rebase-apply

继续重新执行三路合并应用patch:

    (master) % git am -3 /tmp/patches/*
    Applying: B
    Applying: C
    Applying: D
    Applying: X
    Using index info to reconstruct a base tree...
    M       file
    Falling back to patching base and 3-way merge...
    Auto-merging file
    CONFLICT (content): Merge conflict in file
    Failed to merge in the changes.
    Patch failed at 0004 X
    The copy of the patch that failed is found in:
       /path/to/myrepo/.git/rebase-apply/patch
    When you have resolved this problem, run "git am --continue".
    If you prefer to skip this patch, run "git am --skip" instead.
    To restore the original branch and stop patching, run "git am --abort".

    (master*) % git status
    On branch master
    You are in the middle of an am session.
      (fix conflicts and then run "git am --continue")
      (use "git am --skip" to skip this patch)
      (use "git am --abort" to restore the original branch)

    Unmerged paths:
      (use "git reset HEAD <file>..." to unstage)
      (use "git add <file>..." to mark resolution)

            both modified:   file

    no changes added to commit (use "git add" and/or "git commit -a")

这次和之前不一样, 虽然失败了, 但是给了一个机会来处理:

    (master*) % vi file
    (master*) % git add file
    (master*) % git am --continue
    Applying: X
    Applying: Y
    Using index info to reconstruct a base tree...
    M       file
    Falling back to patching base and 3-way merge...
    Auto-merging file
    Applying: Z
    Using index info to reconstruct a base tree...
    M       file
    Falling back to patching base and 3-way merge...
    Auto-merging file
    Applying: F

现在的结构图:

    (master) % git show-branch --more=10
    ! [alt] Z
     * [master] F
    --
     * [master] F
     * [master^] Z
     * [master~2] Y
     * [master~3] X
     * [master~4] D
     * [master~5] C
     * [master~6] B
    +  [alt] Z
    +  [alt^] Y
    +  [alt~2] X
    +  [alt~3] B
    +* [master~7] A


    (master) % git --no-pager  log --graph --oneline --decorate --all
    * b16dc1a (HEAD, master) F
    * 79f431d Z
    * 9642ba2 Y
    * 816197e X
    * 0d3f91b D
    * b30ce22 C
    * 7dd8d42 B
    | * fb5c9a0 (alt) Z
    | * f67540b Y
    | * b50d656 X
    | * 2d1b9ed B
    |/
    * d900590 A

应用patch后的结构是线性的

如果要想和原来的结构保持一致, 估计只能手动来处理之间的关系了:

    # 当前停留在B点
    (master) % git am /tmp/patches/0002-C.patch /tmp/patches/0003-D.patch
    Applying: C
    Applying: D

    (master) % git show-branch --more=3
    [master] D
    [master^] C
    [master~2] B
    [master~3] A

    (master) % git co -b alt master~2
    Switched to a new branch 'alt'

    (alt) % git am /tmp/patches/0004-X.patch /tmp/patches/0005-Y.patch /tmp/patches/0006-Z.patch
    Applying: X
    Applying: Y
    Applying: Z

    (alt) % git co master
    Switched to branch 'master'

    (master) % git show-branch --more=10
    ! [alt] Z
     * [master] D
    --
    +  [alt] Z
    +  [alt^] Y
    +  [alt~2] X
     * [master] D
     * [master^] C
    +* [alt~3] B
    +* [alt~4] A

    (master) % git merge alt
    Auto-merging file
    CONFLICT (content): Merge conflict in file
    Automatic merge failed; fix conflicts and then commit the result.

    # ... 处理冲突 ...
    (master*) % git ci
    [master eab9bcf] Merge branch 'alt'

    (master) % git am /tmp/patches/0007-F.patch
    Applying: F

    (master) % git show-branch --more=10
    ! [alt] Z
     * [master] F
    --
     * [master] F
    +* [alt] Z
    +* [alt^] Y
    +* [alt~2] X
     * [master~2] D
     * [master~3] C
    +* [master~4] B
    +* [master~5] A

## 15. 钩子 ##

Git在操作如提交, 补丁等事件时, 可以通过钩子(hook)来触发一些脚本.

大多数钩子分为两类:

* 前置(pre), 在动作完成前调用
* 后置(post), 在动作完成后调用

如果钩子以非0状态退出(如 `exit 1`), 则表示执行失败, Git动作中止; 不过后置的状态无法影响Git操作的结果.

谨慎的使用钩子:

* 钩子会改变Git的行为
* 钩子是本地的, 不随版本库一起提交到远端, 所以可能多个开发者的动作行为不一样
* 钩子会影响动作的速度

每个版本库新建的时候, 会默认提供一些钩子模板, 以`.sample`结尾, 状态是禁止的:

	(master*) $ tree .git/hooks
	.git/hooks
	├── applypatch-msg.sample
	├── commit-msg.sample
	├── post-update.sample
	├── pre-applypatch.sample
	├── pre-commit
	├── pre-commit.sample
	├── pre-push.sample
	├── pre-rebase.sample
	├── prepare-commit-msg.sample
	└── update.sample

如果要使一个钩子起作用, 必须保证:

* 去掉 .sample 后缀
* 拥有可执行权限

也可以自己写钩子.

因为钩子是针对特定动作的特定时刻起作用的, 所以钩子名(脚本名)需要为特定范围的名字, 可以见 `git help hooks` 查看可用的钩子.

提交相关钩子:

	pre-commit -> prepare-commit-msg -> commit-msg -> post-commit

补丁相关钩子:

	applypatch-msg -> pre-applypatch -> post-applypatch

push相关钩子(Git服务端执行):

	pre-receive -> update -> post-receive -> post-update


## 16. 合并项目 ##

项目管理过程中经常会遇到需要将别的项目加入到自己项目中.

比如某个网站开发, 需要用到一些前端的库. 最简单的方法就是将压缩包下载解压后放到本地指定目录, 升级的时候覆盖就行. 但是一是每次升级这些第三方库时, 还需要做一次无意义的提交, 如果频繁修改是很坑爹的; 另外就是升级也比较麻烦, 并且如果第三方依赖比较大, 也占用了很多无意义的空间.

又比如一个项目的某个子目录是一些功能函数, 现在另一个项目也想用到. 以前用svn时, 是支持部分检出(partial checkout), 但是git是不支持的.

针对上面的这类情况, 都可以考虑子模块(submodule), 说白了就是模块化, 一个模块负责好相应的功能, 其它需要用到它的都使用这个模块, 保证统一性; 并且使用了git的子模块, 对于升级维护都比较方便, 也不需要考虑太多第三方依赖库需要的空间问题.

`git submodule`由两个独立功能组合:

* gitlink
* git submodule命令

gitlink是一个从树对象(tree object)到一个提交对象(commit object)的链接. 之前介绍过git对象时, 一般情况下, 树对象指向的是一组blob对象和树对象. 所以这里是比较特殊的情况.

现在有一个仓库目录git-main, 子目录git-sub, 分别是两个库:

	git-main/ (master*) $ tree
	.
	├── git-sub
	│   └── sub.txt
	└── hello.txt

	1 directory, 2 files

	git-main/ (master*) $ git remote -v
	origin  https://git.example.com/tankywoo/git-main.git (fetch)
	origin  https://git.example.com/tankywoo/git-main.git (push)

	git-main/ (master*) $ cd git-sub
	git-main/git-sub/ (master) $ git remote -v
	origin  https://git.example.com/tankywoo/git-sub.git (fetch)
	origin  https://git.example.com/tankywoo/git-sub.git (push)

	git-main/ (master*) $ gst
	On branch master
	Your branch is up-to-date with 'origin/master'.
	Untracked files:
	  (use "git add <file>..." to include in what will be committed)

			git-sub/

	nothing added to commit but untracked files present (use "git add" to track)

现在将 git-sub 加入到 git-main库:

	git-main/ (master*) $ git add git-sub

	git-main/ (master*) $ gst
	On branch master
	Your branch is up-to-date with 'origin/master'.
	Changes to be committed:
	  (use "git reset HEAD <file>..." to unstage)

			new file:   git-sub

	git-main/ (master*) $ git ci -m 'import git-sub'
	[master 36c4d6e] import git-sub
	 1 file changed, 1 insertion(+)
	 create mode 160000 git-sub

	git-main/ (master) $ git ls-tree HEAD
	160000 commit 1efb773d1740a7ad66e5b53bdf66f10c66440ce5  git-sub
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    hello.txt

这里git-sub子目录是commit类型, 模式码是160000. 这是一个gitlink对象.

注意: 通常情况下, `git add /path/to` 和 `git add /path/to/`(有无斜线结束符)是一样的. 但是在这里创建gitlink时, 两者是不一样的, 如果加了斜线结束符, 则不是创建gitlink, 而是把子目录下的所有文件都添加进来.

	git-main/ (master) $ cp -r git-sub git-non-sub

	git-main/ (master*) $ git add git-non-sub/

	git-main/ (master*) $ gst
	On branch master
	Your branch is ahead of 'origin/master' by 1 commit.
	  (use "git push" to publish your local commits)
	Changes to be committed:
	  (use "git reset HEAD <file>..." to unstage)

			new file:   git-non-sub/sub.txt

	git-main/ (master*) $ git ci -m 'import git-non-sub'
	[master 249c085] import git-non-sub
	 1 file changed, 1 insertion(+)
	 create mode 100644 git-non-sub/sub.txt

	git-main/ (master) $ git ls-tree HEAD
	040000 tree 04756934bd18bee46b7978441ff47dfd695e6344    git-non-sub
	160000 commit 1efb773d1740a7ad66e5b53bdf66f10c66440ce5  git-sub
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    hello.txt

这里git-non-sub就是一个普通的树对象.

git 将 gitlink当做一个简单的指针值或者其它版本库的引用. 绝大部分git操作(如clone)不会对gitlink解引用, 并作用在子模块版本库上.


	git-main/ (master) $ tree
	.
	├── git-non-sub
	│   └── sub.txt
	├── git-sub
	│   └── sub.txt
	└── hello.txt

	2 directories, 3 files

	git-main/ (master) $ cd ..
	 $ git clone git-main git-main2
	Cloning into 'git-main2'...
	done.
	 $ cd git-main2

	git-main2/ (master) $ tree
	.
	├── git-non-sub
	│   └── sub.txt
	├── git-sub
	└── hello.txt

	2 directories, 2 files

	git-main2/ (master) $ cd git-sub
	git-main2/git-sub/ (master) $ git remote -v
	origin  /Users/TankyWoo/dev_env/git-submodule/git-main (fetch)
	origin  /Users/TankyWoo/dev_env/git-submodule/git-main (push)

继续在克隆出来的git-main2上测试:

	git-main2/ (master) $ git ls-files --stage -- git-sub
	160000 1efb773d1740a7ad66e5b53bdf66f10c66440ce5 0       git-sub

	git-main2/ (master) $ rmdir git-sub
	git-main2/ (master*) $ git clone https://git.example.com/tankywoo/git-sub.git git-sub
	Cloning into 'git-sub'...
	Username for 'https://git.example.com': tankywoo
	Password for 'https://tankywoo@git.example.com':
	remote: Counting objects: 3, done.
	remote: Total 3 (delta 0), reused 0 (delta 0)
	Unpacking objects: 100% (3/3), done.
	Checking connectivity... done.

	git-main2/ (master) $ cd git-sub
	git-main2/git-sub/ (master) $ git checkout 1efb773
	Note: checking out '1efb773'.

	You are in 'detached HEAD' state. You can look around, make experimental
	changes and commit them, and you can discard any commits you make in this
	state without impacting any branches by performing another checkout.

	If you want to create a new branch to retain commits you create, you may
	do so (now or later) by using -b with the checkout command again. Example:

	  git checkout -b new_branch_name

	HEAD is now at 1efb773... init sub

这个操作的原理和`git submodule update`类似, 只不过后者的实现更复杂一些.

	git-main2/ (master) $ git submodule update
	No submodule mapping found in .gitmodules for path 'git-sub'

git submodule 首先需要一个基本的配置文件: 放在主库根目录下的`.gitmodules`文件.

git submoduel 的前期操作 init 依赖这个 TODO

可以手动或通过`git submodule add`创建这个文件(有点类似git remote add). 不过这里因为之前已经作了gitlink了, 所以这里只能手动创建这个文件:

	git-main2/ (master*) $ cat .gitmodules
	[submodule "git-sub"]
			path = git-sub
			url = https://git.example.com/tankywoo/git-sub.git

接下来执行`git submodule init`将.gitmodules文件中的配置复制到.git/config中:

	git-main2/ (master*) $ git submodule init
	Submodule 'git-sub' (https://git.example.com/tankywoo/git-sub.git) registered for path 'git-sub'
	git-main2/ (master*) $ cat .git/config
	[core]
			repositoryformatversion = 0
			filemode = true
			bare = false
			logallrefupdates = true
			ignorecase = true
			precomposeunicode = true
	[remote "origin"]
			url = /Users/TankyWoo/dev_env/git-submodule/git-main
			fetch = +refs/heads/*:refs/remotes/origin/*
	[branch "master"]
			remote = origin
			merge = refs/heads/master
	[submodule "git-sub"]
			url = https://git.example.com/tankywoo/git-sub.git

回到git-main, 提交.gitmodules, 在git-sub目录增加一个提交:

	git-main/git-sub/ (master) $ echo 'new line' >> sub.txt
	git-main/git-sub/ (master*) $ git ci -m 'add new line to sub.txt' sub.txt
	[master 4102106] add new line to sub.txt
	 1 file changed, 1 insertion(+)

	git-main/git-sub/ (master) $ cd ..
	git-main/ (master*) $ gst
	On branch master
	Your branch is up-to-date with 'origin/master'.
	Changes not staged for commit:
	  (use "git add <file>..." to update what will be committed)
	  (use "git checkout -- <file>..." to discard changes in working directory)

			modified:   git-sub (new commits)

	no changes added to commit (use "git add" and/or "git commit -a")

	git-main/ (master*) $ git submodule update
	Submodule path 'git-sub': checked out '1efb773d1740a7ad66e5b53bdf66f10c66440ce5'

因为子模块针对主库都是一个指针, 指向子模块的某一个版本.

所以执行git submodule update时, 会更新到指定的版本. 这里是检出之前的一个版本, 这时可以把git-sub更新到新提交.

	git-main/git-sub/ (1efb773) $ git checkout master
	Previous HEAD position was 1efb773... init sub
	Switched to branch 'master'
	Your branch is up-to-date with 'origin/master'.

	git-main/ (master*) $ gst
	On branch master
	Your branch is up-to-date with 'origin/master'.
	Changes to be committed:
	  (use "git reset HEAD <file>..." to unstage)

			modified:   git-sub

	git-main/ (master*) $ git ci -m 'update git-sub'
	[master d052863] update git-sub
	 1 file changed, 1 insertion(+), 1 deletion(-)

可以看到, git-sub在主库的对象就是一个指针:

	git-main/ (master) $ git ls-tree HEAD
	100644 blob 9c7efd6f991c84837049b6ce41233281b54b12a6    .gitmodules
	040000 tree 04756934bd18bee46b7978441ff47dfd695e6344    git-non-sub
	160000 commit 4102106db336adbf5d0ad572b64b379ab5098abc  git-sub
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    hello.txt

	git-main/ (master) $ cd git-sub
	git-main/git-sub/ (master) $ git rev-parse master
	4102106db336adbf5d0ad572b64b379ab5098abc

解引用子模块:

	git-main/ (master) $ git submodule deinit git-sub
	Cleared directory 'git-sub'
	Submodule 'git-sub' (https://git.example.com/tankywoo/git-sub.git) unregistered for path 'git-sub'
	git-main/ (master) $ more .git/config
	[core]
			repositoryformatversion = 0
			filemode = true
			bare = false
			logallrefupdates = true
			ignorecase = true
			precomposeunicode = true
	[remote "origin"]
			url = https://git.example.com/tankywoo/git-main.git
			fetch = +refs/heads/*:refs/remotes/origin/*
	[branch "master"]
			remote = origin
			merge = refs/heads/master

`git submodule status`和 git status类似, 可以查看所有子模块的引用sha-1 id和脏状态

之前提到, git submodle init会把.gitmodules的配置加到.git/config下, 关于这两个文件中针对子模块的配置:

	# .gitmodules
	[submodule "git-sub"]
			path = git-sub
			url = https://git.example.com/tankywoo/git-sub.git

	# .git/config
	[submodule "git-sub"]
			url = https://git.example.com/tankywoo/git-sub.git

TODO: 个人理解是这两个文件互相配合, 针对子模块的路径, 是由.gitmodules控制, 因为这个在.git/config中没有, 关于执行git submodule update的路径, 是由.git/config中的url控制.
另外, 子模块的配置在 `.git/modules/<module-name>/config`中, 和.git/config类似, 那么这里的作用又是?


TODO:

* git pull -s subtree 导入子项目
* git subtree vs git submodule 前者在去年就听过了, 一直没试过.


## 17. 子模块最佳实践(略) ##



## 18. 结合SVN版本库使用Git(略) ##


## 19. 高级操作 ##

`git filter-branch` 是一个通用的分支操作命令, 可以通过自定义命令来利用它操作不同的git对象, 从而重写分支上的提交.

filter-branch命令会在版本库中的一个或多个分支执行一系列过滤器, 每个过滤器可以搭配一条自定义过滤器命令.

和`rebase`, `reset`等类似, 改写历史的操作总是危险的, 所以最好不要在公共分支操作.

另外, filter-branch完成后, 原先包含旧提交历史的引用会存在 `refs/original/`目录下, `refs/heads/` 存的是新的历史.

在操作filter-branch之前, 要保证`refs/original/`目录是空的.

如果确认新的历史OK后, 并确认旧的历史不在使用, 则可以删掉.git/refs/original(直接rm或`git update-ref -d refs/original/<branch>`)

如果不删除此目录, 则在版本库中拥有新旧两套历史记录, 旧的历史会阻止垃圾回收(gc).

如果不想显示删除此目录, 可以克隆一个新的版本库, 旧的历史存在旧的版本库作备份.

关于filter-branch, 最佳实践是先克隆一个心版本库, 然后再执行过滤操作. 个人感觉这个操作的破坏性比rebase等还要强, 很容易导致整个历史脱离自己的预计, 这应该也是它专门提供一个original引用的原因.

例子:

在整个历史中删除某个文件. 一般而言某个文件可能不再用了, 也可能包含了敏感的信息, 需要删除这个文件, 如果只是简单的`git rm`, 只会在当前版本中删除, 但是在历史版本还是可以检出这个文件.

使用`--tree-filter`可以实现这个功能:

	# 4个commit, 其中 e7fc148 引入hello这个空文件
	(master) $ git log --oneline
	20124f8 add hello git to git.txt
	e7fc148 add hello world to world.txt <v0.1>  # 在这块打了一个tag v0.1
	5406b57 add hello
	f1b0b42 first commit

	# 使用--tree-filter可以看到每个版本的文件有哪些
	(master) $ git filter-branch --tree-filter 'ls' master
	Rewrite f1b0b42d0590f35f290e1c47b6e0fc12ed11267c (1/4)t.sh
	Rewrite 5406b570273078b2193fc7b890f20a56b2e697c8 (2/4)hello    t.sh
	Rewrite e7fc1486aea71618c719800e8fbe4fd58ffc29e9 (3/4)hello    t.sh   world.txt
	Rewrite 20124f85c45e360dff4d05b5e9eb4f73132f066b (4/4)git.txt  hello  t.sh    world.txt

	WARNING: Ref 'refs/heads/master' is unchanged

	# 使用--tree-filter删除hello这个文件
	(master) $ git filter-branch --tree-filter 'rm -f hello' master
	Rewrite 20124f85c45e360dff4d05b5e9eb4f73132f066b (4/4)
	Ref 'refs/heads/master' was rewritten

	# 再次查看, 从第2个commit开始sha-1值都变了
	(master) $ git log --oneline
	891b0ec add hello git to git.txt
	4fca41c add hello world to world.txt
	cc1cc50 add hello
	f1b0b42 first commit

	# 当前工作目录下, hello这个文件没了
	(master) $ ls
	git.txt   t.sh   world.txt

	# 再次尝试查看每个版本有哪些文件
	(master) $ git filter-branch --tree-filter 'ls' master
	Cannot create a new backup.
	A previous backup already exists in refs/original/
	Force overwriting the backup with -f

	# 多了一个refs/original/
	(master) $ tree .git/refs
	.git/refs
	├── heads
	│   └── master
	├── original
	│   └── refs
	│       └── heads
	│           └── master
	├── remotes
	│   └── origin
	│       └── HEAD
	└── tags

	7 directories, 3 files

	# 存的老的master head
	(master) $ more .git/refs/original/refs/heads/master
	20124f85c45e360dff4d05b5e9eb4f73132f066b

	# 存的新的master head
	(master) $ more .git/refs/heads/master
	891b0ece810d9d8dcbc34e8f023fb5713e6e4b32

	# 如果把 .git/refs/heads/master改为老的sha-1, 这时就还是原来的历史了
	(master*) $ git status
	On branch master
	Your branch is ahead of 'origin/master' by 2 commits.
	  (use "git push" to publish your local commits)
	Changes to be committed:
	  (use "git reset HEAD <file>..." to unstage)
			deleted:    hello


	# 删除旧的引用
	(master) $ git update-ref -d refs/original/refs/heads/master
	(master) $ tree .git/refs
	.git/refs
	├── heads
	│   └── master
	├── original
	│   └── refs
	│       └── heads
	├── remotes
	│   └── origin
	│       └── HEAD
	└── tags

	7 directories, 2 files

	# 此时可以查看每个版本的文件了
	(master) $ git filter-branch --tree-filter 'ls' master
	Rewrite f1b0b42d0590f35f290e1c47b6e0fc12ed11267c (1/4)t.sh
	Rewrite cc1cc501bd669ff44814ecd384f2dab7fc846cd9 (2/4)t.sh
	Rewrite 4fca41c1d1237963cb62f639dac6b82e9bf2de04 (3/4)t.sh     world.txt
	Rewrite 891b0ece810d9d8dcbc34e8f023fb5713e6e4b32 (4/4)git.txt  t.sh    world.txt

	WARNING: Ref 'refs/heads/master' is unchanged

不过这里有个问题, tag标签没有转过来:

	# 但是之前打的tag v0.1 还是指向老的commit
	(master) $ git rev-parse v0.1
	e7fc1486aea71618c719800e8fbe4fd58ffc29e9

在--tree-filter可以配合--tag-name-filter:

	(master) $ git filter-branch --tree-filter 'rm -f hello' --tag-name-filter cat  master
	Rewrite 20124f85c45e360dff4d05b5e9eb4f73132f066b (4/4)
	Ref 'refs/heads/master' was rewritten
	v0.1 -> v0.1 (e7fc1486aea71618c719800e8fbe4fd58ffc29e9 -> 4fca41c1d1237963cb62f639dac6b82e9bf2de04)

另外, 如果某个文件改名过, 则上面的情况会漏掉改名前的版本, 可以通过之前提到过的`--follow`找到:

	$ git log --name-only --follow --all -- file

接着上面的例子, 使用`--msg-filter`把commit message的hello改为nothing, 当然这里会把最后三条都改掉, 仅仅当一个例子来使用, 正常情况下应该只改第2条, 用rebase合适些.

	(master) $ git filter-branch --msg-filter 'sed -e "s/hello/nothing/"' master
	Rewrite 891b0ece810d9d8dcbc34e8f023fb5713e6e4b32 (4/4)
	Ref 'refs/heads/master' was rewritten

	(master) $ git log --oneline
	f53bafc add nothing git to git.txt
	e216bec add nothing world to world.txt
	47e5bce add nothing
	f1b0b42 first commit

如果filter-branch需要在所有分支上操作, 则在命令最后加上`--all`

最后, 来一个以前用过的例子, 修改提交者的name和email, 有时会遇到这个情况, 可能个人的两个开发环境配置的name不一样, 导致提交会出现多个昵称, 这时可以统一下, github help已经给出了脚本, 用的就是filter-branch的env-filter, 文档链接 [Changing author info](https://help.github.com/articles/changing-author-info/)

	#!/bin/sh
	 
	git filter-branch --env-filter '

	OLD_EMAIL="your-old-email@example.com"
	CORRECT_NAME="Your Correct Name"
	CORRECT_EMAIL="your-correct-email@example.com"

	if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
	then
		export GIT_COMMITTER_NAME="$CORRECT_NAME"
		export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
	fi
	if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
	then
		export GIT_AUTHOR_NAME="$CORRECT_NAME"
		export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
	fi
	' --tag-name-filter cat -- --branches --tags

更多的filter可以man, 暂时也就跟着书折腾了这几个filter.

`git rev-list` 和 git log 类似, 不过只输出sha-1 id. 并且两者的文档很多地方也是一样. 比如对输出范围的限制. 不过git log默认参数是HEAD, 而 rev-list必须指定commit id.

> git log takes options applicable to the `git rev-list` command to control what is shown and how, and options applicable to the `git diff-*` commands to control how the changes each commit introduces are shown.

例子, 找出2015-01-01之前的提交:

    $ git rev-list --before="2015-01-01" master | wc -l
         266

    $ git rev-list --before="2014-01-01" master | wc -l
          73

    $ git rev-list -n 3 --before="2014-01-01" master
    78f19370f4c67ca094565b9de6310917eaf85321
    898309c61f5cea3ec2c52568ec8e0e4fed83a369
    e0332b5dc692d4404b33596ff1a61ee430c36264

    $ git show 78f19370f4c67ca094565b9de6310917eaf85321
    commit 78f19370f4c67ca094565b9de6310917eaf85321
    Author: Tanky Woo <wtq1990@gmail.com>
    Date:   Wed Dec 25 16:56:12 2013 +0800

        add server for preview

    diff --git a/simiki/server.py b/simiki/server.py
    ...

对于基于时间检出commit时, 需要注意:

根据限制的精度, 会影响输出结果. 如果缺乏精确时间, 则相对的是当前时刻. 如上传入的2015-01-01, 默认时间点是当前的点09:00:00; 如果要限制在晚上23点, 则应该传入 2015-01-01 23:00:00. 所以包括yesterday都是这样, 会依赖当前时刻.

和log一样, rev-list也可以限制路径:

    $ git rev-list master -- setup.cfg
    46ff8a318b09c2d915bda22d9c5d93541e719680
    70a7e9e7e55e3c125e2c81682ef21d03fe0a09fe

输出限制某个commit的某个文件, 这个功能也挺给力, 语法 `commit:path`

    # 提交包含添加两个文件
    $ git show --stat HEAD
    commit c10e81d7414e7ea8055e1c36eeb6d0bb58c46c11
    Author: Tanky Woo <wtq1990@gmail.com>
    Date:   Sun Jun 28 09:48:34 2015 +0800

        update git.txt and world.txt

     git.txt   | 1 +
     world.txt | 2 +-
     2 files changed, 2 insertions(+), 1 deletion(-)

    # 只输出git.txt的内容
    $ git show HEAD:git.txt
    hello git
    hello git.txt

这里输出HEAD这个版本是, git.txt的内容. 书上说"需要该提交中确实包含了该文件", 这里说的有歧义, 应该说提交的tree blob有这个文件, 而不是这个提交中此文件必须有diff.

关于数据块的交互式暂存, 也就是`git add -p`和`git stash -p`等, 输出提示已经很详细了.

`git fsck` (file system check)可以帮助找回丢失的数据. 一些操作(如reset, rebase)会使一些对象失去和其它对象的连接, 从而脱离版本库的完整数据结构.

这些对象叫做"不可及的"(unreachable) 或 "悬挂的"(dangling).

如:

    $ git init
    Initialized empty Git repository in /xxx/.git

    $ echo 'foo' >> file
    $ git add file
    $ git ci -m 'add foo'
    [master (root-commit) bfcce61] add foo
     1 file changed, 1 insertion(+)
     create mode 100644 file

    $ echo 'bar' >> file
    $ git ci -m 'add bar' file
    [master 39a6f59] add bar
     1 file changed, 1 insertion(+)

    $ tree .git/objects
    .git/objects
    ├── 25
    │   └── 7cc5642cb1a054f08cc83f2d943e56fd3ebe99
    ├── 39
    │   └── a6f59fd5b646b57c42bd6928d7c36066842891
    ├── 3b
    │   └── d1f0e29744a1f32b08d5650e62e2e62afb177c
    ├── 41
    │   └── 31fe4d33cd85da805ac9a6697c2251c913881c
    ├── 4a
    │   └── 1c03029e7407c0afe9fc0320b3258e188b115e
    ├── bf
    │   └── cce61b0e90cb1cb385a9b1650c2a27bce30275
    ├── info
    └── pack

    $ git cat-file -p 39a6f59fd5b646b57c42bd6928d7c36066842891
    tree 4131fe4d33cd85da805ac9a6697c2251c913881c
    parent bfcce61b0e90cb1cb385a9b1650c2a27bce30275
    author Tanky Woo <wtq1990@gmail.com> 1435458156 +0800
    committer Tanky Woo <wtq1990@gmail.com> 1435458156 +0800

    add bar

    $ git reset --hard HEAD^
    HEAD is now at bfcce61 add foo

    $ git fsck
    Checking object directories: 100% (256/256), done.

    $ rm -rf .git/logs/

    $ git fsck
    Checking object directories: 100% (256/256), done.
    dangling commit 39a6f59fd5b646b57c42bd6928d7c36066842891

因为reflog会防止意外的丢失提前, 所以在上面未删除.git/logs时, fsck没有找到dangling对象.


## 20. 提示、技巧和技术 ##

垃圾回收(garbage collection), 在之前reflog expire时提到过.

git会在下面情况下自动进行垃圾回收:

* 版本库里有过多松散对象
* 当推送到一个远程版本库时 (TODO ???实际测试没有清理)
* 当一些命令引入许多松散对象 (如 filter-branch, rebase)
* 当一些命令明确要求 (如 reflog expire)

手动进行垃圾回收使用:

	$ git gc

当然, 如果要保留一些松散对象, 则要注意别被自动垃圾回收给干掉了.

`git.auto`默认值是6700, 控制版本库允许存在的松散对象数量, 可以强制关闭掉:

	$ git config --global gc.auto 0

从上游rebase中恢复	**TODO**

定制 Git 命令: 定义脚本, 脚本名以`git-`开头, 并保证有可执行权限, 然后把脚本放在`$PATH`路径下.

如书上的例子:

	$ echo $PATH | tr -s ':' '\n' | grep $HOME/bin
	/Users/TankyWoo/bin

	$ more ~/bin/git-top-check
	#!/bin/bash

	if [ -d ".git" ]; then
			echo "This is a top level Git development repository."
			exit 0
	fi

	echo "This is not a top level Git development repository."
	exit -1

	$ git top-check
	This is a top level Git development repository.

这个相对于`git config alias.xxx`就是可以定制逻辑复杂的脚本.

比如把上面branch-filter --env-filter的脚本放在这块.

Github上的[tj/git-extras](https://github.com/tj/git-extras) 包含了很多扩展的命令工具.

快速查看变更:

`git whatchanged`, 又一个给力的命令! 它的参数和git log基本一致, 如果输入`git whatchanged -h`可以看到提示是git log和git show的usage.

例子:

	# 抽取其中一部分作为例子
	$ git whatchanged --oneline
	12e3223 Fix Travis CI - Build #126
	:100755 100755 52c844a... 486a651... M  simiki/cli.py
	e477fa6 Disable logging output when unittest and refactor
	:000000 100644 0000000... 0043f0c... A  tests/__init__.py
	:100644 100644 6441aa8... a9ee8f0... M  tests/test_log.py
	05584a3 Simplify generate argument
	:100755 100755 405f776... 52c844a... M  simiki/cli.py
	:100644 100644 2995ac3... e5fda56... M  simiki/utils.py
	:100644 000000 7796986... 0000000... D  tests/attach/images/linux/opstools.png
	:000000 100644 0000000... 7796986... A  tests/mywiki/attach/images/linux/opstools.png
	:100644 100644 a0c3c56... 2e0ae86... M  tests/test_cli.py
	a54174d move pages to a class variable
	:100755 100755 d150c3a... 405f776... M  simiki/cli.py

在上面例子里, 每个提交有两行.

第一行是commit id 和 commit message

第二行分别是 文件位模式(提交前和提交后), blob的sha-1 id(提交前和提交后), 状态字母, 更改后blob的路径

还可以限制时间, 比如上周有哪些提交, 都修改了哪些文件:

	$ git whatchanged --since='last week 00:00:00' --oneline

还可以显示文件:

	$ git whatchanged --since='last week 00:00:00' /path/to/file

清理仓库工作目录:

`git clean`用于清理仓库的工作目录, 比如一个Python的仓库, 中间经过执行、打包等操作, 会产生一些临时文件, 可以使用此命令删除(也可以自己写Makefile).

git clean默认情况下不会删除`.gitignore`和`.git/info/exclude`指定的文件, 通过`-x`会将列表中的文件也删掉;

如果不确定会删除哪些文件, 可以使用`-n/--dry-run`;

默认只删除文件, 目录会保留, `-d`会将目录也删除.

搜索版本库:

之前提到过`git log -S <string>`用于搜索提交的变更历史中包含指定字符串的功能.

`git grep`用于搜索历史记录上某个特定点的版本库内文件的内容. 默认情况下, 只搜索工作树上被追踪的文件.

此命令支持传统grep命令的参数.

之前用的grep就比较麻烦, 因为会搜到.git/目录下的信息.

更新和删除ref:

`git update-ref`可以用于更新引用、符号引用的值.

	$ git rev-parse refs/heads/master
	ba5ddbed95e2798d6862debe7ce434270ae392a9

	$ git update-ref refs/heads/master 5406b57

	$ git rev-parse refs/heads/master
	5406b570273078b2193fc7b890f20a56b2e697c8

	# 删除引用dev
	$ git update-ref -d refs/heads/dev

跟踪移动的文件: `--follow`选项, 在git log时提到过

保留但不追踪文件:

也是一个很常见的需求, 开发时, 某个文件可能需要做一些参数或其它地方调整, 但是不需要提交. 这时一是有diff, 看着不舒服, 二是没法直接add所有.

`git update-index --assume-unchanged <file>` 可以将指定文件标记为不追踪. 如果有更改需要提交时, 先用`--no-assume-unchanged`改回来.

	$ git diff file
	diff --git a/file b/file
	index 8768061..5329883 100644
	--- a/file
	+++ b/file
	@@ -1 +1,2 @@
	- bar
	+foo bar

	$ git update-index --assume-unchanged file

	$ git status
	On branch master
	Your branch is up-to-date with 'origin/master'.
	nothing to commit, working directory clean

	$ git update-index --no-assume-unchanged file

	$ git status
	On branch master
	Your branch is up-to-date with 'origin/master'.
	Changes not staged for commit:
	  (use "git add <file>..." to update what will be committed)
	  (use "git checkout -- <file>..." to discard changes in working directory)

			modified:   file

	no changes added to commit (use "git add" and/or "git commit -a")

重用已录制的解决方案:

`git rerere`(reuse record resolution), 用于自动解决相同的合并或变基冲突操作.

默认是关闭的, 开启选项:

	$ git config --global rerere.enabled true

该功能会在 `.git/rr-cache`目录下记录合并冲突的左右两侧, 如果把冲突解决了, 还会记录冲突的手动解决方案.

但是rerere 属于本地的概念, 所以.rr-cache目录没法push到远程

	$ tree .git/rr-cache
	.git/rr-cache
	└── 670909b9c4e71983c75c81b566c1ec1ba08d65b5
		├── postimage
		└── preimage

比如我这里, 如果合并时有冲突, 会产生一个preimage, 记录冲突的diff; 如果我修复提交后, 会产生一个postimage, 记录解决冲突后的内容.


## 21. Git 和 Github(略) ##
