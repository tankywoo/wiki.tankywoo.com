---
title: "Vim"
date: 2013-08-17 07:32
updated: 2016-12-23 11:10
collection: "编辑器"
tag: vim
log: "插入特殊字符"
---

[TOC]

配置见[dotfiles](https://github.com/tankywoo/dotfiles)


## 快捷键 ##

### Movement ###
* `h`  - Move *left*
* `j`  - Move *down*
* `k`  - Move *up*
* `l`  - Move *right*
* `0`  - Move to *beginging* of line, 也可以使用 `Home`.
* `^`  - 在有tab或space的代码行里, `0`是移到最行首, 而`^`是移到代码行首
* `$`  - Move to *end* of line
* `gg` - Move to *first* line of file
* `G`  - Move to *last* line of file
* `ngg`- 移动到指定的第n行, 也可以用`nG`
* `w`  - Move *forward* to next word
* `b`  - Move *backward* to next word
* `%`  - 在匹配的括号、块的首尾移动
* `C-o`- 返回到上次移动前的位置, 也可以用两个单引号`'`
* `C-i`- 前进到后一次移动的位置
* `f`  - 后接字符，移动到当前行的下一个指定字符，然后按`;`继续搜索下一个
* `F`  - 同上，移动到上一个
* `|`  - 竖线，前接数字，移动到当前行的指定列，如`30|`，移动到当前行的第30列

### Search ###
* `*`     - Search *forward* for word under cursor
* `#`     - Search *backward* for word under curor
* `/word` - Search *forward* for *word*. Support *RE*
* `?word` - Search *backward* for *word*. Support *RE*
* `n`     - Repeat the last `/` or `?` command  
* `N`     - Repeat the last `/` or `?` command in opposite direction

在搜索后, 被搜索的单词都会高亮, 一般想取消那些高亮的单词, 可以再次搜索随便输入一些字母, 搜索不到自然就取消了. 另外也可以使用 `nohl` 取消这些被高亮的词.

### Deletion ###
* `x`  - Delete character *forward*(under cursor), and remain in normal mode
* `X`  - Delete character *backward*(before cursor), and remain in normal mode
* `r`  - Replace single character under cursor, and remain in normal mode
* `s`  - Delete single character under cursor, and *switch* to insert mode
* `shift+~` - 这个可以把光标下的单词转换为大写/小写, 并自动移到下一个字符
* `dw` - Delete a *word* forward
* `daw`- 上面的`dw`是删除一个单词的前向部分, 而这个是删除整个单词, 不论cursor是否在单词中间
* `db` - Delete a *word* backward
* `dd` - Delete *entire* current line
* `D`  - Delete until end of line


### Yank & Put ###
* `y`   - Yank(copy)
* `yy`  - Yank current line
* `nyy` - Yank `n` lines form current line
* `p`   - Put(paste) yanked text *below* current line
* `P`   - Put(paste) yanked text *above* current line

### Insert Mode ###
* `i` - Enter insert mode to the *left* of the cursor
* `a` - Enter insert mode to the *right* of the cursor
* `o` - Enter insert mode to the line *below* the current line
* `O` - Enter insert mode to the line *above* the current line

### Visual Mode ###
* `v`   - Enter visual mode, highlight characters
* `V`   - Enter visual mode, highlight lines
* `C-v` - Enter visual mode, highlight block

### Other ###
* `u`   - Undo
* `U`   - Undo all changes on current line
* `C-r` - Redo

### Read More ###

* [A handy guide to Vim shortcuts](http://eastcoastefx.vaesite.com/vim)
* [tuxfiles-vimcheat](http://www.tuxfiles.org/linuxhelp/vimcheat.html)
* [What is your most productive shortcut with Vim?](http://stackoverflow.com/questions/1218390/what-is-your-most-productive-shortcut-with-vim)

## Vim自定义插件 ##

依葫芦画瓢, 写了一个针对特定格式的高亮插件时的需求。

* [Writing Vim Syntax Plugins](https://robots.thoughtbot.com/writing-vim-syntax-plugins) \*
* [Vim zh-cn:插件](https://swaroop.wordpress.com/notes/vim_zh-cn-%E6%8F%92%E4%BB%B6/) \*
* [vim doc - syntax](http://vimcdoc.sourceforge.net/doc/syntax.html#:syn-cluster)
* [Writing Vim Plugins](http://stevelosh.com/blog/2011/09/writing-vim-plugins/)


## vimdiff ##

vim套件中的对比工具

* `]c` - 跳到下一个差异点
* `[c` - 上一个差异点
* `dp` - diff put, 将差异点的内容从当前文件复制到另一文件
* `do` - diff get, 相反，从另一文件复制到当前文件]


## 其它版本 ##

* [neovim](https://neovim.io/) 号称是重构了vim，速度变快？暂时没感觉出和传统vim的区别
* [macvim](https://github.com/macvim-dev/macvim) 试了下，还不错，可以替换本地一直作为记事本的TextMate了

	使用brew安装上macvim后， 终端使用`mvim`打开App， 但是按任何键都没有反应。需要把当前shell退出，重新打开才行。这个[issue](https://github.com/macvim-dev/macvim/issues/109)可以参考下。(折腾了我半天。。。)


## 技巧 ##

### shell多行注释 ###

命令行模式下，注释掉line1与line2之间的行

	line1,line2s/^/#/g


### 自动补全 ###

目前使用[jedi-vim](https://github.com/davidhalter/jedi-vim)插件, 可以配合[Supertab](https://github.com/ervandew/supertab)。

有什么omni(智能补全?), 自动补全啥的, 没去研究.

* [Are there any autocompletion plugins for vim?](http://superuser.com/a/841048/251495)
* [Vim autocomplete for Python](http://stackoverflow.com/questions/7138039/vim-autocomplete-for-python)
* [Is it possible to have vim auto-complete function names, variables, etc. when using it to program?](http://vi.stackexchange.com/questions/39/is-it-possible-to-have-vim-auto-complete-function-names-variables-etc-when-us)
* [vi/vim使用进阶: 智能补全](http://easwy.com/blog/archives/advanced-vim-skills-omin-complete/)
* [vi/vim使用进阶: 自动补全](http://easwy.com/blog/archives/advanced-vim-skills-auto-complete/)
* [VIM的JavaScript补全](http://efe.baidu.com/blog/vim-javascript-completion/) 介绍了ins-completion的几个快捷键


### 左右分割打开help文档 ###

默认是上下分割来打开文档，但是对于宽屏，左右分割反而更加方便

	:vert help xxx


### 逐个替换 ###

全文直接替换:

	:%s/old_str/new_str/g

加上参数c可以逐个替换，这样可以对每一个再确认:

	:%s/old_str/new_str/gc


### 关于 search/replace 中的换行符 ###

Search:

`\n` is `newline`, `\r` is `CR`(carriage return = Ctrl-M = ^M)

Replace:

`\r` is newline, `\n` is a null byte(0x00)

比如字符串 test1,test2,test3 把逗号换成换行：

	%s/,/\r/g


### 关于.vimrc和plugin的加载 ###

具体见`:help --noplugin`:

	--noplugin      Skip loading plugins.  Resets the 'loadplugins' option.
					{not in Vi}
					Note that the |-u| argument may also disable loading plugins:
							argument        load vimrc files        load plugins
							(nothing)               yes                 yes
							-u NONE                 no                  no
							-u NORC                 no                  yes
							--noplugin              yes                 no

重新加载配置：

	# % 表示当前文件, so是source简写
	:so %

	# 指定配置文件
	:so ~/.vimrc

### 删除所有匹配的行 ###

	# 删除所有包含abcd的行
	:g/abcd/d

参考: [Delete all lines containing a pattern](http://vim.wikia.com/wiki/Delete_all_lines_containing_a_pattern)

### vim调试插件 ###

在使用dash.vim时遇到的一个问题, 想看看插件中某些变量的值是多少。搜到这篇文章：[Echoing Messages](http://learnvimscriptthehardway.stevelosh.com/chapters/01.html)

比如在插件里加上：

	echom var_name

然后在触发到这条后, 可以执行下面来查看输出

	:messages


### 忽略大小写搜索

首先有两个bool开关:

* `ignorecase` 忽略大小写
* `smartcase` 智能选择匹配, 如果搜索pattern是全小写，则忽略大小写匹配；如果pattern包含大写，则会精准匹配

另外，`\c`, `\C`可以覆盖`ignorecase`和`smartcase`的配置。

`\c`表示搜索pattern忽略大小写，如下都会忽略大小写匹配`hello`：

	# 最前的`/`表示vi中的开始搜索
	/\chello
	/\cHello
	/hello\c
	/HELLO\c

`\C`和`\c`相关，表示大小写敏感。

具体可以：

	:help /\c
	:help /\C
	:help smartcase
	:help ignorecase

参考 [How to do case insensitive search in Vim](http://stackoverflow.com/questions/2287440/how-to-do-case-insensitive-search-in-vim)

### 查看某个按键的映射

一般用于排查按键冲突，可以看某个按键实际被谁绑定了。

以tab为例，本地被supertab插件绑定了：

	:verbose imap <tab>
	i  <Tab>         <Plug>SuperTabForward
		Last set from ~/.vim/bundle/supertab/plugin/supertab.vim

[参考](https://github.com/ervandew/supertab)

### 查看加载的文件

	:scriptnames

### 快速跳回到上次位置

`''`或者<code>``</code>

具体见：[Move cursor to its last position](http://stackoverflow.com/questions/5052079/move-cursor-to-its-last-position)

### 插入特殊字符

最近看Go的字符串编码那块, 想在vim上敲一些特殊字符, 但是不知道怎么弄, 只能在网上找到这个字符, 然后C-v复制到vim里, 但是不行, 于是研究了下这块。

`:digraphs`可以看到支持的特殊字符列表, 比如`u: ü  252`, vim定义了**两个字符**的组合(即digraph)来映射特殊字符, 如这里使用`u:`来表示`ü`; 第三个252表示赋予它的十进制编码.

其中有两种方式来键入特殊字符(`:h digraphs-use`):

1. `CTRL-K {char1} {char2}`  # 任何模式都行
2. `{char1} <BS> {char2}`    # 只支持在digraph模式下,即`:set digraph`

第二种方式还有点疑问, 貌似只能在命令行模式里输入

光标在字符上, 普通模式敲入`ga`, 可以查看这个字符(包括特殊字符)的十进制,十六进制等: `<ü> 252, Hex 00fc, Octal 374`

还可以通过敲入16进制符来输出特殊字符, `<C-v>uXXXX`; 比如上面这个十六进制是00fc, 插入模式输入 `<C-v>u00fc`

其它参考:

* [Vim: enter Unicode characters with 8-digit hex code](http://stackoverflow.com/questions/9119649/vim-enter-unicode-characters-with-8-digit-hex-code)
* [Vim digraphs](http://ricostacruz.com/cheatsheets/vim-digraphs.html) 里面列了一些比较有趣的字符
* [chrisbra/unicode.vim](https://github.com/chrisbra/unicode.vim) 针对unicode字符加强功能的插件

---

## 参考:

* [How to replace a character for a newline in Vim?](http://stackoverflow.com/questions/71323/how-to-replace-a-character-for-a-newline-in-vim)
* [Why is \r a newline for Vim?](http://stackoverflow.com/questions/71417/why-is-r-a-newline-for-vim)
* [How can I add a string to the end of each line in Vim?](http://stackoverflow.com/questions/594448/how-can-i-add-a-string-to-the-end-of-each-line-in-vim)
* [VIM参考手册](http://vimcdoc.sourceforge.net/doc/)
