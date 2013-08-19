#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo @ 2013-08-18

# TODO:
# filter
# daemon
# logging | pyinotify log
# configable

import sys
from time import sleep
import fnmatch
import pyinotify

def suffix_filter(fn):
    suffixes = ["*.md", "*.mkd", "*.markdown"]
    for suffix in suffixes:
        if fnmatch.fnmatch(fn, suffix):
            return False
    return True 

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        if not suffix_filter(event.name):
            print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

    def process_IN_MODIFY(self, event):
        print "Modifing:", event.pathname

    def process_default(self, event):
        print "Default:", event.pathname

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

def monitor():
    mask = pyinotify.IN_DELETE | \
           pyinotify.IN_CREATE | \
           pyinotify.IN_MODIFY  # watched events

    # The watch manager stores the watches and provides operations on watches
    wm = pyinotify.WatchManager()
    wm.add_watch('/tmp', mask, rec=True, auto_add=True)

    # Internally, 'handler' is a callable object which on new events will 
    # be called like this: handler(new_event)
    handler = EventHandler()
    notifier = SleepNotifier(wm, handler)

    notifier.loop()


if __name__ == "__main__":
    monitor()
