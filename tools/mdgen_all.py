#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo @ 2013-08-15


""" This tool is used to convert all markdown files under `tkwiki` directory 
to html files.

You can :

    sudo ln -s /path/to/mdgen_all.py /usr/bin/mdgen_all

And simple use `mdgen_all` to generate all the html files.

TODO:
    * for loops optimize
    * fault tolerance
    * use the base config (the same as mdgen.py)
"""

from __future__ import print_function
import os
import sys
import fnmatch
from os import path as osp

import configs
from mdgen import generator

__author__  = "Tanky Woo <me@tankywoo.com>"
__version__ = "0.1"
__license__ = "MIT License"


if __name__ == "__main__":
    root_path = configs.WIKI_PATH
    patterns = ["*.md", "*.mkd", "*.markdown"]

    for root, dirs, files in os.walk(root_path):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                md_file = osp.join(root, filename)
                generator(md_file)
