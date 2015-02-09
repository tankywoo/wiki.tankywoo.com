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
