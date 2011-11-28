# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import wx
import os
#    DNS is a third party library we include.
#import dns.resolver

import gui
from lib import utils
from lib.config import Config
from lib import const
from lib.backup import Backup, update_crontab
from lib import dlg
from lib.db import DB
from optiondialog import OptionDialog
from runbackupwindow import RunBackupWindow
from historywindow import HistoryWindow
from editpanel import EditPanel, ViewState, NewState
from progressdialog import ProgressDialog
import app

EmptyName = _("<blank>")

#    Do last!
from lib.logger import Logger
log = Logger('ui')

class BackupPanel(EditPanel, gui.BackupPanel):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        log.info("***BackupPanel.init")
        gui.BackupPanel.__init__(self, parent)
        self.btnAddFolder.SetBitmapLabel(wx.Bitmap(os.path.join(const.PixmapDir, "add.png")))
        
        self.db = DB()
        self.config = Config.get_config()

        self.state = ViewState
        self.update_data(False)
        self.nbBackup.SetSelection(0)
        self.clear()
        self.nbBackup.Layout()
        self.Fit()
        self.radSchedDailyWeekly.SetValue(True)

        if self.lstItems.GetCount() > 0:
            self.lstItems.SetSelection(0)
            self.onItemSelected(None)
#        self.onNotifyEmail(None)
        self.image = wx.Bitmap(os.path.join(const.PixmapDir, "backup.png"))
        self.title = _("Backups")

        self.onBackupSchedule(None)
        log.trace("Done BackupPanel.init")



    def update_data(self, set_selection=True):
        #    The next line should be 
        #        for child in self.pnlScheduleTab.GetChildren():
        #            if child.GetName().find("cboTime") == 0:
        #    but there is a bug in wxFormBuilder. It doesn't set the name attribute.
        #    See http://sourceforge.net/tracker/?func=detail&aid=3187563&group_id=135521&atid=733136
        for name in dir(self):
            if name.find("cboTime") == 0:
                child = self.__getattribute__(name)
                child.Clear()
                child.AppendItems(const.HoursOfDay)
                child.SetSelection(0)

            if name.find("cboDay") == 0:
                child = self.__getattribute__(name)
                child.Clear()
                child.AppendItems(const.ShortDaysOfWeek)
                child.SetSelection(0)

            if name.find("cboMonthDay") == 0:
                child = self.__getattribute__(name)
                child.Clear()
                child.AppendItems([str(i) for i in xrange(1, 32)])
                child.SetSelection(0)

        self.txtFolders.Clear()

        self.lstExcludeTypes.Clear()
        self.lstExcludeTypes.AppendItems(self.config.file_types.keys())

        #    Lets update this in a smart fasion. Need to keep the current selection if possible
        old_sel = self.cboStore.GetStringSelection()
        self.cboStore.Clear()
        self.cboStore.AppendItems(self.config.storage.keys())
        self.cboStore.SetStringSelection(old_sel)

        #    Lastly - lets reload the backup list
        self.update_backup_list(set_selection)

    def update_backup_list(self, set_selection=True):
        sel = self.lstItems.GetStringSelection()
        #    Look for new items
        backups = self.lstItems.GetItems()
        keys = self.config.backups.keys()
        keys.sort()
        for item in keys:
            if not item in backups:
                #    new item becomes selected (hopefully the first)
                sel = item
                break

        self.lstItems.Clear()
        self.lstItems.AppendItems(keys)

        if set_selection:
            self.lstItems.SetStringSelection(sel)
            self.onItemSelected(None)


######################################################################3
#
#        EVENTS
#
######################################################################3


    def onHistory(self, event):
        name = self.lstItems.GetStringSelection()
        if len(name) > 0:
            self.history(name)

    def onRun(self, event):
        name = self.lstItems.GetStringSelection()
        if len(name) > 0:
            self.run_backup(name)


    def onAddFolder(self, event):
        dlog = wx.DirDialog(self, _("Select a folder to back up"), "/home")
        ret = dlog.ShowModal()
        if ret == wx.ID_OK:
            folders = self.text_to_list(self.txtFolders.GetValue())
            folders.append(dlog.GetPath())
            self.txtFolders.Clear()
            self.txtFolders.AppendText("\n".join(folders))

    def onBackupSchedule(self, event):
        if self.radSchedAdvanced.GetValue():
            self.pnlAdvanced.Show()
        else:
            self.pnlAdvanced.Hide()


