# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import locale
import os

import gui
from lib.db import DB
from lib import const
from lib.config import Config
from lib import utils
from lib import dlg

from store.folderstore import FolderStore
from store.ftpstore import FTPStore
from store.dropboxstore import DropBoxStore
from store.sharestore import ShareStore
from store.s3store import S3Store
import app
from optiondialog import OptionDialog
from editpanel import EditPanel, ViewState, NewState
from progressdialog import ProgressDialog

#    Do last!
from lib.logger import Logger
log = Logger('ui')


class StoragePanel(EditPanel, gui.StoragePanel):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        log.info("***StorePanel.init")
        gui.StoragePanel.__init__(self, parent)

        self.db = DB()
        self.config = Config.get_config()
        self.state = ViewState
        self.load_static_data()
        self.update_store_list()
        self.clear()
        if self.lstItems.GetCount() > 0:
            self.lstItems.SetSelection(0)
            self.onItemSelected(None)

        self.onAutoManage(None)
        self.image = wx.Bitmap(os.path.join(const.PixmapDir, "storage.png"))
        self.title = _("Storage")

        self.ftp_hidden = True
        self.db_hidden = True

        log.trace("Done StorePanel.init")

    def update_data(self):
        sel = self.lstItems.GetStringSelection()
        self.update_store_list()
        self.lstItems.SetStringSelection(sel)

    def update_store_list(self):
        self.lstItems.Clear()
        self.lstItems.AppendItems(self.config.storage.keys())

    def load_static_data(self):
        self.cboLimitUnits.Clear()
        self.cboLimitUnits.AppendItems(const.DiskUnits)
        self.cboLimitUnits.SetSelection(0)

######################################################################3
#
#        EVENTS
#
######################################################################3


    def onTest(self, event):
        #    Get the name to be tested
        name = self.lstItems.GetStringSelection()
        if len(name) == 0:
            return
        #    Load it
        try:
            with ProgressDialog(self, _("Testing"), _("Testing connectivity and access to the store.\nPlease wait...")):
                s = self.config.storage[name].copy()
                s.test()
            dlg.Info(self, _("Store {store} OK").format(store=name))
        except Exception as e:
            #   Missing backup!
            dlg.Warn(self, str(e))
        finally:
            app.clear_message()

    def onAutoManage(self, event):
        mng = self.chkAutoManage.GetValue()
        self.txtLimitSize.Enabled = mng
        self.cboLimitUnits.Enabled = mng

    def onFolderChoose(self, event):
        dlg = wx.DirDialog(self, _("Choose A Store Folder"), defaultPath=self.txtFolderPath.GetValue())
        if dlg.ShowModal() == wx.ID_OK:
            self.txtFolderPath.SetValue(dlg.GetPath())
        dlg.Destroy()

    def onShareChoose(self, event):
        dlg = wx.DirDialog(self, _("Choose A Store Folder"), defaultPath=self.txtShareRoot.GetValue())
        if dlg.ShowModal() == wx.ID_OK:
            self.txtShareRoot.SetValue(dlg.GetPath())
        dlg.Destroy()

    def onLimitChar(self, event):
        log.trace("StoragePanel.onLimitChar", event, event.GetUniChar())
        if event.GetKeyCode() in [
                                  wx.WXK_TAB,
                                  wx.WXK_BACK,
                                  wx.WXK_RETURN,
                                  wx.WXK_DELETE, 
                                  wx.WXK_CLEAR,
                                  wx.WXK_HOME,
                                  wx.WXK_END,
                                  wx.WXK_LEFT,
                                  wx.WXK_RIGHT,
                                  wx.WXK_UP,
                                  wx.WXK_DOWN,
                                  wx.WXK_INSERT,
                                  wx.WXK_NUMPAD_HOME,
                                  wx.WXK_NUMPAD_END,
                                  wx.WXK_NUMPAD_LEFT,
                                  wx.WXK_NUMPAD_RIGHT,
                                  wx.WXK_NUMPAD_UP,
                                  wx.WXK_NUMPAD_DOWN,
                                  wx.WXK_NUMPAD_INSERT,
                                  wx.WXK_NUMPAD_DELETE]:
            #    OK
            event.Skip()
            return
        ch = unichr(event.GetUniChar())
        dp = unicode(locale.localeconv()['decimal_point'])
        has_dp = self.txtLimitSize.GetValue().find(dp) >= 0

        if ch.isdigit() or (ch == dp and not has_dp):
            if event.HasModifiers() or event.MetaDown() or event.ShiftDown():
                pass
            else:
                #    OK
                event.Skip()
        else:
            #    Eat the event
            pass

    def onDropBoxClick(self, event):
        url = self.url_dropbox_create.GetURL()
        import webbrowser
        webbrowser.open(url, new=1, autoraise=True)
        app.show_message("Opening browser to DropBox")


    def onFTPHidePassword(self, event):
        if self.ftp_hidden:
            self.txtFTPPass.SetWindowStyle(wx.NORMAL)
            self.ftp_hidden = False
            self.btnFTPHidePassword.SetLabel("Hide")
        else:
            self.txtFTPPass.SetWindowStyle(wx.TE_PASSWORD)
            self.ftp_hidden = True
            self.btnFTPHidePassword.SetLabel("Show")

    def onDBHidePassword(self, event):
        if self.db_hidden:
            self.txtDBPass.SetWindowStyle(wx.NORMAL)
            self.db_hidden = False
            self.btnDBHidePassword.SetLabel("Hide")
        else:
            self.txtDBPass.SetWindowStyle(wx.TE_PASSWORD)
            self.db_hidden = True
            self.btnDBHidePassword.SetLabel("Show")


