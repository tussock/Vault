#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.


import os
import shutil
import unittest
import tempfile
import time
from datetime import datetime, timedelta

from lib import const
from lib import utils
from lib import passphrase
from store.folderstore import FolderStore
from lib.backup import Backup
from lib.config import Config

from lib.db import DB
from server.run import Run
from server.restore import Restore

#    Do this last!
from lib.logger import Logger
log = Logger("server")


class BlankClass:
    pass

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config.get_config()
        self.db = DB()
        self.db.check_upgrade()
        self.mark_db_ids()

        self.test_folder = tempfile.mkdtemp()
        self.files_folder = os.path.join(self.test_folder, "files")
        self.store_folder = os.path.join(self.test_folder, "store")
        self.restore_folder = os.path.join(self.test_folder, "restore")
        utils.makedirs(self.files_folder)
        utils.makedirs(self.store_folder)
        utils.makedirs(self.restore_folder)

        utils.build_file_structure(self.files_folder, 50 * const.Kilobyte, 500 * const.Kilobyte)

        #    Build a store object (dont save the config)
        #    Note the careful size selection - we want backups to overflow the FolderStore.
        self.store = FolderStore("teststore", "2MB", True, self.store_folder)
        self.config.storage[self.store.name] = self.store

        #    Build the backup object (dont save config)
        self.backup = Backup("testbackup")
        self.backup.include_folders = [self.files_folder]
        self.backup.store = self.store.name
        self.backup.notify_msg = False
        self.old_pass = passphrase.passphrase
        passphrase.set_passphrase("goofy")
        self.backup.encrypt = True
        self.config.backups[self.backup.name] = self.backup

        #    build an options object for use with the backup
        self.options = BlankClass()
        self.options.dry_run = False
        self.options.message = False
        self.options.email = False
        self.options.shutdown = False
        self.options.norecurse = False


    def tearDown(self):
        passphrase.set_passphrase(self.old_pass)
        #    Remove all DB records created during this test
        self.clean_db()
        shutil.rmtree(self.test_folder)
        self.assertFalse(os.path.isdir(self.test_folder))


    def testBackupRestore(self):
        self.backup_restore_compare()

    def testAutoManagementOfStore1(self):
        #    Run a set of backups that will overload the store. 
        #    The automanaged store should continue to archive old backups as required.
        #    Store space reclaimation happens across all backups (i.e. any run).
        #    We should see older runs from the first backup disappear.
        max_size, _, _ = self.store.limit_details()

        filesize = utils.du(self.backup.include_folders[0])

        #    Lets make sure we are going to do enough backups that
        #    the older ones will be removed.
        RunCount = (max_size // filesize) + 2


        last_start = None
        for cycle in xrange(RunCount):
            if last_start:
                #    Make sure we have ticked to another second since the start of the last backup.
                while datetime.now() - last_start < timedelta(seconds=1):
                    time.sleep(0.01)

            backup = Backup(self.backup.name + str(cycle))
            backup.include_folders = self.backup.include_folders
            backup.store = self.backup.store
            backup.notify_msg = False
            self.config.backups[backup.name] = backup

            #    Run a full backup
            b = Run(backup.name, const.FullBackup, self.options)
            b.run()
            last_start = b.start_time

            #    Assert that the store is still of an appropriate size
            size, used, avail = self.store.current_usage()
            self.assertTrue(avail >= 0)
            self.assertTrue(used <= max_size)

            #    Confirm that's true on disk
            disksize = utils.du(self.store.root)
            self.assertTrue(disksize <= max_size)


        #    Check that some runs have actually been deleted
        runs = self.db.runs(self.backup.name + "0")
        self.assertTrue(len(runs) == 0)
        runs = self.db.runs(self.backup.name + "1")
        self.assertTrue(len(runs) == 0)

    def testAutoManagementOfStore2(self):
        #    Run one backup multiple times to overload a store
        max_size, _, _ = self.store.limit_details()

        filesize = utils.du(self.backup.include_folders[0])

        #    Lets make sure we are going to do enough backups that
        #    the older ones will be removed.
        RunCount = (max_size // filesize) + 2

        last_start = None
        for cycle in xrange(RunCount):

            if last_start:
                #    Make sure we have ticked to another second since the start of the last backup.
                while datetime.now() - last_start < timedelta(seconds=1):
                    time.sleep(0.01)

            #    Run a full backup
            b = Run(self.backup.name, const.FullBackup, self.options)
            b.run()

            last_start = b.start_time

            #    Assert that the store is still of an appropriate size
            size, used, avail = self.store.current_usage()
            self.assertTrue(avail >= 0)
            self.assertTrue(used <= max_size)

            #    Confirm that's true on disk
            disksize = utils.du(self.store.root)
            self.assertTrue(disksize <= max_size)


        #    Check that some runs have actually been deleted
        runs = self.db.runs(self.backup.name)
        self.assertTrue(len(runs) < RunCount)

    def testChanges(self):
        pass
        #    Full Backup
        #    change a file
        #    Incremental backup
        #    Restore most recent. ensure you get latest file
        #    Restore to just prior to incremental, ensure you get earlier file
        #    Run a full backup
        file = os.path.join(self.files_folder, "changer")
        restore_file = os.path.join(self.restore_folder, file[1:])

        #    t=0 - file does not exist
        b = Run("testbackup", const.FullBackup, self.options)
        b.run()

        #    Make sure we have ticked to another second since the start of the last backup.
        while datetime.now() - b.start_time < timedelta(seconds=1):
            time.sleep(0.01)

        #    t=1 - file exists
        with open(file, "w") as f:
            f.write("1")
        b = Run("testbackup", const.IncrBackup, self.options)
        b.run()

        #    Make sure we have ticked to another second since the start of the last backup.
        while datetime.now() - b.start_time < timedelta(seconds=1):
            time.sleep(0.01)

        #    t=2 - file changed
        with open(file, "w") as f:
            f.write("2")
        b = Run("testbackup", const.IncrBackup, self.options)
        b.run()

        #    Get the times
        runs = self.db.runs("testbackup")
        t0 = runs[0].start_time
        t1 = runs[1].start_time
        t2 = runs[2].start_time

        for t, exists, contents in [(t0, False, None), (t1, True, "1"), (t2, True, "2"), (None, True, "2")]:
            #    Attempt to restore most recent of ALL files
            #    This tests the default restore.
            r = Restore(self.restore_folder, [self.files_folder], t, self.options)
            r.run()
            if exists:
                with open(restore_file, "r") as f:
                    self.assertEqual(f.read(), contents)
            else:
                self.assertFalse(os.path.exists(restore_file))
            #    clean
            shutil.rmtree(self.restore_folder)
            utils.makedirs(self.restore_folder)


    def test7bitFilenames(self):
        #    Make some 7 bit filenames
        strange_folder = os.path.join(self.files_folder, "strange")
        utils.makedirs(strange_folder)
        for i in xrange(1, 117, 10):
            name = "".join([chr(j) for j in xrange(i, i + 10) if chr(j) != "/"])
            path = os.path.join(strange_folder, name)
            with open(path, "w") as f:
                f.write(os.urandom(100))

        self.backup_restore_compare()

    def testUnicodeFilenames(self):
        #    Make some unicode bit filenames
        #    Clean out the ordinary files
        shutil.rmtree(self.files_folder)
        utils.makedirs(self.files_folder)
        unicode_folder = os.path.join(unicode(self.files_folder), u"unicode")
        utils.makedirs(unicode_folder)
        for i in xrange(1000, 1200, 10):
            name = u"".join([unichr(j) for j in xrange(i, i + 10) if unichr(j) != u"/"])
            path = os.path.join(unicode_folder, name)
            with open(path, "w") as f:
                f.write(os.urandom(10))

        self.backup_restore_compare()

    def backup_restore_compare(self):
        #    Run a full backup
        b = Run("testbackup", const.FullBackup, self.options)
        b.run()

        #    Make sure we have ticked to another second since the start of the last backup.
        while datetime.now() - b.start_time < timedelta(seconds=1):
            time.sleep(0.01)


        #    Attempt to restore every file
        r = Restore(self.restore_folder, [self.files_folder],
                                          datetime.now(), self.options)
        r.run()

        #    Check that the restored folder and original folder are identical
        left = unicode(self.files_folder)
        right = unicode(os.path.join(self.restore_folder, self.files_folder[1:]))
        d = utils.dircmp(left, right)

        self.assertEqual(d.left_only, set())
        self.assertEqual(d.right_only, set())
        self.assertEqual(d.diff_files, set())
        self.assertTrue(len(d.same_files) > 0)

        #    Check that all files are in the DB
        for folder, _, local_files in os.walk(self.files_folder):
            for file in local_files:
                path = os.path.join(file, folder)
                #    This will raise an exception if it does not exist
                self.db.select_path(path, build=False)

############################################################################
#
#    Utility Routines
#
############################################################################

    def mark_db_ids(self):
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

    def clean_db(self):
        self.db.execute("delete from messages where message_id > ?", (self.max_message_id,))
        self.db.execute("delete from versions where version_id > ?", (self.max_version_id,))
        self.db.execute("delete from fs where fs_id > ?", (self.max_fs_id,))
        self.db.execute("delete from runs where run_id > ?", (self.max_run_id,))




if __name__ == "__main__":
    unittest.main()
