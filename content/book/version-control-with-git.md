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
	git help --all

	# document for git subcommand
	git help <subcommand>
	git <subcommand> --help

命令行中的`双破折号`(double dash):

> About `bare double dash` (`--`), in shell, it indicate the end of the command options; The same as in git, it seperate the option and the path.
[ref 1](http://unix.stackexchange.com/questions/11376/what-does-double-dash-mean-also-known-as-bare-double-dash)
[ref 2](http://unix.stackexchange.com/questions/52167/what-does-mean-in-linux-unix-command-line)
[ref 3](http://stackoverflow.com/questions/1192180/deleting-a-badly-named-git-branch/1192194#1192194)
[ref 4](http://stackoverflow.com/questions/13321458/meaning-of-git-checkout-double-dashes)

查看某个特定提交的详细信息 `git show`:

	# show the details of the most recent commit
	git show

	# To see more detail about a particular commit
	git show <commit number>

查看所有分支的整体情况 `git show-branch`:

	git show-branch --more=10

关于更详细的, 可以看看[GitGuys](http://www.gitguys.com/topics/git-show-branch-to-see-branches-and-their-commits/?lang=zh)上的图解, 讲得很好.

---

## 4.基本的Git概念 ##

**注意**: 这章太重要了, 字字都是珠玑. (真想把整篇都copy过来)

在版本库中, Git维护两个主要的数据结构: `对象库(object store)` 和 `索引(index)`. 所有这些版本库数据存放在工作目录根目录下的`.git`的隐藏目录中.

索引是*暂时*的信息, 对版本库来说是*私有*的, 并且可以在需要的时候按需求进行创建和修改.

对象库是git版本库实现的核心. 包含了原始数据文件和所有日志信息、作者信息、日期, 以及其它用来重建项目任意版本或分支的信息.

### 对象库(Object Store) ##

Git对象库中的对象**只有**四种类型: 块(blog), 目录树(tree), 提交(commit)和标签(tag). 这四种原子对象构成Git高层数据结构的基础.

* `块 (Blob)` : 

    文件的每一个版本都表示未一个块(blob). blob 是`二进制大对象(binary large object)`的缩写. 一个blob保存一个文件的数据, 但不包含任何关于这个文件的元数据, 甚至没有文件名.

* `树 (Tree)` :

    一个目录树(tree)对象代表一层目录信息. 它记录blob标识符, 路径名和在一个目录下所有文件的一些元数据. 它可以递归引用其它目录树或子树对象, 从而建立一个包含文件和子目录的完整层次结构.

* `提交 (Commit)` :

    一个提交(commit)对象保存版本库中每一次变化的元数据, 包括作者、提交者、提交日期和日志消息. 每一个提交对象指向一个目录树对象, 这个目录树对象在一张完整的快照中捕获提交时版本库的状态.

* `标签 (Tag)` :

    一个标签对象分配一个任意的且human readable的名字给一个特定对象, 通常是一个提交对象.

对象库会随着项目的开发一直变化和增长, 为了有效利用磁盘空间和网络带宽, Git把对象压缩并存储在`打包文件(pack file)`里, 这些文件也在对象库里.


### 索引(Index) ###

索引, 又称`暂存区(Stage)`, 是一个临时的、动态的二进制文件.

    (master*) ⇒  file .git/index
    .git/index: data

它捕获项目在某个时刻的整体结构的一个版本.


### 可寻址内容名称 ###

Git对象库被组织及实现成一个内容可寻址的存储系统. 对象库中每个对象都有一个唯一的名称, 这个名称是向对象的内容应用SHA1得到的`SHA1散列值`, SHA1值是一个160位的数, 通常表示为一个40位的十六进制数.

### Git追踪内容 ###

Git不仅是一个VCS, 还是一个内容追踪系统(content tracking system). 主要表现为两个方式:

* Git的对象库基于其对象内容的散列计算的值, 而不是基于用户的原始文件布局的文件名或目录的设置.

    Git追踪的是内容而不是文件, 如果两个文件的内容完全一样, 无论是否在相同的目录, Git在对象库里只保存一份blob形式的内容副本.

* 当文件从一个版本变到下一个版本时, Git的内部数据库有效地存储每个文件的每个版本, 而不是他们的差异.

### 打包文件(pack file) ###

TODO

### 例子 ###

以下例子使用的基本都是Git的底层命令, 在实际使用中, 有更简单的命令封装了这些底层命令, 不过通过底层命令, 可以更清晰的了解Git的工作流程.

* `git cat-file`
* `git write-tree`
* `git commit-tree`
* `git rev-parse`
* `git ls-files`

初始化的Git仓库:

	# An initial git repo
	(master) ⇒ find .git/objects
	.git/objects
	.git/objects/info
	.git/objects/pack

新建一个文件a.txt, 内容是 'hello', sha1值 ce013625030ba8dba906f756967f9e9ca394464a, 使用`git cat-file`查看散列的内容:

	(master) ⇒ echo 'hello' > a.txt
	(master*) ⇒ git add a.txt
	(master*) ⇒ find .git/objects
	.git/objects
	.git/objects/ce
	.git/objects/ce/013625030ba8dba906f756967f9e9ca394464a
	.git/objects/info
	.git/objects/pack

	(master*) ⇒ git cat-file -p ce013625030ba8dba906f756967f9e9ca394464a
	hello

使用`git ls-files`查看staged信息:

    (master*) ⇒  git ls-files -s
    100644 ce013625030ba8dba906f756967f9e9ca394464a 0       a.txt

捕获索引状态并保存到一个树对象:

	(master*) ⇒ git write-tree
	2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1

	(master*) ⇒ git cat-file -p 2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt

现在增加文件b.txt, 内容和a.txt一样, 可以看到, 两个使用同一个blob:

	(master*) ⇒ echo 'hello' > b.txt
	(master*) ⇒ git add b.txt

	(master*) ⇒ git write-tree
	b5b0cccf7401633f12e0fafc6b85731251b86850

	(master*) ⇒ git cat-file -p b5b0cccf7401633f12e0fafc6b85731251b86850
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    b.txt

现在改变文件a.txt内容, b.txt还是指向原来的blob:

	(master*) ⇒ echo 'world' >> a.txt
	(master*) ⇒ git add a.txt

	(master*) ⇒ git write-tree
	579c3877d5f450e34ea642b3a29d2d01dcf8e392

	(master*) ⇒ git cat-file -p 579c3877d5f450e34ea642b3a29d2d01dcf8e392
	100644 blob 94954abda49de8615a048f8d2e64b5de848e27a1    a.txt
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    b.txt

添加一个子目录, 里面也放一个a.txt, 内容一样:

    (master*) ⇒  mkdir subdir
    (master*) ⇒  cp a.txt subdir/
    (master*) ⇒  tree
    .
    ├── a.txt
    └── subdir
        └── a.txt

    1 directory, 2 files
    (master*) ⇒  git add subdir/a.txt

    (master*) ⇒  git ls-files -s
    100644 ce013625030ba8dba906f756967f9e9ca394464a 0       a.txt
    100644 ce013625030ba8dba906f756967f9e9ca394464a 0       subdir/a.txt

    (master*) ⇒  git write-tree
    ec518d6bb3cabb8e88b5458cf18d862aa0514622

    (master*) ⇒  git cat-file -p ec518d6bb3cabb8e88b5458cf18d862aa0514622
    100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt
    040000 tree 2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1    subdir

可以看到, subdir这个tree对象的sha1 id和之前父目录是一样的.

现在a.txt的blob已经有了, 树对象也有了, 接着就是提交:

    (master*) ⇒  echo -n 'commit a file' | git commit-tree ec518d6bb3cabb8e88b5458cf18d862aa0514622
    7dc4ee9984a52278b3b67480feb712e36ea5a64c

    (master*) ⇒  git cat-file -p 7dc4ee9984a52278b3b67480feb712e36ea5a64c
    tree ec518d6bb3cabb8e88b5458cf18d862aa0514622
    author Tanky Woo <me@tankywoo.com> 1431832347 +0800
    committer Tanky Woo <me@tankywoo.com> 1431832347 +0800

    commit a file%

`author` vs `committer`(引用 [Pro Git](http://git-scm.com/book/ch2-3.html))

> The author is the person who originally wrote the patch, whereas the committer is the person who last applied the patch. So, if you send in a patch to a project and one of the core members applies the patch, both of you get credit — you as the author and the core member as the committer.

更详细的[解释](http://stackoverflow.com/a/18754896/1276501)

打标签:

    (master*) ⇒  git tag -m 'add tag v1.0' v1.0 7dc4ee9984a52278b3b67480feb712e36ea5a64c

    (master*) ⇒  git rev-parse v1.0
    76a2a639a517e26a6c79fdcd09c0a5ffec97e099

    (master*) ⇒  git cat-file -p v1.0
    object 7dc4ee9984a52278b3b67480feb712e36ea5a64c
    type commit
    tag v1.0
    tagger Tanky Woo <me@tankywoo.com> 1431832535 +0800

    add tag v1.0

    (master*) ⇒  git cat-file -p 76a2a639a517e26a6c79fdcd09c0a5ffec97e099
    object 7dc4ee9984a52278b3b67480feb712e36ea5a64c
    type commit
    tag v1.0
    tagger Tanky Woo <me@tankywoo.com> 1431832535 +0800

    add tag v1.0

---

## 5. 文件管理和索引 ##

关于文件管理, 与其它版本管理系统类似, 不过Git在工作目录(working directory)与版本库(repository)之间, 增加了一个Index(Stage)层, 称为索引(暂存)目录. 在工作目录下编辑, 在索引中积累修改, 然后把索引中积累的修改作为一次性的变更来进行提交.

![Git process](https://marklodato.github.io/visual-git-guide/basic-usage-2.svg)

(图片引用 [图解Git](https://marklodato.github.io/visual-git-guide/index-zh-cn.html))

> Linus Torvalds 在git mailing list里提到，如果不先理解Index的目的，就无法理解和领会Git的强大。

Git 的Index不存放任何文件的内容，它只简单的记录准备提交的文件，当运行`git commit`时，git 会检查Index而不是工作目录。

Git 把文件分为三个大类: `已追踪(Tracked)`, `未追踪(Untracked)`和`被忽略(Ignored)`，其中`Tracked`又可以分为`暂存(Staged)` 和 `未暂存(Unstaged)`，在工作目录下修改的文件是Unstaged，经过`git add`后变为Staged。


`git ls-files --stage` 可以查看stage中的文件的`SHA1`值:

	(master*) ⇒ git ls-files --stage  # 或 git ls-files -s
	100644 8d0e41234f24b6da002d962a26c2495ea16a425f 0       fa

`git hash-object`可以计算文件的`SHA1`值并输出:

	(master*) ⇒ git hash-object fa
	8d0e41234f24b6da002d962a26c2495ea16a425f

简单的说是文件fa已经在 索引(index) 中了，本质是文件在 对象库(object store) 中，Index指向它。

关于 `--all` 在 `git add` 和 `git commit`中有点区别，文件必须要经过add才会被tracked，`git add --all` 会把所有tracked 和 untracked的文件都add，但是`git commit --all`只会add所有tracked的文件并提交。

关于`git rm`，如果tracked中的文件被修改了，则可以通过`git rm --cached`来从git库中移除，并在本地保存为untracked的，也可以通过`-f`强制删除。

对于被误删的文件，如果在Index中，如下:

	(master*) ⇒ gst
	# On branch master
	# Changes to be committed:
	#   (use "git reset HEAD <file>..." to unstage)
	#
	#       deleted:    fa
	#

可以通过 `git checkout HEAD -- fa` 或 `git reset HEAD fa && git checkout -- fa` 来返回。

如果是移除被提交，则可以通过`git reset HEAD^`或rebase来取回。

关于`git mv`，等价于:

	mv fa fb
	git rm fa
	git add fb

Git 把文件fa改为fb，会在`object store`中保存原始的文件内容，然后把文件名(路径名path)重新关联到这个内容:

	(master) ⇒ git ls-files --stage
	100644 15acaeb140c2805acdbb2d0dbdedeeea6bb73b06 0       fa

	(master) ⇒ git mv fa fb
	(master*) ⇒ git ls-files --stage
	100644 15acaeb140c2805acdbb2d0dbdedeeea6bb73b06 0       fb

把fa改为fb后，`SHA1`值并没变。

经过mv操作后，使用`git log fb`只会看到变更后的提交(包括变更的那个提交)，即关联内容并为fb文件的历史，可以通过`git log --follow fb` 来查看关联这段内容的完整历史。

关于 `.gitignore` 文件, 简单语法:

* 忽略空行, `#` **开头** 作为注释, 如果跟在其它文本后面, 则不是注释
* 简单的字符文件名匹配任何目录下的同名文件或**目录**
* 目录名由反斜线`/`结尾, 表示只匹配同名的目录, 不匹配文件和软链接
* `*`作为通配符, 类似shell
* 感叹号`!`表示对改行其余部分的模式取反

Git版本库中任何目录下都可以有.gitignore文件, 且只影响当前目录及子目录. 作用规则是*级联*的, 可以覆盖父级以上的规则.

另外Git有多个地方可以影响ignore文件, 所以有优先级关系(从高到低):

* 命令行中指定的模式
* 当前目录下.gitignore文件中的模式
* 父级以上目录中.gitignore文件中的模式
* `.git/info/exclude`文件中的模式
* 环境配置`core.excludedfile`指定文件中的模式

5.9节 Git中对象模型和文件的详细视图, 把一次从 干净->编辑->add->commit 的原理图画出来了, 讲得非常好.

**TODO** 抽时间补上这块的图

## 6. 提交 ##

当提交时, Git会记录索引的快照并把快照放进对象库.

Git可以通过显示引用(explicit ref)或隐式引用(implied ref)来表示提交. 散列id(sha1)是显示引用, HEAD等是隐式引用.

引用(ref)是一个SHA1散列值, 指向Git对象库中的对象.

符号引用(symref) 是一个指向引用的引用(指针), 间接的指向git对象. 存放在`.git/`目录下.

本地特性分支名, 远程跟踪分支名, 标签名都是引用.

每一个符号引用都有一个以 refs/ 开始的明确名称, 并且都分层存储在版本库的`.git/refs/` 目录中. 基本分为三种:

* refs/heads/<ref> 代表本地分支
* refs/remotes/<ref> 代表远程跟踪分支
* refs/tags/<ref> 代表标签

比如本地分支dev, 就是 refs/heads/dev 的缩写:

    (category-index*) ⇒  git --no-pager show dev
    commit e31b74d259b83af0f69683b9b12a29ebb3946748
    Merge: 12e3223 5488c82
    Author: Tanky Woo <wtq1990@gmail.com>
    Date:   Fri Apr 10 19:11:27 2015 +0800

        Merge branch 'project-tools' into dev

    (category-index*) ⇒  git --no-pager show refs/heads/dev
    commit e31b74d259b83af0f69683b9b12a29ebb3946748
    Merge: 12e3223 5488c82
    Author: Tanky Woo <wtq1990@gmail.com>
    Date:   Fri Apr 10 19:11:27 2015 +0800

        Merge branch 'project-tools' into dev

    (category-index*) ⇒  more .git/refs/heads/dev
    e31b74d259b83af0f69683b9b12a29ebb3946748


Git 有几个特殊符号引用:

* `HEAD`
* `ORIG_HEAD`
* `FETCH_HEAD`
* `MERGE_HEAD`

`HEAD`: `.git/HEAD`, 总是指向当前分支的最后一次提交, 当分支改变，HEAD也会变

    (master) ⇒ more .git/HEAD
    ref: refs/heads/master

`ORIG_HEAD`: `.git/ORIG_HEAD`, 一些操作, 如`merge`或`reset`, 会记录操前的commit(HEAD). 作为一个保护措施，使操作可以回溯.

比如最近三个commits:

    * d46546a - (HEAD, master) update d (42 seconds ago) <Tanky Woo>
    * 8ed2d79 - update f (76 seconds ago) <Tanky Woo>
    * 75b09c2 - (tag: v0.1) Merge branch 'dev' (3 days ago) <Tanky Woo>

`ORIG_HEAD` 存储的是之前某一个commit:

    (master) ⇒ more .git/ORIG_HEAD
    015b5b99f5c9973e840f29c9f6e6b936c99b92a5

做一次reset操作:

    (master) ⇒ git reset --soft HEAD^

查看`ORIG_HEAD`, 会指向之前的HEAD:

    (master) ⇒ more .git/ORIG_HEAD
    d46546a5192b7e1c834947b612e3401a6f7729c7

这样就可以回溯到reset之前的版本:

    git reset ORIG_HEAD

然后 `ORIG_HEAD` 又指向 8ed2d79 这个id

`HEAD` vs `ORIG_HEAD` [HEAD and ORIG\_HEAD in Git](http://stackoverflow.com/questions/964876/head-and-orig-head-in-git)

`FETCH_HEAD`: `.git/FETCH_HEAD`, 当使用远程库时, git fetch 命令将所有抓去分支的头记录到这个文件中, 是最近fetch的分支HEAD的简写.

`MERGE_HEAD`: 当一个合并操作正在进行时, 其它分支的头暂时记录在 `MERGE_HEAD` 中. 即是正在合并进HEAD的提交.

`git symbolic-ref` 操作符号引用:

    (master*) ⇒  git symbolic-ref HEAD
    refs/heads/master

详细可以参考[progit-9.3](http://git-scm.com/book/en/Git-Internals-Git-References)

SHA1 id是绝对提交名, 通过`~`和`^`则可以代表相对提交名.

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

    (master*) ⇒  git --no-pager diff fa
    diff --git a/fa b/fa
    index 89b24ec..7bba8c8 100644
    --- a/fa
    +++ b/fa
    @@ -1 +1,2 @@
     line 1
    +line 2

    (master*) ⇒  git --no-pager show :fa
    line 1

fa在历史库中只有line 1这一行, 在unstaged中增加了line 2.

还可以查看远程追踪分支中某文件的blob内容, 如:

    $ git show origin/master:setup.py

使用`git log <start>..<end>` **两个dot** 语法来查看某一段历史, 表示 "结束" 的提交可到达 且 "开始" 的提交不可到达的一组提交. 如:

    $ git log master~12..master~10  # 查看master~11, master~10, 但是不包括 master~12

实际也就是:

    $ git log ^X Y

**TODO** 这块看图6-9, 6-11, 6-12, 6-13

`<start>..<end>` 的范围表示集合的减法运算, 而 `<A>...<B>` **三个dot** 表示A和B的对称差(symmetric difference), 也就是 A或B可达 且又 不同时在 A和B的并集 中.

比如 dev 是从master的init这个提交衍生出来的, 随后master和dev各增加一个提交:

    # master: init -> add fc
    # dev:    init -> add fb

    (master) ⇒  git --no-pager log master...dev --oneline
    52bdb27 add fc
    20d2444 add fb

下面这个命令效果是一致(**TODO**):

    (master) ⇒  git rev-list --abbrev-commit master...dev --not $(git merge-base --all master dev)
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

    line 1      line 1
    row  2   -> line 3
    line 3      row  3

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

    (master*) ⇒  git show-branch master dev category-index
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

	$  diff -u -r dir1 dir2
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

    ⇒  git mv log.py log2.py
    ⇒  git --no-pager diff --cached -M
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

## 11. 储藏和引用日志 ##

储藏(stash)是一个很常用的功能, 工作目录有一些修改时, 如:

* 此时需要紧急修复一个bug, 可以stash储藏之前的修改, 然后开始修复bug
* 需要临时切换分支去修改一些东西, 因为一些冲突导致无法切换过去, 也可以先stash起来
* 需要pull更新本地, 但是有冲突导致pull失败, 可以stash起来, pull后在pop解决冲突

直接执行`git stash`则储藏当前的修改, 默认是save子命令

	⇒  git stash
	Saved working directory and index state WIP on master: 7f63cf0 update master file
	HEAD is now at 7f63cf0 update master file

这里WIP是work in process的缩写

stash的数据结构是一个`栈`, 即先进后出FILO(first in, last out), 相应的还原最近一个储藏则是:

	$ git stash pop

查看stash栈:

	⇒  git stash list
	stash@{0}: WIP on master: 7f63cf0 update master file
	stash@{1}: WIP on master: 7965691 master

这里储藏时是用的默认的信息, 指出了分支, 当前sha1 id.

`stash@{0}`是储藏的编号, 根据FILO的原则, 0表示最新的一个储藏

也可以手动输入信息:

	⇒  git stash save 'do a stash'
	Saved working directory and index state On master: do a stash
	HEAD is now at 7965691 master
	⇒  git --no-pager stash list
	stash@{0}: On master: do a stash

stash也是一个引用指针(`refs/stash`), 所以也可以使用这个引用来查看:

	⇒  git show-branch stash
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

    ⇒  git --no-pager reflog show master
    3dd62fb master@{0}: reset: moving to ORIG_HEAD
    7f63cf0 master@{1}: reset: moving to HEAD^

或者:

    ⇒  git --no-pager reflog show refs/heads/master
    3dd62fb refs/heads/master@{0}: reset: moving to ORIG_HEAD
    7f63cf0 refs/heads/master@{1}: reset: moving to HEAD^

针对输出结果, 第一列的sha1 id和第二列的别名是对应的, 第三列只出相应的操作类型和操作内容

`HEAD@{0}` 始终指向当前的HEAD, 这里可以看到`HEAD@{14}`是第一次提交

例子:

    ⇒  git --no-pager ll
    * 3dd62fb - (HEAD, mod, master) update file in mod (17 hours ago) <Tanky Woo>
    * 7f63cf0 - update master file (3 days ago) <Tanky Woo>
    ...

    ⇒  git --no-pager reflog | head -n 1
    3dd62fb HEAD@{0}: checkout: moving from mod to master

    (master) ⇒  git reset --hard HEAD^
    HEAD is now at 7f63cf0 update master file

    ⇒  git --no-pager reflog | head -n 2
    7f63cf0 HEAD@{0}: reset: moving to HEAD^
    3dd62fb HEAD@{1}: checkout: moving from mod to master

现在本地执行了一次reset, 如果发现是误操作, 想要返回, 但是本地的修改没有推送到远程, 这是可以通过reflog撤回:

    ⇒  git reset --hard HEAD@{1}
    HEAD is now at 3dd62fb update file in mod

表明要重置到老的HEAD版本.

当然, 这种情形下还有一个方法, 使用`ORIG_HEAD`:

    ⇒  git reset --hard ORIG_HEAD
    HEAD is now at 3dd62fb update file in mod

如`HEAD@{1}`, 如果使用形式`@{X}`, 则表示当前分支:

    ⇒  git --no-pager show @{0}
    commit 3dd62fb79377c7d0419ca12183db780489287731
    Author: Tanky Woo <wtq1990@gmail.com>
    Date:   Sat Jun 20 21:56:27 2015 +0800

    ...

    ⇒  git --no-pager reflog show @{0}
    3dd62fb refs/heads/master@{0}: reset: moving to ORIG_HEAD
    7f63cf0 refs/heads/master@{1}: reset: moving to HEAD^
    ...

另外, reflog的花括号内还可以指定时间限定符, 如:

    TankyWoo $ /tmp/test/ (master) ⇒  git --no-pager reflog 'HEAD@{1 hours ago}'
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

    ⇒  tree .git/logs/
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


## 14. 补丁 ##


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

	(master*) ⇒  tree .git/hooks
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

	(master) $ git --no-pager log --oneline
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

    $ git --no-pager show 78f19370f4c67ca094565b9de6310917eaf85321
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
    $ git --no-pager show HEAD:git.txt
    hello git
    hello git.txt

这里输出HEAD这个版本是, git.txt的内容. 书上说"需要该提交中确实包含了该文件", 这里说的有歧义, 应该说提交的tree blob有这个文件, 而不是这个提交中此文件必须有diff.

关于数据块的交互式暂存, 也就是`git add -p`和`git stash -p`等, 输出提示已经很详细了.

`git fsck` (file system check)可以帮助找回丢失的数据. 一些操作(如reset, rebase)会使一些对象失去和其它对象的连接, 从而脱离版本库的完整数据结构.

这些对象叫做"不可及的"(unreachable) 或 "悬挂的"(dangling).

如:

    ⇒  git init
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

	$  more ~/bin/git-top-check
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
