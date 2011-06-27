# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import tempfile
import stat
import os
import re

from subprocess import Popen, PIPE
import binascii
import filecmp
import commands
from timer import Timer


class PipeWrap():
    '''
    A class that represents an os.pipe, but
    presents it in a file-like object
    
    The read and write function are called on this
    object. Its assumed to be one way
    '''
    def __init__(self):
        self.readp, self.writep = os.pipe()

    def closewriter(self):
        '''
        Close the writer, should close the reader.
        '''
        os.close(self.writep)

    def close(self):
        '''
        Close the writer, should close the reader.
        '''
        os.close(self.writep)

    def closereader(self):
        '''
        Close the reader, should signal the writer.
        '''
        os.close(self.readp)

    def read(self, bytes= -1):
        return os.read(self.readp, bytes)

    def write(self, bytes):
        os.write(self.writep, bytes)


def secure_file(path):
        '''
        Secure a file as best we can. 
        We ensure we own it, and that it is read/write only by us.
        
        Exceptions are passed up to the caller to deal with.
        '''
        #    Make sure the config file is owned by me (usually root).
        #    This should fail if the config file is owned by root, and
        #    a normal user tries running the program.
        os.chown(path, os.getuid(), os.getgid())
        #    Make sure the config file has the right privileges. 
        #    It needs to be protected because it may contain passwords.
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

class dircmp():
    '''
    A unicode supported, cut down dircmp class
    '''
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self._left_only = None
        self._right_only = None
        self._left_list = None
        self._right_list = None
        self._same_files = None
        self._diff_files = None
    @property
    def left_only(self):
        '''
        Files/folders that are only in the left directory
        '''
        if self._left_only is None:
            self.build_file_list()
        return self._left_only
    @property
    def right_only(self):
        '''
        Files/folders that are only in the right directory
        '''
        if self._left_only is None:
            self.build_file_list()
        return self._right_only
    @property
    def left_list(self):
        '''
        The complete list of files/folders in the left directory
        '''
        if self._left_only is None:
            self.build_file_list()
        return self._left_list
    @property
    def right_list(self):
        '''
        The complete list of files/folders in the right directory
        '''
        if self._left_only is None:
            self.build_file_list()
        return self._right_list
    @property
    def common(self):
        '''
        A set of tuples 
        '''
        if self._left_only is None:
            self.build_file_list()
        return self._common

    #    The following are expensive. Only build if necessary
    @property
    def same_files(self):
        if self._same_files is None:
            self.build_file_compares()
        return self._same_files

    @property
    def diff_files(self):
        if self._same_files is None:
            self.build_file_compares()
        return self._diff_files

    def build_file_list(self):
        '''
        Create the left and right lists, plus the differences.
        '''
        self._left_list = self.build_list(self.left)
        self._right_list = self.build_list(self.right)
        self._left_only = self._left_list.difference(self._right_list)
        self._right_only = self._right_list.difference(self._left_list)
        self._common = self._left_list.intersection(self._right_list)

    def build_list(self, path):
        '''
        Create and return a set of all files and folders under a given path.
        @param path:
        '''
        l = set()
        for dir, folders, files in os.walk(path):
            d = dir[len(path) + 1:]
            for name in folders:
                l.add(os.path.join(d, name))
            for name in files:
                l.add(os.path.join(d, name))
        return l

    def build_file_compares(self):
        '''
        For every *file* that exists in both left and right, 
        compare them.
        
        Will build a same list and difference list. 
        A byte by byte compare is used if the files are the same size.
        '''
        self._same_files = set()
        self._diff_files = set()
        for file in self._common:
            left = os.path.join(self.left, file)
            right = os.path.join(self.right, file)
            if os.path.isfile(left) and os.path.isfile(right):
                if os.path.getsize(left) != os.path.getsize(right):
                    #    Diff size, must be different
                    self._diff_files.add(file)
                else:
                    #    Same size. Check contents
                    if filecmp.cmp(left, right, shallow=0):
                        self._same_files.add(file)
                    else:
                        self._diff_files.add(file)


class meminfo():
    def __init__(self):
        ps = Popen(['cat', '/proc/meminfo'], stdout=PIPE).communicate()[0]
        rows = ps.split('\n')
        sep = re.compile('([^:]*):\s+([0-9]*).*')
        for row in rows:
            m = re.match(sep, row)
            if m:
                name = m.group(1)
                value = m.group(2)
                self.__dict__[name] = int(value)*1024