######################################################################
#
#        Save and Load
#
######################################################################
    def update_state(self):
        if self.state == ViewState:
            self.lblName.Show(True)
            self.txtName.Show(False)
        if self.state == NewState:
            self.lblName.Show(False)
            self.txtName.Show(True)
            self.pnlName.Fit()


    def clear(self):
        d = FolderStore("<name>", "", False, "<folder>")
        self.show_store(d)

    def delete(self, name):
        use = self.db.store_usage(name)
        if use.size > 0:
            log.debug(name, utils.readable_form(use.size))
            msg = _("Store '{store}' contains {size} of backups.\nAre you sure?").format(
                                                store=name, size=utils.readable_form(use.size))
            mbox = OptionDialog(self, msg, _("Delete Store"), _("Also delete all backup data stored on the store."))
            if mbox.ShowModal() == wx.ID_OK:
                with ProgressDialog(self, _("Deleting"), _("Deleting store %s.\nPlease wait. This can take a while..." % name)):
                    
                    self.delete_store(name, mbox.chkOption.GetValue())
                    self.clear()
                    self.state = ViewState
        else:
            ret = dlg.OkCancel(self, _("Store '{store}' is not currently used. Delete?").format(store=name))
            if ret == wx.ID_OK:
                with ProgressDialog(self, _("Deleting"), _("Deleting store %s.\nPlease wait. This can take a while..." % name)):
                    self.delete_store(name, False)
                    self.clear()
                    self.state = ViewState
        app.broadcast_update()


    def show(self, name):
        #    Load it
        try:
            store = self.config.storage[name].copy()
            self.state = ViewState
            self.show_store(store)
        except :
            #   Missing backup!
            dlg.Warn(self, _("The store '{store}' seems to be corrupt.").format(store=name))
