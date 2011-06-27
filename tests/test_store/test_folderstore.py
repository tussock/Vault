#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
'''
Created on 15/02/2011

@author: paul
'''

import unittest

from store.storebase import *
from store.folderstore import *
from test_storebase import StoreBaseTests


class Test_FolderStore(StoreBaseTests, unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        StoreBaseTests.__init__(self)
        unittest.TestCase.__init__(self, methodName)

    def setUp(self):
        StoreBaseTests.setUp(self)
        self.store_folder = tempfile.mkdtemp()
        self.store = FolderStore("storetest", 0, False, self.store_folder)

    def tearDown(self):
        StoreBaseTests.tearDown(self)


if __name__ == "__main__":
    unittest.main()
