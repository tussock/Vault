# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import os

from lib import const
from lib.config import Config
from lib import wizard
from lib import dlg
from store.folderstore import FolderStore
from store.ftpstore import FTPStore
from store.dropboxstore import DropBoxStore
from store.sharestore import ShareStore
from store.s3store import S3Store
from progressdialog import ProgressDialog
import app

#    Do last!
from lib.logger import Logger
log = Logger('ui')


#####################################################################################
#
#    Disaster Recovery
#
#####################################################################################


def wiz_execute(wiz):
    #    Connect
    if wiz.fields["storagetype"].value == _("Local Folder"):
        name = wiz.fields["name"].value
        path = wiz.fields["folderpath"].value
        store = FolderStore(name, 0, False, path)
    elif wiz.fields["storagetype"].value == _("FTP Server"):
        name = wiz.fields["name"].value
        server = wiz.fields["ftpserver"].value
        login = wiz.fields["ftplogin"].value
        password = wiz.fields["ftppassword"].value
        root = wiz.fields["ftproot"].value
        sftp = wiz.fields["sftp"].value
        store = FTPStore(name, 0, False, server, root, login, password, sftp)
        log.debug("Store = ", store)
    elif wiz.fields["storagetype"].value == _("DropBox"):
        name = wiz.fields["name"].value
        login = wiz.fields["dblogin"].value
        password = wiz.fields["dbpassword"].value
        root = wiz.fields["dbroot"].value
        key = wiz.fields["dbkey"].value
        secret_key = wiz.fields["dbsecretkey"].value
        store = DropBoxStore(name, 0, False, root, login, password, key, secret_key)
    elif wiz.fields["storagetype"].value == _("Amazon S3"):
        name = wiz.fields["name"].value
        key = wiz.fields["s3key"].value
        secret_key = wiz.fields["s3secretkey"].value
        bucket = wiz.fields["s3bucket"].value
        store = S3Store(name, 0, False, bucket, key, secret_key)
    elif wiz.fields["storagetype"].value == _("Server Share"):
        name = wiz.fields["name"].value
        path = wiz.fields["sharepath"].value
        mountcmd = wiz.fields["sharemountcmd"].value
        umountcmd = wiz.fields["shareumountcmd"].value
        store = ShareStore(name, 0, False, path, mountcmd, umountcmd)
    try:
        with ProgressDialog(wiz, _("Creating Store"), _("Creating and testing new store.\nPlease wait...")):
            #    we will rely on the user to test the store
#            store.test()
            config = Config.get_config()
            config.storage[store.name] = store
            config.save()
        
        dlg.Info(wiz, _("Store successfully created."))
        app.broadcast_update()
    except Exception as e:
        dlg.Warn(wiz, str(e), _("Failed to create store"))
        


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
    key = wizard.fields["dbkey"].value
    secret_key = wizard.fields["dbsecretkey"].value
    store = DropBoxStore("store", 0, False, root, login, password, key, secret_key)
    
    do_test(wizard, store)

def s3_test(wizard):
    bucket = wizard.fields["s3bucket"].value
    key = wizard.fields["s3key"].value
    secret_key = wizard.fields["s3secretkey"].value
    store = S3Store("store", 0, False, bucket, key, secret_key)
    
    do_test(wizard, store)
    


def share_test(wizard):
    path = wizard.fields["sharepath"].value
    mountcmd = wizard.fields["sharemountcmd"].value
    umountcmd = wizard.fields["shareumountcmd"].value
    store = ShareStore("store", 0, False, path, mountcmd, umountcmd)
    
    do_test(wizard, store)

def do_test(wizard, store):    
    log.debug("Test connect To", store)

    try:
        with ProgressDialog(wizard, _("Testing"), _("Testing connection to Store.\nPlease wait...")):
            store.test()
        dlg.Info(wizard, _("Successfully connected and tested store"), _("Success"))
    except Exception as e:
        dlg.Warn(wizard, _("Store Test Failed: {error}").format(error=str(e)))


