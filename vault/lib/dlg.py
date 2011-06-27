# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Useful dialogs
'''
from __future__ import division, with_statement, print_function

import wx
import os
from pynotify import Notification
import gettext
_ = gettext.gettext
import const

def YesNo(parent, question, caption='Yes or no?'):
    '''
    Returns True if the answer was Yes, False otherwise
    
    @param parent:
    @type parent:
    @param question:
    @type question:
    @param caption:
    @type caption:
    '''
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

def OkCancel(parent, question, caption=_('Ok or cancel?')):
    '''
    Returns wx.OK or wx.CANCEL
    
    @param parent:
    @type parent:
    @param question:
    @type question:
    @param caption:
    @type caption:
    '''
    dlg = wx.MessageDialog(parent, question, caption, wx.OK | wx.CANCEL | wx.ICON_QUESTION)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

def YesNoCancel(parent, question, caption=_('Yes, no or cancel?')):
    '''
    Returns wx.YES, wx.NO, wx.CANCEL
    
    @param parent:
    @type parent:
    @param question:
    @type question:
    @param caption:
    @type caption:
    '''
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

def Info(parent, message, caption=const.AppTitle):
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()
def InfoModeless(parent, message, caption=const.AppTitle):
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
    dlg.Show()
    return dlg
def Warn(parent, message, caption=_('Warning')):
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()
def Error(parent, message, caption=_('Error!')):
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_STOP)
    dlg.ShowModal()
    dlg.Destroy()

#   Using the notification system in Gnome
#!/usr/bin/python

def Notify(title, message=""):
    #    Trick = you need to set the display so notify can find it.
    os.environ["DISPLAY"] = ":0.0"
    n = Notification(title, message)
    n.show()

