<!-- title : vim -->

# Vim #

[.vimrc](https://github.com/tankywoo/linux-autoconfig/blob/master/.vimrc)


# 快捷键 #
## Movement ##
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

## Search ##
* `*`     - Search *forward* for word under cursor
* `#`     - Search *backward* for word under curor
* `/word` - Search *forward* for *word*. Support *RE*
* `?word` - Search *backward* for *word*. Support *RE*
* `n`     - Repeat the last `/` or `?` command  
* `N`     - Repeat the last `/` or `?` command in opposite direction

在搜索后, 被搜索的单词都会高亮, 一般想取消那些高亮的单词, 可以再次搜索随便输入一些字母, 搜索不到自然就取消了. 另外也可以使用 `nohl` 取消这些被高亮的词.

## Deletion ##
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


## Yank & Put ##
* `y`   - Yank(copy)
* `yy`  - Yank current line
* `nyy` - Yank `n` lines form current line
* `p`   - Put(paste) yanked text *below* current line
* `P`   - Put(paste) yanked text *above* current line

## Insert Mode ##
* `i` - Enter insert mode to the *left* of the cursor
* `a` - Enter insert mode to the *right* of the cursor
* `o` - Enter insert mode to the line *below* the current line
* `O` - Enter insert mode to the line *above* the current line

## Visual Mode ##
* `v`   - Enter visual mode, highlight characters
* `V`   - Enter visual mode, highlight lines
* `C-v` - Enter visual mode, highlight block

## Other ##
* `u`   - Undo
* `U`   - Undo all changes on current line
* `C-r` - Redo

## Read More ##

* [A handy guide to Vim shortcuts](http://eastcoastefx.vaesite.com/vim)
* [tuxfiles-vimcheat](http://www.tuxfiles.org/linuxhelp/vimcheat.html)
* [What is your most productive shortcut with Vim?](http://stackoverflow.com/questions/1218390/what-is-your-most-productive-shortcut-with-vim)


# 技巧 #

## shell多行注释 ##

命令行模式下，注释掉line1与line2之间的行

	line1,line2s/^/#/g


## 自动补全 ##

	Ctrl+n Ctrl+p
	Ctrl+x Ctrl+?{....}

## 左右分割打开help文档 ##

默认是上下分割来打开文档，但是对于宽屏，左右分割反而更加方便

	:vert help xxx


## 逐个替换 ##

全文直接替换:

	:%s/old_str/new_str/g

加上参数c可以逐个替换，这样可以对每一个再确认:

	:%s/old_str/new_str/gc



# 修改历史 #

* 2013-05-28 : 创建
* 2013-07-10 : 补充 匹配括号的移动, 前后位置的移动. 这两个都是非常实用的快捷键.
* 2013-07-12 : showcase时和同事分享了, 也给了我很多他们积累的技巧, 赞!
