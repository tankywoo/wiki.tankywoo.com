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
from os import path as osp

import configs
import comm
from mdgen import generator

if __name__ == "__main__":
    root_path = configs.WIKI_PATH

    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if comm.filter_suffix(filename):
                continue
            md_file = osp.join(root, filename)
            try:
                generator(md_file)
            except BaseException, e:
                print(str(e))
