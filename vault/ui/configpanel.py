# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import os

import gui
import app
from lib import const
from lib.config import Config
from lib import dlg
from lib.db import DB
from lib import sendemail
from lib import utils
from lib import cryptor
from progressdialog import ProgressDialog
from optiondialog import OptionDialog
#    Do last!
from lib.logger import Logger
log = Logger('ui')

#    Edit States
ViewState, NewState = range(2)

class ConfigPanel(gui.ConfigPanel):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        log.info("***ConfigPanel.init")

        gui.ConfigPanel.__init__(self, parent)
        self.config = Config.get_config()
        self.db = DB()        

        self.state = ViewState
        self.update_filetype_list()
        self.clear_filetype()
        self.image = wx.Bitmap(os.path.join(const.PixmapDir, "configure.png"))
        self.title = _("Configuration")
        if self.lstFileTypes.GetCount() > 0:
            self.lstFileTypes.SetSelection(0)
            self.onFileType(None)
        self.show_mail()
        self.txtMailServer.SetFocus()
        self.nb_config.SetSelection(0)

        self.show_security()
        self.pwd_hidden = True
        self.mail_hidden = True

        log.trace("Done ConfigPanel.init")

    def update_data(self):
        pass

    def update_filetype_list(self):
        self.lstFileTypes.Clear()
        self.lstFileTypes.AppendItems(self.config.file_types.keys())


######################################################################3
#
#        FILE TYPE EVENTS
#
######################################################################3


    def onSaveTypes(self, event):
        self.save_filetype()
        self.state = ViewState
        self.update_state()
        self.lstFileTypes.SetStringSelection(self.txtName.GetValue())

    def onFileType(self, event):
        #    Get the name to be showed
        name = self.lstFileTypes.GetStringSelection()
        if len(name) == 0:
            return
        #    Load it
        try:
            list = self.config.file_types[name]
            self.state = ViewState
            self.show_filetype(name, list)
        except Exception:
            #   Missing backup!
            dlg.Warn(self, _("That File Type seems to be missing or corrupt."))
            self.update_filetype_list()
            self.state = ViewState
            self.clear_filetype()
            return


    def onDelete(self, event):
        #    Get the name to be showed
        name = self.lstFileTypes.GetStringSelection()
        if len(name) == 0:
            return
        if dlg.OkCancel(self, _("Delete File Type definition %s and all its data! Are you sure?") % name) == wx.ID_OK:
            self.delete_filetype(name)
            self.clear_filetype()
            self.state = ViewState


    def onNew(self, event):
        log.info("New!")
        self.state = NewState
        self.clear_filetype()
        self.txtName.SetFocus()


    def onName(self, event):
        self.update_state()

    def onSSL(self, event):
        if self.chkMailSSL.GetValue():
            self.txtMailPort.SetValue("465")
        else:
            self.txtMailPort.SetValue("25")


######################################################################3
#
#        EMAIL EVENTS
#
######################################################################3

    def onHideMailPassword(self, event):
        if self.mail_hidden:
            self.txtMailPassword.SetWindowStyle(wx.NORMAL)
            self.mail_hidden = False
            self.btnHideMailPassword.SetLabel("Hide")
        else:
            self.txtMailPassword.SetWindowStyle(wx.TE_PASSWORD)
            self.mail_hidden = True
            self.btnHideMailPassword.SetLabel("Show")

    def onMailAuth(self, event):
        auth = self.chkMailAuth.GetValue()
        self.txtMailLogin.Enable(auth)
        self.txtMailPassword.Enable(auth)

    def onMailSave(self, event):
        self.config.mail_server = self.txtMailServer.GetValue()
        self.config.mail_port = self.txtMailPort.GetValue()
        self.config.mail_ssl = self.chkMailSSL.GetValue()
        self.config.mail_auth = self.chkMailAuth.GetValue()
        self.config.mail_login = self.txtMailLogin.GetValue()
        self.config.mail_password = self.txtMailPassword.GetValue()

        self.config.mail_from = self.txtMailFrom.GetValue()
        self.config.mail_to = self.txtMailTo.GetValue()
        self.config.save()

    def onMailTest(self, event):

        try:
            if not self.txtMailServer.GetValue() \
                    or not self.txtMailFrom.GetValue() \
                    or not self.txtMailTo.GetValue():
                raise Exception(_("Mail server, from address and to address are required."))

            with ProgressDialog(self, _("Sending"), _("Sending a test email.\nPlease wait...")):
                import time
                time.sleep(1)
                log.debug("Doing send")
                sendemail.sendemail2(self.txtMailServer.GetValue(),
                       int(self.txtMailPort.GetValue()),
                       self.chkMailSSL.GetValue(),
                       self.txtMailFrom.GetValue(),
                       self.txtMailTo.GetValue(),
                       self.chkMailAuth.GetValue(),
                       self.txtMailLogin.GetValue(),
                       self.txtMailPassword.GetValue(),
                       _('The Vault Backup System - Test Message'),
                       _("This is a test message from The Vault Backup System.\n"
                       "If you have received this, then email is correctly configured."))
            dlg.Info(self, _("Mail was sent successfully. Please check it arrived."))
        except Exception as e:
            dlg.Warn(self, str(e))


    def show_mail(self):
        self.txtMailServer.SetValue(self.config.mail_server)
        self.txtMailPort.SetValue(str(self.config.mail_port))
        self.chkMailSSL.SetValue(self.config.mail_ssl)
        self.chkMailAuth.SetValue(self.config.mail_auth)
        self.txtMailLogin.SetValue(self.config.mail_login)
        self.txtMailPassword.SetValue(self.config.mail_password)

        self.txtMailFrom.SetValue(self.config.mail_from)
        self.txtMailTo.SetValue(self.config.mail_to)
        self.onMailAuth(None)

