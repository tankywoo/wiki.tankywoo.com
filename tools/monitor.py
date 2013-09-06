#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo @ 2013-08-18

import sys
import logging
from os import path as osp

import pyinotify

import configs
import comm
from mdgen import generator


SUFFIXES = {".md", ".mkd", ".markdown"}
LOG_FILE = "/var/log/wiki_monitor.log"

def filter_event(event):
    """
    This will also filter the new directory

    Ref: http://stackoverflow.com/a/18308871/1276501
    """
    # return True to stop processing of event (to "stop chaining")
    return osp.splitext(event.name)[1] not in SUFFIXES

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self):
        comm.print_ok("Starting wiki monitor daemon...")
        FORMAT = ("%(asctime)s %(levelname)8s "
        "%(funcName)s(%(filename)s:%(lineno)s) : %(message)s")
        logging.basicConfig(
                level=logging.INFO, 
                filename=LOG_FILE, 
                format=FORMAT)
        logging.info("Starting wiki monitor...")

    def _generate(self, event):
        try:
            generator(event.pathname)
            logging.info("Svn up: %s" % event.pathname)
        except BaseException, e:
            logging.error("Svn up: %s. %s" % (event.pathname, str(e)))

    def process_IN_CREATE(self, event):
        """Do nothing. If open a new file and edit, it will trigger CREATE and 
        MODIFY event, only need to treat the MODIFY event.  If the event is a 
        mkdir, then the filter will ignore.
        """
        logging.info("Creating: %s" % event.pathname)

    def process_IN_DELETE(self, event):
        """
        TODO:
            If delete a .md file, it should auto delete the corresponding html 
            file, and update the directory's html file.
        """
        logging.info("Removing: %s" % event.pathname)

    def process_IN_MODIFY(self, event):
        """When the .md file is modified, update the corresponging html.
        """
        self._generate(event)

    def process_IN_MOVED_TO(self, event):
        """For `svn up`.
        """
        self._generate(event)

    def process_default(self, event):
        logging.info("Default: %s" % event.pathname)


def monitor(path):
    mask = pyinotify.IN_DELETE | \
           pyinotify.IN_CREATE | \
           pyinotify.IN_MODIFY | \
           pyinotify.IN_MOVED_TO # watched events

    # The watch manager stores the watches and provides operations on watches
    wm = pyinotify.WatchManager()
    wm.add_watch(path, mask, rec=True, auto_add=True)

    # Internally, 'handler' is a callable object which on new events will 
    # be called like this: handler(new_event)
    handler = EventHandler(pevent=filter_event)
    notifier = pyinotify.Notifier(wm, handler)

    notifier.loop()


if __name__ == "__main__":
    monitor(configs.WIKI_PATH)
