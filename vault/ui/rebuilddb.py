# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import os
from datetime import datetime
import tempfile
import gzip
import shutil
import wx

from lib.db import DB
from lib import const
from lib import passphrase
from lib import wizard
from lib import dlg
from lib.cryptor import decrypt_file               #@UnresolvedImport
from lib.config import Config
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


def wiz_execute(wiz):

    db = DB()
    config = Config.get_config()

    backups = config.backups.keys()
    backups.sort()
    for name in backups:
        if wiz.fields[name].value:
            #    Get the backup object and store
            backup = config.backups[name]
            store = config.storage[backup.store]

            #    For each run on the store
            with ProgressDialog(wiz, _("Connecting"), _("Connecting to the store.\nPlease wait...")):
                store.connect()
            prog_dlg = ProgressDialog(wiz, _("Loading"), _("Retrieving data from store.\nPlease wait..."))
            prog_dlg.Show()
            try:
                try:
                    runs = store.list(backup.name)
                except:
                    #    If it fails, there were no backup runs
                    runs = []
                runs.sort()
                for run in runs:
                    (date, type) = run.split(" ")
                    date = datetime.strptime(date, const.DateTimeFormat)

                    db.start_run(backup.name, store.name, type, date)
                    db.save_message(_("Database rebuild started"))
                    try:
                        store_size, file_sizes, nfiles, nfolders = recover_run(db, backup, store, run)

                        db.save_message(_("Database rebuild complete"))
                        db.update_run_stats(store_size, nfiles, nfolders, backup.include_packages, "")
                        db.update_run_status(const.StatusSuccess)
                    except Exception as e:
                        msg = _("Database rebuild failed. {error}").format(error=str(e))
                        db.save_message(msg)
                        db.update_run_status(const.StatusFailed)
                        dlg.Warn(wiz, msg, _("Error"))
                        return

            finally:
                prog_dlg.Destroy()
                store.disconnect()


    wiz.parent.force_rebuild()
    #    Now tell app about change.
    app.broadcast_update()
    dlg.Info(wiz, _("Your backup files database has been rebuilt.\nYou can now view your file and backup history."), _("Rebuild"))


def recover_run(db, backup, store, run):
    wx.Yield()
    #    Grab the LOF
    tmp_dir = tempfile.mkdtemp()
    try:
        #    Create encrypted and clear pathnames
        lof_remote = os.path.join(backup.name, run, const.LOFFile)
        lof_remote_enc = os.path.join(backup.name, run, const.LOFFile + const.EncryptionSuffix)
        #    Look at the remote site - is it encrypted or not?
        if store.exists(lof_remote):
            src = lof_remote
            encrypted = False
        elif store.exists(lof_remote_enc):
            src = lof_remote_enc
            encrypted = True
        else:
            raise Exception(_("Backup '{backup}' run '{run}' is corrupt").format(backup=backup.name, run=run))

        #    Get the LOF file
        store.copy_from(src, tmp_dir)
        lof_file = os.path.join(tmp_dir, const.LOFFile)
        #    Decrypt if required.
        if encrypted:
            decrypt_file(passphrase.passphrase, lof_file + const.EncryptionSuffix, lof_file)

        #    Now we open and walk through the ZIP file.
        lof = gzip.GzipFile(lof_file, "rb")
        folder = ""
        nfiles = 0 # the config file
        nfolders = 0
        file_sizes = 0
        while True:
            #    Get the next line, and remove the CR
            line = lof.readline()
            if line is None or line == "":
                break
            if line[-1:] == '\n':
                line = line[:-1]
            log.debug("Next Line", line)
            if line == "":
                #    New folder on the next line
                line = lof.readline()
                if line is None or line == "":
                    break
                if line[-1:] == '\n':
                    line = line[:-1]
                folder = utils.unescape(line)
                nfolders += 1
            else:
                parts = line.split(",")
                type = parts[0]
                name = utils.unescape(parts[1])
                path = os.path.join(folder, name)
                path = utils.path_to_unicode(path)
                if type == "F" or type == "D":
                    mod_time = parts[2]
                    size = parts[3]
                    db.fs_saved(path, mod_time, size, type)
                    if type == 'F':
                        nfiles += 1
                        file_sizes += int(size)
                elif type == 'X':
                    db.fs_deleted(path)
                else:
                    raise Exception(_("Corrupt type in file list"))
            wx.Yield()
        #    To calculate the amount of size, we need to see how big the data files are.
        run_dir = os.path.join(backup.name, run)
        size = 0
        log.debug("Checking files sizes")
        files = store.list(run_dir)
        for file in files:
            size += store.size(os.path.join(run_dir, file))
            wx.Yield()

    finally:
        shutil.rmtree(tmp_dir)
    log.trace("Completed recover run: ", size, file_sizes, nfiles, nfolders)
    return size, file_sizes, nfiles, nfolders

def do_rebuilddb(parent):
    config = Config.get_config()
    wiz = wizard.Wizard(parent, _("Backup Database Recovery"),
                 _("Welcome to the Backup Database Recovery wizard.\n"
                    "\n"
                    "This wizard will interrogate your stores to recover information\n"
                    "about your backed up files. This information is stored locally and\n"
                    "means that backup software can tell you about saved files without\n"
                    "need to contact and read from the store.\n"
                    "\n"
                    "Note that this wizard does not actually recover files, it just recovers\n"
                    "information about those files."),
                 _("We are now ready to restore your backup information."), wiz_execute, 
                 icon=os.path.join(const.PixmapDir, "storage.png"))

    #    Type of storage
    page = wizard.Page(wiz, _("Choose Backups"))
    backups = config.backups.keys()
    backups.sort()
    wizard.LabelField(page, "label",
                      _("Choose which backups to recover details for. This does not recover your\n"
                      "actual files themselves, just information about which files were backed\n"
                      "up and when. Usually you will want to select all."))
    for backup in backups:
        wizard.CheckField(page, backup, None, backup,
                          default=False if not const.Debug else True)

    #    Run the wizard
    wiz.run()
