# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import wx

import gui
from lib import const

#    Do last!
from lib.logger import Logger
log = Logger('ui')



MinColour = 128
MaxColour = 192

class AboutWindow(gui.AboutWindow):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        gui.AboutWindow.__init__(self, parent)
        self.lblTitle.SetLabel(const.AppTitle)
        self.lblSubTitle.SetLabel(const.Description)
        self.lblCopyright.SetLabel(const.Copyright)
        self.lblVersion.SetLabel(_("Version") + " " + const.Version)


        self.min_color = 160
        self.max_color = 192
        self.SetBackgroundColour(wx.Color(self.min_color, self.min_color, self.min_color))
        self.delta = 1

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(50)

        icon = wx.Icon("images/storage.png", wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)
        
    def onLeftUp(self, event):
        self.Close()

    def update(self, event):
        bkg = self.GetBackgroundColour()
        (r, g, b) = bkg.Get(False)
        if r >= self.max_color:
            self.delta = -1
        if r <= self.min_color:
            self.delta = 1
        r += self.delta
        g += self.delta
        b += self.delta
        self.SetBackgroundColour(wx.Colour(r, g, b))


