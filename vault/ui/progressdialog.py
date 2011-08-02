# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import wx.animate
import gui
import os

#    Do last!
from lib.logger import Logger
log = Logger('ui')

class ProgressDialog(gui.ProgressDialog):
    '''
    classdocs
    '''


    def __init__(self, parent, title, message):
        '''
        Constructor
        '''
        gui.ProgressDialog.__init__(self, parent)
        self.SetTitle(title)
        self.lblMessage.SetLabel(message)
        self.Fit()

        busy_fname = os.path.join(const.PixmapDir, "animated/rotating_arrow.gif")
        busy_ani = wx.animate.GIFAnimationCtrl(self.aniPanel, -1, busy_fname, pos=(0, 0))
        busy_ani.GetPlayer().UseBackgroundColour(True)
        # continuously loop through the frames of the gif file (default)
        busy_ani.Play()

        self.CenterOnParent()
        self.Show()
        wx.Yield()

    def __enter__(self):
        self.Show()
    
    def __exit__(self, type, value, traceback):
        self.Destroy()

