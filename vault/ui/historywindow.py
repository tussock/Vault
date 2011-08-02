# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import os


import gui
from lib import const
from lib.config import Config
from lib import utils
from lib.db import DB
from rundetailswindow import RunDetailsWindow
#    Do last!
from lib.logger import Logger
log = Logger('ui')


class HistoryWindow(gui.HistoryWindow):
    '''
    classdocs
    '''


    def __init__(self, parent, default_name=None):
        '''
        Constructor
        '''
        gui.HistoryWindow.__init__(self, parent)

        log.trace("Starting up a history panel")
        self.db = DB()
        self.config = Config.get_config()

        self.order = const.ASC
        
        if default_name:
            self.cboBackup.SetStringSelection(default_name)
        self.update_data()

#        self.imgList = wx.ImageList(16, 16)
#        self.img_up = self.imgList.Add(wx.Bitmap("images/go-up.png", wx.BITMAP_TYPE_PNG))
#        self.img_down = self.imgList.Add(wx.Bitmap("images/go-down.png", wx.BITMAP_TYPE_PNG))
#        self.lstRuns.SetImageList(self.imgList, wx.IMAGE_LIST_SMALL)

        icon = wx.Icon(os.path.join(const.PixmapDir, "storage.png"), wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

#        listmix.ColumnSorterMixin.__init__(self, 7)
#        self.Bind(wx.EVT_LIST_COL_CLICK, self.onColClick, self.lstRuns)

#        self.SortListItems(2, 1)

        #    Ensure the right page is showing
        self.nb_history.SetSelection(0)
        self.Show()


    def update_data(self):
        all = _("***All Backups***")
        old_sel = self.cboBackup.GetStringSelection()
        if not old_sel:
            old_sel = all
        self.cboBackup.Clear()
        self.cboBackup.AppendItems([all])
        self.cboBackup.AppendItems(self.config.backups.keys())
        self.cboBackup.SetStringSelection(old_sel)

        self.update_runs()
        self.update_messages()

    def update_runs(self):
        if self.cboBackup.GetSelection() == 0:
            runs = self.db.runs()
        else:
            backup_name = self.cboBackup.GetStringSelection()
            runs = self.db.runs(backupname=backup_name)
            
        if self.order == const.ASC:
            runs.sort(key=lambda x : x.start_time_str, reverse=False)
            self.txtOrder.SetLabel("Order: Oldest First")
        else:
            runs.sort(key=lambda x : x.start_time_str, reverse=True)
            self.txtOrder.SetLabel("Order: Newest First")

        self.lstRuns.DeleteAllColumns()
        self.lstRuns.DeleteAllItems()
        self.lstRuns.InsertColumn(0, _("Name"), wx.LIST_FORMAT_LEFT)
        self.lstRuns.InsertColumn(1, _("Type"), wx.LIST_FORMAT_CENTER)
        self.lstRuns.InsertColumn(2, _("Time"), wx.LIST_FORMAT_CENTER)
        self.lstRuns.InsertColumn(3, _("Status"), wx.LIST_FORMAT_CENTER)
        self.lstRuns.InsertColumn(4, _("Files"), wx.LIST_FORMAT_CENTER)
        self.lstRuns.InsertColumn(5, _("Folders"), wx.LIST_FORMAT_CENTER)
        self.lstRuns.InsertColumn(6, _("Size"), wx.LIST_FORMAT_CENTER)

        self.itemDataMap = {}
        idx = 0
        for run in runs:
            row = [run.name, run.type, run.start_time_str, run.status, str(run.nfiles), str(run.nfolders), utils.readable_form(run.size)]
            self.lstRuns.Append(row)
            self.lstRuns.SetItemData(idx, run.run_id)
            self.itemDataMap[idx + 1] = row
            idx = idx + 1
        self.itemIndexMap = self.itemDataMap.keys()

        self.lstRuns.SetColumnWidth(0, 100)
        self.lstRuns.SetColumnWidth(1, 50)
        self.lstRuns.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.lstRuns.SetColumnWidth(3, 80)
        self.lstRuns.SetColumnWidth(4, 120)
        self.lstRuns.SetColumnWidth(5, 100)
        self.lstRuns.SetColumnWidth(6, wx.LIST_AUTOSIZE)

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.lstRuns

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.img_down, self.img_up)


    def onColClick(self, event):
        event.Skip()



    def update_messages(self):

        self.lstMessages.DeleteAllColumns()
        self.lstMessages.DeleteAllItems()
        self.lstMessages.InsertColumn(0, _("Time"))
        self.lstMessages.InsertColumn(1, _("Message"))


        if self.cboBackup.GetSelection() == 0:
            messages = self.db.messages()
        else:
            backup_name = self.cboBackup.GetStringSelection()
            messages = self.db.backup_messages(backup_name)

        if self.order == const.ASC:
            messages.sort(reverse=False, key=lambda msg: msg.time)
        else:
            messages.sort(reverse=True, key=lambda msg: msg.time)

        for msg in messages:
            item = (msg.time, msg.message)
            self.lstMessages.Append(item)

        self.lstMessages.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.lstMessages.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def onBackup(self, event):
        self.update_data()

    def onRefresh(self, event):
        self.update_data()

    def onDetails(self, event):
        #    Get the selected item
        sel = self.lstRuns.GetFirstSelected()
        if sel == -1:
            return
        run_id = self.lstRuns.GetItemData(sel)
        #    Will raise an exception if no run
        run = self.db.run_details(run_id)
        RunDetailsWindow(self, run)

    def onLeftDClick(self, event):
        self.onDetails(event)

    def onOrder(self, event):
        if self.order == const.ASC:
            self.order = const.DESC
        else:
            self.order = const.ASC
        self.update_data()