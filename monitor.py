#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo @ 2013-08-18

# TODO:
# daemon
# configable

import sys
import logging
from time import sleep
from os import path as osp

import pyinotify

from mdgen import generator

BASE_DIR = osp.dirname(osp.realpath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(BASE_DIR)

# CONFIGURATION
WIKI_NAME = "tkwiki"
WIKI_PATH = osp.join(BASE_DIR, WIKI_NAME) # markdown wiki file

SUFFIXES = {".md", ".mkd", ".markdown"}

def filter_event(event):
    """
    This will also filter the new directory

    Ref: http://stackoverflow.com/a/18308871/1276501
    """
    # return True to stop processing of event (to "stop chaining")
    return osp.splitext(event.name)[1] not in SUFFIXES

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self):
        FORMAT = ("%(asctime)s %(levelname)8s "
        "%(funcName)s(%(filename)s:%(lineno)s) : %(message)s")
        logging.basicConfig(
                level=logging.INFO, 
                format=FORMAT)
        logging.info("Starting monitor...")

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
        try:
            generator(event.pathname)
            logging.info("Modifing: %s" % event.pathname)
        except BaseException, e:
            logging.error("Modifing: %s. %s" % (event.pathname, str(e)))

    def process_default(self, event):
        logging.info("Default: %s" % event.pathname)

class SleepNotifier(pyinotify.Notifier):
    def loop(self, callback=None, daemonize=False, **args):
        if daemonize:
            self.__daemonize(**args)

        # Read and process events forever
        while 1:
            try:
                self.process_events()
                if (callback is not None) and (callback(self) is True):
                    break
                # check_events is blocking
                if self.check_events():
                    # TODO what's the purpose of notifier._timeout?
                    sleep(3) # TODO
                    self.read_events()
            except KeyboardInterrupt:
                # Stop monitoring if sigint is caught (Control-C).
                # TODO
                break
        # Close internals
        self.stop()

def monitor(path):
    mask = pyinotify.IN_DELETE | \
           pyinotify.IN_CREATE | \
           pyinotify.IN_MODIFY  # watched events

    # The watch manager stores the watches and provides operations on watches
    wm = pyinotify.WatchManager()
    wm.add_watch(path, mask, rec=True, auto_add=True)

    # Internally, 'handler' is a callable object which on new events will 
    # be called like this: handler(new_event)
    handler = EventHandler(pevent=filter_event)
    notifier = SleepNotifier(wm, handler)

    notifier.loop()


if __name__ == "__main__":
    monitor(WIKI_PATH)
