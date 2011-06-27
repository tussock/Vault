#    Copyright 2010, 2011  Paul Reddy <paul@kereru.org>, All Rights Reserved.


import os               #@UnusedImport
import sys              #@UnusedImport
import unittest
import tempfile

from lib.utils import *     #@UnusedImport 
from lib import const

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testStringFuncs(self):

        self.assertRaises(ValueError, readable_form, -5)
        self.assertRaises(ValueError, readable_form, 50000000000000000000000000000000)
        self.assertEqual(readable_form(1024 * 5), "5.0KB")
        self.assertEqual(readable_form(5000), "4.0KB")
        self.assertEqual(readable_form(97 * 1024 * 1024), "97.0MB")
        self.assertEqual(readable_form(0), "0.0KB")
        self.assertEqual(readable_form(1024 * 1024 * 1.5), "1.5MB")
        f = from_readable_form("1.2KB")
        self.assertEqual(f[0], int(1.2 * 1024))
        self.assertEqual(f[2], "KB")
        f = from_readable_form("7.356TB")
        self.assertEqual(f[0], int(7.356 * 1024 * 1024 * 1024 * 1024))
        self.assertEqual(f[2], "TB")


        s = "".join([chr(i) for i in xrange(256)])
        self.assertEqual(s, unescape(escape(s)))

        u = u"".join([unichr(i) for i in xrange(1024)])
        self.assertEqual(u, unescape(escape(u)))
        self.assertTrue(isinstance(escape(u), unicode))
        self.assertTrue(isinstance(unescape(escape(u)), unicode))

        u = u"".join([unichr(i) for i in xrange(50000, 70000)])
        self.assertEqual(u, unescape(escape(u)))

        s = chr(10) + chr(11) + chr(12) + "abcd"
        esc = "%0A%0B%0Cabcd"
        self.assertEqual(esc, escape(s))


        self.assertEqual(splitall("///d/e/f/g"), ["d", "e", "f", "g"])
        self.assertEqual(ancestor_paths("///d/e/f/g"), ["/d", "/d/e", "/d/e/f", "/d/e/f/g"])

    def testDiskFuncs(self):
        self.assertTrue(du(os.path.join(const.AppDir, "..", "run", "files")) > 1000)
                        

        data = fs_space(".")
        self.assertTrue(len(data) == 3)
        f = maketempfile(12345)
        try:
            self.assertEqual(os.path.getsize(f), 12345)
        finally:
            os.remove(f)

    def testDirCmp(self):
        l = tempfile.mkdtemp()
        r = tempfile.mkdtemp()
        #    d1 is in both. d2 in left, d3 in right
        makedirs(os.path.join(l, "d1"))
        makedirs(os.path.join(l, "d2"))
        makedirs(os.path.join(r, "d1"))
        makedirs(os.path.join(r, "d3"))
        s1 = "1234"
        s2 = "5678"
        #    Focus on d1
        #    f1 in both, f2 in left, f3 in right. All same contents
        open(os.path.join(l, "d1", "f1"), "w").write(s1)
        open(os.path.join(l, "d1", "f2"), "w").write(s1)
        open(os.path.join(r, "d1", "f1"), "w").write(s1)
        open(os.path.join(r, "d1", "f3"), "w").write(s1)

        #    This file will appear in both, but be a different size
        open(os.path.join(l, "d1", "diff1"), "w").write(s1)
        open(os.path.join(r, "d1", "diff1"), "w").write(s1 + "b")
        #    This file will appear in both, same size, diff contents
        open(os.path.join(l, "d1", "diff2"), "w").write(s1)
        open(os.path.join(r, "d1", "diff2"), "w").write(s2)

        d = dircmp(l, r)
        self.assertEqual(d.left_list, set(["d1", "d2", "d1/f1", "d1/f2", "d1/diff1", "d1/diff2"]))
        self.assertEqual(d.right_list, set(["d1", "d3", "d1/f1", "d1/f3", "d1/diff1", "d1/diff2"]))

        self.assertEqual(d.left_only, set(["d2", "d1/f2"]))
        self.assertEqual(d.right_only, set(["d3", "d1/f3"]))

        self.assertEqual(d.common, set(["d1", "d1/f1", "d1/diff1", "d1/diff2"]))
        self.assertEqual(d.same_files, set(["d1/f1"]))
        self.assertEqual(d.diff_files, set(["d1/diff1", "d1/diff2"]))

    def testDirCmpUnicode(self):
        l = tempfile.mkdtemp()
        r = tempfile.mkdtemp()

        s1 = os.urandom(10)
        #    Focus on d1
        #    UNICODE
        unames = []
        for i in xrange(1024, 2048, 100):
            uname = u"".join([unichr(j) for j in xrange(i, i + 20)])
            unames.append(uname.encode(sys.getfilesystemencoding()))

        for uname in unames:
            uleft = os.path.join(l, uname)
            uright = os.path.join(r, uname)
            open(uleft, "w").write(s1)
            open(uright, "w").write(s1)

        unique = u"".join([unichr(j) for j in xrange(4096, 4110)]).encode()
        open(os.path.join(l, unique), "w").write(s1)

        d = dircmp(l, r)

        self.assertEqual(d.common, set(unames))
        self.assertEqual(d.left_only, set([unique]))

    def testPackages(self):
        l = get_packages()
        self.assertTrue(len(l) > 1000)
        
    def testCommaInt(self):
        self.assertEqual(comma_int(999), "999")
        self.assertEqual(comma_int(9999), "9,999")
        self.assertEqual(comma_int(99999), "99,999")
        self.assertEqual(comma_int(999999), "999,999")
        self.assertEqual(comma_int(999999999), "999,999,999")
        self.assertEqual(comma_int(123456789), "123,456,789")
        self.assertEqual(comma_int(1), "1")
        self.assertEqual(comma_int(0), "0")
        
    def testMemInfo(self):
        d = meminfo()
        self.assertTrue(d.MemTotal)
        self.assertTrue(d.MemTotal > 100*1024*1024)
        
    def testJoin(self):
        self.assertEqual(join_paths("a", "b"), "a/b")
        self.assertEqual(join_paths("a", "/b"), "a/b")
        self.assertEqual(join_paths("a", "b/"), "a/b/")
        self.assertEqual(join_paths("a", "", "c"), "a/c")
        self.assertEqual(join_paths("/a", "/b", "/c"), "/a/b/c")
        self.assertEqual(join_paths("a", "///b"), "a/b")
        self.assertEqual(join_paths("a/", "///b///", "c"), "a/b///c")


if __name__ == "__main__":
    unittest.main()
