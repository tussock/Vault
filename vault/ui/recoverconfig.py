# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import os
import sys
import subprocess

from lib import const
from lib import wizard
from lib import dlg
from lib import passphrase
from store.folderstore import FolderStore
from store.ftpstore import FTPStore
from store.sharestore import ShareStore
from store.dropboxstore import DropBoxStore
from lib import cryptor               #@UnresolvedImport
from lib import utils
import app
from progressdialog import ProgressDialog

#    Do last!
from lib.logger import Logger
log = Logger('ui')


#####################################################################################
#
#    Disaster Recovery
#
#####################################################################################


def cb(page):
    if page[0] == "a":
        raise wizard.ValidationException("The value 'a' is illegal")

def wiz_execute(wiz):
    #    Connect
    if wiz.fields["storagetype"].value == _("Local Folder"):
        store = FolderStore("store", 0, False, wiz.fields["folderpath"].value)
    elif wiz.fields["storagetype"].value == _("FTP Server"):
        server = wiz.fields["ftpserver"].value
        login = wiz.fields["ftplogin"].value
        password = wiz.fields["ftppassword"].value
        root = wiz.fields["ftproot"].value
        sftp = wiz.fields["sftp"].value
        store = FTPStore("store", 0, False, server, root, login, password, sftp)
    elif wiz.fields["storagetype"].value == _("DropBox"):
        login = wiz.fields["dblogin"].value
        password = wiz.fields["dbpassword"].value
        root = wiz.fields["dbroot"].value
        store = DropBoxStore("store", 0, False, root, login, password)
    elif wiz.fields["storagetype"].value == _("Server Share"):
        mountcmd = wiz.fields["mountcmd"].value
        umountcmd = wiz.fields["umountcmd"].value
        shareroot = wiz.fields["shareroot"].value
        store = ShareStore("store", 0, False, shareroot, mountcmd, umountcmd)
    else:
        raise Exception("Internal error: bad store type")
    log.debug("Store = ", store)
    try:
        store.connect()

        folders = []
        #    List all backups
        backups = store.list(".")
        for backup in backups:
            try:
                runs = store.list(backup + "/")
                for run in runs:
                    folders.append((backup, run))
            except:
                pass

        log.debug("Folders", folders)
        if len(folders) == 0:
            raise Exception(_("There are no backup runs in this store"))
        #    Sort them based on the path name
        folders.sort(key=lambda item: item[1], reverse=True)
        #    Now the first item is the one to use (as it is the most recent).
        backupname, backuprun = folders[0]
        config = os.path.join(backupname, backuprun, const.ConfigName)
        configenc = config + const.EncryptionSuffix
        #    Check if the config exists.
        if store.exists(config):
            src = config
            encrypted = False
        elif store.exists(configenc):
            src = configenc
            encrypted = True
        else:
            raise Exception(_("The backup runs are missing or corrupt (no config files)"))

        if not encrypted:
            store.copy_from(src, const.ConfigDir)
        else:
            #    Fetch the file.
            enc_file = const.ConfigFile + const.EncryptionSuffix
            clear_file = const.ConfigFile
            store.copy_from(src, const.ConfigDir)

            #    ENCRYPTED
            bad = True  #    keep going until we get a good password
            while bad:
                password = GetPassword(wiz, backupname, backuprun)
                if password == None:
                    #    User is quitting
                    return

                #    Lets check the file is good.
                try:
                    log.debug("Decrypting", enc_file, clear_file, password)
                    ret = cryptor.decrypt_file(password, enc_file, clear_file)
                    log.debug("Return from decrypt", ret)
                    if ret != 0:
                        raise Exception(_("Failed encryption"))
                    bad = False
                    if os.path.exists(enc_file):
                        os.remove(enc_file)
                    #    Looks like this password is a good one. 
                    #    We will save it.
                    passphrase.set_passphrase(password)
                except:
                    log.info("Invalid backup password")
                    dlg.Warn(wiz, _("Invalid password. Please enter the correct backup password."))
                    os.remove(clear_file)


        dlg.Info(wiz, _("Your configuration has been restored. Restarting the UI..."), _("Restore"))

        python = sys.executable
        log.debug("Starting:", [python, const.UIPath])
        subprocess.Popen([python, const.UIPath])
        app.quit()

    except Exception as e:
        dlg.Warn(wiz, str(e), _("Configuration restore failed"))
    finally:
        store.disconnect()

def GetPassword(wiz, backupname, backuprun):
    # need to get password, and make sure its good.
    pwd_entry = wx.PasswordEntryDialog(wiz,
                            _("The backup '{backup}' which ran on '{date}' is encrypted.\nPlease enter the master password").format(
                                        backup=backupname, date=backuprun),
                                        _("Encrypted Backups"),
                                        "")
    try:
        if pwd_entry.ShowModal() == wx.ID_OK:
            pwd = pwd_entry.GetValue()
        else:
            pwd = None
    finally:
        pwd_entry.Destroy()
    return pwd


