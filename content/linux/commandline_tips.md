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
