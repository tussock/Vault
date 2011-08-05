#!/usr/bin/env python
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

from __future__ import print_function

from datetime import datetime
import argparse
import os
import sys

#    Need const for languages.
#    Since we have const - lets check root.
from lib import const
#    Check that the runner is root (unless debugging)
#    We need to do this early, because we may not have
#    access to any config files further down.
if not const.Debug:
    if not os.geteuid() == 0:
        #    We are going to crash
        sys.exit("The Vault must be run as root")


#    Set up translations
import locale
locale.setlocale(locale.LC_ALL, os.environ["LANG"])

import gettext
gettext.bindtextdomain(const.AppTitle, const.LocaleDir)
gettext.textdomain(const.AppTitle)
_ = gettext.gettext
gettext.install(const.AppTitle)

#    Do this first (of the app imports)
from lib.logger import LogManager
LogManager(const.LogFile)

#    This next line sets up defaults
from lib.config import Config
Config.get_config()

from lib.db import DB

from server.run import Run
from server.restore import Restore
from server.tester import Tester

#    Do this last!
from lib.logger import Logger
log = Logger("server")







def run():
    try:
        DB().check_upgrade()
        parser = argparse.ArgumentParser(description="Backup and restore files", prog=const.AppTitle)
        parser.add_argument("-d", "--dry-run", action="store_true",
                            help="This option will cause the program to print out what it would have done, " +
                            "without actually performing the action")
        parser.add_argument("-m", "--message", action="store_true",
                            help="Display a system notification when the action is complete. " +
                            "(If performing a backup, this will override the value in the backup definition)")
        parser.add_argument("-e", "--email", action="store_true",
                            help="Email when the action is complete. " +
                            "(If performing a backup, this will override the value in the backup definition)")
        parser.add_argument("-s", "--shutdown", action="store_true",
                            help="Shut down the computer when the action is complete. " +
                            "(If performing a backup, this will override the value in the backup definition)")
        sub = parser.add_subparsers(help="Type of action", title="Actions")

        #    The Backup options
        backup_parser = sub.add_parser("backup", help="Backup files and folders")
        group = backup_parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-f", "--full", action="store_true",
                           help="Do a full backup of all files specified by the backup name")
        group.add_argument("-i", "--incremental", action="store_true",
                           help="Only backup files that have changed since the last run of the given backup")
        backup_parser.add_argument("backupname", nargs="+",
                                   help="Name of the backup definition.")
        backup_parser.set_defaults(func=do_backup)

        #    The Restore options
        rest_parser = sub.add_parser("restore", help="Restore files and folders")
        rest_parser.add_argument("-w", "--when", metavar="datetime",
                                 help="Restore files/folders as at a given date and time. Format must be 'YYYY-MM-DDTHH:MM:SS'. If you dont specify this, " + \
                                 "the latest version of the file/folder will be used.")
        rest_parser.add_argument("-n", "--norecurse", default=False,
                          action="store_true",
                          help="By default, any folders listed will be recursively restored (i.e. all sub-folders, sub-sub-folders etc). " + \
                          "This option will cause only the contents of a listed folder to be restored, and not sub-folders. " + \
                          "It has no effect on files.")
        rest_parser.add_argument("destfolder",
                                 help="Destination folder - where to place all restored files.")
        rest_parser.add_argument("files", nargs="+",
                                 help="Files or folders to be backed up.")
        rest_parser.set_defaults(func=do_restore)

        #    The Test Options
        test_parser = sub.add_parser("test",
                                     help="Run a full test of the backup system")
        test_parser.add_argument("-c", "--cycles", metavar="cycles", default=5,
                                 help="How many iterations should the test run for.")
        test_parser.add_argument("-s", "--size", metavar="size", default="5MB",
                                 help="How large a test to run. " +
                                 "The format is [0-9]*(KB|MB|TB). For example: 512KB or 2MB. " +
                                 "Note that two stores will be created that are each 3x this size, plus the test data. " +
                                 "So you need 7x this space available. ")
        test_parser.add_argument("-S", "--store", metavar="store",
                                 help="By default, two 'Local Folder' stores are created. You can override this and have the tester " +
                                 "use a store you have already created/configured. Be warned that this store will be heavily used, and " +
                                 "all data inside it will be removed. " +
                                 "The store needs at least 3x the size.")
        test_parser.add_argument("testfolder", default="/tmp/tests",
                                 help="Test folder - a temporary folder used for all test files. All testdata is removed afterwards.")
        test_parser.set_defaults(func=do_test)

        options = parser.parse_args()
        options.func(options)
    except Exception as e:
        print("Error: ", str(e))

def do_backup(options):
    if options.full:
        backup_type = const.FullBackup
    else:
        backup_type = const.IncrBackup

    for name in options.backupname:
        try:
            r = Run(name, backup_type, options)
            r.run()
        except Exception as e:
            print("Failed: " + str(e))

def do_restore(options):
    try:
        if options.when:
            when = datetime.strptime(options.when, const.DateTimeFormat)
        else:
            when = None
    except:
        raise Exception("Invalid date format")

    r = Restore(options.destfolder, options.files, when, options)
    r.run()

def do_test(options):
    r = Tester(options.testfolder, options)
    r.run()


if not const.Debug:
    os.nice(const.Niceness)
if const.Profiling:
    import cProfile
    import pstats
    cProfile.run("run()", "BackupProfile")

    p = pstats.Stats('BackupProfile')
    p.strip_dirs().sort_stats("cumulative").print_stats()
else:
    run()