def ftp_test(wizard):
    server = wizard.fields["ftpserver"].value
    login = wizard.fields["ftplogin"].value
    password = wizard.fields["ftppassword"].value
    root = wizard.fields["ftproot"].value
    sftp = wizard.fields["sftp"].value
    store = FTPStore("store", 0, False, server, root, login, password, sftp)

    do_test(wizard, store)

def db_test(wizard):
    login = wizard.fields["dblogin"].value
    password = wizard.fields["dbpassword"].value
    root = wizard.fields["dbroot"].value
    store = DropBoxStore("store", 0, False, login, password, root)

    do_test(wizard, store)

def share_test(wizard):
    mountcmd = wizard.fields["mountcmd"].value
    umountcmd = wizard.fields["umountcmd"].value
    shareroot = wizard.fields["shareroot"].value
    store = ShareStore("store", 0, False, shareroot, mountcmd, umountcmd)

    do_test(wizard, store)

def do_test(wizard, store):
    log.debug("Connect To", store)

    prog_dlg = ProgressDialog(wizard, _("Testing..."), _("Connecting to and testing the store.\nPlease wait..."))
    prog_dlg.Show()
    wx.Yield()
    try:
        store.connect()
        wx.Yield()
        store.test()
        wx.Yield()
        dlg = wx.MessageDialog(None, _("Successfully connected to store"), _("Success"), wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        dlg = wx.MessageDialog(None, str(e), _("Test Failed"), wx.OK | wx.ICON_WARNING)
    finally:
        store.disconnect()
        prog_dlg.Destroy()
    dlg.ShowModal()
    dlg.Destroy()



def do_recover(parent):
    wiz = wizard.Wizard(parent, _("Configuration Reload Wizard"),
                 _("Welcome to the disaster recovery wizard.\n"
                    "\n"
                    "You need to provide details to a recently used store.\n"
                    "The wizard will fetch your old configuration from the latest backup\n"
                    "run in that store."),
                 _("We are now ready to recover your backup configuration."), wiz_execute, 
                 icon=os.path.join(const.PixmapDir, "storage.png"))

    #    Type of storage
    page = wizard.Page(wiz, _("Type Of Storage"))
    wizard.OptionsField(page, "storagetype", _("What type of storage will we connect to?"),
                 [_("Local Folder"), _("FTP Server"), _("Server Share"), _("DropBox")],
                 default=None if not const.Debug else _("Local Folder"))

    #    Folder storage
    page = wizard.Page(wiz, _("Folder Storage Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("Local Folder"))
    wizard.DirEntryField(page, "folderpath", _("Path To Store"), must_exist=True,
                 default=None if not const.Debug else os.path.join(const.RunDir, "store"))

    #    FTP Storage
    page = wizard.Page(wiz, _("FTP Storage Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("FTP Server"))
    wizard.TextField(page, "ftpserver", _("Name or IP Address of FTP Server"),
                 default=None)
    wizard.CheckField(page, "sftp", _("Use an encrypted connection"), _("Enable SFTP"),
                 default=None if not const.Debug else True)
    wizard.TextField(page, "ftplogin", _("Login name"),
                 default=None if not const.Debug else "ftptest")
    wizard.TextField(page, "ftppassword", _("Password"),
                 default=None)
    wizard.TextField(page, "ftproot", _("Path To Store"),
                 default=None if not const.Debug else "store")
    wizard.ButtonField(page, "ftptest", _("Test"), ftp_test)

    #    DropBox Storage
    page = wizard.Page(wiz, _("DropBox Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("DropBox"))
    wizard.TextField(page, "dblogin", _("Login name"),
                 default=None)
    wizard.TextField(page, "dbpassword", _("Password"),
                 default=None)
    wizard.TextField(page, "dbroot", _("Path To Store"),
                 default=None if not const.Debug else "store")
    wizard.ButtonField(page, "dbtest", "Test", db_test)

    #    Share Storage
    page = wizard.Page(wiz, _("Server Share Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("Server Share"))
    wizard.TextField(page, "mountcmd", _("Command to mount the share"),
                 default=None if not const.Debug else "")
    wizard.TextField(page, "umountcmd", _("Command to unmount the share"),
                 default=None if not const.Debug else "")
    wizard.TextField(page, "shareroot", _("Root folder (after mounting)"),
                 default=None if not const.Debug else "")
    wizard.ButtonField(page, "sharetest", "Test", share_test)

    #    Run the wizard
    wiz.run()
