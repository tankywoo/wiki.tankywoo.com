# Vim #

# 我的配置 #



# 快捷键 #
## Movement ##
`h`  - Move *left*
`j`  - Move *down*
`k`  - Move *up*
`l`  - Move *right*
`0`  - Move to *beginging* of line
`$`  - Move to *end* of line
`gg` - Move to *first* line of file
`G`  - Move to *last* line of file
`w`  - Move *forward* to next word
`b`  - Move *backward* to next word

## Search ##
`*`     - Search *forward* for word under cursor
`#`     - Search *backward* for word under curor
`/word` - Search *forward* for *word*. Support *RE*
`?word` - Search *backward* for *word*. Support *RE*
`n`     - Repeat the last `/` or `?` command  
`N`     - Repeat the last `/` or `?` command in opposite direction

## Deletion ##
`x`  - Delete character *forward*(under cursor), and remain in normal mode
`X`  - Delete character *backward*(before cursor), and remain in normal mode
`r`  - Replace single character under cursor, and remain in normal mode
`s`  - Delete single character under cursor, and *switch* to insert mode
`dw` - Delete a *word* forward
`db` - Delete a *word* backward
`dd` - Delete *entire* current line
`D`  - Delete until end of line

## Yank & Put ##
`y`   - Yank(copy)
`yy`  - Yank current line
`nyy` - Yank `n` lines form current line
`p`   - Put(paste) yanked text *below* current line
`P`   - Put(paste) yanked text *above* current line

## Insert Mode ##
`i` - Enter insert mode to the *left* of the cursor
`a` - Enter insert mode to the *right* of the cursor
`o` - Enter insert mode to the line *below* the current line
`O` - Enter insert mode to the line *above* the current line

## Visual Mode ##
`v`   - Enter visual mode, highlight characters
`V`   - Enter visual mode, highlight lines
`C-v` - Enter visual mode, highlight block

## Other ##
`u`   - Undo
`U`   - Undo all changes on current line
`C-r` - Redo


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

    :set spr
    :vert help xxx


## 逐个替换 ##

一般情况下

    :%s/old_str/new_str/g
    }}}
    是对old_str做全文替换，加上参数c可以逐个替换，这样可以对每一个再确认
    {{{
    :%s/old_str/new_str/gc


# 修改历史 #

最后修改: 2013-05-28
