#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
'''
Created on 15/02/2011

@author: paul
'''

import unittest
import shutil

from store.storebase import *
from store.sharestore import *
from test_storebase import StoreBaseTests


class Test_ShareStore(StoreBaseTests, unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        '''
        To run the sharestore tests, you must create a section in the ~/.vault
        test config file with the following form:
        
        [Share]
        folder = <folder that the remote system will be mounted to>
        mount = <mount command>
        umount = <umount command>
        
        The folder will be deleted after the tests have run.
        
        For example:
        [Share]
        folder = /tmp/vault-test
        mount = sshfs <name>@<server>:<remote-folder> /tmp/vault-test
        umount = fusermount -u /tmp/vault-test
        '''
        StoreBaseTests.__init__(self)
        unittest.TestCase.__init__(self, methodName)
        try:
            self.folder = self.config.get("Share", "folder")
            self.mount = self.config.get("Share", "mount")
            self.umount = self.config.get("Share", "umount")
        except:
            raise Exception("Share config missing from vault test config")

    def setUp(self):
        StoreBaseTests.setUp(self)
        utils.makedirs(self.folder)
       
        self.store = ShareStore("storetest", 0, False, self.folder, self.mount, self.umount)

    def tearDown(self):
        StoreBaseTests.tearDown(self)

#    def testFail(self):
#        self.store2 = ShareStore("storetest2", 0, False, "/tmp/badfolder", "badcmd", "badcmd")
#        self.store2.test()
#        self.store2.connect()
        
        

if __name__ == "__main__":
    unittest.main()

