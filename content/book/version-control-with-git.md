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

