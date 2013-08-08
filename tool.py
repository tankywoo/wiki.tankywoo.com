#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo@2013-06-23

""" Convert Markdown file to html, which is embeded in html template.

Requirement:

    * argparse : python 2.7.x include it by default
    * markdown2 : http://github.com/trentm/python-markdown2

Use this tool, please:

    sudo ln -s /path/to/tool.py /usr/bin/mdgen

Usage:

    mdgen -h

Directory Structure:

    .
    ├── articles.py
    ├── html
    │   ├── template
    │   └── tkwiki
    ├── tkwiki
    └── tool.py

"""

from __future__ import print_function

import sys
import re
import argparse
import markdown2

from os import path as osp

__author__  = 'Tanky Woo <me@tankywoo.com>'
__version__ = "1.0"
__license__ = "MIT License"

BASE_DIR = osp.dirname(osp.realpath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(BASE_DIR)

# CONFIGURATION
WIKI_NAME = "tkwiki"
DIR_WIKI = osp.join(BASE_DIR, WIKI_NAME) # markdown wiki file
DIR_HTML = osp.join(BASE_DIR, "html/%s" % WIKI_NAME) # generrated html file
DIR_TPL = osp.join(BASE_DIR, "html/template/markdown.tpl") # html template

def _check_md_file_exists(md_file):
    """Check if the md_file exists."""
    if not osp.exists(md_file):
        sys.exit("%s does not exists" % md_file)

def _check_suffix(md_file):
    """Check if the md_file's suffix is right.

    Supported markdown suffixes are .md, .mkd, .markdown. Do not use 
    other suffixes.
    """
    md_suffixes = ["md", "mkd", "markdown"]
    md_suffix = md_file.split(".")[-1]
    if md_suffix not in md_suffixes:
        sys.exit("markdown file's suffix is wrong!")

def _get_dir_and_md_name(md_file):
    """Get the subdir's name and markdown file's name"""
    dir_name = md_file.split("/")[-2] # html subdir
    md_name = md_file.split("/")[-1].split(".")[0]
    return (dir_name, md_name)

def _get_title(md_file):
    """Get the wiki's title.

    Established:
        The first line of wiki is the title, written in html comment syntax.
        such as:
            <!-- title : The wiki title -->
    """
    notations = {"left" : "<!--", "right" : "-->"}
    with open(md_file, "r") as fd:
        first_line = fd.readline().strip()
        if "title" not in first_line.lower():
            sys.exit("the wiki's first line must have `title` keyword")
        if not (first_line.startswith(notations["left"]) 
                and first_line.endswith(notations["right"])):
            sys.exit("the wiki's title syntax is wrong!")

        for notation in notations.values():
            first_line = first_line.replace(notation, "")
        first_line = first_line.strip()

        # strip the space between `title` and `:`
        first_line = first_line.split(":", 1)
        first_line[0] = first_line[0].strip().lower()
        first_line = ":".join(first_line)

        title = first_line.lstrip("title:").strip()

        return title

def _md2html(md_file):
    """Generate the html from md file, and embed it in html template"""
    content = markdown2.markdown_path(md_file)
    tpl = open(DIR_TPL, "r")
    tpl_html = "".join(tpl.readlines())
    html = re.sub("{{ content }}", content, unicode(tpl_html, "utf-8"))
    title = _get_title(md_file)
    html = re.sub("{{ title }}", unicode(title, "utf-8"), html)
    html = html.encode("utf-8")

    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", "--file", dest="md_file", required=True, 
            help="")
    parser.add_argument("--debug", dest="debug", action="store_true", 
            help="")
    parser.add_argument("--version", action="version", 
            version="%(prog)s " + __version__)

    parse_args = parser.parse_args()
    md_file = osp.realpath(parse_args.md_file)
    debug_mode = parse_args.debug

    _check_md_file_exists(md_file)

    _check_suffix(md_file)

    dir_name, md_name = _get_dir_and_md_name(md_file)

    html = _md2html(md_file)

    if debug_mode:
        print(html)
    else:
        html_path = osp.join(DIR_HTML, dir_name, md_name+".html")
        with open(html_path, "w") as wfd:
            wfd.write(html)
