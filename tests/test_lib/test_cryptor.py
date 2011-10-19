#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.

import os
import shutil
import filecmp
import unittest
from threading import Thread
import tempfile
import time

from lib import utils
from lib.cryptor import entropy, encrypt_string, decrypt_string, encrypt_file, \
        decrypt_file, EncryptStream, DecryptStream, CopyThread, Buffer, CipherError

class CrypterTestCase(unittest.TestCase):

    def setUp(self):
        self.bigdata = os.urandom(10240)
        self.tinydata = os.urandom(1024)
        self.password = "squigglywiggle"
        self.testdir = tempfile.mkdtemp()


    def tearDown(self):
        shutil.rmtree(self.testdir)
    
    
    def testCrypt(self):
        enc = encrypt_string(self.password, self.bigdata)
        dec = decrypt_string(self.password, enc)
        self.assertEqual(self.bigdata, dec)
   
    def testPadding(self):
        for i in xrange(1, 64):
            data = os.urandom(i)
            enc = encrypt_string(self.password, data)
            dec = decrypt_string(self.password, enc)
            self.assertEqual(data, dec)

    def testPasswords(self):
        for i in xrange(1, 32):
            password = os.urandom(i)
            enc = encrypt_string(password, self.bigdata)
            dec = decrypt_string(password, enc)
            self.assertEqual(self.bigdata, dec)
   
    def testStreamEncryptor(self):
        crypt = EncryptStream(self.password)
        c = self.bigdata
        mid = len(c)//2
        crypt.write(c[:mid])
        crypt.write(c[mid:])
        crypt.close()
        enc = crypt.read()
        
        dec = decrypt_string(self.password, enc)
        self.assertEqual(c, dec)
        
    def testStreamDecryptor(self):
        enc = encrypt_string(self.password, self.bigdata)
        crypt = DecryptStream(self.password)
        mid = len(enc)//2
        crypt.write(enc[:mid])
        crypt.write(enc[mid:])
        crypt.close()
        dec = crypt.read()
        
        self.assertEqual(self.bigdata, dec)
        
    def testStreamers(self):
        crypt = EncryptStream(self.password)
        clear = ""
        for dummy in xrange(64):
            data = os.urandom(1024)
            crypt.write(data)
            clear += data
        crypt.close()
        crypt2 = DecryptStream(self.password)
        crypt2.write(crypt.read())
        crypt2.close()
        
        self.assertEqual(clear, crypt2.read())
    
    def write_thread(self, outfile):
        #    Slowely write the data to the stream
        blocksize = 59
        for block in [self.tinydata[i:i+blocksize] for i in range(0, len(self.tinydata), blocksize)]:
            outfile.write(block)
            time.sleep(0.05)
        outfile.close()
    
        
    def read_thread(self, infile):
        data = infile.read()
        l=0
        while data:
            l+=len(data)
            self.read_buffer.append(data)
            data = infile.read()
        infile.close()
             
    def testThreaded(self):
        crypt = EncryptStream(self.password)
        decrypt = DecryptStream(self.password)
        self.read_buffer = []
        t1=Thread(target=self.write_thread, args=(crypt, ))
        t2=CopyThread(crypt, decrypt)
        t3=Thread(target=self.read_thread, args=(decrypt, ))
        t1.start()
        t2.start()
        t3.start()
        
        t1.join()
        t2.join()
        t3.join()
        clear = "".join(self.read_buffer)
        self.assertEqual(self.tinydata, clear)

        
    def testFile(self):
        clear_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        crypt_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file2 = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file.write(self.bigdata)
        clear_file.close()
        crypt_file.close()
        clear_file2.close()
        encrypt_file(self.password, clear_file.name, crypt_file.name)
        decrypt_file(self.password, crypt_file.name, clear_file2.name)
        self.assertTrue(filecmp.cmp(clear_file.name, clear_file2.name, shallow=False))
        self.assertFalse(filecmp.cmp(clear_file.name, crypt_file.name, shallow=False))
        
    def testSmallFile(self):
        clear_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        crypt_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file2 = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file.write("abc")
        clear_file.close()
        crypt_file.close()
        clear_file2.close()
        encrypt_file(self.password, clear_file.name, crypt_file.name)
        decrypt_file(self.password, crypt_file.name, clear_file2.name)
        self.assertTrue(filecmp.cmp(clear_file.name, clear_file2.name, shallow=False))
        self.assertFalse(filecmp.cmp(clear_file.name, crypt_file.name, shallow=False))
        
    def testBufferFullRead(self):
        buf = Buffer()
        buf.write(self.tinydata)
        buf.close()
        d = buf.read()
        self.assertEqual(d, self.tinydata)
        
    def testBufferPartialRead(self):
        buf = Buffer()
        buf.write(self.tinydata)
        buf.close()
        d = buf.read(5)
        self.assertEqual(d, self.tinydata[:5])
        d += buf.read()
        self.assertEqual(d, self.tinydata)


    def testBufferLocking(self):
        buffer = Buffer()
        self.read_buffer = []
        t1=Thread(target=self.write_thread, args=(buffer, ))
        t2=Thread(target=self.read_thread, args=(buffer, ))
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        result = "".join(self.read_buffer)
        self.assertEqual(self.tinydata, result)
        
    def testOpenSSLCompatabilityEncrypt(self):
        clear_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        crypt_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file2 = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file.write(self.tinydata)
        clear_file.close()
        crypt_file.close()
        clear_file2.close()
        encrypt_file(self.password, clear_file.name, crypt_file.name)
        cmd = "openssl enc -d -md sha256 -aes-256-cbc -pass pass:%s -in %s -out %s" % \
                (self.password, crypt_file.name, clear_file2.name)
        os.system(cmd) 
        self.assertTrue(filecmp.cmp(clear_file.name, clear_file2.name, shallow=False))
        self.assertFalse(filecmp.cmp(clear_file.name, crypt_file.name, shallow=False))
        
    def testOpenSSLCompatabilityDecrypt(self):
        clear_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        crypt_file = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file2 = tempfile.NamedTemporaryFile(delete=False, dir=self.testdir)
        clear_file.write(self.tinydata)
        clear_file.close()
        crypt_file.close()
        clear_file2.close()
        cmd = "openssl enc -md sha256 -aes-256-cbc -pass pass:%s -in %s -out %s" % \
                (self.password, clear_file.name, crypt_file.name)
        os.system(cmd) 
        decrypt_file(self.password, crypt_file.name, clear_file2.name)
        self.assertTrue(filecmp.cmp(clear_file.name, clear_file2.name, shallow=False))
        self.assertFalse(filecmp.cmp(clear_file.name, crypt_file.name, shallow=False))
        
        
    def testBadEncrypt(self):
        fname = utils.maketempfile(1024)
        self.assertRaises(CipherError, decrypt_file, self.password, fname)
        
    def testEntropy(self):
        passlist = ["a", "hello", "hellob", "(*&^KJHGjkhgrtoiua123"]
        for i in xrange(len(passlist)-1):
            self.assertTrue(entropy(passlist[i]) < entropy(passlist[i+1]))
    
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