def do_store_wizard(parent):
    wiz = wizard.Wizard(parent, _("Store Creation Wizard"),
                 _("Welcome to the store creation wizard.\n"
                    "\n"
                    "The first time you use The Vault, you need to configure\n"
                    "a store to hold your backups. This wizard will guide you\n"
                    "through the creation of your store."),
                 _("We are now ready to create the store."), wiz_execute, icon="images/storage.png")

    #    Name
    page = wizard.Page(wiz, _("Store Name"))
    wizard.TextField(page, "name", _("What shall we call this store?"),
                 default=None if not const.Debug else "TestName")
    #    Type of storage
    page = wizard.Page(wiz, _("Type Of Storage"))
    wizard.OptionsField(page, "storagetype", _("What type of store will we connect to?"),
                 [_("Local Folder"), _("FTP Server"), _("Server Share"), _("DropBox"), _("Amazon S3")],
                 default=None if not const.Debug else _("Local Folder"))

    #    Folder storage
    page = wizard.Page(wiz, _("Folder Storage Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("Local Folder"))
    wizard.DirEntryField(page, "folderpath", _("Path To Store"), must_exist=True,
                 default=None if not const.Debug else os.path.join(const.RunDir, "store"))

    #    FTP Storage
    page = wizard.Page(wiz, _("FTP Storage Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("FTP Server"))
    wizard.TextField(page, "ftpserver", _("Name or IP Address of FTP Server"),
                 default=None if not const.Debug else "127.0.0.1")
    wizard.CheckField(page, "sftp", _("Use an encrypted connection"), _("Enable SFTP"),
                 default=None if not const.Debug else False)
    wizard.TextField(page, "ftplogin", _("Login name"),
                 default=None if not const.Debug else "ftpuser")
    wizard.PasswordField(page, "ftppassword", _("Password"),
                 default=None if not const.Debug else "")
    wizard.TextField(page, "ftproot", _("Path to store"),
                 default=None if not const.Debug else "store")
    wizard.ButtonField(page, "ftptest", _("Test"), ftp_test)

    #    DropBox Storage
    page = wizard.Page(wiz, _("DropBox Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("DropBox"))
    wizard.TextField(page, "dblogin", _("Login name"),
                 default=None if not const.Debug else "dbtest")
    wizard.PasswordField(page, "dbpassword", _("Password"),
                 default=None if not const.Debug else "")
    wizard.TextField(page, "dbroot", _("Path To Store"),
                 default=None if not const.Debug else "store")
    wizard.TextField(page, "dbkey", _("Application Key"),
                 default=None if not const.Debug else "key")
    wizard.TextField(page, "dbsecretkey", _("Application Secret Key"),
                 default=None if not const.Debug else "secret key")
    wizard.ButtonField(page, "dbtest", _("Test"), db_test)

    #    S3 Storage
    page = wizard.Page(wiz, _("Amazon S3 Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("Amazon S3"))
    wizard.TextField(page, "s3key", _("Access Key ID"),
                 default=None if not const.Debug else "key")
    wizard.TextField(page, "s3secretkey", _("Secret Access Key ID"),
                 default=None if not const.Debug else "secret key")
    wizard.TextField(page, "s3bucket", _("Bucket Name"),
                 default=None if not const.Debug else "bucket")
    wizard.ButtonField(page, "s3test", _("Test"), s3_test)

    #    Server Share storage
    page = wizard.Page(wiz, _("Server Share Storage Details"), show_cb=lambda wiz: wiz.fields["storagetype"].value == _("Server Share"))
    wizard.DirEntryField(page, "sharepath", "Mount Point", must_exist=True,
                 default=None if not const.Debug else os.path.join(const.RunDir, "store"))
    wizard.TextField(page, "sharemountcmd", _("Command to mount share"),
                 default=None if not const.Debug else "sleep 1")
    wizard.TextField(page, "shareumountcmd", _("Command to unmount share"),
                 default=None if not const.Debug else "sleep 1")
    wizard.ButtonField(page, "sharetest", _("Test"), share_test)


    #    Run the wizard
    wiz.run()
