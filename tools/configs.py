#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo @ 2013-08-20

""" This is the configuration file of wiki.
The `WIKI_NAME` can be set to any, and should rename the directory of markdown 
files.

"""

import sys
from os import path as osp

# This is the base directory of the wiki project
BASE_DIR = osp.dirname(osp.dirname(osp.realpath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# The markdown files's directory name
WIKI_NAME = "tkwiki"

# The directory to store markdown files
WIKI_PATH = osp.join(BASE_DIR, WIKI_NAME)

# The directory to store the generated html files
HTML_PATH = osp.join(BASE_DIR, "html/%s" % WIKI_NAME)

# The path of html template file
TPL_PATH = osp.join(BASE_DIR, "html/template/markdown.tpl")

# Allowed suffixes ( aka "extensions" )
SUFFIXES = {".md", ".mkd", ".markdown"}
