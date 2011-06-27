# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import os
import time
import subprocess

import gui
from lib.config import Config
from lib import utils
from lib.db import DB
from lib import dlg
#    Do last!
from lib.logger import Logger
log = Logger('ui')


class PackageWindow(gui.PackageWindow):
    '''
    classdocs
    '''


    def __init__(self, parent, package_list):
        '''
        Constructor
        '''
        gui.PackageWindow.__init__(self, parent)
        log.info("Starting up a package window")
        self.package_list = package_list
        self.load_packages()
        self.Show()

    def load_packages(self):
        self.installed_list = utils.get_packages()

        s_old = set(self.package_list)
        s_installed = set(self.installed_list)

        missing = s_old.difference(s_installed)
        self.install_packages = list(missing)
        self.install_packages.sort()
        self.lstSoftware.Clear()
        self.lstSoftware.AppendItems(self.install_packages)
        self.lstSoftware.SetChecked(range(len(self.install_packages)))

        self.check_packages()
    
    def check_packages(self):
        '''
        Check if no packages are selected, disable to check box.
        '''
        if len(self.install_packages) == 0 or len(self.lstSoftware.GetChecked()) == 0:
            self.btnBegin.Enable(False)
        else:
            self.btnBegin.Enable(True)

    def onCheckBox(self, event):
        '''
        After any change to the list box - check if the button can be enabled?
        @param event:
        '''
        self.check_packages()

    def onBegin(self, event):
        #   Install all checked packages
        self.progress.SetValue(0)
        self.progress.SetRange(len(self.lstSoftware.GetCheckedStrings()))
        for package in self.lstSoftware.GetCheckedStrings():
            self.lblCurrentFile.SetLabel(package)
            self.lblCurrentFile.Update()
            #    We run this in a terminal so any user interaction is taken care of
            cmd = ["gnome-terminal", "--disable-factory", "--execute", 
                   "sudo", "apt-get", "install", "-y", package]
            log.debug("Running ", cmd)
            status = subprocess.call(cmd)
            log.debug("Results:", status)
            #    Now lets verify the results
            cmd = 'sudo dpkg -l %s | grep "^ii"' % package
            status = subprocess.call(cmd, shell=True)
            if status != 0:
                dlg.Warn(self, _("Error during install of {package}").format(package=package))
            self.progress.SetValue(self.progress.GetValue() + 1)
            self.progress.Update()
            
        self.load_packages()
