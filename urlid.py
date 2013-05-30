#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wutq@2013-05-30

# TODO 暂时还没想好怎么做, 先放着

"""作用
* 读取wiki的uuid配置文件
* 如果url没有在配置文件中，则通过此代码生成
* 把uuid链接放置一份在相应目录，nginx做好配置
"""

from os import path as osp
import uuid

def gen_uuid(url):
    return uuid.uuid3(uuid.NAMESPACE_URL, url)

if __name__ == '__main__':
    cur_dir = osp.dirname(osp.realpath(__file__))
    wiki_dir = osp.join(cur_dir, 'tkwiki')
