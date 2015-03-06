#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import os.path
from sys import exit
import datetime
from fabric.api import env, local, run
from fabric.colors import blue, red
import fabric.contrib.project as project

# Remote host and username
env.hosts = ["192.81.133.96"]
env.user = "root"
env.colorize_errors = True

# Local output path
env.local_output = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "output/")
# Remote path to deploy output
env.remote_output = "/opt/wiki.tankywoo.com/output"

# Other options
env.rsync_delete = False

def update_simiki():
    print(blue("Old Version: "))
    run("simiki -V")
    run("pip install -U simiki")
    print(blue("New Version: "))
    run("simiki -V")

def deploy():
    if not env.remote_output:
        if env.rsync_delete:
            print(red("You can't enable env.rsync_delete option "
                "if env.remote_output is not set!!!"))
            print(blue("Exit"))
            exit()

        print(red("Warning: env.remote_output directory is not set!\n"
                    "This will cause some problems!!!"))
        ans = raw_input(red("Do you want to continue? (y/N) "))
        if ans != "y":
            print(blue("Exit"))
            exit()

    project.rsync_project(
        local_dir = env.local_output,
        remote_dir = env.remote_output.rstrip("/") + "/",
        delete = env.rsync_delete
    )

def g():
    local("simiki generate")

def p():
    local("simiki preview")

def gp():
    g()
    p()

def commit(commit_file=None, message=None):
    '''Auto commit tracked changes to git
    
    Usage:
        fab commit - commit all modified tracked files
        fab commit:[commit_file=]'file1 file2 fil3' - commit specified files
        fab commit:[commit_file=]'file1 file2 file3',[message=]'your commit message' - commit specified files with custom commit message
        fab commit:message='your commit message' - commit all modified tracked files with custom commit message
    '''
    if not message:
        message = 'Update {0}'.format(datetime.datetime.now()
                                      .strftime("%Y-%m-%d %H:%M:%S"))
    # add all tracked files
    # TODO change . to content/ ?
    if not commit_file:
        commit_file = '-u .'

    local("git add {0}".format(commit_file))
    local("git commit -m '{0}'".format(message))
