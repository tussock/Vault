#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
'''
Created on 15/02/2011

@author: paul
'''

import unittest

from store.storebase import *
from store.s3store import *
from test_storebase import StoreBaseTests


class Test_S3Store(StoreBaseTests, unittest.TestCase):
    '''
    We assume that you will create a ~/.vault file.
    Inside that file will be a section:
        [Amazon]
        aws_access_key_id = <your amazon access key>
        aws_secret_access_key = <your secret amazon access key>
        bucket = <bucket name for store>
    '''
        
    def __init__(self, methodName = "runTest"):
        StoreBaseTests.__init__(self)
        unittest.TestCase.__init__(self, methodName)
        
        try:
            self.key = self.config.get("Amazon", "aws_access_key_id")
            self.secret_key = self.config.get("Amazon", "aws_secret_access_key")
            self.bucket = self.config.get("Amazon", "bucket")
        except:
            raise Exception("Amazon keys missing from vault test config")


    def setUp(self):
        StoreBaseTests.setUp(self)
        self.store = S3Store("s3storetest", 0, False, bucket=self.bucket, key=self.key, secret_key=self.secret_key)

#    def tearDown(self):
#        StoreBaseTests.tearDown(self)


if __name__ == "__main__":
    unittest.main()
