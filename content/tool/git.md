---
title: "Git"
date: 2013-11-08 00:02
---

[TOC]

Git的`help`信息非常好，很多可以直接help来了解

## 给Git输出信息增加颜色 ##

编辑`/etc/gitconfig`
比如要对`git status`设置颜色，可以:

	[color]
		ui = auto
	[color "branch"]
		current = yellow reverse
		local = yellow
		remote = green
	[color "diff"]
		meta = yellow bold
		frag = magenta bold
		old = red bold
		new = green bold
	[color "status"]
		added = yellow
		changed = green
		untracked = cyan

参考:

* [How to show git colors on zsh](http://stackoverflow.com/questions/12255028/how-to-show-git-colors-on-zsh)
* [Enabling git syntax highlighting for macs terminal](http://stackoverflow.com/questions/8131322/enabling-git-syntax-highlighting-for-macs-terminal)
* [How to colours in git](http://nathanhoad.net/how-to-colours-in-git)


## 关于Git的分支 ##

参考的 [何谓分支](http://git-scm.com/book/zh/Git-%E5%88%86%E6%94%AF-%E4%BD%95%E8%B0%93%E5%88%86%E6%94%AF)

因为Git是保存的快照，Git仓库有以下几个基本对象

* `blob` 对象用于表示文件快照内容
* `tree` 对象记录目录树内容和各个文件对应的blob对象索引
* `commit` 对象记录提交信息，指向tree对象或其他commit对象

Git的分支，其本质是一个指向commit对象的可变`指针`，Git使用`master`作为分支的默认名字

`HEAD`指针指向当前的分支指针

使用`git branch`是查看当前的分支列表

使用`git branch branch_name`新建分支，然后可以使用`git checkout branch_name`切换分支

最后可以用`git merge branch_name`来合并分支

如果遇到冲突，需要到冲突的文件下根据提示编辑后再commit

## 远程分支 ##

参考的 [远程分支](http://git-scm.com/book/zh/Git-%E5%88%86%E6%94%AF-%E8%BF%9C%E7%A8%8B%E5%88%86%E6%94%AF)

从远程Git repo克隆，Git会自动将此remote repo命名为`origin`，并下载其中所有的数据，建立一个指向它的`master`分支的指针，在本地命名为`origin/master`

但无法在本地更改其数据。接着，Git建立一个属于自己的本地`master`分支，始于`origin`上`master`分支相同的位置，这样可以就此开始工作

	touch README.md
	git init
	git add README.md
	git commit -m "first commit"
	git remote add origin git@github.com:tankywoo/test.git
	git push -u origin master

这里origin是remote repo name，branch name 是master

### 关于fetch和pull区别 ###

What is `git fetch`? and what is the difference to `git pull`?

`git fetch`是update from remote repo，但是不合并

`git pull`是fetch and merge

## Git标签 ##

* 含附注的标签(annotated)
* 轻量级标签(lightweight)

[2.6 Git 基础 - 打标签](http://git-scm.com/book/zh/Git-%E5%9F%BA%E7%A1%80-%E6%89%93%E6%A0%87%E7%AD%BE)

删除远程标签:

	git push origin :tagname

或

	git push --delete origin tagname

[参考](http://stackoverflow.com/a/5480292/1276501)

## Git 全局配置 ##

全局忽略文件

* [忽略文件](http://git-scm.com/book/zh/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-%E9%85%8D%E7%BD%AE-Git)
* [git ignore repo](https://github.com/GitHub/gitignore)

## 使用vimdiff ##

默认的diff应该是使用diff命令, 这个命令也非常有必要掌握.

但是, 更直观的, 可以选择vimdiff.

	# 配置Git使用vimdiff来做差异比较
	git config --global diff.tool vimdiff
	# 在merge时使用
	git config --global merge.tool vimdiff
	# 因为在使用vimdiff时, vim会有如下提示:
	# Viewing: 'tkwiki/tool/git.wiki'
	# Launch 'vimdiff' [Y/n]: y
	# 可以取消这个提示
	git config --global difftool.prompt false

然后就可以

	git difftool tkwiki/tool/git.wiki

来查看修改的地方, 效果图:

![git vimdiff](http://tankywoo-wb.b0.upaiyun.com/git_vimdiff.png)

参考:

* [Git and Vimdiff](http://usevim.com/2012/03/21/git-and-vimdiff/)
* [Using Vimdiff with Git](http://agileadam.com/using-vimdiff-git)

## 查看提交log ##

git log 会查看当前git repo里所有的提交历史

git log filename 会查看这个文件的所有提交历史

git log -p -2 [filename] 会把最近的2次提交变更展开

git log --pretty=oneline [filename] 这个太牛逼了, 只显示id和提交说明.

git log --pretty=format:"xxxx" 这个更牛逼, 自定义查看log的输出格式

参考:

* [查看提交历史](http://git-scm.com/book/zh/Git-%E5%9F%BA%E7%A1%80-%E6%9F%A5%E7%9C%8B%E6%8F%90%E4%BA%A4%E5%8E%86%E5%8F%B2)

## 文件中文名问题 ##

最近遇到同步文件下来, 中文文件名全部是unicode, 解决这个问题加配置:

	git config --global core.quotepath false

## Git mv 日志问题 ##

在 `git mv` (rename) 文件后, 直接 git log 只能看到这个文件被 rename 后的日志, 想要看到完整的日志, 要用 `git log --follow xxx`

参考:

* [Is it possible to move/rename files in git and maintain their history?](http://stackoverflow.com/questions/2314652/is-it-possible-to-move-rename-files-in-git-and-maintain-their-history)
* [What's the purpose of git-mv?](http://stackoverflow.com/questions/1094269/whats-the-purpose-of-git-mv)

## 指定路径pull ##

以前都是 cd 到仓库当前目录然后 pull. 因为想到 `svn up` 可以直接指定路径, 这种基本功能 git 肯定会有的, 但是直接指定路径不行.

搜了下, StackOverflow 上的 [回答1](http://stackoverflow.com/a/9876901/1276501) 和 [回答2](http://stackoverflow.com/a/9746005/1276501) 非常给力.

Git 的参数 `--git-dir` 可以指定 Git 的路径, 即使用这个 `.git` 的配置等来更新 repo. 但是这个会以 `pwd` 为要更新的 repo 路径.
所以还需要 `--work-tree` 来指定要更新的 repo 的路径, 而不需要 cd 过去.

```bash
git --git-dir=/path/to/git-repo/.git --work-tree=/path/to/git-repo/ pull
```

## 查看指定目录下的 status ##

	git status [path]

比如当前目录下的 status:

	git status .

[git status - is there a way to show changes only in a specific directory?](http://stackoverflow.com/questions/715321/git-status-is-there-a-way-to-show-changes-only-in-a-specific-directory)

## 选择一部分修改提交 ##

使用 `git add -p filename`。

具体见:

* [Git 工具 - 交互式暂存](http://git-scm.com/book/zh/Git-%E5%B7%A5%E5%85%B7-%E4%BA%A4%E4%BA%92%E5%BC%8F%E6%9A%82%E5%AD%98)
* [How can I commit only part of a file in git](http://stackoverflow.com/questions/1085162/how-can-i-commit-only-part-of-a-file-in-git)

## 只从 git repo 中移除文件, 但不删除实际文件##

	git rm --cached file

默认使用 `git rm` 会把文件也一并删除掉.

## 修改最后一次提交 ##

使用:

	git commit --amend

如果当前 stage区 没有东西, 则相当于可以修改 commit comment.

如果 stage区 有新的文件, 比如有个文件staged后忘了和上次的提交一次commit, 则可以撤销并重新提交.

## 修改commit的author ##

如果是staged的文件，提交时直接指定 `--author` 就可以了:

	git commit -m "xxx" --author="Tanky Woo <noreply@tankywoo.com>"

修改最后一次提交的author，可以配合 `--amend`:

	git commit --amend --author="Tanky Woo <noreply@tankywoo.com>"

如果user config配置修改了，可以直接`--reset-author`:

	git commit --amend --reset-author

修改指定commit的author:

	* 2f1e828 - (HEAD, origin/test, origin/master, test, master) update test-git-submodule (2 days ago) <Tanky Woo>
	* 3243b09 - first commit with submodule (2 days ago) <Tanky Woo>
	* 5956ab0 - why conflict and merge? (3 weeks ago) <Tanky Woo>

现在想修改 3243b09 的 author name，需要从它之前的一个commit开始`rebase`:

	TankyWoo@Mac::test-git/ (master) » git rebase -i 5956ab0

Git 会使用设置的编辑器打开如下:

	pick 3243b09 first commit with submodule
	pick 2f1e828 update test-git-submodule

	# Rebase 5956ab0..2f1e828 onto 5956ab0
	#
	# Commands:
	#  p, pick = use commit
	#  r, reword = use commit, but edit the commit message
	#  e, edit = use commit, but stop for amending
	#  s, squash = use commit, but meld into previous commit
	#  f, fixup = like "squash", but discard this commit's log message
	#  x, exec = run command (the rest of the line) using shell
	#
	# These lines can be re-ordered; they are executed from top to bottom.
	#
	# If you remove a line here THAT COMMIT WILL BE LOST.
	#
	# However, if you remove everything, the rebase will be aborted.
	#
	# Note that empty commits are commented out

根据提示，把需要修改的一行用`edit`替换`pick`:

	edit 3243b09 first commit with submodule
	pick 2f1e828 update test-git-submodule

保存关闭后会提示:

	Stopped at 3243b09... first commit with submodule
	You can amend the commit now, with

			git commit --amend

	Once you are satisfied with your changes, run

			git rebase --continue

如果要对first commit开始做rebase:

	git rebase -i --root

我设置的PS1的括号里是分支名，可以看到现在的分支是这个要修改的commit id:

	TankyWoo@Mac::test-git/ (3243b09*) » git commit --amend --author="Tanky <noreply@tankywoo.com>"

修改完后会进入下一个commit id分支，直接`--continue`，因为604c35c这个commit设置的是pick，所以不会做改动:

	TankyWoo@Mac::test-git/ (604c35c*) » git rebase --continue
	Successfully rebased and updated refs/heads/master.

再查看日志:

	* 16c4757 - (HEAD, master) update test-git-submodule (2 seconds ago) <Tanky Woo>
	* b9fbd8a - first commit with submodule (15 seconds ago) <Tanky>
	* 5956ab0 - why conflict and merge? (3 weeks ago) <Tanky Woo>

[SO](http://stackoverflow.com/a/3042512/1276501)上的回答:

> For example, if your commit history is `A-B-C-D-E-F` with `F` as `HEAD`, and you want to change the author of `C` and `D`, then you would...
> 
>  1. Specify `git rebase -i B`
>  2. change the lines for both `C` and `D` to `edit`
>  3. Once the rebase started, it would first pause at `C`
>  4. You would `git commit --amend --author="Author Name <email@address.com>"`
>  5. Then `git rebase --continue`
>  6. It would pause again at `D`
>  7. Then you would `git commit --amend --author="Author Name <email@address.com>"` again
>  8. `git rebase --continue`
>  9. The rebase would complete.

如果要修改指定用户全部commit的author:

	git filter-branch -f --env-filter '
	an="$GIT_AUTHOR_NAME"
	am="$GIT_AUTHOR_EMAIL"
	cn="$GIT_COMMITTER_NAME"
	cm="$GIT_COMMITTER_EMAIL"

	if [ "$GIT_COMMITTER_EMAIL" = "<OLD EMAIL>" ] ; then
		cn="<NEW NAME>"
		cm="<NEW EMAIL>"
		export GIT_COMMITTER_NAME="$cn"
		export GIT_COMMITTER_EMAIL="$cm"
	fi
	if [ "$GIT_AUTHOR_EMAIL" = "<OLD EMAIL>" ] ; then
		an="<NEW NAME>"
		am="<NEW EMAIL>"
		export GIT_AUTHOR_NAME="$an"
		export GIT_AUTHOR_EMAIL="$am"
	fi
	'

这个在[github官方help](https://help.github.com/articles/changing-author-info)里也有脚本。

StackOverflow上有两篇讨论非常好:

* [How do I change the author of a commit in git?](http://stackoverflow.com/questions/750172/how-do-i-change-the-author-of-a-commit-in-git)
* [Change commit author at one specific commit](http://stackoverflow.com/questions/3042437/change-commit-author-at-one-specific-commit)

## Git diff 技巧 ##

(待整理)

	git diff tag                    比较tag和HEAD之间的不同。
	git diff tag file               比较一个文件在两者之间的不同。
	git diff tag1..tag2             比较两个tag之间的不同。
	git diff SHA11..SHA12           比较两个提交之间的不同。
	git diff tag1 tag2 file or
	git diff tag1:file tag2:file    比较一个文件在两个tag之间的不同。

`ORIG_HEAD` 用于指向前一个操作状态，因此在git pull之后如果想得到pull的
	内容就可以：
	 
	git diff ORIG_HEAD
	 
	git diff --stat                 用于生成统计信息。
	git diff --stat ORIG_HEAD

## `HEAD` vs `ORIG_HEAD` ##

关于 `HEAD` 和 `ORIG_HEAD` 的区别，来至StackOverflow的[回答](http://stackoverflow.com/a/967611/1276501):

> `HEAD` is (direct or indirect, i.e. symbolic) reference to the current commit. It is a commit that you have checked in the working directory (unless you made some changes, or equivalent), and it is a commit on top of which "git commit" would make a new one. Usually `HEAD` is symbolic reference to some other named branch; this branch is currently checked out branch, or current branch. `HEAD` can also point directly to a commit; this state is called "detached HEAD", and can be understood as being on unnamed, anonymous branch.

> `ORIG_HEAD` is previous state of `HEAD`, set by commands that have possibly dangerous behavior, to be easy to revert them. It is less useful now that Git has reflog: `HEAD@{1}` is roughly equivalent to `ORIG_HEAD` (`HEAD@{1}` is always last value of `HEAD`, `ORIG_HEAD` is last value of `HEAD` before dangerous operation).

For more information read [git(1) manpage](http://www.kernel.org/pub/software/scm/git/docs/git.html), [Git User's Manual](http://www.kernel.org/pub/software/scm/git/docs/user-manual.html), the [Git Community Book](http://book.git-scm.com/) and [Git Glossary](http://www.kernel.org/pub/software/scm/git/docs/gitglossary.html)

其它的一些讲解:

* [ORIG\_HEAD, FETCH\_HEAD, MERGE\_HEAD etc](http://stackoverflow.com/questions/17595524/orig-head-fetch-head-merge-head-etc)
* [GIT基本概念和用法总结](http://guibin.iteye.com/blog/1014369)

## git revert/reset/checkout 区别 ##

讲得挺好的一篇 [Undoing Git Changes](https://www.atlassian.com/git/tutorial/undoing-changes)，关于`git checkout`, `git revert`,`git reset`, `git clean` 的对比。

## 统计每个提交者的提交次数 ##

	git shortlog --numbered --summary

## git reflog ##

TODO

## git cherry-pick ##

TODO

## Git Commit Message 基本准则 ##

一些基本的准则:

* commmit时不建议使用`-m/--message`，这样能提交的信息太简单的；建议直接commit通过编辑器来撰写message.
* **第一行不**超过50个字符，作为简单的描述，第二行为空行，第三行开始再做详细描述，例子(<http://git-scm.com/book/ch5-2.html>):

		Short (50 chars or less) summary of changes

		More detailed explanatory text, if necessary.  Wrap it to about 72
		characters or so.  In some contexts, the first line is treated as the
		subject of an email and the rest of the text as the body.  The blank
		line separating the summary from the body is critical (unless you omit
		the body entirely); tools like rebase can get confused if you run the
		two together.

		Further paragraphs come after blank lines.

		 - Bullet points are okay, too

		 - Typically a hyphen or asterisk is used for the bullet, preceded by a
		   single space, with blank lines in between, but conventions vary here	

* **第一行** 结尾不要用句号，这个可以认为是一个标题
* **第三行** 开始的详细描述长度不超过72个字符
* 使用 `git diff --check` 对无用的空白做检查:

		--check -- warn if changes introduce trailing whitespace or space/tab indents

* 使用 `fix`, `add`, `change` 而不是 `fixed`, `added`, `changed`

	> Write the summary line and description of what you have done in the imperative mode, that is as if you were commanding someone. Write "fix", "add", "change" instead of "fixed", "added", "changed".

* 尽量使用英文提交
* 针对Github，在commit message中使用 `#id`(id 为具体issue的标号)，可以把message关联到具体的issue

可以看看Git源码的提交log : <https://git.kernel.org/cgit/git/git.git/log/>

一些不错的文章:

* [5 Useful Tips For A Better Commit Message](http://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message)
* [Git commit 注释格式](http://www.fwolf.com/blog/post/14)
* [http://www.fwolf.com/blog/post/14](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
* [Writing good commit messages](https://github.com/erlang/otp/wiki/Writing-good-commit-messages)
* [Distributed Git - Contributing to a Project](http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project)

## git add 只添加 tracked 的文件 ##

git add 有一个 `-u` 选项，会只添加tracked的文件，比如在项目根目录下，可以添加所有修改过的已经tracked的文件:

	git add -u .

如果单纯的`git add .` 会把untracked的文件也加进去

## 删除untracked files ##

	git clean -f

**But beware... there's no going back. Use -n or --dry-run to preview the damage you'll do.**

If you want to also remove directories, run `git clean -f -d`

If you just want to remove ignored files, run `git clean -f -X`

If you want to remove ignored as well as non-ignored files, run `git clean -f -x`

Note the case difference on the X for the two latter commands.

If `clean.requireForce` is set to "true" (the default) in your configuration, then unless you specify -f nothing will actually happen, with a recent enough version of git.

See the [git-clean docs](http://git-scm.com/docs/git-clean) for more information.

[from](http://stackoverflow.com/a/64966/1276501)

## 同一个文件选择部分提交 ##

You can do `git add -p filename`, and it'll ask you what you want to stage. You can then:

* hit `s` to split whatever change into smaller hunks. This only works if there is at least one unchanged line in the "middle" of the hunk, which is where the hunk will be split
* then hit either:
	* `y` to stage that hunk, or
	* `n` to not stage that hunk, or
	* `e` to manually edit the hunk (useful when git can't split it automatically)
* and `d` to exit or go to the next file.
* Use `?` to get the whole list of available options.

If the file is not in the repository yet, do first `git add -N filename`. Afterwards you can go on with `git add -p filename`.

[Source](http://stackoverflow.com/a/1085191/1276501)

## checkout 指定的 tag ##

    git checkout tags/<tag_name>

[参考](http://stackoverflow.com/questions/791959/download-a-specific-tag-with-git)

## git add的几个参数和通配符 ##

* `git add .` stages new and modified, in Git 1.x, **without deleted**, in Git 2.x, **with deleted**
* `git add -u` stages modified and deleted, **without new**
* `git add -A` stages **All**
* `git add *` stages new(except name begin with `dot`) and modified, **without deleted**

这里得注意, `git add .` 在 Git 1.x 和 Git 2.0以后是不一样的.

详细讨论见:

* [Difference between “git add -A” and “git add .”](http://stackoverflow.com/questions/572549/difference-between-git-add-a-and-git-add/16162511#16162511)
* [git add * (asterisk) vs git add . (period)](http://stackoverflow.com/questions/26042390/git-add-asterisk-vs-git-add-period)

## 检查repo是否dirty ##

    git status --porcelain

关于git提示的状态, 见`man git-status`的 `[OUTPUT] -> [Short Format]` 一节

参考:

* [Checking for a dirty index or untracked files with Git](http://stackoverflow.com/questions/2657935/checking-for-a-dirty-index-or-untracked-files-with-git)
* [How can I check in a bash script if my local git repo has changes](http://stackoverflow.com/questions/5143795/how-can-i-check-in-a-bash-script-if-my-local-git-repo-has-changes)
* [How do I programmatically determine if there are uncommited changes?](http://stackoverflow.com/questions/3878624/how-do-i-programmatically-determine-if-there-are-uncommited-changes)

## 检查repo当前HEAD是否提示ahead或behind远程仓库分支 ##

比如像这样的:

    $ /opt/nlo/nginx# git status
    # On branch master
    # Your branch is ahead of 'origin/master' by 13 commits.
    #
    nothing to commit (working directory clean)

使用:

    git rev-list --left-right --count origin/master...master

将master与远程仓库origin/master作比较.

如果master的HEAD比origin/master新则报ahead, 否则behind.

返回结果格式是:

    {behind}\t{ahead}

参考:

* [git: programmatically know by how much the branch is ahead/behind a remote branch](http://stackoverflow.com/questions/2969214/git-programmatically-know-by-how-much-the-branch-is-ahead-behind-a-remote-branc)
* [git ahead/behind info between master and branch?](http://stackoverflow.com/questions/20433867/git-ahead-behind-info-between-master-and-branch)
* [git-branch-status](https://gist.github.com/vitalk/8639831)

## 获取当前分支名 ##

在`Git 1.8`及以后:

    $ git symbolic-ref --short HEAD

`Git 1.7+`:

    $ git rev-parse --abbrev-ref HEAD

[参考](http://stackoverflow.com/questions/6245570/how-to-get-current-branch-name-in-git)

## 删除分支 ##

远程分支被删除后(如Github在页面上删除分支), 本地删除追踪分支:

    git fetch -p

## Git本地设置某个远程库readonly ##

如Github, Gitlab等可以在页面上设置某个用户的权限. 不过有时为了防止出问题, 在本地也可以设置.

其实就是简单的将remote url的push地址重写为任意字符串.

    $ git remote set-url --push origin 'do not push'


## 关于 HEAD^ 和 HEAD~ 的区别 ##

`HEAD^` 表示当前分支的第一个父分支的第一个点, 等同于 `HEAD^1`; `HEAD^2`表示第二个父分支的第一个点

`HEAD~1` 表示当前分支的第一个父分支的第一个点, 等同于 `HEAD~1`, 效果也等同于 `HEAD^`; `HEAD~2`表示第一个父分支的第二个点.

stackoverflow上这个[回答](http://stackoverflow.com/a/12527561/1276501)描述的很详细:

    G   H   I   J
     \ /     \ /
      D   E   F
       \  |  / \
        \ | /   |
         \|/    |
          B     C
           \   /
            \ /
             A
    A =      = A^0
    B = A^   = A^1     = A~1
    C = A^2  = A^2
    D = A^^  = A^1^1   = A~2
    E = B^2  = A^^2
    F = B^3  = A^^3
    G = A^^^ = A^1^1^1 = A~3
    H = D^2  = B^^2    = A^^^2  = A~2^2
    I = F^   = B^3^    = A^^3^
    J = F^2  = B^3^2   = A^^3^2

其它讲解:

* [head where are we where were we](http://www.gitguys.com/topics/head-where-are-we-where-were-we/?lang=zh)


## 查看两个分支的差异 ##

遇到一个问题, 删除一个已合并分支时, 提示此分支没有完全合并:

> error: The branch 'xxx' is not fully merged

在so上发现一个给力的[回答](http://stackoverflow.com/a/7549118/1276501)

    $ git log --graph --left-right --cherry-pick --oneline master...experiment


## 查看某个commit在哪些release(tag)引进 ##

之前考虑的是知道某个commit, 这时就知道它的提交时间, 然后找出release/tag在它之后即可, 也就是:

	$ git log --tags --simplify-by-decoration --pretty="format:%ai %d"

然后根据commit的提交时间找到从那个tag开始有.

不过后来想了下, 这块有问题, 因为当前发布分支不一定merge了这个commit.

后来搜到git tag有这个功能`--contains`选项:

	$ git tag --contains <commit id>

延伸下: 如果查看哪些分支包含某个指定commit id:

	$ git branch --contains <commit id>

## Git subtree ##

对`submodule`的使用应该是非常熟悉了. 听过subtree这个东西有1、2年了, 一直没时间去了解, 前阵子简单了解过, 今晚又看了下文档和一些博客并尝试了(2015-11-11, 好吧, 双十一, 刚剁手完~~~), 也算大致有了一个了解认识.

首先说一下, 国内很多博客人云亦云, 都没什么实践场景, 就跟着别人说: submodule太复杂, 不好用, 应该用subtree. 这个是相当坑爹的.

然后放几个链接, 技术上就不详细说明:

* man git-subtree
* [git subtrees: a tutorial](https://medium.com/@v/git-subtrees-a-tutorial-6ff568381844) 很好的入门资料, 详细的例子
* [Alternatives To Git Submodule: Git Subtree](https://www.atlassian.com/git/articles/alternatives-to-git-submodule-git-subtree/)
* [Git submodule 还是 Git Subtree](http://blog.zlxstar.me/blog/2014/07/18/git-submodule-vs-git-subtree/) 评价还算中肯
* [使用GIT SUBTREE集成项目到子目录](http://aoxuis.me/post/2013-08-06-git-subtree) 里面提到的一些链接文章可以看看

简单说下使用(merge和split还没去尝试):

    git subtree add   -P <prefix> <repository> <ref>
    git subtree pull  -P <prefix> <repository> <ref>
    git subtree push  -P <prefix> <repository> <ref>

subtree add命令将一个项目拉到本地作为一个子目录, 这个和submodule类似. prefix执行子目录名.

子仓库独立更新, 主仓库使用subtree pull命令下拉作更新, 会产生一个merge commit

主仓库下子目录的仓库作了更新, 可以使用subtree push将修改推到子仓库

子仓库可以修改并提交, 这个提交是在主仓库历史可以直接git log看到的(不同于submodule)

因为每次都要敲repository, 可以把这个用git remote增加一个remote alias.

建议:

* subtree pull建议加上`--squash`, 将子仓库的多个提交合并为一个提交merge到主仓库, 否则会增加一堆commit.
* 主仓库的修改和子仓库的修改分开提交, 主库和子库互相pull/push时会比较混乱

实例:

* [Deploying a subfolder to GitHub Pages](https://gist.github.com/cobyism/4730490) Jekyll可以用到的一个例子.

感受:

* 至少目前来说, 我还是喜欢submodule
* 说submodule麻烦是因为不了解, 有人说需要.gitmodule配置文件, 我觉得这个的优点之一就是简化文件, 不然每次都要敲prefix, repository很麻烦不是?
* subtree导致历史看起来比较脏, 对于submodule, 主库一个逻辑提交可以直接包含子库的相应commit id即可
* subtree对于一些小项目比较合适
* subtree依赖使用团队的规范约束, 否则历史容易乱.

当然, 上面也只是我了解一些皮毛的感受, 希望后续有机会能更多的去实践.

另外, submodule的教程:

* [Git Submodule使用完整教程](http://www.kafeitu.me/git/2012/03/27/git-submodule.html)


## git diff 相关 ##

关于 `git diff A..B` 和 `git diff A...B`:

![git diff help](http://tankywoo-wb.b0.upaiyun.com/git-diff-help.png) [图片来源](http://stackoverflow.com/questions/7251477/what-are-the-differences-between-double-dot-and-triple-dot-in-git-dif)

参考:

* [What are the differences between double-dot “..” and triple-dot “…” in Git diff commit ranges?](http://stackoverflow.com/questions/7251477/what-are-the-differences-between-double-dot-and-triple-dot-in-git-dif)
* [git diff doesn't show enough](http://stackoverflow.com/questions/5256249/git-diff-doesnt-show-enough/5257065#5257065)
* [What are the differences between double-dot “..” and triple-dot “…” in Git commit ranges?](http://stackoverflow.com/questions/462974/what-are-the-differences-between-double-dot-and-triple-dot-in-git-com)


## Git资料 ##

* [ProGit中文版](http://git-scm.com/book/zh)
* [Git Reference](http://gitref.org/)
