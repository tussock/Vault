# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import subprocess
import wx
import os

import gui
from lib import const
from lib import dlg
#    Do last!
from lib.logger import Logger
log = Logger('ui')


class RunRestoreWindow(gui.RunRestoreWindow):
    '''
    classdocs
    ''' 


    def __init__(self, parent, source):
        '''
        Constructor
        '''
        gui.RunRestoreWindow.__init__(self, parent)
        log.trace("Starting up a run restore window")
        self.txtSource.SetValue(source)

        self.Show()

        icon = wx.Icon("images/storage.png", wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)
        

    def onStart(self, event):
        options = ['python', const.ServerPath]
        if self.chkNoRecurse.GetValue():
            options.append("--norecurse")
        if self.chkNotify.GetValue():
            options.append("--message")
        if self.chkEmail.GetValue():
            options.append("--email")
        if self.chkShutdown.GetValue():
            options.append("--shutdown")

        options.append("restore")
        options.append(self.cboDest.GetPath())
        options.append(self.txtSource.GetValue())

        log.debug("Starting restore: ", " ".join(options))
        subprocess.Popen(options)
        dlg.Info(self, _("Restore has been started"))
        self.Close()

    def onClose(self, event):
        self.Close()
