<!-- title : git -->

# Git #

**NOTE**: git的`help`信息非常好，很多可以直接help来了解

## 给git输出信息增加颜色 ##

编辑`/etc/gitconfig`
比如要对git status设置颜色，可以:

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

因为git是保存的快照，Git仓库有以下几个基本对象

* `blob` 对象用于表示文件快照内容
* `tree` 对象记录目录树内容和各个文件对应的blob对象索引
* `commit` 对象记录提交信息，指向tree对象或其他commit对象

Git的分支，其本质是一个指向commit对象的可变`指针`，git使用`master`作为分支的默认名字

`HEAD`指针指向当前的分支指针

使用`git branch`是查看当前的分支列表

使用`git branch branch_name`新建分支，然后可以使用`git checkout branch_name`切换分支

最后可以用`git merge branch_name`来合并分支

如果遇到冲突，需要到冲突的文件下根据提示编辑后再commit

## 远程分支 ##

参考的 [远程分支](http://git-scm.com/book/zh/Git-%E5%88%86%E6%94%AF-%E8%BF%9C%E7%A8%8B%E5%88%86%E6%94%AF)

从远程git repo克隆，Git会自动将此remote repo命名为`origin`，并下载其中所有的数据，建立一个指向它的`master`分支的指针，在本地命名为`origin/master`

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


## Git 全局配置 ##

全局忽略文件

* [忽略文件](http://git-scm.com/book/zh/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-%E9%85%8D%E7%BD%AE-Git)
* [git ignore repo](https://github.com/GitHub/gitignore)

## 使用vimdiff ##

默认的diff应该是使用diff命令, 这个命令也非常有必要掌握.

但是, 更直观的, 可以选择vimdiff.

	# 配置git使用vimdiff来做差异比较
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

![git vimdiff](http://wutianqi-wiki.b0.upaiyun.com/git_vimdiff.png)

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
[2013-07-25] 更新:

最近遇到同步文件下来, 中文文件名全部是unicode, 解决这个问题加配置:

	git config --global core.quotepath false

## git mv 日志问题 ##
[2013-08-17] 更新:

在 `git mv` (rename) 文件后, 直接 git log 只能看到这个文件被 rename 后的日志, 想要看到完整的日志, 要用 `git log --follow xxx`

参考:
* [Is it possible to move/rename files in git and maintain their history?](http://stackoverflow.com/questions/2314652/is-it-possible-to-move-rename-files-in-git-and-maintain-their-history)
* [What's the purpose of git-mv?](http://stackoverflow.com/questions/1094269/whats-the-purpose-of-git-mv)

## 指定路径pull ##
[2013-09-03] 更新:

以前都是 cd 到仓库当前目录然后 pull. 因为想到 `svn up` 可以直接指定路径, 这种基本功能 git 肯定会有的, 但是直接指定路径不行.

搜了下, StackOverflow 上的 [回答1](http://stackoverflow.com/a/9876901/1276501) 和 [回答2](http://stackoverflow.com/a/9746005/1276501) 非常给力.

git 的参数 `--git-dir` 可以指定 git 的路径, 即使用这个 `.git` 的配置等来更新 repo. 但是这个会以 `pwd` 为要更新的 repo 路径.
所以还需要 `--work-tree` 来指定要更新的 repo 的路径, 而不需要 cd 过去.

```bash
git --git-dir=/path/to/git-repo/.git --work-tree=/path/to/git-repo/ pull
```

# 查看指定目录下的 status #

	git status [path]

比如当前目录下的 status:

	git status .

[git status - is there a way to show changes only in a specific directory?](http://stackoverflow.com/questions/715321/git-status-is-there-a-way-to-show-changes-only-in-a-specific-directory)


## Github ##

### 关于对一个项目语言识别的问题 ###

最近发现, 我写的这个 [tkwiki](https://github.com/tankywoo/tkwiki) 程序, 其语言被识别为 CSS 和 Javascript.

这个有点闹心啊, 明明是用 Python 写的, 只是因为是一个 web 程序, 所以不可避免会有一些自定义或第三方的 CSS 和 JS.

Github 是用其项目 [Linguist](https://github.com/github/linguist) 来识别项目语言的, 按照项目中每个语言的代码量排序.

暂时还没找到方法可以解决这个问题.

参考:

* [Github Help - My repository is marked as the wrong language](https://help.github.com/articles/my-repository-is-marked-as-the-wrong-language)
* [How does github figure out a project's language?](http://stackoverflow.com/questions/5318580/how-does-github-figure-out-a-projects-language)

## Git资料 ##

* [ProGit中文版](http://git-scm.com/book/zh)
* [Git Reference](http://gitref.org/)

## 修改历史 ##

* 2013-02-07 : 创建
* 2013-06-04 : git使用vimdiff
* 2013-07-25 : 补充文件名是中文的问题
* 2013-08-17 : 补充 git mv 后日志的问题
* 2013-09-03 : 更新指定路径更新git方法
