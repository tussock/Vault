#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
'''
Created on 15/02/2011

@author: paul
'''


import unittest

from store.storebase import *
from store.ftpstore import *
from store.folderstore import *
from test_storebase import StoreBaseTests


class Test_FTPStore(StoreBaseTests, unittest.TestCase):
    '''
    We assume that you will create a ~/.vault file.
    Inside that file will be a section:
        [FTP]
        server = <ip address or dns name of ftp server>
        login = <your login id>
        password = <your password>
        folder = <folder for store>
    Note that SFTP will always be used.
    '''

    def __init__(self, methodName="runTest"):
        StoreBaseTests.__init__(self)
        unittest.TestCase.__init__(self, methodName)

        try:
            self.server = self.config.get("FTP", "server")
            self.login = self.config.get("FTP", "login")
            self.password = self.config.get("FTP", "password")+"x"
            self.folder = self.config.get("FTP", "folder")

        except Exception as e:
            raise Exception("FTP server, login or password missing from vault test config", str(e))



    def setUp(self):
        StoreBaseTests.setUp(self)
        self.store = FTPStore("storetest", 0, False, self.server, self.folder, self.login, self.password, sftp=True)

    def tearDown(self):
        StoreBaseTests.tearDown(self)


if __name__ == "__main__":
    unittest.main()