######################################################################
#
#        Save and Load
#
######################################################################
    def update_state(self):
        if self.state == ViewState:
            self.lblName.Show(True)
            self.txtName.Show(False)
        if self.state == NewState:
            self.lblName.Show(False)
            self.txtName.Show(True)
        self.onBackupSchedule(None)
        self.Fit()
        self.Refresh()

    def clear(self):
        b = Backup(EmptyName)
        self.show_backup(b)
        self.nbBackup.SetSelection(0)

    def delete(self, name):
        #    Lets get some statistics
        runs = self.db.runs(backupname=name)
        num_runs = len(runs)
        size = 0
        for run in runs:
            size += run.size

        if num_runs > 0:
            msg = _("Backup '{backup}' has {numruns} runs stored, " \
                    "totalling {size} of remote data.\n" \
                    "Are you sure you want to delete the backup definition?\n" \
                    "(hint - its usually better to just deactivate the backup)").format(\
                    backup=name, numruns=num_runs, size=utils.readable_form(size))
            mbox = OptionDialog(self, msg, _("Delete Backup Definition"),
                                _("Also delete all backup data stored remotely\nNote that this cannot be undone."))
            if mbox.ShowModal() != wx.ID_OK:
                return
            delete_offsite_data = mbox.chkOption.GetValue()

        else:
            msg = _("Backup '{backup}' has never run. Are you " \
                    "sure you want to delete the backup definition?").format(backup=name)
            if dlg.OkCancel(self, msg, _("Confirm Delete")) != wx.ID_OK:
                return
            delete_offsite_data = False


        with ProgressDialog(self, _("Deleting"), 
                            _("Deleting backup %s%s.\nPlease wait...") % 
                            (name, " and all offsite data" if delete_offsite_data else "")):
            self.delete_backup(name, delete_offsite_data)
            import time
            time.sleep(3)
        self.clear()
        self.state = ViewState
        app.broadcast_update()



    def show(self, name):
        try:
            backup = self.config.backups[name]
            self.state = ViewState
            self.show_backup(backup)
        except Exception as e:
            #   Missing backup!
            dlg.Warn(self, _("The backup '{backup}' seems to be corrupt. {error}").format(backup=name, error=str(e)))
#            self.update_backup_list()
#            self.state = ViewState
#            self.clear()


    def show_backup(self, b):

        #    General Information
        self.txtName.SetValue(b.name)
        self.lblName.SetLabel(b.name)

        self.chkActive.SetValue(b.active)

        #    Folder Information
        self.txtFolders.Clear()
        self.txtFolders.AppendText("\n".join(b.include_folders))
        self.chkPackages.SetValue(b.include_packages)
        #    Exclusions
        self.lstExcludeTypes.SetCheckedStrings(b.exclude_types)
        self.txtExcludePatterns.Clear()
        self.txtExcludePatterns.AppendText("\n".join(b.exclude_patterns))

        #    Destination        
        self.cboStore.SetStringSelection(b.store)

        self.chkEncrypt.SetValue(b.encrypt)
        self.chkVerify.SetValue(b.verify)

        #    Schedule
        if b.sched_type == "custom":
            self.radSchedAdvanced.SetValue(True)
            incr, full = b.sched_times.split("\n")
            self.txtCronIncr.SetValue(incr)
            self.txtCronFull.SetValue(full)
        else:
