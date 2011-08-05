# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import tempfile
from subprocess import Popen, PIPE
import re
import os

import const
import passphrase
from serializer import Serializer

#    Do last!
from lib.logger import Logger
log = Logger('library')

def update_crontab(bdict):
    '''
    Given a dictionary of backup entries, make the crontab
    entries for them all.
    
    @param bdict:
    '''
    log.trace("update_crontab", bdict)
    #    The cron entry's guards
    cronentry = "\n####Vault Starts#### (DO NOT EDIT)\n%s####Vault Ends####\n"
    #   Regex to extract the VAULT's cron entry
    cronregex = "^(.*)(.####Vault Starts.*Vault Ends####.)(.*)$"

    #    Get the old crontab
    crontab = Popen(["crontab", "-l"], stdout=PIPE).communicate()[0]

    #   Look for any old crontab entries
    m = re.match(cronregex, crontab, re.DOTALL)
    if m:
        #    Need to delete the old Vault crontab entry
        crontab = m.group(1) + m.group(3)
    #    Now add on our entry
    entries = "".join(
                    [bkp.cron_strings()
                     for bkp in bdict.itervalues()
                     if bkp.active])
    if len(entries) > 0:
        crontab = crontab + cronentry % entries

    #    Now apply the new crontab
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        log.debug("New crontab", crontab)
        tmp.write(crontab)
        tmp.close()
        proc = Popen(["crontab", tmp.name])
        ret = proc.wait()
        if ret != 0:
            log.error("Failed to save schedule", crontab)
            raise Exception(_("Error saving schedule: badly formatted crontab entry"))
    finally:
        os.remove(tmp.name)
    log.trace("Done update_crontab")


class Backup(Serializer):
    '''
    A backup object
    
    include_folders: (list) folders that will be examined recursively during backup.
    include_packages: (boolean) should we also backup the list of installed packages?
    store: (string) which store should we back up to.
    sched_type: (string) format is "<incr_type>/<full type>"
            Currently supported values are:
                daily/weekly
                daily/monthly
                hourly/weekly
                none/daily
                none/weekly
        OR
                custom
    sched_times: (string) 
            sched_times = 
                hh:mm/dow    inc time, dow for full
                hh:mm/dom    inc time, dom for full
                hh:mm/dom    time, dom for full, inc every hour
                hh:mm/*      time for full
                hh:mm/dow    time, dow for full
            OR (for custom)
                crontab\ncrontab
    '''
    def __init__(self, name=u"<blank>"):
        log.trace("***Backup.init", name)
        if len(name) == 0:
            raise Exception(_("You cannot have a blank backup"))
        if name[0] == "_":
            raise Exception(_("Backup names starting with '_' are reserved."))
        self.name = name
        self.active = True
        self.include_folders = []
        self.include_packages = False
        self.exclude_types = []
        self.exclude_patterns = [u"*/.local/share/Trash"]
        self.store = u""
        self.encrypt = False
        self.verify = False

        self.sched_type = u"daily/weekly"
        self.sched_times = u"19:30/Sun"

        self.notify_msg = True
        self.notify_email = False
        self.shutdown_after = False
        self.check()
        log.trace("Done Backup.init")


    def check(self):
        '''
        Checks the consistency of this backup. 
        '''
        if len(self.name) == 0:
            raise Exception(_("Backups cannot have a blank name"))
        if self.name == const.RecoveryFolder:
            raise Exception(_("The name %s is reserved and cannot used used for a backup") %
                            const.RecoveryFolder)
        if self.encrypt and not passphrase.passphrase:
            raise Exception(_("Cannot enable encryption when the passphrase is blank"))


    def __str__(self):
        return("Backup: name=%s active=%s include_folders=%s include_packages=%s exclude_types=%s exclude_patterns=%s store=%s encrypt=%s verify=%s sched_type=%s sched_times=%s" %
               (self.name, self.active, u"|".join(self.include_folders), self.include_packages, u"|".join(self.exclude_types),
                u"|".join(self.exclude_patterns), self.store, self.encrypt, self.verify, self.sched_type, self.sched_times))

    def cron_strings(self):
        '''
        Return a 2 line string in crontab format for running this
        backup.
         
        '''
        incr_entry = None
        full_entry = None
        if self.sched_type == "custom":
            incr, full = self.sched_times.split("\n")
            if incr.strip():
                incr_entry = incr.strip()
            if full.strip():
                full_entry = full.strip()
        else:
            time, day = self.sched_times.split("/")
            hour, min = time.split(":")
            if day == "*":
                day_no = -1     #    Wont be used
            elif day.isdigit():
                day_no = int(day)
            else:
                day_no = const.ShortDaysOfWeek.index(day)

            if self.sched_type == "daily/weekly":
                incr_entry = "%s %s * * %s" % (min, hour, self.exclusive_cron_string(0, 6, day_no))
                full_entry = "%s %s * * %d" % (min, hour, day_no)
            elif self.sched_type == "daily/monthly":
                incr_entry = "%s %s %s * *" % (min, hour, self.exclusive_cron_string(1, 31, day_no))
                full_entry = "%s %s %s * *" % (min, hour, day)
            elif self.sched_type == "hourly/weekly":
                incr_entry = "01 * * * *"
                full_entry = "%s %s * * %d" % (min, hour, day_no)
            elif self.sched_type == "none/daily":
                full_entry = "%s %s * * *" % (min, hour)
            elif self.sched_type == "none/weekly":
                full_entry = "%s %s * * %d" % (min, hour, day_no)
            else:
                raise Exception(_("This backup is corrupt. Invalid schedule type"))

        entry = ""
        if incr_entry:
            entry += incr_entry + " " + "%s backup --incremental \"%s\"\n" % \
                    (" ".join(const.ServerProgram), self.name)
        if full_entry:
            entry += full_entry + " " + "%s backup --full \"%s\"\n" % \
                    (" ".join(const.ServerProgram), self.name)
        return entry

    def exclusive_cron_string(self, start, end, excl):
        '''
        Return a CRON style string that includes start..end,
        but excludes the parameter excl.
        Note that start and end are INCLUSIVE.
        @param start:
        @param end:
        @param excl:
        '''
        if excl == start:
            return "%d-%d" % (excl + 1, end)
        if excl == start + 1:
            return "%d,%d-%d" % (start, excl + 1, end)
        elif excl == end:
            return "%d-%d" % (start, excl - 1)
        elif excl == end - 1:
            return "%d-%d,%d" % (start, excl - 1, end)
        else:
            return "%d-%d,%d-%d" % (start, excl - 1, excl + 1, end)
