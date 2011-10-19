#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.


import os
import shutil
import unittest
import tempfile

from lib import const
from lib import utils
from store.folderstore import FolderStore
from lib.backup import Backup
from store.streamer import StreamOut

from lib.config import Config
from lib.db import DB
from server.run import Run
from server.verify import Verify

#    Do this last!
from lib.logger import Logger
log = Logger("server")


class BlankClass:
    pass

class VerifyTestCase(unittest.TestCase):

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

        #    Build a store object (dont save config)
        #    Note the careful size selection - we want backups to overflow the FolderStore.
        self.store = FolderStore("teststore", "2MB", True, self.store_folder)
        self.config.storage[self.store.name] = self.store

        #    Build the backup object (dont save config)
        self.backup = Backup("testbackup")
        self.backup.include_folders = [self.files_folder]
        self.backup.store = self.store.name
        self.backup.notify_msg = False
        self.include_packages = True
        self.config.backups[self.backup.name] = self.backup

        #    build an options object for use with the backup
        self.options = BlankClass()
        self.options.dry_run = False
        self.options.message = False
        self.options.email = False
        self.options.shutdown = False
        self.options.norecurse = False

        self.old_pass = self.config.data_passphrase
        self.config.data_passphrase = "banana"


    def tearDown(self):
        self.config.data_passphrase = self.old_pass
        #    Remove all DB records created during this test
        self.clean_db()
        shutil.rmtree(self.test_folder)
        self.assertFalse(os.path.isdir(self.test_folder))


    def testVerify(self):
        #    Run a full backup
        b = Run("testbackup", const.FullBackup, self.options)
        b.run()

        #    Get the times
        runs = self.db.runs("testbackup")
        run = runs[0]


        v = Verify("testbackup", run.start_time)
        self.assertTrue(v.run())


    def testBadVerify(self):
        #    Run a full backup
        b = Run("testbackup", const.FullBackup, self.options)
        b.run()

        #    Get the times
        runs = self.db.runs("testbackup")
        run = runs[0]

        #    Get the location of the data file from the streamer
        streamer = StreamOut(None, self.store, b.backup_folder)
        datafile = os.path.join(self.store.root, streamer.get_path(0))
        size = os.path.getsize(datafile)
        #    Now corrupt the data file a little
        with open(datafile, "r+b") as f:
            f.seek(size // 2, 0)
            f.write("X")


        v = Verify("testbackup", run.start_time)
        self.assertRaises(Exception, v.run)


    def testBadConfig(self):
        #    Run a full backup
        b = Run("testbackup", const.FullBackup, self.options)
        b.run()

        #    Get the times
        runs = self.db.runs("testbackup")
        run = runs[0]

        #    Delete The Config File
        configfile = os.path.join(run.folder, const.ConfigName)
        self.store.remove_file(configfile)


        v = Verify("testbackup", run.start_time)
        self.assertRaises(Exception, v.run)

    def testBadVerifyEncrypted(self):
        backup = self.config.backups[self.backup.name]
        backup.encrypt = True
        self.config.backups[backup.name] = backup

        #    Run a full backup
        b = Run("testbackup", const.FullBackup, self.options)
        b.run()

        #    Get the times
        runs = self.db.runs("testbackup")
        run = runs[0]

        #    Get the location of the data file from the streamer
        streamer = StreamOut(None, self.store, b.backup_folder)
        datafile = os.path.join(self.store.root, streamer.get_path(0))
        #    Now corrupt the data file a little
        size = os.path.getsize(datafile)
        with open(datafile, "r+b") as f:
            f.seek(size // 2, 0)
            f.write("X")


        v = Verify("testbackup", run.start_time)
        self.assertRaises(Exception, v.run)



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
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
