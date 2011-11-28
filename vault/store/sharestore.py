# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Created on Nov 10, 2010

@author: paul

ShareStore - for general purpose mounting.

Simply passed a mount/umount command to run.
That command MUST return 0 for success
'''


from folderstore import FolderStore
from subprocess import Popen, PIPE
#    Do this last!
from lib.logger import Logger
log = Logger("io")



class ShareStore(FolderStore):
    def __init__(self, name="__dummy__", limit="", auto_manage=False, 
                 root="/var/backups/store", mount="", umount=""):
        FolderStore.__init__(self, name, limit, auto_manage, root)
        self.mount = mount
        self.umount = umount
        for attr in ["mount", "umount"]:
            self._persistent.append(attr)

    def copy(self):
        '''
        Used by the persistence system to initialize a new FolderStore
        
        Returns a fully initialized duplicate of self.

        '''
        log.trace("Copy constructor")
        return ShareStore(self.name, self.limit, self.auto_manage, self.root, self.mount, self.umount)

    def __str__(self):
        return "SHARE: (%s, %s)" % (self.name, self.root)

    def _connect(self):
        proc = Popen(self.mount, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = proc.communicate()
        ret = proc.returncode
        if ret != 0:
            raise Exception("Mount command failed: %s" % err) 
            
    def _disconnect(self):
        proc = Popen(self.umount, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = proc.communicate()
        ret = proc.returncode
        if ret != 0:
            raise Exception("Unmount command failed: %s" % err)

    def _remove_dir(self, path):
        log.info("Share Removing dir", path)
        if path in ["", "."]:
            #    Can't remove the root folder here...
            items = self.list(path)
            for item in items:
                try:
                    self.remove_file(item)
                except:
                    self.remove_dir(item)
        else:
            FolderStore._remove_dir(self, path)