def makedirs(path):
    '''
    Identical to os.makedirs, but will not raise an exception 
    if the directory exists.
    @param path:
    '''
    if not os.path.isdir(path):
        os.makedirs(path)

def maketempfile(size=1024, dir=None):
    '''
    Create a temporary file in the system temp file space.
    If you pass in a folder, the temporary file will be made there. 
    Fill it with an appropriate amount of random junk.
    Then close it and return its path. 
    
    @param size:
    @param dir:
    '''
    fp = tempfile.NamedTemporaryFile(mode="w+b", delete=False, dir=dir)
    fp.write(os.urandom(size))
    fp.close()
    return fp.name

def path_to_unicode(path):
    '''
    Try a number of encodings to get a path converted from
    whatever encoding it has, to Unicode.
    
    @param path:
    '''
    try:
        return path.decode("utf-8")
    except:
        try:
            return path.decode("cp1252")
        except:
            try:
                return path.decode("ascii")
            except:
                try:
                    return path.decode("latin-1")
                except:
                    #    Unknown encoding!
                    return path
                
def build_file_structure(root, filesize, totalsize):
    '''
    Breadth first recursive file/folder creation.
    Stops when it reaches the appropriate maximum size
    Each file is filled with the same random data.
    
    @param test_folder:
    '''
    remaining = totalsize
    contents = os.urandom(filesize)
    list = [root]
    done = False
    while not done:
        newlist = []
        for folder in list:
            makedirs(folder)
            for dname in ["dir1", "dir2", "dir3"]:
                path = os.path.join(folder, dname)
                newlist.append(path)
            for fname in ["f1.avi", "f2.mp3", "f3.exe", "f4.txt"]:
                path = os.path.join(folder, fname)
                with open(path, "w") as f:
                    f.write(contents)
                remaining -= filesize
                #    Check after each file for hitting size limits
                if remaining <= 0:
                    done = True
                    break
            if remaining <= 0:
                done = True
                break
        list = newlist

    return

def ancestor_paths(path):
    '''
    Given a path, will return all ancestors.
    So for /A/B/C/D.dd
    it will return
        /A, /A/B, /A/B/C, /A/B/C/D.dd
    
    For A/B/C it will return
        A, A/B, A/B/C
        
    @param path:
    '''
    if path == "":
        return []
    paths = splitall(path)
    pathtree = []
    curpath = "/" if path[0] == "/" else ""
    for p in paths:
        curpath = os.path.join(curpath, p)
        pathtree.append(curpath)
    return pathtree

def splitall(path):
    '''
    Given a path, return all components of that path, in order.
    
    @param path:
    '''
    path = os.path.normpath(path)
    paths = []
    while path != os.sep and path != "":
        path, name = os.path.split(path)
        paths.insert(0, name)

    return paths

SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
cLimitRE = "([0-9]+([.][0-9]+)?)([KMGTPEZY]B)"

def readable_form(size):
    '''Convert a file size to human-readable form.                          

    Keyword arguments:
    size -- file size in bytes

    Returns: string

    '''
    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024
    for suffix in SUFFIXES:
        size /= multiple
        if size < multiple:
            return '{0:.1f}{1}'.format(size, suffix)

    raise ValueError('number too large')

def from_readable_form(size_str):
    '''
    Convert a string to a number.
    The string must be in the form <num><units>.
    Units are one of KB, MB, GB, TB, ...
    Num is of the form 0-9+(.[0-9]*), so 3, 3.0, 3.65 etc.
    
    Returns an integer
    @param size_str:
    '''
    m = re.match(cLimitRE, size_str)
    if not m:
        raise Exception("Invalid number format (%s)" % size_str)
    num = m.group(1)
    units = m.group(3)
    if not units in SUFFIXES:
        raise Exception("Invalid units")
    units_idx = SUFFIXES.index(units)
    total = float(num) * 1024
    for _ in xrange(units_idx):
        total = total * 1024
    total = int(total)
    return (total, num, units)


def comma_int(number):
    '''
    Convert an INT into a string, with locale correct 
    thousands separator. 
    @param number:
    @param sep:
    '''
    import locale
    locale.setlocale(locale.LC_ALL, "")
    return locale.format("%d", number, grouping=True)


