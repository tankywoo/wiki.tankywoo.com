#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo@2013-06-23

from __future__ import print_function

import sys
import re
import markdown2


# The global 
MDPATH = ''  # The path put markdown files
HTMLPATH = ''  # The path put the generated html files
TPLPATH = ''  # The template file path


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('>>ERROR: ', '')
        sys.exit(1)
    md_file = sys.argv[1]
    md_suffix = ['md', 'mkd', 'markdown']
    if md_file.split('.')[1] not in md_suffix:
        print('>>ERROR: ', '')
        sys.exit(1)

    html = markdown2.markdown_path('/tmp/tmux.markdown')
    tpl = open('markdown.tpl', 'r')
    tpl_html = ''.join(tpl.readlines())
    newhtml = re.sub('{{ content }}', html, unicode(tpl_html, 'utf-8'))
    newhtml = newhtml.encode('utf-8')
