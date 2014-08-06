---
title: "Version Control with Git"
date: 2014-04-28 23:31
---

[TOC]

## 3. Getting Started ##

	# For a complete list of git subcommands
	git help --all

	# document for git subcommand
	git help <subcommand>
	git <subcommand> --help

double dash in command #todo# P19

`git show` : 

	# show the details of the most recent commit
	git show

	# To see more detail about a particular commit
	git show <commit number>

`git show-branch` :

	git show-branch --more=10

## 4.Basic Git Concepts ##

**NOTE**: This chapter is the most important section in this book.

Within a repository, Git maintains two primary data structures, the `object store` and the `index`.

At the heart of Git’s repository implementation is the object store. It contains your original data files and all the log messages, author information, dates, and other infor- mation required to rebuild any version or branch of the project.

### Object Store ##

Git places only four types of objects in the object store: `blob`, `tree`, `commit`, and `tag`.

* Blob : 

    Each version of a file is represented as a blob. "Blob" is a contraction of "binary large object". A blob holds a file’s data but does not contain any metadata about the file or even its name.

* Tree :

    A tree object represents one level of directory information. It records blob identifiers, pathnames, and a bit of metadata for all the files in one directory.

* Commit :

    A commit object holds metadata for each change introduced into the repository, including the author, committer, commit date, and log message. Each commit points to a tree object that captures, in one complete snapshot, the state of the repository at the time the commit was performed. The initial commit, or root com- mit, has no parent.

* Tag :

    A tag object assigns an arbitrary yet presumably human-readable name to a specific object, usually a commit.

In the four objects, the `tag` is optional.

### Index ###

The index is a temporary and dynamic binary file, captures a version of the project’s overall structure at some moment in time.

It records and retains changes, keeping them safe until ready to commit them.

Index also called `stage area`.

### Content-Addressable Names ###

Git object store is organized and implemented as as content-addressable storage system.

Each object in the object store has a unique name produced by applying SHA1 to the contents of the object, yielding an SHA1 hash value. SHA1 values are 160-bit values that are usually represented as a 40-digit hexadecimal number.

### Git Tracks Content ###

**Git is a content tracking system**

Git’s object store is based on the hashed computation of the contents of its objects, not on the file or directory names from the user’s original file layout.

If two separate files have exactly the same content, whether in the same or different directories, Git stores a single copy of that content as a blob within the object store.

	# An initial git repo
	TankyWoo@Mac::test/ (master) » find .git/objects
	.git/objects
	.git/objects/info
	.git/objects/pack

Add a file a.txt which content is 'hello' to the index, the SHA1 value is ce013625030ba8dba906f756967f9e9ca394464a

	TankyWoo@Mac::test/ (master) » echo 'hello' > a.txt
	TankyWoo@Mac::test/ (master*) » git add a.txt
	TankyWoo@Mac::test/ (master*) » find .git/objects
	.git/objects
	.git/objects/ce
	.git/objects/ce/013625030ba8dba906f756967f9e9ca394464a
	.git/objects/info
	.git/objects/pack
	TankyWoo@Mac::test/ (master*) » git cat-file -p ce013625030ba8dba906f756967f9e9ca394464a
	hello

Write this change to the tree object

	TankyWoo@Mac::test/ (master*) » git write-tree
	2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1
	TankyWoo@Mac::test/ (master*) » git cat-file -p 2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt

Now add another file b.txt, which is the same content with a.txt

	TankyWoo@Mac::test/ (master*) » echo 'hello' > b.txt
	TankyWoo@Mac::test/ (master*) » git add b.txt
	TankyWoo@Mac::test/ (master*) » git write-tree
	b5b0cccf7401633f12e0fafc6b85731251b86850
	TankyWoo@Mac::test/ (master*) » git cat-file -p b5b0cccf7401633f12e0fafc6b85731251b86850
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    b.txt

a.txt and b.txt point to the same blob object.

Now change the content of a.txt file.

	TankyWoo@Mac::test/ (master*) » echo 'world' >> a.txt
	TankyWoo@Mac::test/ (master*) » git add a.txt
	TankyWoo@Mac::test/ (master*) » git write-tree
	579c3877d5f450e34ea642b3a29d2d01dcf8e392
	TankyWoo@Mac::test/ (master*) » git cat-file -p 579c3877d5f450e34ea642b3a29d2d01dcf8e392
	100644 blob 94954abda49de8615a048f8d2e64b5de848e27a1    a.txt
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    b.txt

b.txt still point to the old blob, and a.txt point to the new blob

### Pathname Versus Content ###

