# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
from datetime import datetime, timedelta
import os

import gui
from lib.db import DB
from lib import const
from lib.config import Config
from lib import utils
from historywindow import HistoryWindow
from storewizard import do_store_wizard
from backupwizard import do_backup_wizard
#    Do last!
from lib.logger import Logger
log = Logger('ui')

class OverviewPanel(gui.OverviewPanel):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        log.info("***OverviewPanel.init")
        
        gui.OverviewPanel.__init__(self, parent)
        self.db = DB()
        self.config = Config.get_config()

        self.update_data()
        self.image = wx.Bitmap(os.path.join(const.PixmapDir, "overview.png"))
        self.title = "Overview"
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_data, self.timer)
        #    Update the display every 30 seconds
        self.timer.Start(30000)
        log.trace("Done OverviewPanel.init")



    def update_data(self, event=None):
        '''
        Main update routine. Called by the refresh button and by the timer.
        @param event:
        '''

        self.update_status()
        self.update_details()
        self.update_stores()
        self.Fit()

    def update_status(self):
        '''
        Update the status display. Uses a heuristic to decide if we are in an error
        or warning state.
        '''
        status, messages = self.calculate_status()
        if status == const.SystemStateError:
            self.imgStatus.SetBitmap(
                                     wx.Bitmap(os.path.join(const.PixmapDir, "status-fail.png"), 
                                               wx.BITMAP_TYPE_PNG)
                                     )
            self.lblStatus.SetLabel(_("Error"))
        elif status == const.SystemStateWarn:
            self.imgStatus.SetBitmap(
                                     wx.Bitmap(os.path.join(const.PixmapDir, "status-warn.png"), 
                                               wx.BITMAP_TYPE_PNG)
                                     )
            self.lblStatus.SetLabel(_("Warning"))
        else:
            self.imgStatus.SetBitmap(
                                     wx.Bitmap(os.path.join(const.PixmapDir, "status-ok.png"), 
                                               wx.BITMAP_TYPE_PNG)
                                     )
            self.lblStatus.SetLabel(_("Healthy"))

        self.lblMessages.SetLabel("\n".join(messages))


    def calculate_status(self):
        '''
        The heuristic for warning and errors states.
        Choose the *worst* condition and return that.

        The Heuristic is:
        #    backup should be hourly, and its been 1 day since last successful run, OR
        #    backup should be daily, at its been 5 days since last successful run. OR
        #    backup should be weekly and its been 2 weeks since last successful run
        '''
        messages = []
        state = const.SystemStateOK

        #    Check for any active backups in an error status.
        runs = self.db.run_states()
        for backup in self.config.backups.itervalues():
            if backup.name in runs and backup.active:
                run = runs[backup.name]
                #    It HAS run and its active:
                if run.status == const.StatusFailed:
                    messages.append(_("Backup %s last run failed") % backup.name)
                    state = max(state, const.SystemStateError)

        #    For each backup, check if its been tool long since last run.
        for backup in self.config.backups.itervalues():
            #    For each backup
            if backup.active:
                #    Look at only active backups
                if not backup.name in runs:
                    messages.append(_("Backup %s marked active but has never run") % backup.name)
                    state = max(state, const.SystemStateWarn)
                else:
                    run = runs[backup.name]
                    last_run = run.start_time
                    now = datetime.now()
                    timesince = now - last_run
                    if backup.sched_type == "custom":
                        #    Cannot check these at the moment
                        pass
                    else:
                        incr, full = backup.sched_type.split("/")
                        if incr == "hourly" and timesince > timedelta(hours=24):
                            messages.append(_("Backup {backup} should run hourly, but has not run in {hours} hours").format(
                                            backup=backup.name, hours=timesince.seconds // 3600))
                            state = max(state, const.SystemStateWarn)
                        if (incr == "daily" or full == "daily") and timesince > timedelta(days=5):
                            messages.append(_("Backup {backup} should run daily, but has not run in {days} day(s)").format(
                                            backup=backup.name, days=timesince.days))
                            state = max(state, const.SystemStateWarn)
                        if (incr == "weekly" or full == "weekly") and timesince > timedelta(weeks=2):
                            weeks = timesince.days // 7
                            messages.append(_("Backup {backup} should run weekly, but has not run in {weeks} week(s)").format(
                                            backup=backup.name, weeks=weeks))
    
                            state = max(state, const.SystemStateWarn)
        #    If there are no active backups - that too is a warning.
        if len([backup for backup in self.config.backups.itervalues() if backup.active]) == 0:
            state = max(state, const.SystemStateWarn)
            messages.append(_("There are no active backups, so nothing will be backed up"))
        return (state, messages)

    def update_details(self):
        '''
        Update backup detail display.
        '''
        if len(self.config.backups) == 0:
            self.lstBackups.Hide()
            self.lblNoBackups.Show()
        else:
            self.lblNoBackups.Hide()
            self.lstBackups.Show()
            self.lstBackups.DeleteAllColumns()
            self.lstBackups.DeleteAllItems()
            self.lstBackups.InsertColumn(0, _("Name"))
            self.lstBackups.InsertColumn(1, _("State"))
            self.lstBackups.InsertColumn(2, _("Last Run"))
            runs = self.db.run_states()
            for bname, backup in self.config.backups.iteritems():
                active = _("Active") if backup.active else _("Inactive")
                if bname in runs:
                    run = runs[bname]
                    if run.status == const.StatusFailed:
                        msg = ("Ran %s, failed") % run.start_time_str
                    elif run.status == const.StatusRunning:
                        msg = _("Running now, started {time}").format(time=run.start_time_str)
                    else:
                        msg = _("Ran {time}, saved {files} files, compressed size {size}").format(
                            time=run.start_time_str, files=run.nfiles, size=utils.readable_form(run.size))
#                    line = "%s: last run %s, backed up %d files, total size %s" % (bname, run.start_time_str, run.nfiles, utils.readable_form(run.size))
                else:
                    msg = _("Never run")
                self.lstBackups.Append([bname, active, msg])

            self.lstBackups.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.lstBackups.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.lstBackups.SetColumnWidth(2, wx.LIST_AUTOSIZE)

            return

    def update_stores(self):
        '''
        Update store detail display.
        
        Note that the size is gleaned from the sum of all runs, 
        PLUS (because running runs have size 0)
            the sum of all files in a running run.
        '''
        log.trace("update_stores")
        if len(self.config.storage) == 0:
            self.lstStores.Hide()
        else:
            self.lblNoStores.Hide()
            self.lstStores.DeleteAllColumns()
            self.lstStores.DeleteAllItems()
            self.lstStores.InsertColumn(0, _("Name"))
            self.lstStores.InsertColumn(1, _("Space"))
            self.lstStores.InsertColumn(2, _("Used"))

            #    Includes runs that have completed.
            uses = self.db.store_usages()
            
            log.debug("Update Stores: uses=", uses)
            
            for sname, store in self.config.storage.iteritems():
                if sname in uses:
                    used = uses[sname].size
                else:
                    used = 0

                self.lstStores.Append([store.name,
                                       _("Unlimited") if not store.auto_manage else store.limit,
                                       utils.readable_form(used)])

            self.lstStores.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.lstStores.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.lstStores.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        log.trace("completed update_stores")


    def onHistory(self, event):
        self.hist_window = HistoryWindow(self)

    def onRefresh(self, event):
        self.update_data()

    def onSetupStore(self, event):
        do_store_wizard(self)

    def onSetupBackup(self, event):
        do_backup_wizard(self)

