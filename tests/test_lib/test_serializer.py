'''
Created on Apr 23, 2011

@author: paul
'''
import unittest
import json
import os

from backup import Backup
from serializer import to_json, from_json

class TestSerializer(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        os.remove("test.json")
        pass

    
    def testLoadSave(self):
        bkp = Backup(u"Name2")
        with open('test.json', 'w') as f:
            json.dump(bkp, f, default=to_json, sort_keys=True, indent=4)

        with open('test.json', 'r') as f:
            bkp2 = json.load(f, object_hook=from_json)
            
        #    Test that all items are the same.
        #    NOTE the unicode conversion.
        for key, value in bkp.__dict__.iteritems():
            self.assertTrue(hasattr(bkp2, key))
            self.assertEqual(unicode(bkp2.__dict__[key]), unicode(value))
             
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()