#            self.update_store_list()
#            self.state = ViewState
#            self.clear()
            return


    def show_store(self, d):
        try:
            #    General Information
            self.txtName.SetValue(d.name)
            self.lblName.SetLabel(d.name)

            #    Storage Information. More specialised first. then more general
            if isinstance(d, ShareStore):
                self.nbStoreType.SetSelection(2)
                self.txtShareRoot.SetValue(d.root)
                self.txtShareMount.SetValue(d.mount)
                self.txtShareUMount.SetValue(d.umount)
            elif isinstance(d, FolderStore):
                self.nbStoreType.SetSelection(0)
                self.txtFolderPath.SetValue(d.root)
            elif isinstance(d, FTPStore):
                self.nbStoreType.SetSelection(1)
                self.txtFTPAddress.SetValue(d.ip)
                self.txtFTPRoot.SetValue(d.root)
                self.chkSFTP.SetValue(d.sftp)
                self.txtFTPLogin.SetValue(d.login)
                self.txtFTPPass.SetValue(d.password)
            elif isinstance(d, DropBoxStore):
                self.nbStoreType.SetSelection(3)
                self.txtDBRoot.SetValue(d.root)
                self.txtDBLogin.SetValue(d.login)
                self.txtDBPass.SetValue(d.password)
                self.txtDBKey.SetValue(d.app_key)
                self.txtDBSecretKey.SetValue(d.app_secret_key)
            elif isinstance(d, S3Store):
                self.nbStoreType.SetSelection(4)
                self.txtAmazonBucket.SetValue(d.bucket)
                self.txtAmazonKey.SetValue(d.key)
                self.txtAmazonSecretKey.SetValue(d.secret_key)
            else:
                raise Exception("Invalid store type")

            (dummy, num, units) = d.limit_details()
            self.txtLimitSize.SetValue(str(num))
            self.cboLimitUnits.SetStringSelection(units)

            self.chkAutoManage.SetValue(d.auto_manage)
            self.onAutoManage(None)

            #    Whats inside the store.
            use = self.db.store_usage(d.name)
            if not use or use.size == 0:
                self.lblContentDetails.SetLabel("Empty")
            else:
                self.lblContentDetails.SetLabel(
                            _("Size {size}, Files {files}, Folders {folders}").format(
                            size=utils.readable_form(use.size), files=utils.comma_int(use.nfiles),
                            folders=utils.comma_int(use.nfolders)))



            self.update_state()
        except Exception as e:
            log.error("Error showing store:", str(e))
            dlg.Error(self, _("Store {store} appears to be corrupt. Unable to show.").format(name=d.name))


    def save(self):

        #    BUILD THE Storage
        if len(self.txtName.GetValue()) == 0:
            raise Exception(_("Storage name cannot be blank"))
        try:
            #    Create the new backup object
            name = self.txtName.GetValue()
            auto_manage = self.chkAutoManage.GetValue()
            #    Convert to float and back to string. Cleans up the number
            limit = str(float(self.txtLimitSize.GetValue())) + self.cboLimitUnits.GetStringSelection()

            if self.nbStoreType.GetSelection() == 0:
                root = self.txtFolderPath.GetValue()
                d = FolderStore(name, limit, auto_manage, root)
            elif self.nbStoreType.GetSelection() == 1:
                ip = self.txtFTPAddress.GetValue()
                root = self.txtFTPRoot.GetValue()
                sftp = self.chkSFTP.GetValue()
                login = self.txtFTPLogin.GetValue()
                password = self.txtFTPPass.GetValue()
                d = FTPStore(name, limit, auto_manage, ip, root, login, password, sftp)
            elif self.nbStoreType.GetSelection() == 2:
                root = self.txtShareRoot.GetValue()
                mount = self.txtShareMount.GetValue()
                umount = self.txtShareUMount.GetValue()
                d = ShareStore(name, limit, auto_manage, root, mount, umount)
            elif self.nbStoreType.GetSelection() == 3:
                root = self.txtDBRoot.GetValue()
                login = self.txtDBLogin.GetValue()
                password = self.txtDBPass.GetValue()
                app_key = self.txtDBKey.GetValue()
                app_secret_key = self.txtDBSecretKey.GetValue()
                d = DropBoxStore(name, limit, auto_manage, root, login, password, 
                                 app_key, app_secret_key)
            elif self.nbStoreType.GetSelection() == 4:
                bucket = self.txtAmazonBucket.GetValue()
                key = self.txtAmazonKey.GetValue()
                secret_key = self.txtAmazonSecretKey.GetValue()
                d = S3Store(name, limit, auto_manage, bucket, key, secret_key)
            else:
                log.error("Invalid Storage Type")
                raise Exception(_("Invalid Storage type"))
        except Exception as e:
            raise e
        if self.state == ViewState:
            #    Delete the old name
            oldname = self.lstItems.GetStringSelection()
            try:
                del self.config.storage[oldname]
            except:
                pass
        self.config.storage[d.name] = d

        self.config.save()

        self.update_store_list()
        self.show_store(d)

######################################################################3
#
#        Misc Routines
#
######################################################################3
    def delete_store(self, name, delete_store_data):
        store = self.config.storage[name].copy()
        self.db.delete_store(name)
        if delete_store_data:
            store.delete_store_data()
        del self.config.storage[name]
        self.config.save()
        self.update_store_list()
