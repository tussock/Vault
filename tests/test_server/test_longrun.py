#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.


import os
import shutil
import unittest
import tempfile
import time
from datetime import datetime, timedelta
import ConfigParser

from lib import const
from lib import utils
from store.folderstore import FolderStore
from store.dropboxstore import DropBoxStore
from store.s3store import S3Store
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

class LongRunTestCase(unittest.TestCase):

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
        
        #    Build the base set of files
        with open(os.path.join(self.files_folder, "base"), "w") as f:
            f.write("base")

        with open(os.path.join(self.files_folder, "incr"), "w") as f:
            f.write("0")
            
        config_file = os.path.expanduser("~/.vault")
        if not os.path.exists(config_file):
            raise Exception("Vault test configuration file (~/.vault) does not exist")
        self.store_config = ConfigParser.RawConfigParser()
        self.store_config.read(config_file)

    #    FOLDER STORE
        self.store = FolderStore("teststore", "50MB", True, self.store_folder)
    #    DROPBOX STORE
#        self.login = self.store_config.get("DropBox", "login")
#        self.password = self.store_config.get("DropBox", "password")
#        self.folder = self.store_config.get("DropBox", "folder")
#        self.app_key = self.store_config.get("DropBox", "app_key")
#        self.app_secret_key = self.store_config.get("DropBox", "app_secret_key")
#        self.store = DropBoxStore("teststore", 0, False, self.folder, self.login, self.password,
#                                  self.app_key, self.app_secret_key)
    #    S3 STORE
#        self.key = self.store_config.get("Amazon", "aws_access_key_id")
#        self.secret_key = self.store_config.get("Amazon", "aws_secret_access_key")
#        self.bucket = self.store_config.get("Amazon", "bucket")
#        self.store = S3Store("teststore", 0, False, bucket=self.bucket, key=self.key, secret_key=self.secret_key)

        #    Now record the existance of this store
        self.config.storage[self.store.name] = self.store


        #    Build the backup object (dont save config)
        self.backup = Backup("testbackup")
        self.backup.include_folders = [self.files_folder]
        self.backup.store = self.store.name
        self.backup.notify_msg = False
        self.old_pass = self.config.data_passphrase
        self.config.data_passphrase = "goofy"
        self.backup.encrypt = True
        self.config.backups[self.backup.name] = self.backup

        #    build an options object for use with the backup
        self.options = BlankClass()
        self.options.dry_run = False
        self.options.message = False
        self.options.email = False
        self.options.shutdown = False
        self.options.norecurse = False
        
        #    How many cycles?
        self.cycles = 20

    def tearDown(self):
        self.config.data_passphrase = self.old_pass
        #    Remove all DB records created during this test
        self.clean_db()
        shutil.rmtree(self.test_folder)
        self.assertFalse(os.path.isdir(self.test_folder))


    def testLongRun(self):

        #    Run a full backup
        b = Run(self.backup.name, const.FullBackup, self.options)
        b.run()

        for cycle in xrange(self.cycles):
            print(str(cycle)+"\r")
            time.sleep(1)
            
            #    Change some files
            with open(os.path.join(self.files_folder, "incr"), "w") as f:
                f.write(os.urandom(100))

            with open(os.path.join(self.files_folder, str(cycle)), "w") as f:
                f.write(os.urandom(100))
            

            #    Run an incr backup
            b = Run(self.backup.name, const.IncrBackup, self.options)
            b.run()

        
        #    Attempt to restore every file
        r = Restore(self.restore_folder, [self.files_folder],
                                          datetime.now(), self.options)
        r.run()
        
        #    Lets break it
#        os.remove(os.path.join(self.restore_folder, self.files_folder[1:], "1"))
#        with open(os.path.join(self.files_folder, "incr"), "w") as f:
#            f.write("-1")       
#        with open(os.path.join(self.restore_folder, self.files_folder[1:], "8"), "w") as f:
#            f.write("-1")       

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
