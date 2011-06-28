# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
'''
Created on Nov 10, 2010

@author: paul
'''

import os
import shutil
import sys


from storebase import *
from lib import utils
from lib import const
#    Do this last!
from lib.logger import Logger
log = Logger("io")


class FolderStore(StoreBase):
    def __init__(self, name="__dummy", limit="", auto_manage=False, root="/var/backups/store"):
        StoreBase.__init__(self, name, limit, auto_manage)

        if len(root) == 0:
            raise Exception(_("Root folder cannot be blank"))
        self.root = root

        self._persistent.append("root")

    def copy(self):
        '''
        Used by the persistence system to initialize a new FolderStore
        
        Returns a fully initialized duplicate of self.

        '''
        log.trace("Copy constructor")
        return FolderStore(self.name, self.limit, self.auto_manage, self.root)

    def __str__(self):
        return "%s: %s" % (self.name, self.root)
   
############################################################################
#
#    File-like functions.
#
#        Override: with a folder store, we can stream straight to the dest file
#
############################################################################

    def open(self, path, mode):
        if not self.connected:
            self.connect()
        self.make_dir(os.path.split(path)[0])
        self.io_path = utils.join_paths(self.root, path)
        if "w" in mode:
            self.io_state = ioWriting
            self.io_fd = open(self.io_path, "wb")
        else:
            self.io_state = ioReading
            self.io_fd = open(self.io_path, "rb")
        return self
    
    def close(self):
        self.io_fd.close()
        self.io_state = ioClosed 
########################################################
#
#    Core functions all take paths relative to root
#
########################################################
    def _connect(self):
        pass
    def _disconnect(self):
        pass
    def _send(self, src, dest):
        #    Switch to absolute path.
        rem_dest = utils.join_paths(self.root, dest)
        shutil.copyfile(src, rem_dest)
        return dest

    def _get(self, src, dest):
        src = utils.join_paths(self.root, src)
        shutil.copyfile(src, dest)
        return dest
    
    def _make_dir(self, folder):
        #    Make the folder. utils.makedirs wont fail if the folder exists.
        if folder in ["", ".", "/"]:
            folder = self.root
        else:
            folder = utils.join_paths(self.root, folder)
        utils.makedirs(folder)
        if not os.path.isdir(folder):
            raise Exception("Unable to build folder")


    def _remove_file(self, path):
        log.info("Removing file", path)
        path = utils.join_paths(self.root, path)
        if not os.path.isfile(path):
            raise Exception(_("Missing file"))
        os.remove(path)
        if os.path.isfile(path):
            raise Exception("Unable to delete file")

    def _remove_dir(self, path):
        log.info("Removing dir", path)
        if path in ["", "."]:
            path = self.root
        else:
            path = utils.join_paths(self.root, path)
        if not os.path.isdir(path):
            raise Exception("Missing folder")
        shutil.rmtree(path)
        if os.path.isdir(path):
            raise Exception("Unable to delete folder")

    def _list(self, dir):
        path = utils.join_paths(self.root, dir)
        return os.listdir(path)

    def _size(self, path):
        path = utils.join_paths(self.root, path)
        return os.path.getsize(path)
