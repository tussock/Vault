#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.

'''
Created on 15/02/2011

@author: paul
'''

import filecmp
import ConfigParser
import shutil
import time

import gettext
_ = gettext.gettext

from store.storebase import *
from store.folderstore import FolderStore
from store.ftpstore import FTPStore
from lib.timer import Timer
from lib import utils

class StoreBaseTests:
    def __init__(self):
        self.store = None
        #    Get the test configuration from the ~/.vault file
        config_file = os.path.expanduser("~/.vault")
        if not os.path.exists(config_file):
            raise Exception("Vault test configuration file (~/.vault) does not exist")
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        
    def setUp(self):
        self.working_folder = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.working_folder)
        self.store.remove_dir("")
        self.store.disconnect()

    def testTest(self):
        self.store.test()
        

    def testCopy(self):
        temp_path = utils.maketempfile(1000)
        temp_path2 = temp_path + "2"
        try:
            remote = self.store.send(temp_path, "test/")
            self.store.get(remote, temp_path2)
            self.assertTrue(filecmp.cmp(temp_path, temp_path2, shallow=False))
        finally:
            os.remove(temp_path)
            if os.path.exists(temp_path2):
                os.remove(temp_path2)
            #     local_path will be removed during tearDown
            try:
                #    This could fail if there was an exception above
                self.store.remove_dir("test")
            except:
                pass
            
    def testCopyFolder(self):
        temp_path = utils.maketempfile(100)
        fname = os.path.basename(temp_path)
        try:
            self.store.send(temp_path, "test/")
            self.assertTrue(self.store.exists(os.path.join("test", fname)))
            
            self.store.get(os.path.join("test", fname), self.working_folder + os.sep)
            self.assertTrue(os.path.isfile(os.path.join(self.working_folder, fname)))
        finally:
            os.remove(temp_path)
             
    def testCopyLarge(self):
        temp_path = utils.maketempfile(100000)
        temp_path2 = temp_path + "2"
        
        try:
            remote = self.store.send(temp_path, "test/")
            self.store.get(remote, temp_path2)
            self.assertTrue(filecmp.cmp(temp_path, temp_path2, shallow=False))
        finally:
            os.remove(temp_path)
            os.remove(temp_path2)
            #     local_path will be removed during tearDown
            self.store.remove_dir("test")

    def testCopyManySmall(self):
        local = []
        numFiles = 5
        tempf = tempfile.mkdtemp()
        try:
            for i in xrange(numFiles):
                local_file = utils.maketempfile(1000, dir=tempf)
                local.append(local_file)
                self.store.send(local_file, "test/")
    
            #    Make sure each file made it
            files = self.store.list("test")
            for i in xrange(numFiles):
                self.assertTrue(os.path.basename(local[i]) in files)
                
            for i in xrange(numFiles):
                remote_contents = self.store.get_contents(os.path.join("test", os.path.basename(local[i])))
                local_contents = open(local[i]).read()
                self.assertEqual(local_contents, remote_contents)
                
            #    Make sure list is only returning those files
            self.assertEqual(len(files), numFiles)
        finally:
            shutil.rmtree(tempf)
            self.store.remove_dir("test")
            
    def testGetSet(self):
        str = os.urandom(1033)
        self.store.set_contents("test/test/test/x", str)
        str2 = self.store.get_contents("test/test/test/x")
        self.assertEqual(str, str2)
