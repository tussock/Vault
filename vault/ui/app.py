# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import wx
import gettext
_ = gettext.gettext

from mainwindow import MainWindow 
from lib.db import DB

#    Do this last!
from lib.logger import Logger
log = Logger("ui")

_app = None

def get_app():
    global _app
    return _app

def broadcast_update():
    global _app
    _app.update_data()
    
def show_message(msg):
    global _app
    _app.show_message(msg)
def clear_message():
    global _app
    _app.clear_message()
    
def quit():
    global _app
    _app.frame.Close()

class App(wx.App):
    def __init__(self):
        DB().check_upgrade()

#        gettext.install(const.AppTitle, './locale', unicode=False)
#        self.presLan_en = gettext.translation(const.AppTitle, "./locale", languages=['en'])
#        #presLan_fr = gettext.translation(const.AppTitle, "./locale", languages=['fr'])
#        self.presLan_en.install()
#        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
#        self.locale.setlocale(locale.LC_ALL, 'EN')
        
        wx.App.__init__(self)
        log.info(_("App init"))
        
        global _app
        _app = self

    def OnInit(self):
        log.info("App OnInit")
        self.frame = MainWindow(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True
    
    def update_data(self):
        self.frame.update_data()
        
    def show_message(self, message):
        self.frame.show_message(message)
    
    def clear_message(self):
        self.frame.clear_message()
            