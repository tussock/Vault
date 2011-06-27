#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
'''
Created on 15/02/2011

@author: paul
'''

import unittest
from cStringIO import StringIO
import shutil
import ConfigParser

from store.folderstore import *
from store.ftpstore import *
from store.streamer import *


#    Do this last!
from lib.logger import Logger
log = Logger("io")

class Test_Streamer(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        unittest.TestCase.__init__(self, methodName)
        #    Get the test configuration from the ~/.vault file
        config_file = os.path.expanduser("~/.vault")
        if not os.path.exists(config_file):
            raise Exception("Vault test configuration file (~/.vault) does not exist")
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)

        try:
            self.server = self.config.get("FTP", "server")
            self.login = self.config.get("FTP", "login")
            self.password = self.config.get("FTP", "password")
            self.folder = self.config.get("FTP", "folder")
            
        except Exception as e:
            raise Exception("FTP server, login or password missing from vault test config", str(e))

    def setUp(self):
        self.store_folder = tempfile.mkdtemp()
        self.store = FolderStore("storetest", 0, False, self.store_folder)

        self.ftpstore = FTPStore("storetest", 0, False, self.server, self.folder, self.login, self.password, sftp=True)
        

    def tearDown(self):
        self.store.remove_dir("")
        self.store.disconnect()
        self.ftpstore.remove_dir("")
        self.ftpstore.disconnect()
        
        
    def testNoSplit(self):
        self.stream_test(self.store, 1024)
    def testFTPNoSplit(self):
        self.stream_test(self.ftpstore, 1024)
        
    def testSplit(self):
        self.stream_test(self.store, int(const.ChunkSize * 30.1))
    def testFTPSplit(self):
        self.stream_test(self.ftpstore, int(const.ChunkSize * 30.1))


    def stream_test(self, store, size):
        datastream = StringIO(os.urandom(size))
        self.stream_out = StreamOut(datastream, store, "testdir")
        self.stream_out.start()
        self.stream_out.join()
        
        #    Now check that the right files exists at the store
        store.connect()
        nfiles = (size-1) // const.ChunkSize + 1
        total_size = 0
        for i in xrange(nfiles):
            fname = self.stream_out.get_path(i)
            self.assertTrue(store.exists(fname))
            #    Check files are right size. Last one will be smaller.
            if i < nfiles-1:
                self.assertEqual(store.size(fname), const.ChunkSize)
            total_size += store.size(fname)
        #    File 0..<nfiles-1> should exist.
        fname = self.stream_out.get_path(nfiles)
        self.assertFalse(store.exists(fname))
        #    Check the right amount of data went
        self.assertEqual(size, total_size)
        
        #    Now read that data back...
        instream = StringIO()
        self.stream_in = StreamIn(instream, store, "testdir")
        self.stream_in.start()
        self.stream_in.join()
        
        indata = instream.getvalue()
        self.assertEqual(len(indata), size)
        self.assertEqual(datastream.getvalue(), indata)
        
            

if __name__ == "__main__":
    unittest.main()
