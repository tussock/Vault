# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
'''
Created on Nov 10, 2010

@author: paul

Note message levels:

ERROR:    A serious error has occurred, usually fatal to the operation
WARN:     An error has occurred, but can be worked around
INFO:     Notification of major operation
DEBUG:    Low level notifications, helpful to find issues
TRACE:    Entry/Exit to every function.

Normally, you should run WARN.

'''
import cStringIO
import os
import sys
import ConfigParser
from datetime import datetime
import threading

cOutputs = ["stdout", "stderr", "null"]
cDefaultOutput = "stdout"
ALL, TRACE, DEBUG, INFO, WARN, ERROR = range(6)
cLevels = ["ALL", "TRACE", "DEBUG", "INFO", "WARN", "ERROR"]
cDefaultLevel = "WARN"
cDefaultFormat = "%(asctime)s - %(name)s - %(levelname)s - %(thread)s - %(message)s"

#    Global log manager object
logmgr = None

class LogDef():
    '''
    The definition of a log module.
    This is built from the config file, and is shared with each logger
    object.
    '''
    def __init__(self, name, output, level, format):
        self.name = name
        self.output = output
        self.level_str = level
        self.level = cLevels.index(level)
        self.format = format

        assert self.output in cOutputs, "Invalid output type"
        assert self.level >= 0, "Invalid level type"

        if self.output == "stdout":
            self.output_fn = self.stdout_out
        elif self.output == "stderr":
            self.output_fn = self.stderr_out
        elif self.output == "null":
            self.output_fn = self.null_out
        else:
            raise Exception("Undefined logger output function")

    def stdout_out(self, msg):
        print >> sys.stdout, msg

    def stderr_out(self, msg):
        print >> sys.stderr, msg

    def null_out(self, msg):
        pass


class LogManager():
    '''
    Sets up logging. Create this ONCE in the app. 
    '''
    def __init__(self, path=None):
        self.log_defs = {}
        self.add_logdef("default", cDefaultOutput, cDefaultLevel, cDefaultFormat)

        if path is None:
            try:
                #    No path provided - lets try to load a default.
                if os.path.exists("logger.conf"):
                    self.load_config("logger.conf")
            except:
                print("Failed to load default config")
        else:
            self.load_config(path)

        self.mutex = threading.RLock()

        #    Now save it where all loggers can get it.
        global logmgr
        logmgr = self

    def load_config(self, path):
        if not os.path.isfile(path):
            return
        config = ConfigParser.RawConfigParser()
        config.read(path)
        #    Load the names
        names = [s.strip() for s in config.get("modules", "names").split(",")]
        for name in names:
            section = "module:" + name
            if config.has_option(section, "output"):
                output = config.get(section, "output")
            else:
                output = cDefaultOutput

            if config.has_option(section, "level"):
                level = config.get(section, "level")
            else:
                level = cDefaultLevel

            if config.has_option(section, "format"):
                fmt = config.get(section, "format")
            else:
                fmt = cDefaultFormat
            self.add_logdef(name, output, level, fmt)

    def add_logdef(self, name, output=cDefaultOutput, level=cDefaultLevel, format=cDefaultFormat):
        self.log_defs[name] = LogDef(name, output, level, format)

class Logger():
    '''
    A logger object for a single module. 
    Points to the log_def for this module name/type.
    '''

    def __init__(self, name):
        global logmgr
        try:
            self.log_def = logmgr.log_defs[name]
        except:
            if not logmgr:
                LogManager()
            self.log_def = logmgr.log_defs['default']
            #    We dont provide any warning.
            #    That way, if there is no logging.conf, we are silent
            #self.warn(name + " is an undefined log module. Using default..")

    def trace(self, *args):
        if self.log_def.level <= TRACE:
            self.output(TRACE, *args)
            return True
        return False

    def debug(self, *args):
        if self.log_def.level <= DEBUG:
            self.output(DEBUG, *args)
            return True
        return False

    def info(self, *args):
        if self.log_def.level <= INFO:
            self.output(INFO, *args)
            return True
        return False

    def warn(self, *args):
        if self.log_def.level <= WARN:
            self.output(WARN, *args)
            return True
        return False

    def error(self, *args):
        if self.log_def.level <= ERROR:
            self.output(ERROR, *args)
            return True
        return False

    def output(self, level, *args):
        output = cStringIO.StringIO()
        for arg in args:
            print >> output, arg,
        contents = output.getvalue()

        d = {}
        d["asctime"] = datetime.isoformat(datetime.now())
        d["name"] = self.log_def.name
        d["levelname"] = cLevels[level]
        d["process"] = os.getpid()
        d["message"] = contents
        d["thread"] = threading.current_thread().name

        global logmgr
        logmgr.mutex.acquire()
        try:
            self.log_def.output_fn(self.log_def.format % d)
        finally:
            logmgr.mutex.release()


import unittest

class testLogger1(unittest.TestCase):
    testconf = """
[modules]
names=debug_name, warn_name, defs

[module:debug_name]
output=console
level=DEBUG

[module:warn_name]
level=WARN
output=null

[module:defs]
"""
    def setUp(self):
        self.conffile = "./test.conf"
        with open(self.conffile, "w") as f:
            f.write(self.testconf)
        LogManager(self.conffile)

    def tearDown(self):
        os.remove(self.conffile)


    def test1(self):
        wlog = Logger("warn_name")
        dlog = Logger("debug_name")
        self.assertFalse(wlog.debug("SHOULD NOT SEE THIS"))
        self.assertTrue(wlog.warn("Output an warn message"))

        dlog.error("Test message")


        pass
