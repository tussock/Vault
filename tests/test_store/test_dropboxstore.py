#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
'''
Created on 15/02/2011

@author: paul
'''

import unittest

from store.storebase import *
from store.dropboxstore import *
from test_storebase import StoreBaseTests

#    Do this last!
from lib.logger import Logger
log = Logger("io") 



class Test_DropBoxStore(StoreBaseTests, unittest.TestCase):
    '''
    We assume that you will create a ~/.vault file.
    Inside that file will be a section:
        [DropBox]
        login = <your login id>
        password = <your password>
        folder = <store root folder>
        app_key = <application key>
        app_secret_key = <app_secret_key>
    '''
    def __init__(self, methodName = "runTest"):
        StoreBaseTests.__init__(self)
        unittest.TestCase.__init__(self, methodName)

        try:
            self.login = self.config.get("DropBox", "login")
            self.password = self.config.get("DropBox", "password")
            self.folder = self.config.get("DropBox", "folder")
            self.app_key = self.config.get("DropBox", "app_key")
            self.app_secret_key = self.config.get("DropBox", "app_secret_key")
        except Exception as e:
            raise Exception("DropBox login or password missing from vault test config", str(e))
        

    def setUp(self):
        StoreBaseTests.setUp(self)
        self.store = DropBoxStore("storetest", 0, False, self.folder, self.login, self.password,
                                  self.app_key, self.app_secret_key)

#    def tearDown(self):
#        StoreBaseTests.tearDown(self)


if __name__ == "__main__":
    unittest.main()

#if __name__ == '__main__':
#    import cProfile
#    import pstats
#    cProfile.run("unittest.main()", "BackupProfile")
#
#    p = pstats.Stats('BackupProfile')
#    p.strip_dirs().sort_stats("cumulative").print_stats()
