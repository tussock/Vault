#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.


import shutil
import filecmp
import unittest

from lib import utils
from encryption import *

class EncryptionTestCase(unittest.TestCase):

    def setUp(self):
        self.testfile1 = utils.maketempfile(1024)
        self.password = "squigglywiggle"


    def tearDown(self):
        os.remove(self.testfile1)




    def testCrypt(self):
        cryptfile = self.testfile1 + ".enc"
        clearfile = self.testfile1 + ".clr"
        shutil.copy(self.testfile1, clearfile)
        try:
            encrypt_file(self.password, clearfile, cryptfile)
            self.assertFalse(filecmp.cmp(self.testfile1, cryptfile, shallow=False) == 1)
            decrypt_file(self.password, cryptfile, clearfile)
            self.assertTrue(filecmp.cmp(self.testfile1, clearfile, shallow=False) == 1)
        finally:
            if os.path.exists(cryptfile):
                os.remove(cryptfile)
            if os.path.exists(clearfile):
                os.remove(clearfile)

    def testCryptInplace(self):
        filename = self.testfile1 + ".crypt"
        shutil.copy(self.testfile1, filename)
        try:
            encrypt_file(self.password, filename)
            self.assertNotEqual(filecmp.cmp(self.testfile1, filename, shallow=False), 1)
            decrypt_file(self.password, filename)
            self.assertEqual(filecmp.cmp(self.testfile1, filename, shallow=False), 1)
        finally:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