Git’s physical data layout isn’t modeled after the user’s file directory structure. Instead, it has a completely different structure that can, nonetheless, reproduce the user’s orig- inal layout. Git’s internal structure is a more efficient data structure for its own internal operations and storage considerations.

### Practise ###

Every object store under `.git/objects`:

	TankyWoo@Mac::test-git2/ (master*) » find .git/objects
	.git/objects
	.git/objects/3b
	.git/objects/3b/18e512dba79e4c8300dd08aeb37f8e728b8dad
	.git/objects/info
	.git/objects/pack

	TankyWoo@Mac::test-git2/ (master*) » git cat-file -p 3b18e512dba79e4c8300dd08aeb37f8e728b8dad
	hello world

Git inserts a / after the first two digits to improve filesystem efficiency.

Such as `.git/objects/3b/18e512dba79e4c8300dd08aeb37f8e728b8dad`, the hash id is `3b18e512dba79e4c8300dd08aeb37f8e728b8dad`

Use `git cat-file` to see the content of object store:

	TankyWoo@Mac::test-git2/ (master*) » git cat-file -p 3b18e512dba79e4c8300dd08aeb37f8e728b8dad
	hello world

Tip:

Use `git rev-parse` can parse short hash to completely hash:

	TankyWoo@Mac::test-git2/ (master*) » git rev-parse 3b18
	3b18e512dba79e4c8300dd08aeb37f8e728b8dad

As mentioned before, Git tracks the pathnames of files through another kind of object called a `tree`.

When you use git add, Git creates an object(blob) for the contents of each file you add(in .git/objects/), but it doesn’t create an object for your tree right away. Instead, it updates the index.

The index is found in `.git/index` and keeps track of file pathnames and corre-sponding blobs.

`git ls-files` can show information about files in the index and the working tree

`git write-tree` create a tree object from current index by capturing a snapshot of its current information

	TankyWoo@Mac::test/ (master*) » git ls-files -s
	100644 ce013625030ba8dba906f756967f9e9ca394464a 0       a.txt

	TankyWoo@Mac::test/ (master*) » git write-tree
	2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1

### Tree Hierarchies ###

	TankyWoo@Mac::test/ (master*) » tree .git/objects
	.git/objects
	├── 2e
	│   └── 81171448eb9f2ee3821e3d447aa6b2fe3ddba1
	├── ce
	│   └── 013625030ba8dba906f756967f9e9ca394464a
	├── info
	└── pack

The tree object `2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1`:

	TankyWoo@Mac::test/ (master*) » git cat-file -p 2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt

Create a sub directory, and copy a.txt in it:

	TankyWoo@Mac::test/ (master*) » git add subdir/a.txt
	TankyWoo@Mac::test/ (master*) » git write-tree
	ec518d6bb3cabb8e88b5458cf18d862aa0514622

In the new tree object, subdir object is a tree object, and point to `2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1`.
which is the same as the top tree object.

	TankyWoo@Mac::test/ (master*) » git cat-file -p ec518d6bb3cabb8e88b5458cf18d862aa0514622
	100644 blob ce013625030ba8dba906f756967f9e9ca394464a    a.txt
	040000 tree 2e81171448eb9f2ee3821e3d447aa6b2fe3ddba1    subdir

The new tree for subdir contains only one file, a.txt, and that file contains the same old “hello” content. So the subdir tree is exactly the same as the older, top-level tree! And of course it has the same SHA1 object name as before.

### Commits ###

Use the low-level command `git commit-tree` to commit the tree object, and generate a commit object:

	TankyWoo@Mac::test/ (master*) » echo -n 'Init site\n' | git commit-tree ec518d6bb3cabb8e88b5458cf18d862aa0514622
	5c5e63c0ee9a9c51304f352ec0581704411003ad


	TankyWoo@Mac::test/ (master*) » git cat-file -p 5c5e63c0ee9a9c51304f352ec0581704411003ad
	tree ec518d6bb3cabb8e88b5458cf18d862aa0514622
	author Tanky Woo <wtq1990@gmail.com> 1406774332 +0800
	committer Tanky Woo <wtq1990@gmail.com> 1406774332 +0800

	Init site