#            itime, dummy = incr.split("/")       # iday not used
#            ftime, fday = full.split("/")
            time, day = b.sched_times.split("/")
            if b.sched_type == "daily/weekly":
                self.radSchedDailyWeekly.SetValue(True)
                self.cboTime1.SetStringSelection(time)
                self.cboDay1.SetStringSelection(day)
            elif b.sched_type == "daily/monthly":
                self.radSchedDailyMonthly.SetValue(True)
                self.cboTime2.SetStringSelection(time)
                self.cboMonthDay2.SetStringSelection(day)
            elif b.sched_type == "hourly/weekly":
                self.radSchedHourlyWeekly.SetValue(True)
                self.cboTime3.SetStringSelection(time)
                self.cboDay3.SetStringSelection(day)
            elif b.sched_type == "none/daily":
                self.radSchedNoneDaily.SetValue(True)
                self.cboTime4.SetStringSelection(time)
            elif b.sched_type == "none/weekly":
                self.radSchedNoneWeekly.SetValue(True)
                self.cboDay5.SetStringSelection(day)
                self.cboTime5.SetStringSelection(time)
            else:
                raise Exception(_("This backup is corrupt. Invalid schedule type"))

        #    Notifications
        self.chkNotifyMsg.SetValue(b.notify_msg)
        self.chkNotifyEmail.SetValue(b.notify_email)
        self.chkShutdown.SetValue(b.shutdown_after)

        self.update_state()

    def text_to_list(self, text):
        list = [item.strip() for item in text.split("\n") if len(item.strip()) > 0]
        return list

    def get_time_str(self, cronitem):
        hour = cronitem.hour().render()
        if not hour.isdigit():
            hour = "19"
        if len(hour) == 1:
            hour = '0' + hour
        min = cronitem.minute().render()
        if not min.isdigit():
            min = "00"
        if len(min) == 1:
            min = '0' + min
        time = "%s:%s" % (hour, min)
        return time

    def get_dow(self, cronitem):
        dow = cronitem.dow().render()
        if not dow.isdigit():
            dow = "0"
        return int(dow)
    def get_dom(self, cronitem):
        dom = cronitem.dom().render()
        if not dom.isdigit():
            dom = "0"
        return int(dom)


    def save(self):
        #    BUILD THE BACKUP
        if len(self.txtName.GetValue()) == 0:
            raise Exception(_("Backup name cannot be blank"))
        if self.chkEncrypt.GetValue() and not self.config.data_passphrase:
            raise Exception(_("You cannot select encryption when the passphrase is blank (see Configuration page)."))
        if self.txtName.GetValue() == EmptyName:
            raise Exception(_("You need to provide a proper backup name"))
        try:
            #    Create the new backup object
            b = Backup(self.txtName.GetValue())
            #    General Information
            b.active = self.chkActive.GetValue()

            #    Folder Information
            b.include_folders = self.text_to_list(self.txtFolders.GetValue())
            b.include_packages = self.chkPackages.GetValue()

            #    Exclusions
            b.exclude_types = list(self.lstExcludeTypes.GetCheckedStrings()) # returns a tuple, convert to array
            b.exclude_patterns = self.text_to_list(self.txtExcludePatterns.GetValue())

            #    Destination
            b.store = self.cboStore.GetStringSelection()
            b.encrypt = self.chkEncrypt.GetValue()
            b.verify = self.chkVerify.GetValue()

            #    Schedule
            if self.radSchedAdvanced.GetValue():
                b.sched_type = "custom"
                b.sched_times = "%s\n%s" % (self.txtCronIncr.GetValue(), self.txtCronFull.GetValue())
            else:
                if self.radSchedDailyWeekly.GetValue():
                    b.sched_type = "daily/weekly"
                    time = self.cboTime1.GetStringSelection()
                    day = self.cboDay1.GetStringSelection()
                elif self.radSchedDailyMonthly.GetValue():
                    b.sched_type = "daily/monthly"
                    time = self.cboTime2.GetStringSelection()
                    day = self.cboMonthDay2.GetStringSelection()
                elif self.radSchedHourlyWeekly.GetValue():
                    b.sched_type = "hourly/weekly"
                    time = self.cboTime3.GetStringSelection()
                    day = self.cboDay3.GetStringSelection()
                elif self.radSchedNoneDaily.GetValue():
                    b.sched_type = "none/daily"
                    time = self.cboTime4.GetStringSelection()
                    day = "*"
                elif self.radSchedNoneWeekly.GetValue():
                    b.sched_type = "none/weekly"
                    time = self.cboTime5.GetStringSelection()
                    day = self.cboDay5.GetStringSelection()
                else:
                    raise Exception(_("Corrupt backup"))

                b.sched_times = time + "/" + day

            #    Notifications
            b.notify_msg = self.chkNotifyMsg.GetValue()
            b.notify_email = self.chkNotifyEmail.GetValue()
            b.shutdown_after = self.chkShutdown.GetValue()

            b.check()
        except Exception as e:
            raise e
        if self.state == ViewState:
            #    Delete the old name
            oldname = self.lstItems.GetStringSelection()
            try:
                del self.config.backups[oldname]
            except:
                pass
        self.config.backups[b.name] = b
        self.config.save()
        self.update_backup_list()

        #    Attempt to save the crontab. If this fails, the backup was corrupt.
        #    But it has been saved. So that is a problem
        update_crontab(self.config.backups)

######################################################################3
#
#        Misc Routines
#
######################################################################3
    def hour_min_from_str(self, str):
        hour, min = str.split(":")
        return int(hour), int(min)

    def delete_backup(self, name, delete_offsite_data):
        #    Delete the database runs.
        backup = self.config.backups[name]
        #    Read the runs
        dummy = self.db.runs(name)
        success = True
        try:
            if delete_offsite_data:
                wx.Yield()
                store = self.config.storage[backup.store].copy()
                store.delete_backup_data(name)
            wx.Yield()
            self.db.delete_backup(name)
        except:
            #    Most likely this will happen with a corrupt backup object.
            #    We dont want that corruption to stop the deletion.
            success = False
        #    Now delete the configuration.
        wx.Yield()
        del self.config.backups[name]
        update_crontab(self.config.backups)
        self.config.save()
        self.update_backup_list()
        if not success:
            dlg.Warn(self, _("There were errors during the delete. You should check/delete the offsite store manually."),
                     _("Error During Delete"))


    def history(self, default_name):
        #    Open the file list window
        win = HistoryWindow(self, default_name)
        win.Show()

    def run_backup(self, backup_name):
        win = RunBackupWindow(self, backup_name)
        win.Show()







