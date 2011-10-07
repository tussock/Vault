# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function
#    Version of this file. Increment this number if you make any changes
#    to either this file or recoveryui.*
__version__=11

# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Created on Jan 25th 2011

@author: paul

This is the disaster recovery program.
It is run after a complete hard drive failure.

It is run from a STORE folder, and takes
the last FULL and all subsequent INCR backups
and restores the directories to the state they
were in at the last backup.

It presents a UI via wx.
'''

import wx
import os
import glob
import re
import tempfile
from subprocess import Popen, PIPE
import shutil
from gzip import GzipFile
import time

AppTitle = "Vault"
AppDir = os.path.dirname(os.path.dirname(__file__))
LocaleDir = os.path.join(AppDir, "i18n")

import locale
locale.setlocale(locale.LC_ALL, os.environ["LANG"])

#    Set up translations
import gettext
gettext.bindtextdomain(AppTitle, LocaleDir)
gettext.textdomain(AppTitle)
_ = gettext.gettext

import recoveryui

StoreMarker = "_store_"
RecoveryFolder = "_recovery_"

#    If the parent folder is called '_recovery_', then we
#    are in the running environment (Debug=False)
#    Lets get the abs path of this module, then the name of the folder.
cur_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
print(cur_dir)
Debug = cur_dir != RecoveryFolder
print(Debug)
if Debug:
    RootDir = "../../run/store"
else:
    RootDir = ".."

def log(*args):
    if Debug:
        for arg in args:
            print(arg, end="")
        print("")

class MyApp(wx.App):
    def OnInit(self):
        frame = RecoveryWindow(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

class RecoveryWindow(recoveryui.RecoveryWindow):
    def __init__(self, parent):
        recoveryui.RecoveryWindow.__init__(self, parent)
        ret = self.load_static()
        if not ret:
            dlg = wx.MessageDialog(self, 
                            _("The current folder does not appear to be a backup store, or has no backups"), 
                            _("Not a store"), 
                            wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            self.Close()
            return
        #    Select the first item
        if Debug:
            self.dirAlternate.SetPath("/tmp")
            self.radAlternate.SetValue(True)
            self.txtPassword.SetValue("password")
        else:
            self.dirAlternate.SetPath("/")
        self.cboBackup.Select(0)
        self.onBackup(None)
        self.onDestination(None)


    def load_static(self):
        is_store = False
        list = os.listdir(RootDir)
        list.sort(reverse=False)
        for name in list:
            log("Found backup name:", name)
            if name == StoreMarker:
                is_store = True
                continue
            path = os.path.join(RootDir, name)
            if os.path.isdir(path) and name != RecoveryFolder:
                self.cboBackup.Append(name)
            #    Everything else we ignore
        return is_store and self.cboBackup.GetCount() > 0

    #    A backup has been selected
    def onBackup(self, event):
        #    Get the last full backup name
        dir = os.path.join(RootDir, self.cboBackup.GetStringSelection())
        items = os.listdir(dir)
        items.sort()
        if len(items) == 0:
            status = _("That folder has no backups")
            encrypted = False
        else:
            #    Get the last
            last = items[-1]
            (time, type) = last.split(" ")
            enc_files = glob.glob(os.path.join(dir, last, "*.enc"))
            encrypted = len(enc_files) > 0
            status = _("Last backup run at %s.") % time
            if encrypted:
                status = status + " " + _("Backups are encrypted")
            else:
                status = status + " " + _("Backups are not encrypted")
                
        self.lblStatus.SetLabel(status)
        self.txtPassword.Enable(encrypted)

    def onDestination(self, event):
        self.dirAlternate.Enable(self.radAlternate.GetValue())

    def onClose(self, event):
        self.Close()

    def onRecover(self, event):
        backup = self.cboBackup.GetStringSelection()
        if self.txtPassword.Enabled:
            password = self.txtPassword.GetValue()
        else:
            password = ""
        if self.radOriginal.GetValue():
            destination = "/"
        else:
            destination = self.dirAlternate.GetPath()
            #print(self.dirAlternate, self.dirAlternate.GetPath())


        try:
            self.do_recovery(backup, password, destination)
        except Exception as e:
            dlg = wx.MessageDialog(self, str(e), _("Error during restore"), wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()


    def do_recovery(self, backup, password, destination):
        if destination == "":
            raise Exception(_("Destination cannot be blank"))
        dir = os.path.join(RootDir, backup)
        items = os.listdir(dir)
        items.sort()
        #    Find the LAST Full
        full_idx = rmatch(items, "^.* Full$")
        if full_idx == -1:
            raise Exception(_("There are no Full backups"))
        for name in items[full_idx:]:
            (time, type) = name.split(" ")
            self.statusBar.SetFields(
                            [_("Restoring {type} backup, date {date}").format(
                                    type=type, date=time)
                            ])

            b_folder = os.path.join(dir, name)

            self.recover_one(b_folder, password, destination)

        self.statusBar.SetFields([_("Complete")])


    def recover_one(self, folder, password, destination):
        log("recover_one", folder, password, destination)
        save_cwd = os.getcwd()
        os.chdir(folder)
        encrypted = len(password) > 0
        tmp_dir = tempfile.mkdtemp()
        try:
            ############
            #
            #    PROCESSING THE TAR FILE
            #
            ############
            if encrypted:
                log("Password required")
                pass_file = os.path.join(tmp_dir, "pwd")
                os.mkfifo(pass_file, 0600)

                cat = Popen('find data -type f -print | sort | xargs cat', shell=True, stdout=PIPE)
                openssl = Popen("/usr/bin/openssl enc -d -aes256 -md sha256 -pass 'file:%s'" % pass_file, shell=True,
                                stdin=cat.stdout, stdout=PIPE)
                tar = Popen("/bin/tar -xzf - --directory '%s'" % (destination,), shell=True,
                            stdin=openssl.stdout, stdout=PIPE, stderr=PIPE)

                #    Send the passphrase via a pipe file. 
                #    It wont appear in the process list (via cmd line arg).
                tmp_fd = open(pass_file, "w")
                tmp_fd.write(password)
                tmp_fd.close()
            else:
                log("Starting tar")
                cat = Popen('find data -type f -print | sort | xargs cat', shell=True, stdout=PIPE)
                tar = Popen("/bin/tar -xzf - --directory '%s'" % destination, shell=True,
                            stdin=cat.stdout, stdout=PIPE, stderr=PIPE)

            #    Wait for the TAR to finish
            log('Waiting for tar to finish')

            stdout, stderr = tar.communicate()
            log("stderr=", stderr)
            log("stdout=", stdout)
            tar.wait()
            log("Main extraction complete")
            print("Errors:", stderr)


            ############
            #
            #    PROCESSING THE LOF FILE
            #
            ############
            if encrypted:
                log("starting lof processing")
                pass_file = os.path.join(tmp_dir, "pwd2")
                os.mkfifo(pass_file, 0600)

                lof_file = os.path.join(tmp_dir, "lof")

                openssl = Popen("/usr/bin/openssl enc -d -aes256 -md sha256 -pass 'file:%s' -in lof.enc -out '%s'" % (pass_file, lof_file),
                                shell=True, stdout=PIPE)
                #    Send the passphrase via a pipe file. 
                #    It wont appear in the process list (via cmd line arg).
                tmp_fd = open(pass_file, "w")
                tmp_fd.write(password)
                tmp_fd.close()
                openssl.wait()
                lof = GzipFile(lof_file, mode="rb")
            else:
                lof = GzipFile("lof", "r")
            try:
                log("Start LOF processing for Deletes")
                while True:
                    line = lof.readline()
                    if not line:
                        log("Done!")
                        break
                    #    Remove the \n
                    line = line[:-1]
                    log("line", line)
                    if line == "":
                        #    New folder (remember to strip the \n
                        folder = lof.readline()[:-1].decode("quopri_codec")
                        log("New folder", folder)
                        continue

                    parts = line.split(",")
                    log("Line parts:", parts)
                    name = parts[0].decode("quopri_codec")
                    type = parts[1]
                    if type != "X":
                        log("Not a delete")
                        continue

                    if folder[0] == os.sep:
                        folder = folder[1:]
                    path = os.path.join(destination, folder, name)
                    log("DELETE ", path)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
            finally:
                lof.close()
        except Exception as e:
            print("Got exception in recover:", str(e))
        finally:
            #    Remove the temp dir
            shutil.rmtree(tmp_dir)
            os.chdir(save_cwd)



def rmatch(list, reg):
    for idx in xrange(len(list) - 1, -1, -1):
        #print("Comparing %s %s" % (list[idx], reg))
        if re.match(reg, list[idx]):
            return idx
    return - 1

app = MyApp(0)
app.MainLoop()
