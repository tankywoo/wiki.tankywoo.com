#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo @ 2013-08-20

import sys
from os import path as osp

BASE_DIR = osp.dirname(osp.dirname(osp.realpath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# GLOBAL CONFIG
WIKI_NAME = "tkwiki"
WIKI_PATH = osp.join(BASE_DIR, WIKI_NAME) # markdown wiki file
HTML_PATH = osp.join(BASE_DIR, "html/%s" % WIKI_NAME) # generrated html file
TPL_PATH = osp.join(BASE_DIR, "html/template/markdown.tpl") # html template
