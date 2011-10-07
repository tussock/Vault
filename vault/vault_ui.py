#!/usr/bin/env python
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

#    Load up all constants
import os
import sys
from lib import const
import locale
locale.setlocale(locale.LC_ALL, os.environ["LANG"])

#    Set up translations
import gettext
gettext.bindtextdomain(const.AppTitle, const.LocaleDir)
gettext.textdomain(const.AppTitle) 
_ = gettext.gettext
gettext.install(const.AppTitle)

#    APPLICATION IMPORTS. ONLY IN ONE PLACE
from lib.logger import LogManager
LogManager(const.LogFile)
 

from ui.app import App  
from lib import dlg
#    Do this last!
from lib.logger import Logger
log = Logger("ui")
 

def run():
    #    Check that the runner is root (unless debugging)
    if not const.Debug:
        if not os.geteuid()==0:
            #    We are going to crash, get wx up enough to show a dialog.
            import wx
            _ = wx.PySimpleApp()
            dlg.Error(None, _("The Vault must be run as root"))
            sys.exit("The Vault must be run as root")
 
    log.info("Loading application")
    try:

        #    Now build the app object
        appl = App()
    
    
    except Exception as e:
        print(_("Failed to initialize application: {error}").format(error=str(e)))
        exit()
    appl.MainLoop()

if __name__ == "__main__":
    run()


