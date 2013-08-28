#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo@2013-06-23

""" Convert Markdown file to html, which is embeded in html template.

Requirement:

    * argparse : python 2.7.x include it by default
    * Python-Markdown : https://github.com/waylan/Python-Markdown

Use this tool, please:

    sudo ln -s /path/to/mdgen.py /usr/bin/mdgen

Usage:

    mdgen -h

Directory Structure:

    .
    ├── articles.py
    ├── html
    │   ├── template
    │   └── tkwiki
    ├── tkwiki
    └── mdgen.py

"""

from __future__ import print_function

import os
import sys
import re
import argparse
import markdown

from os import path as osp

import configs
import comm

__author__  = 'Tanky Woo <me@tankywoo.com>'
__version__ = "2.0"
__license__ = "MIT License"


def _check_path_exists(path):
    """Check if the path(include file and directory) exists."""
    if not osp.exists(path):
        return False
    return True

def _check_suffix(md_file):
    """Check if the md_file's suffix is right.

    Supported markdown suffixes are .md, .mkd, .markdown. Do not use 
    other suffixes.
    """
    md_suffixes = ["md", "mkd", "markdown"]
    md_suffix = md_file.split(".")[-1]
    if md_suffix not in md_suffixes:
        _, md_name = _get_dir_and_md_name(md_file)
        sys.exit(comm.color_error("[%s] suffix is wrong!" % md_name))

def _get_dir_and_md_name(md_file):
    """Get the subdir's name and markdown file's name."""
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
    _, md_name = _get_dir_and_md_name(md_file)
    with open(md_file, "rb") as fd:
        first_line = fd.readline().strip()
        if "title" not in first_line.lower():
            sys.exit(comm.color_error(
                "[%s] first line must have `title` keyword" % md_name))
        if not (first_line.startswith(notations["left"]) 
                and first_line.endswith(notations["right"])):
            sys.exit(comm.color_error("[%s] title syntax is wrong!" % md_name))

        for notation in notations.values():
            first_line = first_line.replace(notation, "")
        first_line = first_line.strip()

        # strip the space between `title` and `:`
        first_line = first_line.split(":", 1)
        first_line[0] = first_line[0].strip().lower()
        first_line = ":".join(first_line)

        title = first_line.lstrip("title:").strip()

        return title

def _md2html(md_file, title):
    """Generate the html from md file, and embed it in html template."""
    md_file_text = "".join(open(md_file, "rb").readlines())
    content = markdown.markdown(md_file_text, \
            extensions=["fenced_code", "codehilite(guess_lang=False)"])
    tpl = open(configs.TPL_PATH, "rb")
    tpl_html = "".join(tpl.readlines())
    html = re.sub("{{ content }}", content, unicode(tpl_html, "utf-8"))
    html = re.sub("{{ title }}", unicode(title, "utf-8"), html)
    html = html.encode("utf-8")

    return html

def _update_dir_page(dir_name, md_name, title):
    """The dir_page is directory page to list the wiki(html)'s link.

    A <li> label's syntax is:

        <li><a href="../`dir_name`/`md_name`.html">`title`</a></li>

    Insert the new <li>..</li> in the first line of the <li> lists. Make sure 
    the top wiki is the newest.

    TODO:
        * if there is blanklines between <li>, delete it.
        * if there is blanklinks out of <ul>..</ul>, delete it.
    """
    dir_page_file = osp.join(configs.HTML_PATH, dir_name+".html")

    # append mode will ignore seek
    if _check_path_exists(dir_page_file):
        file_mode = "rb+"
    else:
        file_mode = "wb+"

    with open(dir_page_file, file_mode) as fd:
        li_list = fd.readlines()[1:-1]  # ignore the <ul>..</ul> label
        new_li = "<li><a href=\"../%s/%s.html\">%s</a></li>" % \
                (dir_name, md_name, title)

        # if new_li exists, ignore; otherwise insert it in the first <li> list
        for li in li_list:
            if new_li in li:
                return
        fd.seek(0) # set current position to the beginning of the file
        li_list.insert(0, "\t%s\n"%new_li)
        new_content = "<ul>\n" + "".join(li_list) + "</ul>\n"
        fd.write(new_content)

def _update_wiki_page(dir_name, md_name, html):
    """Write the wiki html to file.

    If the parent directory not exists, mkdir it.
    """
    html_dir_path = osp.join(configs.HTML_PATH, dir_name)
    if not _check_path_exists(html_dir_path):
        os.mkdir(html_dir_path)
    html_path = osp.join(html_dir_path, md_name+".html")
    with open(html_path, "wb") as wfd:
        wfd.write(html)

def generator(md_file, debug_mode=False):
    if not _check_path_exists(md_file):
        _, md_name = _get_dir_and_md_name(md_file)
        sys.exit(comm.color_error("[%s] file does not exists" % md_name))
    _check_suffix(md_file)

    dir_name, md_name = _get_dir_and_md_name(md_file)
    title = _get_title(md_file)
    html = _md2html(md_file, title)

    if debug_mode:
        print(html)
    else:
        _update_wiki_page(dir_name, md_name, html)
        _update_dir_page(dir_name, md_name, title)
        comm.print_ok("[%s]" % md_name, " updated ok.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", "--file", dest="md_file", required=True, 
            help="The markdown file")
    parser.add_argument("--debug", dest="debug", action="store_true", 
            help="Display to stdout")
    parser.add_argument("--version", action="version", 
            version="%(prog)s " + __version__)

    parse_args = parser.parse_args()
    md_file = osp.realpath(parse_args.md_file)
    debug_mode = parse_args.debug

    generator(md_file, debug_mode)
