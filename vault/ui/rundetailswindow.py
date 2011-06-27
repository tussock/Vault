# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import os

import gui
from lib.config import Config
from lib import utils
from lib.db import DB
from progressdialog import ProgressDialog
#    Do last!
from lib.logger import Logger
log = Logger('ui')


class RunDetailsWindow(gui.RunDetailsWindow):
    '''
    classdocs
    '''


    def __init__(self, parent, run):
        '''
        Constructor
        '''
        gui.RunDetailsWindow.__init__(self, parent)
        log.info("Starting up a run details window")

        self.run = run
        self.db = DB()
        self.config = Config.get_config()
        self.paths = {}

        self.load_run_details()
        self.load_files(200)
        self.load_messages()

        icon = wx.Icon("images/storage.png", wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        #    Ensure the right page is showing
        self.nbDetails.SetSelection(0)
        self.Show()


##################################################################
#
#    Event Handlers
#
##################################################################

    def onAllFiles(self, event):
        self.load_files(None)
        self.pnlAllFiles.Hide()
        self.pnlFiles.Fit()



##################################################################
#
#    Utilities
#
##################################################################

    def load_run_details(self):
        #(run_id=3, name=u'test', type=1, start_time=u'2010-12-28T15:09:39.455313', hash=u'6da92e0e7f25d003bfcc2cc7d845868fe6a433e1c0fe349300659fc86c8f66ba', size=59764, nfiles=0, status=u'Succeeded')
        self.lstDetails.InsertColumn(0, _("Name"))
        self.lstDetails.InsertColumn(1, _("Value"))

        self.lstDetails.Append([_("Backup Name"), self.run.name])

        self.lstDetails.Append([_("Run Date"), self.run.start_time_str])
        self.lstDetails.Append([_("Run Type"), self.run.type])
        self.lstDetails.Append([_("Status"), self.run.status])
        self.lstDetails.Append([_("Files Backed Up"), str(self.run.nfiles)])
        self.lstDetails.Append([_("Folders Backed Up"), str(self.run.nfolders)])
        self.lstDetails.Append([_("Installed Software List"), _("Included") if self.run.packages else _("Not included")])
        self.lstDetails.Append([_("Total Size"), utils.readable_form(self.run.size)])

        self.lstDetails.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.lstDetails.SetColumnWidth(1, wx.LIST_AUTOSIZE)


    def load_files(self, limit):
        with ProgressDialog(self, _("Loading"), _("Loading run files.\nPlease wait...")):
            self.lstFiles.DeleteAllColumns()
            self.lstFiles.DeleteAllItems()

            self.lstFiles.InsertColumn(0, _("Path"))
            self.lstFiles.InsertColumn(1, _("Size"))
            self.lstFiles.InsertColumn(2, _("Mod Time"))

            self.lstFiles.Freeze()
            try:
                files = self.db.run_contents(self.run.run_id, limit)
                for file in files:
                    wx.Yield()
                    if file.type == "F":
                        size = utils.readable_form(file.size)
                        mod_time = file.mod_time
                    elif file.type == 'D':
                        size = _("Folder")
                        mod_time = file.mod_time
                    elif file.type == 'X':
                        size = _("(deleted)")
                        mod_time = ""
                    else:
                        size = "ERROR: Bad type"
                    path = os.path.join(self.get_path(file.parent_id), file.name)
                    item = (utils.display_escape(path), size, mod_time)
                    self.lstFiles.Append(item)
                self.lstFiles.SetColumnWidth(0, wx.LIST_AUTOSIZE)
                self.lstFiles.SetColumnWidth(1, wx.LIST_AUTOSIZE)
                self.lstFiles.SetColumnWidth(2, wx.LIST_AUTOSIZE)
            finally:
                self.lstFiles.Thaw()

            if self.lstFiles.GetItemCount() < limit:
                #    There probably aren't that many files.
                self.pnlAllFiles.Hide()
                self.pnlFiles.Fit()


    def load_messages(self):
        self.lstMessages.InsertColumn(0, _("Time"))
        self.lstMessages.InsertColumn(1, _("Message"))


        messages = self.db.run_messages(self.run.run_id)
        for msg in messages:
            item = (msg.time, msg.message)
            self.lstMessages.Append(item)

        self.lstMessages.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.lstMessages.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def get_path(self, fs_id):
        if fs_id in self.paths:
            return self.paths[fs_id]

        if fs_id == 0:
            return "/"

        #    Get THIS node
        fs = self.db.get_fs(fs_id)
        path = os.path.join(self.get_path(fs.parent_id), fs.name)
        self.paths[fs.fs_id] = path
        return path

    def get_paths(self, files):
        #    For each file, we need to calculate the full path.
        #    That requires getting paths for any path that we dont have yet.
        paths = {}
        for file in files:
            parent_id = file.parent_id
            #    Do we know this parent_id yet?
            file.path = os.path.join(self.get_path(paths, parent_id), file.name)



