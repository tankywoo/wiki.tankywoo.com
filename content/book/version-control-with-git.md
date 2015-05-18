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

在版本库中, Git维护两个主要的数据结构: `对象库(object store)` 和 `索引(index)`. 所有这些版本库数据妇女放在工作目录根目录下的`.git`的隐藏目录中.

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

## 6. Commits ##

To identify commits, there are two ways: explicit references and a few implied references.

The explicit reference to commit is its hash ID(SHA1).

Git also provides mechanisms for identifying a commit relative to another reference.

such as `master^` and `master~2` etc.

The `caret`(`^`) is used to select a different parent.

Given a commit C, C^1 is the first parent, C^2 is the second parent, C^3 is the third parent, and so on, as shown in Figure 6-1(see on book).

The `tilde`(`~`) is used to go back before an ancestral parent and select a preceding generation. Again, given the commit C, C~1 is the first parent, C~2 is the first grandparent, and C~3 is the first great-grandparent. as shown in Figure 6-2.(see on book)

For example, a simple repo log:

    *   75b09c2 - (HEAD, master) Merge branch 'dev' (4 seconds ago) <Tanky Woo>
    |\
    | * 0aab100 - (dev) Add d (26 seconds ago) <Tanky Woo>
    | * 6a9379e - Add c (31 seconds ago) <Tanky Woo>
    * | 015b5b9 - Add f (14 seconds ago) <Tanky Woo>
    |/
    * 545851d - Add b (59 seconds ago) <Tanky Woo>
    * 1509ece - Add a (80 seconds ago) <Tanky Woo>

Choose the first parent:

    $ git log -1 --pretty=oneline --abbrev-commit -p master^1
    015b5b9 Add f

Choose the second parent, this is the dev branch commit merged into master:

    $ git log -1 --pretty=oneline --abbrev-commit -p master^1
    0aab100 Add d

such as `master^` refers to the penultimate commit on the master branch.

Use `tilde`:

    $ git log -1 --pretty=oneline --abbrev-commit -p master~1
    015b5b9 Add f

`master^1` is the same as `master~1`

If the number is not specified, as `master^` or `master~`, it's default to `master^1` or `master~1`, also, `master^^` is the same as `master^1^1`, and it's the same as `master~2`.

See the parent of the second parent:

    $ git log -1 --pretty=oneline --abbrev-commit -p master^2~1
    6a9379e Add c


**TODO** 
2. `git show-branch`

### refs and symrefs ###

1. A ref is an SHA1 hash ID that refers to an object within the Git object store. Although a ref may refer to any Git object, it usually refers to a commit object.
2. A symbolic reference, or symref, is a name that indirectly points to a Git object. It is still just a ref.

`refs`(reference, 引用), 一般指向某个commit.

Local topic branch names, remote tracking branch names, and tag names are all refs.

本地分支名, 远程分支名, tag名都是refs.

* local branch - `.git/refs/heads/`
* remote branch - `.git/refs/remotes/`
* tag - `.git/refs/tags/`

所以如本地分支`master`, 全名就是`.git/refs/heads/master`

存放在`.git/refs` 目录下:

    TankyWoo@Mac::simiki/ (master) ⇒ tree .git/refs
    .git/refs
    ├── heads
    │   ├── dev
    │   ├── jinja-extensions
    │   └── master
    ├── remotes
    │   └── origin
    │       ├── HEAD
    │       ├── dev
    │       └── master
    └── tags
        └── v1.2.1

master这个refs存放的就是master分支的最后一次commit id:

    TankyWoo@Mac::simiki/ (master) ⇒ more .git/refs/heads/master
    569898602add495da34fb8684e39f60d26176a19

tags记录的是最新的一个tag

`symrefs`(symbol reference, 符号引用), 是一个指向引用的引用(指针).存放在`.git/`目录下

`HEAD`: `.git/HEAD`, 总是指向当前分支的最后一次提交, 当分支改变，HEAD也会变

    TankyWoo@Mac::simiki/ (master) ⇒ more .git/HEAD
    ref: refs/heads/master

`ORIG_HEAD`: `.git/ORIG_HEAD`, 一些操作, 如`merge`或`reset`, 会记录操前的commit(HEAD). 作为一个保护措施，使操作可以回溯.

比如最近三个commits:

    * d46546a - (HEAD, master) update d (42 seconds ago) <Tanky Woo>
    * 8ed2d79 - update f (76 seconds ago) <Tanky Woo>
    * 75b09c2 - (tag: v0.1) Merge branch 'dev' (3 days ago) <Tanky Woo>

`ORIG_HEAD` 存储的是之前某一个commit:

    TankyWoo@Mac::test-git/ (master) ⇒ more .git/ORIG_HEAD
    015b5b99f5c9973e840f29c9f6e6b936c99b92a5

做一次reset操作:

    TankyWoo@Mac::test-git/ (master) ⇒ git reset --soft HEAD^

查看`ORIG_HEAD`, 会指向之前的HEAD:

    TankyWoo@Mac::test-git/ (master) ⇒ more .git/ORIG_HEAD
    d46546a5192b7e1c834947b612e3401a6f7729c7

这样就可以回溯到reset之前的版本:

    git reset ORIG_HEAD

`HEAD` vs `ORIG_HEAD` [HEAD and ORIG\_HEAD in Git](http://stackoverflow.com/questions/964876/head-and-orig-head-in-git)

`FETCH_HEAD`: TODO

`MERGE_HEAD`: TODO

`git symbolic-ref` TODO

详细可以参考[progit-9.3](http://git-scm.com/book/en/Git-Internals-Git-References)

### Viewing Old Commits ###

Specify a commit range using the form `since..until`, this will show the commit from since(**exclude**) to until(**include**)

    $ git log --pretty=oneline --abbrev-commit master~3..master~1
    015b5b9 Add f
    545851d Add b

Use `-p|--patch` option to print the patch(changes):

    $ git log -1 -p master

This is the same as:

    $ git show master

`git show` can also display blob in remote branch. **TODO**

    $ git show origin/master:setup.py

Notice the `-1` to restricts the output to a single commit, otherwise will display all commits in master. type `-n` to limit output to at most n commits.

`--stat` option enumerates the files changed in a commit and tallies how many lines were modified in each file.

### Commit Ranges ###

TODO

### Finding Commits ###

`git bisect`
`git blame`

TODO

## 8. Diffs ##

four fundamental comparisons:

`git diff` : between working directory and the index.

`git diff <commit>` : between working directory and the given commit.

`git diff --cached <commit>` : between the staged changes in the index and the given commit. `--staged` is the new synonym of `--cached`.

`git diff <commit1> <commit2>` : between the arbitrary two commits.

Options:

`-M` : #todo#

> The --M option detects renames and generates a simplified output that simply re- cords the file rename rather than the complete removal and subsequent addition of the source file. If the rename is not a pure rename but also has some additional content changes, Git calls those out.

`-w` or `--ignore-all-space`: compare without considering changes in whitespace as significant.

`--stat` : show statistics about the difference between any two tree states.

git diff with Path Limiting:

	# limit changes in specify directory
	git diff some_directory

	# limit changes in specify file
	git diff some_file

search changes containing string with `-S`:

	# search the past 50 commits to the master branch for changes containing string "octopus"
	git diff -S "octopus" master~50

