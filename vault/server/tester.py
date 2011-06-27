# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import os
import shutil
from datetime import datetime
import time

from lib import const
from lib.config import Config
from lib.db import DB
from lib.backup import Backup
from server.run import Run
from server.restore import Restore
from lib import utils
from lib.dlg import Notify
from lib import sendemail
from store.folderstore import FolderStore

#    Do this last!
from lib.logger import Logger
log = Logger("server")

class BlankClass:
    pass

class Tester():
    def __init__(self, test_folder, options):

        self.test_folder = os.path.join(test_folder, "tester")
        self.options = options
        self.config = Config.get_config()

        self.store_folder = os.path.join(self.test_folder, "stores")
        self.files_folder = os.path.join(self.test_folder, "files")
        self.restore_folder = os.path.join(self.test_folder, "restore")

        self.db = DB()

        self.max_fs_id = self.db.query("select max(fs_id) from fs", ())[0][0]
        if self.max_fs_id is None:
            self.max_fs_id = 0
        self.max_version_id = self.db.query("select max(version_id) from versions", ())[0][0]
        if self.max_version_id is None:
            self.max_version_id = 0
        self.max_run_id = self.db.query("select max(run_id) from runs", ())[0][0]
        if self.max_run_id is None:
            self.max_run_id = 0
        self.max_message_id = self.db.query("select max(message_id) from messages", ())[0][0]
        if self.max_message_id is None:
            self.max_message_id = 0
        log.debug("MAX IDs", self.max_fs_id, self.max_version_id, self.max_run_id, self.max_message_id)

        self.teststring1 = os.urandom(204800)
        self.teststring2 = os.urandom(204800)


    def run(self):
        try:
            self.simpleCycleTest()
            self.restoreTest()
        except:
            pass
            
        if self.options.message:
            Notify(const.AppTitle, "Test run is complete")
        if self.options.email:
            self.send_email(True)
        if self.options.shutdown:
            os.system("shutdown -P +2")
        
        
    def simpleCycleTest(self):
        try:
            #   build the test files/folders
            self.make_folders()
            #    fill the files folder with the initial set of files
            self.fill_files()


            #    Build a backup and store
            self.build_config()

#            self.run_test()

            for i in xrange(int(self.options.cycles)):
                log.info("Cycle", i)
                #    Run a full and one incremental 
                self.run_cycle_test()

        except Exception as e:
            log.error("Test run failed: %s" % str(e))
        finally:
            self.cleanup()

        log.info("********Success")

    def restoreTest(self):
        try:
            #   build the test files/folders
            self.make_folders()
            #    fill the files folder with the initial set of files
            self.fill_files()
        except:
            pass

#    def build_config(self):
#        log.trace("build_config")
#        try:
#            if self.options.store:
#                store = self.config.storage[self.options.store]
#            else:
#                #    Make the store about 3x the options size
#                s, _, _ = utils.from_readable_form(self.options.size)
#                store_size = utils.readable_form(s * 3)
#                store = FolderStore("teststore1", store_size, True, os.path.join(self.store_folder, "teststore1"))
#                self.config.storage[store.name] = store
#    
#            backup = Backup("testbackup1")
#            backup.include_folders = [self.files_folder]
#            backup.store = store.name
#            backup.notify_msg = False
#            self.config.backups[backup.name] = backup
#
#
#            #    Run full backup
#            #    change some files
#            #    Run incremental backup
#            #    restore as at full date
#            #    restore as at incr date
#
#
#        except Exception as e:
#            log.error("Test run failed: %s" % str(e))
#        finally:
#            self.cleanup()

        log.info("********Success")
        

    def send_email(self, result, error_message=None):
        '''
        Send a message to the appropriate users.
        If result is False (failure) then error message will contain the reason.
        
        @param result:
        @param error_message:
        '''
        log.debug("send_email: ", result, error_message)
        if result:
            message_text = "Test to folder %s completed." % (self.test_folder)

            subject = "Test Completed"
        else:
            message_text = "Test FAILED\n\nERROR: %s" % (error_message)
            subject = "Test FAILED"

        log.debug("Starting mail send")
        try:
            sendemail.sendemail(subject, message_text)
        except Exception as e:
            self.db.save_message("Unable to email results: %s" % str(e))

        log.trace("send_email completed")

    def run_cycle_test(self):
        options = BlankClass()
        options.dry_run = False
        options.message = False
        options.email = False
        options.shutdown = False
        options.norecurse = False
        #    Run a full backup
        b = Run("testbackup1", const.FullBackup, options)
        b.run()
        #    Run a full backup
        b = Run("testbackup2", const.FullBackup, options)
        b.run()

        #    Now restore two files, one that will be on each store.
        restore_file1 = os.path.join(self.files_folder, "dir1", "f2.mp3")
        dest_file1 = os.path.join(self.restore_folder, restore_file1[1:])
        restore_file2 = os.path.join(self.files_folder, "dir2", "f3.exe")
        dest_file2 = os.path.join(self.restore_folder, restore_file2[1:])
        restore_file3 = os.path.join(self.files_folder, "dir3", "f4.txt")
        dest_file3 = os.path.join(self.restore_folder, restore_file3[1:])
        r = Restore(self.restore_folder, [restore_file1, restore_file2, restore_file3],
                                          datetime.now(), options)
        r.run()

        for path in [dest_file1, dest_file2, dest_file3]:
            if not os.path.exists(path):
                raise Exception("File %s was not restored" % path)
            if open(path).read() != self.teststring1:
                raise Exception("Restored file contents incorrect %s" % path)
            os.remove(path)

        #    Make sure the store is the right size
        for name in self.config.storage:
            store = self.config.storage[name].copy()
            size, used, avail = store.current_usage()
            log.debug("Store", store.name, "size", size, "used", used, "avail", avail)
            if store.auto_manage and used > size:
                raise Exception("Store %s has grown too large" % store.name)

        ######################PART 2

        #wait a little
        time.sleep(1.1)

        for path in [restore_file1, restore_file2, restore_file3]:
            #    Make a change
            with open(path, "w") as f:
                f.write(self.teststring2)

        #wait a little
        time.sleep(1.1)


        #    Run an incremental backup
        b = Run("testbackup1", const.IncrBackup, options)
        b.run()
        #    Run an incremental backup
        b = Run("testbackup2", const.IncrBackup, options)
        b.run()
        
        time.sleep(1.1)

        r = Restore(self.restore_folder, [restore_file1, restore_file2, restore_file3],
                                          datetime.now(), options)
        r.run()

        for path in [dest_file1, dest_file2, dest_file3]:
            if not os.path.exists(path):
                raise Exception("File %s was not restored after INCR %s" % path)
            if open(path).read() != self.teststring2:
                raise Exception("Restored file contents incorrect after INCR %s" % path)

