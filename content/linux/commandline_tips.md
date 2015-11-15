---
title: "CommandLine Tips"
date: 2015-02-09 15:00
---

`git rebase` 保持合并的分支和时间:

	git rebase -p --ignore-date -i $COMMIT_ID

[ref 1](http://stackoverflow.com/questions/10016707/git-rebase-branch-with-merged-children)
[ref 2](http://stackoverflow.com/questions/2973996/git-rebase-without-changing-commit-timestamps)

---

本地构建pip install的开发环境:

开发python package, 为了模拟pip install后的环境, 可以在开发过程中随时测试, 不需要手动构建软链接，使用:

	pip install -e $PACKAGE/

会在python package目录下新建一个`*.egg-link`文件, 文件内容是包的路径.

[ref 1](http://stackoverflow.com/questions/7926060/python-package-install-using-pip-to-source-doesnt-create-a-symlink)
[ref 2](https://docs.djangoproject.com/en/1.7/topics/install/)

---

重命名Git分支(Rename Git Branch):

本地分支(local branch):

    git branch -m <oldname> <newname>

如果要重命名当前分支, 直接:

    git branch -m <newname>

[ref 1](http://stackoverflow.com/questions/6591213/rename-local-git-branch)

远程分支(remote branch):

没有一个直接的方法可以重命名远程分支, 需要先删除远程分支, 然后本地将重命名后的分支推送到远程:

    git push origin :<oldname>
    git push -u origin <newname>

[ref 1](http://blog.changecong.com/2012/10/rename-a-remote-branch-on-github/)
[ref 2](http://www.benjaminlhaas.com/blog/locally-and-remotely-renaming-branch-git)
[ref 3](http://stackoverflow.com/questions/1526794/rename-master-branch-for-both-local-and-remote-git-repositories)

---

git stash相关

stash时包含untracked files(默认只有stage和index中的files):

	git stash [--include-untracked|-u]

stash pop后, 原先index中的files会恢复为staged, 如果要保持index, 则:

	git stash [--keep-index|-k]

---

同时修改 author 和 committer

比如提交后发现author和committer都错了.

如果只是:

	git commit --amend --author="username <useremail>"

则只修改 author 信息, 如果要同时修改author和committer信息则:

	git -c user.name="New Author Name" -c user.email=email@address.com commit --amend --reset-author

如果修改了 `~/.gitconfig` 则可以直接:

	git commit --amend --reset-author

[ref](http://stackoverflow.com/a/1320317/1276501)

---

统计所有提交的用户及提交次数:

	git shortlog -sn

也可以加上相应的email:

	git shortlog -sne

[ref](http://blog.vogella.com/2013/02/26/git-how-to-determine-the-committers-or-authors-in-a-git-repository-by-lars-vogel/)

---

查看某次提交的author/committer:

	git --no-pager show -s --format='author: %an <%ae> \ committer: %cn <%ce>' <commit_id>

`--no-pager` 这个参数很赞！

[ref](http://www.quora.com/Whats-the-simplest-git-command-to-get-a-commits-author-and-their-email-address-if-available)

---

快速将一个cpu打满:

    dd if=/dev/zero of=/dev/null

或:

    yes > /dev/null

其它可见[参考](http://stackoverflow.com/questions/2925606/how-to-create-a-cpu-spike-with-a-bash-command)

---

进制间转换:

    # 十六进制 转 十进制
    # 注意字母要 **大写**
    $ echo 'ibase=16; FF' | bc
    255

    # 十进制 转 十六进制
    $ echo 'obase=16; 32' | bc
    20

    # 十六进制 转 二进制
    $ echo 'ibase=16; obase=2; F' | bc
    1111

    # 使用printf, 十六进制 转 十进制
    $ printf "%d\n" 0xff
    255

参考 [ref1](http://www.cyberciti.biz/faq/linux-unix-convert-hex-to-decimal-number/), [ref2](http://www.linuxnix.com/2012/05/convert-binaryhex-oct-decimal-linuxunix.html)

---

`du` human-readable output by size:

    du -h | sort -h
    du --human-readable | sort --human-numeric-sort

参考 [ref1](http://www.cyberciti.biz/faq/how-do-i-sort-du-h-output-by-size-under-linux/)