######################################################################3
#
#        Security EVENTS
#
######################################################################3

    def onHidePassword(self, event):
        if self.pwd_hidden:
            self.txtMasterPassword.SetWindowStyle(wx.NORMAL)
            self.pwd_hidden = False
            self.btnHidePassword.SetLabel("Hide")
        else:
            self.txtMasterPassword.SetWindowStyle(wx.TE_PASSWORD)
            self.pwd_hidden = True
            self.btnHidePassword.SetLabel("Show")

    def show_security(self):
        if not self.config.data_passphrase:
            self.txtMasterPassword.SetValue("")
        else:
            self.txtMasterPassword.SetValue(self.config.data_passphrase)
        self.onMasterPasswordChar(None)

    def onMasterPasswordChar(self, event):
        """Recalculate entropy any time the password changes."""
        pwd = self.txtMasterPassword.GetValue()
        e = int(cryptor.entropy(pwd))
        if e < 0:
            e = 0
        if e > 100:
            e = 100
        self.strength.SetValue(e)
        if event:
            event.Skip()

    def onSavePassword(self, event):
        pwd = self.txtMasterPassword.GetValue()
        if pwd != self.config.data_passphrase:
            #    Password has changed. Do we have any stored backups? 
            #    If so, they should be deleted.
            runs = self.db.runs()
            num_runs = len(runs)
            if num_runs > 0:
                size = 0
                for run in runs:
                    size += run.size                
                #    Check with the user.
                msg = _("You current have {numruns} backup runs stored, " \
                        "totalling {size} of remote data.\n" \
                        "Changing the Master Password means old encrypted backups cannot be used.\n" \
                        "Note that they can be kept for disaster recovery if needed,\n" \
                        "but we suggest you simply start fresh.").format(\
                        numruns=num_runs, size=utils.readable_form(size))
                mbox = OptionDialog(self, msg, _("Delete Backup Runs"),
                                    _("Also delete all encrypted backup data stored remotely."), 
                                    default=True)
                if mbox.ShowModal() != wx.ID_OK:
                    return
                delete_offsite_data = mbox.chkOption.GetValue()

                #    TODO skip if no runs
                #    We keep track of all errors
                errors = ""
                with ProgressDialog(self, _("Deleting"), _("Deleting old encrypted backup data.\nPlease wait...")):
                    for backup in self.config.backups.itervalues():
                        #    If its encrypted
                        if backup.encrypt:
                            #    If the option set - delete all offline data at the store
                            if delete_offsite_data:
                                try:
                                    #    Get the list of unique stores used by runs of this backup
                                    runs = self.db.runs(backup.name)
                                    stores = set([r.store for r in runs]) 
                                    #    Get the store and delete all data.
                                    for storename in stores:
                                        store = self.config.storage[storename].copy()
                                        store.delete_backup_data(backup.name)
                                except Exception as e:
                                    errors += "\nDelete offline data for %s failed: %s" % (backup.name, str(e))
                            #    Now delete the database records of the run abd backup
                            try:
                                self.db.delete_backup(backup.name)
                            except Exception as e:
                                errors += "\nDelete local backup information for %s failed: " % (backup.name, str(e))
                
                if len(errors) > 0:
                    dlg.Error(self, errors)
                
        if not pwd:
            self.config.data_passphrase = None
            app.show_message('Password cleared')
        else:
            self.config.data_passphrase = pwd
            app.show_message('Password set')
        self.config.save()
        #    Now delete all the backups and offsite data.
        
        
        

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

        #self.pnlDetails.Fit()
        self.pnlDetails.Refresh()


    def clear_filetype(self):
        self.show_filetype("<name>", [])


    def show_filetype(self, name, list):
        try:
            #    General Information
            self.txtName.SetValue(name)
            self.lblName.SetLabel(name)


            # TODO!
            self.txtExtensions.Clear()
            list.sort()
            self.txtExtensions.AppendText("\n".join(list))

            self.update_state()
        except Exception as e:
            log.error("Error showing File Type:", str(e))


    def save_filetype(self):

        #    BUILD THE Storage
        if len(self.txtName.GetValue()) == 0:
            dlg.Warn(self, _("File Type name cannot be blank"))
            return
        list = self.txtExtensions.GetValue().split("\n")
        try:
            #    Create the new file_type object
            name = self.txtName.GetValue()
            #    We already have list from above

            #    ensure the list is clean
            cleanlist = []
            for item in list:
                item = item.strip()
                while len(item) > 0 and item[0] == ".":
                    item = item[1:]
                if len(item) == 0:
                    continue
                if item not in cleanlist:
                    cleanlist.append(item)
            cleanlist.sort()
        except Exception as e:
            dlg.Warn(self, str(e))
            return
        if self.state == ViewState:
            #    Delete the old name
            oldname = self.lstFileTypes.GetStringSelection()
            try:
                del self.config.file_types[oldname]
            except:
                pass
        self.config.file_types[name] = cleanlist

        self.config.save()

        self.update_filetype_list()
        self.show_filetype(name, cleanlist)

######################################################################3
#
#        Misc Routines
#
######################################################################3
    def delete_filetype(self, name):
        del self.config.file_types[name]
        self.config.save()
        self.update_filetype_list()