#        raise Exception("Test Failure")

        #    Make sure the store is the right size
        for name in self.config.storage:
            store = self.config.storage[name].copy()
            size, used, avail = store.current_usage()
            log.debug("Store", store.name, "size", size, "used", used)
            if store.auto_manage and used > size:
                raise Exception("Store %s has grown too large" % store.name)

        time.sleep(1.1)


        #    change it back
        for path in [restore_file1, restore_file2, restore_file3]:
            with open(path, "w") as f:
                f.write(self.teststring1)

    def build_config(self):
        log.trace("build_config")
        #store1 = FTPStore("teststore1", "4MB", True, "localhost", "store1", "ftpuser", "ftpuserX9", False)
        #store2 = FTPStore("teststore2", "4MB", True, "localhost", "store2", "ftpuser", "ftpuserX9", False)
        if self.options.store:
            store1 = self.config.storage[self.options.store]
            store2 = store1
        else:
            #    Make the store about 3x the options size
            s, _, _ = utils.from_readable_form(self.options.size)
            store_size = utils.readable_form(s * 3)
            store1 = FolderStore("teststore1", store_size, True, os.path.join(self.store_folder, "teststore1"))
            store2 = FolderStore("teststore2", store_size, True, os.path.join(self.store_folder, "teststore2"))
            self.config.storage[store1.name] = store1
            self.config.storage[store2.name] = store2

        backup1 = Backup("testbackup1")
        backup1.include_folders = [self.files_folder]
        backup1.include_packages = True
        backup1.exclude_types = ["Music"]
        backup1.exclude_patterns = []
        backup1.store = store1.name
        backup1.notify_msg = False
        self.config.backups[backup1.name] = backup1

        backup2 = Backup("testbackup2")
        backup2.include_folders = [self.files_folder]
        backup2.include_packages = True
        backup2.exclude_patterns = []
        backup1.exclude_types = ["Videos", "Programs"]
        backup2.store = store2.name
        backup2.notify_msg = False
        self.config.backups[backup2.name] = backup2

    def fill_files(self, remaining=None, root=None):
        log.trace("fill_files")
        if not remaining:
            #    First time in...
            remaining, _, _ = utils.from_readable_form(self.options.size)
            root = self.files_folder
            
        list = [root]
        done = False
        while not done:
            newlist = []
            for folder in list:
                for dname in ["dir1", "dir2", "dir3"]:
                    path = os.path.join(folder, dname)
                    utils.makedirs(path)
                    newlist.append(path)
                for fname in ["f1.avi", "f2.mp3", "f3.exe", "f4.txt"]:
                    path = os.path.join(folder, fname)
                    with open(path, "w") as f:
                        f.write(self.teststring1)
                    remaining -= len(self.teststring1)
                if remaining < 0:
                    done = True
                    break
            list = newlist
            
        return
                
            


    def make_folders(self):
        log.trace("make_folders")
        if not os.path.isdir(self.test_folder):
            os.makedirs(self.test_folder)

#        if not os.path.isdir(self.store_folder):
#            os.makedirs(self.store_folder)
        if not os.path.isdir(self.files_folder):
            os.makedirs(self.files_folder)
        if not os.path.isdir(self.restore_folder):
            os.makedirs(self.restore_folder)


    def cleanup(self):
        log.trace("Cleanup")
        self.db.execute("delete from messages where message_id > ?", (self.max_message_id,))
        self.db.execute("delete from versions where version_id > ?", (self.max_version_id,))
        self.db.execute("delete from fs where fs_id > ?", (self.max_fs_id,))
        self.db.execute("delete from runs where run_id > ?", (self.max_run_id,))


        if self.options.store:
            stores = self.options.store
        else:
            stores = ["teststore1", "teststore2"]
        for name in stores:
            log.info("Cleaning up", name)
            store = self.config.storage[name].copy()
            store.connect()
            store.delete_store_data()
            store.disconnect()

        if not self.options.store:
            del self.config.storage["teststore1"]
            del self.config.storage["teststore2"]
        del self.config.backups["testbackup1"]
        del self.config.backups["testbackup2"]

        shutil.rmtree(self.test_folder)