#        self.store.get_contents("blah")
        self.assertRaises(IOError, self.store.get_contents, "badfile")
            
    def testSize(self):
        tempf = utils.maketempfile(1037)
        try:
            remote = self.store.send(tempf, "test/")
            size = self.store.size(remote)
        
            self.assertEqual(size, 1037)
        finally:
            os.remove(tempf)
            self.store.remove_dir("test")
        
    def testFolder(self):
        self.store.make_dir("blah")
        self.assertTrue(self.store.exists("blah"))
        self.store.remove_dir("blah")
        self.assertFalse(self.store.exists("blah"))

    def testDeleteFile(self):
        tempf = utils.maketempfile(1037)
        try:
            remote = self.store.send(tempf, "/")
            self.assertTrue(self.store.exists(remote))
            self.store.remove_file(remote)
            self.assertFalse(self.store.exists(remote))
        finally:
            os.remove(tempf)
        
    def testRecursiveDelete(self):
        self.store.make_dir("test")
        self.assertTrue(self.store.exists("test"))
        t = utils.maketempfile(1037)
        try:
            remote1 = self.store.send(t, "test/")
            remote2 = self.store.send(t, "test2/")
            
            self.assertTrue(self.store.exists(remote1))
            self.assertTrue(self.store.exists(remote2))
            self.store.remove_dir("test")
            #    Make sure both the folder and file are gone
            self.assertFalse(self.store.exists(remote1))
            self.assertFalse(self.store.exists("test"))
            #    Make sure the delete didn't touch any other files
            self.assertTrue(self.store.exists(remote2))
            
        finally:
            os.remove(t)
            self.store.remove_dir("test2")
            
    def testSpeed(self):
        tempf = utils.maketempfile(128000)
        try:
            with Timer(self.store.__class__.__name__ + " 128k Copy"):
                self.store.send(tempf, "test/")
        finally:
            os.remove(tempf)
            self.store.remove_dir("test")
        
        
    def testWrite(self):
        teststring = os.urandom(1024)
        fd = self.store.open("test/blah", "w")
        fd.write(teststring)
        fd.close()
        self.store.flush()
        remote_data = self.store.get_contents("test/blah")
        self.assertEqual(len(teststring), len(remote_data))
        self.assertEqual(teststring, remote_data)

    def testBadOpen(self):
        
        self.assertRaises(IOError, self.store.open, "bad", "r")
        
    def testQueuedWrite(self):
        if isinstance(self.store, FolderStore) or isinstance(self.store, FTPStore):
            # These classes stream rather than queue
            return
        teststring = os.urandom(1024)
        fd = self.store.open("test/blah", "wq")
        fd.write(teststring)
        fd.close()
        fd = self.store.open("test/blah2", "wq")
        fd.write(teststring)
        fd.close()
        fd = self.store.open("test/blah3", "wq")
        fd.write(teststring)
        fd.close()
        print("Sent all")
        self.assertTrue(self.store.queue.qsize() > 0)
        self.store.flush()
        print("Flushed")
        remote_data = self.store.get_contents("test/blah")
        self.assertEqual(len(teststring), len(remote_data))
        self.assertEqual(teststring, remote_data)
        remote_data = self.store.get_contents("test/blah2")
        self.assertEqual(len(teststring), len(remote_data))
        self.assertEqual(teststring, remote_data)
        remote_data = self.store.get_contents("test/blah3")
        self.assertEqual(len(teststring), len(remote_data))
        self.assertEqual(teststring, remote_data)
        
    def testQueuedSend(self):
        if isinstance(self.store, FolderStore) or isinstance(self.store, FTPStore):
            # These classes stream rather than queue
            return
        fname = utils.maketempfile(1031)
        contents = open(fname).read()
        try:
            self.store.send(fname, "test/send1", block=False)
            self.store.flush()
            remote = self.store.get_contents("test/send1")
            self.assertEqual(contents, remote)
            self.assertFalse(os.path.isfile(fname))
        finally:
            #    In case sometihng failed - we ensure the file is gone
            if os.path.isfile(fname):
                os.remove(fname)
            
    def testQueuedFail(self):
        if isinstance(self.store, FolderStore) or isinstance(self.store, FTPStore):
            # These classes stream rather than queue
            return
        #    This next statement will ensure queued xmits fail.
        self.store.debug_fail = True
        teststring = os.urandom(1024)
        fd = self.store.open("test/fail1", "wq")
        fd.write(teststring)
        #    Close will queue the job and start the worker
        #    (which will then fail)
        fd.close()
        #    Now we check that flush detects the failure properly
        #    And that the right exception is passed back to us.
        #    Flush should clean up the error condition too.
        self.assertRaises(DebugException, self.store.flush)

    def testQueuedFail2(self):
        if isinstance(self.store, FolderStore) or isinstance(self.store, FTPStore):
            # These classes stream rather than queue
            return
        #    This next statement will ensure queued xmits fail.
        self.store.debug_fail = True
        teststring = os.urandom(1024)
        fd = self.store.open("test/fail1", "wq")
        fd.write(teststring)
        #    Close will queue the job and start the worker
        fd.close()
        #    Give it a second to get going...
        time.sleep(0.5)
        #    Now try another non-blocking send. That should detect the error
        fd = self.store.open("test/fail2", "wq")
        fd.write(teststring)
        #    Close will queue the job and start the worker
        #    This will cause flush to clean up the error condition
        self.assertRaises(DebugException, fd.close)

    def testRead(self):
        testfile = utils.maketempfile(1037)
        try:
            remote = self.store.send(testfile, "test/")
        
            fd = self.store.open(remote, "r")
            remote_data = fd.read()
            fd.close()
            self.assertEqual(remote_data, open(testfile).read())
        finally:
                os.remove(testfile)
               
    def testSeek(self):
        pass



