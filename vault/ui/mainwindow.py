# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

from __future__ import division, with_statement, print_function

import wx
import gui
import subprocess
import os

from lib import const

from backuppanel import BackupPanel
from overviewpanel import OverviewPanel
from restorepanel import RestorePanel
from storagepanel import StoragePanel
from configpanel import ConfigPanel
from aboutwindow import AboutWindow


#    Do last!
from lib.logger import Logger
log = Logger('ui')

class MainWindow(gui.MainWindow):
    '''
    classdocs
    '''


    def __init__(self, parent):
        log.debug("Building main window")
        gui.MainWindow.__init__(self, parent)
        self.notebook = wx.Toolbook(self, id= -1, style=wx.BK_LEFT)
        self.GetSizer().Add(self.notebook, flag=wx.EXPAND, proportion=1)

        icon = wx.Icon(os.path.join(const.PixmapDir, "storage.png"), wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        log.debug("Building panels")
        self.panels = []
        self.panels.append(OverviewPanel(self.notebook))
        self.panels.append(BackupPanel(self.notebook))
        self.panels.append(StoragePanel(self.notebook))
        self.panels.append(RestorePanel(self.notebook))
        self.panels.append(ConfigPanel(self.notebook))
        log.debug("Building image list and pages")
        image_list = wx.ImageList(32, 32)
        self.notebook.AssignImageList(image_list)
        for panel in self.panels:
            image_list.Add(panel.image)
            image_idx = image_list.GetImageCount() - 1

            self.notebook.AddPage(panel, panel.title, imageId=image_idx)

        log.debug("Completed panel build")
        self.notebook.Layout()
        self.Center()
        self.Fit()
        self.Show()
        self.notebook.SetSelection(0)
        self.Show()

    def onQuit(self, event):
        self.Close()

    def onHelp(self, event):
        subprocess.Popen([const.HelpViewer, const.HelpPath])
        self.show_message("Opening help...")

    def update_data(self):
        for panel in self.panels:
            panel.update_data()

    def onSetFocus(self, event):
        #print("Set focus")
        pass

    def onAbout(self, event):
        win = AboutWindow(self)
        win.Show()

    def show_message(self, msg, clear_after=10000):
        self.SetStatusText(msg)
        if clear_after:
            wx.CallLater(clear_after, self.clear_message)
    def clear_message(self):
        self.SetStatusText("")
        