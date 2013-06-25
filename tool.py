#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo@2013-06-23

from __future__ import print_function

import sys
import re
import markdown2

from os import path as osp


# The global 
MDPATH = './tkwiki'  # The path put markdown files
HTMLPATH = './html/tkwiki'  # The path put the generated html files
TPLPATH = './html/template/markdown.tpl'  # The template file path


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('>>ERROR: ', 'Need a markdown file')
        sys.exit(1)
    _md = sys.argv[1]
    dir_name = _md.split('/')[-2]
    md_name = _md.split('/')[-1]
    md_suffix = ['md', 'mkd', 'markdown']
    if '.' not in md_name or md_name.split('.')[1] not in md_suffix:
        print('>>ERROR: ', 'Suffix is error')
        sys.exit(1)

    html = markdown2.markdown_path(_md)
    tpl = open(TPLPATH, 'r')
    tpl_html = ''.join(tpl.readlines())
    newhtml = re.sub('{{ content }}', html, unicode(tpl_html, 'utf-8'))
    newhtml = newhtml.encode('utf-8')
    html_path = osp.join(HTMLPATH, dir_name, md_name.split('.')[0]+'.html2')
    with open(html_path, 'w') as wfd:
        wfd.write(newhtml)
