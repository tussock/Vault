# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Constants that will remain unchanged
This is loaded first off all application imports
Must not depend on anything else (apart from os and sys).
'''
from __future__ import division, with_statement, print_function
import os

#    Are we debugging. NOTE: this is changed below after the appdir
#    is calculated.
Debug = False            #    Running in a live system (config in /etc)
Profiling = False       #    Profile the application on exit
FailureTest = True     #    Not used at the moment.


#    The description can be i18n'd
AppTitle = "Vault"
PackageName = "vault"
Description = "Backups for the rest of us!"
Author = "Paul Reddy"
Copyright = "(c) 2011 Paul Reddy <paul@kereru.org>"
Version = "1.0.2"


####################################################################
#
#    Default Locations
#
####################################################################

#    App is installed one folder above this file's folder
AppDir = os.path.dirname(os.path.dirname(__file__))
RunDir = AppDir

#    If we are running in the home folder, then debugging will be enabled.
if AppDir.startswith("/home"):
    Debug = True
    

#    Config directory. MUST BE A FIXED LOCATION
ConfigDir = os.path.join("/etc", PackageName)
#    Database directory. MUST BE A FIXED LOCATION
DataDir = "/var/backups"
#    This is the standard location for help
HelpDir = os.path.join("/usr/share/gnome/help", PackageName, "C")
#    Where are the language files
LocaleDir = os.path.join(AppDir, "i18n")

if Debug:
    VaultDir = os.path.dirname(AppDir)    
    RunDir = os.path.join(VaultDir, "run")
    ConfigDir = os.path.join(RunDir, "config")
    DataDir = os.path.join(RunDir, "data")
    HelpDir = os.path.join(VaultDir, "help/C")


HelpFile = "vault.xml"
HelpPath = os.path.join(HelpDir, HelpFile)
HelpViewer = "yelp"

ConfigName = "vault.conf"
ConfigFile = os.path.join(ConfigDir, ConfigName)
DataName = "vault.db"
DataFile = os.path.join(DataDir, DataName)
EncryptionSuffix = ".enc"
PackageFile = "packages"
UIProgram = ["vault"]
ServerProgram = ["vault_svr"]
if Debug:
    #    We actually run using python.
    #UIProgram = ["python", os.path.join(AppDir, "vault.py")]
    #ServerProgram = ["python", os.path.join(AppDir, "vault_svr.py")]
    UIProgram = ["python", os.path.join("/home/paul/Dev/Vault/bin", "vault")]
    ServerProgram = ["python", os.path.join("/home/paul/Dev/Vault/bin", "vault_svr")]
    
StoreMarkerFile = "_store_"
RecoveryFolder = "_recovery_"
#    The first file holds the version
RecoveryFiles = ["recovery.py", "recoveryui.py"]
RecoveryVersionFile = "recovery.py"
LOFFile = "lof"

LogName = "logger.conf"
LogFile = os.path.join(ConfigDir, LogName)

if Debug:
    VaultDir = os.path.dirname(AppDir) 
    PixmapDir = os.path.join(VaultDir, "pixmaps")
else:
    PixmapDir = os.path.join("/", "usr", "share", "vault", "pixmaps")


####################################################################
#
#    Static Values/Tuning
#
####################################################################

#    NOTE: these need to be in the order to match Cron. 0 == Sunday
DaysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
ShortDaysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
def ToShortDOW(dow):
    return ShortDaysOfWeek[DaysOfWeek.index(dow)]
DaysOfMonth = ["%.02d" % i for i in xrange(1, 32)]
#    Gives me 00:00 - 23:30
HoursOfDay = ["%02d:%02d" % (h, m) for h in range(24) for m in [0, 30]]

#    Sizes
Kilobyte = 1024
Megabyte = 1024 * 1024
Gigabyte = 1024 * 1024 * 1024
Terabyte = 1024 * 1024 * 1024 * 1024
Petabyte = 1024 * 1024 * 1024 * 1024 * 1024
Exabyte = 1024 * 1024 * 1024 * 1024 * 1024 * 1024
#    Units of measurement - disk size
DiskUnits = ["MB", "GB", "TB", "PB"]



FullBackup = "Full"
IncrBackup = "Incremental"

StatusSuccess = "Success"
StatusFailed = "Failed"
StatusRunning = "Running"

Daily = 0
Weekly = 1
Monthly = 2

DestLocal = 0
DestFTP = 1
DestShare = 2

SystemStateOK = 0
SystemStateWarn = 1
SystemStateError = 2

#    Any longer than this, and the server is seriously 
#    compromised
FTPTimeout = 20

#    How many retries on data transfers
Retries = 1

#    Files are always split along <2GB chunks, in case
#    we are targetting FAT32 file systems.
#    Also makes it easier to resize.
#    So we use relatively small chunks, and put them in folders.
#    QueueSize is how many Chunks we can have queued up at a time
#    before we block.
if Debug:
    ChunkSize = 10 * Kilobyte
    ChunksPerFolder = 5
    QueueSize = 2
else:
    ChunkSize = 20 * Megabyte
    ChunksPerFolder = 100
    QueueSize = 2

#    We always ensure there is space for at least two chunks to be written.
MinSpaceAvail = 2*ChunkSize


#    How much will we attempt to read/write at a time. (1m)
if Debug:
    BufferSize = 10 * Kilobyte
else:
    BufferSize = 1 * Megabyte

if Debug:
    FSCacheSize = 5
else:
    FSCacheSize = 500

#    Minimum size of a Storage area
if Debug:
    MinStoreSize = 1 * Megabyte
else:
    MinStoreSize = 10 * Megabyte




DateTimeFormat = "%Y-%m-%dT%H:%M:%S"
ShortDateFormat = "%x"
ShortTimeFormat = "%X"
ShortDateTimeFormat = "%x %X"

EmailFormat = "([a-zA-Z-_.0-9]+)@([a-zA-Z-_.0-9]+)"

#    The server NICE's itself to reduce impact on system performance.
Niceness = 10

#    Sort Orders
ASC = 1
DESC = 2

#    Is this the first time we have run the program?
FirstTime = False