`author` vs `committer`(from [Pro Git](http://git-scm.com/book/ch2-3.html))

> The author is the person who originally wrote the patch, whereas the committer is the person who last applied the patch. So, if you send in a patch to a project and one of the core members applies the patch, both of you get credit — you as the author and the core member as the committer.

A more detailed explanation see [this](http://stackoverflow.com/a/18754896/1276501)

### Tag ###

Create an annotated, unsigned tag:

	TankyWoo@Mac::test/ (master*) » git tag -m 'version 1.0 tag' v1.0 5c5e63c0ee9a9c51304f352ec0581704411003ad

Get the SHA1 id by tag name:

	TankyWoo@Mac::test/ (master*) » git rev-parse v1.0
	606d5478f68648e14de7b204d5484e4b83b2a3a0

The tag object:

	TankyWoo@Mac::test/ (master*) » git cat-file -p 606d5478f68648e14de7b204d5484e4b83b2a3a0
	object 5c5e63c0ee9a9c51304f352ec0581704411003ad
	type commit
	tag v1.0
	tagger Tanky Woo <wtq1990@gmail.com> 1406811935 +0800

	version 1.0 tag

**NOTE**: In this section, most of the commands are the low-level comamnds. In real life, should not use this commands!

## 5. File Management and the Index ##

与其它版本管理系统不同，Git在工作目录(working directory)与已提交历史(history)之间，增加了一个Index(Stage)层，称为索引(暂存)目录。

> Linus Torvalds 在git mailing list里提到，如果不先理解Index的目的，就无法理解和领会Git的强大。

Git 把文件分为三个大类: `Tracked`, `Untracked`和`Ignored`，其中`Tracked`又可以分为`Staged` 和 `Unstaged`，在工作目录下修改的文件是Unstaged，经过`git add`后变为Staged。

Git 的Index不存放任何文件的内容，它只简单的记录准备提交的文件，当运行`git commit`时，git 会检查Index而不是工作目录。

`git ls-files --stage` 可以查看stage中的文件的`SHA1`值:

	TankyWoo@Mac::git-test/ (master*) » git ls-files --stage
	100644 8d0e41234f24b6da002d962a26c2495ea16a425f 0       fa

`git hash-object`可以计算文件的`SHA1`值并输出:

	TankyWoo@Mac::git-test/ (master*) » git hash-object fa
	8d0e41234f24b6da002d962a26c2495ea16a425f

简单的说是文件fa已经在Index中了，本质是文件在`object store`中，Index指向它。

关于 `--all` 在 `git add` 和 `git commit`中有点区别，文件必须要经过add才会被tracked，`git add --all` 会把所有tracked 和 untracked的文件都add，但是`git commit --all`只会add所有tracked的文件并提交。

关于`git rm`，如果tracked中的文件被修改了，则可以通过`git rm --cached`来从git库中移除，并在本地保存为untracked的，也可以通过`-f`强制删除。

对于被误删的文件，如果在Index中，如下:

	TankyWoo@Mac::git-test/ (master*) » gst
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

	TankyWoo@Mac::git-test/ (master) » git ls-files --stage
	100644 15acaeb140c2805acdbb2d0dbdedeeea6bb73b06 0       fa
	TankyWoo@Mac::git-test/ (master) » git mv fa fb
	TankyWoo@Mac::git-test/ (master*) » git ls-files --stage
	100644 15acaeb140c2805acdbb2d0dbdedeeea6bb73b06 0       fb

把fa改为fb后，`SHA1`值并没变。

经过mv操作后，使用`git log fb`只会看到变更后的提交(包括变更的那个提交)，即关联内容并为fb文件的历史，可以通过`git log --follow fb` 来查看关联这段内容的完整历史。

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

    TankyWoo@Mac::simiki/ (master) » tree .git/refs
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

    TankyWoo@Mac::simiki/ (master) » more .git/refs/heads/master
    569898602add495da34fb8684e39f60d26176a19

tags记录的是最新的一个tag

`symrefs`(symbol reference, 符号引用), 是一个指向引用的引用(指针).存放在`.git/`目录下

`HEAD`: `.git/HEAD`, 总是指向当前分支的最后一次提交, 当分支改变，HEAD也会变

    TankyWoo@Mac::simiki/ (master) » more .git/HEAD
    ref: refs/heads/master

`ORIG_HEAD`: `.git/ORIG_HEAD`, 一些操作, 如`merge`或`reset`, 会记录操前的commit(HEAD). 作为一个保护措施，使操作可以回溯.

比如最近三个commits:

    * d46546a - (HEAD, master) update d (42 seconds ago) <Tanky Woo>
    * 8ed2d79 - update f (76 seconds ago) <Tanky Woo>
    * 75b09c2 - (tag: v0.1) Merge branch 'dev' (3 days ago) <Tanky Woo>

`ORIG_HEAD` 存储的是之前某一个commit:

    TankyWoo@Mac::test-git/ (master) » more .git/ORIG_HEAD
    015b5b99f5c9973e840f29c9f6e6b936c99b92a5

做一次reset操作:

    TankyWoo@Mac::test-git/ (master) » git reset --soft HEAD^

查看`ORIG_HEAD`, 会指向之前的HEAD:

    TankyWoo@Mac::test-git/ (master) » more .git/ORIG_HEAD
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