def fs_space(path):
    '''
    Given a path, return the size, used, avail for the file
    system that the path resides in.

    df -h <path>
    Filesystem            Size  Used Avail Use% Mounted on
    <device>              917G  666G  205G  77% <mount point>

    
    @param path:
    @type path:
    
    Returns tuple containing:
        size, used, avail
    '''
    proc = Popen(["df", "-h", path], stdout=PIPE)
    output = proc.communicate()[0]
    #    Split into lines.
    lines = output.split('\n')
    if len(lines) < 2:
        raise Exception("df failed - perhaps %s not mounted?" % path)

    items = lines[1].split(" ")
    #    Remove the blanks
    items = [item for item in items if item.strip() != ""]

    if len(items) < 6:
        raise Exception("Invalid df output (%s)" % output)
    return (items[1], items[2], items[3])

def du(path):
    proc = Popen(["du", "-sb", path], stdout=PIPE)
    output = proc.communicate()[0]
    #    One line, "size path"
    size = output.split("\t")[0]
    return int(size)

def get_packages():
    '''
    Return a list containing the currently installed packages
    
    This is created using dpkg --list-selections with only
    the "install" packages included.
    '''
    (status, output) = commands.getstatusoutput("dpkg --get-selections")
    if status != 0:
        raise Exception(_("Failed to retrieve package list"))
    l = []
    for line in output.split("\n"):
        fields = line.split()
        if len(fields) == 2 and fields[1] == "install":
            l.append(fields[0])
    return l

class _defaultdict(dict):
    def __getitem__(self, x):
        '''
        This will ensure that getitem always returns a value.
        If the value does not exist in the dict (i.e. there is no safe mapping)
        then we just return the character unchanged.
        @param x:
        '''
        try:
            return dict.__getitem__(self, x)
        except:
            return x

_safemap = _defaultdict()
for i in range(256):
    c = chr(i)
    _safemap[c] = c if i > 20 and i <= 127 and c != "%" and c != "," else ('%%%02X' % i)
_displaymap = _defaultdict()
for i in range(256):
    c = chr(i)
    _displaymap[c] = c if i > 20 and i <= 127 else ('%%%02X' % i)
_usafemap = _defaultdict()
for i in range(256):
    c = unichr(i)
    _usafemap[c] = c if i > 20 and i <= 127 and c != "%" and c != "," else ('%%%02X' % i)
_udisplaymap = _defaultdict()
for i in range(256):
    c = unichr(i)
    _udisplaymap[c] = c if i > 20 and i <= 127 else ('%%%02X' % i)


def escape(s):
    '''
    This escapes all special characters in a string
    and is reversable using unescape.

    Sort of copied from the python urllib code, but changed
    to support unicode.
    
    @param s:
    '''
    if isinstance(s, unicode):
        mapping = _usafemap
    else:
        mapping = _safemap
    ret = map(mapping.__getitem__, s)
    return "".join(ret)

def display_escape(s):
    '''
    Escape a string so that it is suitable for display.
    Note that we leave '%' alone. This is *not* reversable using unescape
    and is for display only.

    Sort of copied from the python urllib code, but changed
    to support unicode.    
    
    @param s:
    '''
    if isinstance(s, unicode):
        mapping = _udisplaymap
    else:
        mapping = _displaymap
    ret = map(mapping.__getitem__, s)
    return "".join(ret)

#    _hextochr is a mapping of XX to chr(XX).
_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a + b, chr(int(a + b, 16))) for a in _hexdig for b in _hexdig)

def unescape(s):
    """unquote('abc%20def') -> 'abc def'."""
    res = s.split('%')
    for i in xrange(1, len(res)):
        item = res[i]
        try:
            res[i] = _hextochr[item[:2]] + item[2:]
        except KeyError:
            res[i] = '%' + item
        except UnicodeDecodeError:
            res[i] = unichr(int(item[:2], 16)) + item[2:]
    return "".join(res)


#def unescape(s):
#    '''
#    Undoes an escape to return the original string.
#    @param s:
###    '''
#    
#    return s.decode("quopri_codec")

def crc(path):
    with open(path, "rb") as f:
        data = f.read(10240)
        crc = binascii.crc32(data)
        while data:
            data = f.read(10240)
            crc = binascii.crc32(data, crc)
    return crc

def join_paths(*paths):
    '''
    Join a set of paths together.
    
    This differs from os.path.join in that a '/' does not cause
    the path to reset.
        os.path.join("a", "/b") == /b
        join__paths("a", "/b") == a/b
    '''
    ps = []
    for path in paths:
        if len(ps) == 0:
            #    Its ok for the first element to start with '/'
            ps.append(path)
        else: 
            while len(path) > 0 and path[0] == os.sep:
                #    Any other element that starts with '/' has the '/' removed 
                path = path[1:]
            ps.append(path)
    return os.path.join(*ps)