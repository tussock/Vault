#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.
       
import os
import unittest

from xmlsettings import XMLSettings

class _testclass:
    def __init__(self):
        self.a = 1
        self.b = 12345687901234567890
        self.c = 1234.568790
        self.d = "hello"
        self.e = {"a": 1234, "b": complex(25, 23), 4: [1,2,3,4,"asdf"]}
        self.f = None



    def __cmp__(self, other):
        return not (self.a == other.a and \
            self.b == other.b and \
            self.c == other.c and \
            self.d == other.d and \
            self.e == other.e) 
        
class _persistentClass:
    def __init__(self):
        self.a = 1
        self.b = "hi"
        self.c = 9.4
        self._persistent = ["a", "b"]
                 
class xmlSettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.xml = XMLSettings()
        self.xml.filename = "TestSettings.xml"
        
    def tearDown(self):
        if os.path.exists(self.xml.filename):
            os.remove(self.xml.filename)
        
    def testTuple(self):
        i = (1, 2, 3, 4)
        self.xml.save(i)
        i2 = self.xml.load()
        assert(i == i2)
    def testList(self):
        l = [1, 2, "asdf", (1, 2, 3)]
        self.xml.save(l)
        l2 = self.xml.load()
        assert(l == l2)
    def testDict(self):
        d = {"a": (1, 2, 3), 4: 5, "d": 676745764576674657}
        self.xml.save(d)
        d2 = self.xml.load()
        assert(d == d2)
    def testBaseTypes(self):
        d = [1, 12345687901234568790, 123.3465789, complex(1, 3.5), True, False, "Hello", None]
        self.xml.save(d)
        d2 = self.xml.load()
        assert(d == d2)
    def testClass(self):
        c = _testclass()
        self.xml.save(c)
        c2 = self.xml.load()
        assert(c == c2)
    def testBigObject(self):
        import random
        d = {}
        for k in xrange(500):
            v = random.randint(0, 500)
            d[k] = v
        l = []
        for k in xrange(500):
            l.append(random.randint(0, 500))
        d["list"] = l
        #    Double the length
        d["dict"] = d.copy()
        self.xml.save(d)
        d2 = self.xml.load()
        assert(d == d2)
        
    def testPersistentFields(self):
        a = _persistentClass()
        a.c = 99
        self.xml.save(a)
        b = self.xml.load()
        self.assertTrue(hasattr(b, "a"))
        self.assertTrue(hasattr(b, "b"))
        #    b should have the default constructed vault for 'c'
        self.assertNotEqual(b.c, 99)
        
if __name__ == "__main__":
    unittest.main()
