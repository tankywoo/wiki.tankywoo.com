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

Within a repository, Git maintains two primary data structures, the `object store` and the `index`.

At the heart of Git’s repository implementation is the object store. It contains your original data files and all the log messages, author information, dates, and other infor- mation required to rebuild any version or branch of the project.

### Object Store ##

Git places only four types of objects in the object store: `blob`, `tree`, `commit`, and `tag`.

* Blob : 

    Each version of a file is represented as a blob. A blob holds a file’s data but does not contain any metadata about the file or even its name.

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

Every commit content store under `.git/objects`:

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

**TODO**

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

