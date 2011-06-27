# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import os
import tarfile
import tempfile
import gettext
_ = gettext.gettext

from lib import const
from lib.config import Config
from lib import passphrase
from lib.db import DB
from store.streamer import StreamIn
from lib import cryptor                #@UnresolvedImport

#    Do this last!
from lib.logger import Logger
log = Logger("server")

class Verify():
    def __init__(self, backup_name, run_date):
        '''
        Verify a run to ensure it is valid
        
        '''
        self.config = Config.get_config()
        self.backup = self.config.backups[backup_name]
        self.store = self.config.storage.get(self.backup.store)

        self.db = DB()

        #    Find the run
        runs = self.db.runs(self.backup.name, run_date)
        if len(runs) == 0:
            raise Exception(_("Verify failed: Backup run does not exist"))
        self.vrun = runs[0]


    def run(self):

        self.test_store()
        #    Get config and packages
        self.fetch_config()

        #    We only check the data if there is actually something stored there.
        if self.vrun.nfiles == 0 and self.vrun.nfolders == 0:
            return True

        self.prepare_input(self.vrun, self.backup, self.store)
        try:
            #    Only check for tar data if there are files backed up
            #    Otherwise the tar will simply return an error
            tarinfo = self.tarfile.next()
            while tarinfo:
                tarinfo = self.tarfile.next()

        finally:
            self.close_input(self.backup)

        store_size, store_hash, = self.store_thread.get_hash()
        run_hash = self.vrun.hash
        run_size = self.vrun.size
        if store_size == run_size and store_hash == run_hash:
            return True
#        print(store_size, store_hash, run_size, run_hash)
        raise Exception(_("Verify failed - Run data is corrupt"))

    def test_store(self):
        store = self.config.storage.get(self.store.name)
        store.connect()
        try:
            store.test()
        finally:
            store.disconnect()

    def fetch_config(self):
        store = self.config.storage.get(self.store.name)
        store.connect()
        try:
            encrypted = False
            config = os.path.join(self.vrun.folder, const.ConfigName)
            if not store.exists(config):
                encrypted = True
                config = config + const.EncryptionSuffix
                if not store.exists(config):
                    raise Exception(_("Configuration file missing. Bad run"))

            store.get(config, os.path.join(tempfile.gettempdir(), "__vault__tmp__"))
            os.remove(os.path.join(tempfile.gettempdir(), "__vault__tmp__"))
            if self.backup.include_packages:
                packages = os.path.join(self.vrun.folder, const.PackageFile)
                if encrypted:
                    packages = packages + const.EncryptionSuffix
                store.get(packages, os.path.join(tempfile.gettempdir(), "__vault__tmp__"))
                os.remove(os.path.join(tempfile.gettempdir(), "__vault__tmp__"))
        finally:
            store.disconnect()

    def prepare_input(self, run, backup, store):
        '''
        Open the tar file.
        Connect the output of the tar to either:
        a) the storage handler
        b) to encryption (openssl), THEN the storage handler
        
        '''
        log.trace("Setting up input processes")

        #    Set up the encryptor (use TEE for now)
        self.crypt_proc = None
        if backup.encrypt:
            log.debug("Creating crypt objects")
            self.crypto = cryptor.DecryptStream(passphrase.passphrase)
        else:
            self.crypto = cryptor.Buffer()

        #    Set up the storage handler
        log.debug("Starting storage thread")

        self.store_thread = StreamIn(self.crypto, store, run.folder)
        self.store_thread.start()

        log.debug("Connecting tar object")
        self.tarfile = tarfile.open(mode="r|gz", fileobj=self.crypto)

        log.trace("Completed input preparation")

    def close_input(self, backup):
        log.trace("Closing output managers")
        #    If we are using an external save command, we do nothing here
        try:
            self.tarfile.close()
            self.crypto.close()
            #    Now we are ready to wait for the storage.
            self.store_thread.join()
            if self.store_thread.error:
                log.error("Closing store. Got error", str(self.store_thread.error))
#                self.db.save_message("Error saving backup: %s" % str(self.store_thread.error))
                raise self.store_thread.error

        finally:
            pass
        log.debug("All input closed")



#    def run(self):
#        '''
#        Execute the restore
#        '''
#        log.info("Starting restore")
#        self.start_time = datetime.now()
#        self.nfiles = 0
#        self.nfolders = 0
#        #    We need to build a complete list of files to be restored.
#        #    Warning... this could be large.
#        self.restore_list = []
#        for path in self.files:
#            try:
#                self.find_offline_files(path, self.date)
#            except:
#                log.warn("Given file/folder has never been backed up (%s)" % path)
#        log.debug("Files to be restored", self.restore_list)
#        log.info("%d files to be restored" % len(self.restore_list))
#
#        #    Now find all the runs (using a set so they are unique) then sort so we go from the oldest run forwards. 
#        #    TODO! NOTE: some folders wont have a run because they haven't been backed up.
#        #    But we still need to create them as intermediate paths.
#        run_ids = set([item.run_id for item in self.restore_list if item.run_id])
#        log.debug("Runs:", run_ids)
#        run_ids = list(run_ids)
#        run_ids.sort()
#
#        #    Now we have to do this one run at a time as we may have to connect to each run's store.
#        runs = self.db.runs()
#        for run_id in run_ids:
#            try:
#                paths_in_run = set([item.path for item in self.restore_list if item.run_id == run_id])
#                log.debug("In Run", run_id, "looking for files", paths_in_run)
#                #    Stream in the tar file, looking for one of these files.
#                #    Where will we put it? In destfolder+path
#                #    Find the run
#                run = [run for run in runs if run.run_id == run_id][0]
#                backup = self.config.backups[run.name]
#                #    Get a fresh copy of the store
#                store = self.config.storage.get(run.store)
#                folder = run.folder
#                log.debug("folder", folder, "run", run, "backup", backup, "store", store)
#                self.prepare_input(folder, run, backup, store)
#                tarinfo = self.tarfile.next()
#                while tarinfo:
#                    #    tarinfo.name always has the leading pathsep removed 
#                    #    We need to add it back in for comparison
#                    path = os.sep + tarinfo.name
#                    log.trace("Current tar file", path)
#                    if path in paths_in_run:
#                        if self.dry_run:
#                            print("Restore %s" % path)
#                        else:
#                            self.tarfile.extract(tarinfo, self.destfolder)
#                            log.debug("Extracted", path, "to", self.destfolder)
#                            paths_in_run.remove(path)
#                    tarinfo = self.tarfile.next()
#                self.close_input(backup)
#                #    What files didn't get restored?
#                if len(paths_in_run) > 0:
#                    sys.stderr.write("Failed to restore files:\n")
#                    for file in paths_in_run:
#                        sys.stderr.write(file + "\n")
#            except Exception as e:
#                #    Any exception during this run? We note it but still continue
#                sys.stderr.write("Failed during read from Backup. %s Error: '%s', continuing...\n" % (str(run), str(e)))
#            # TODO! Check for files that weren't found.
#
#        if self.options.message:
#            log.debug("Notifying user")
#            Notify(const.AppTitle, "Restore is complete")
#        if self.options.email:
#            log.debug("Emailing user")
#            self.send_email(True)
#        if self.options.shutdown:
#            log.debug("Shutting down")
#            os.system("shutdown -P +2")
#
##        sys.stdout.write("Completed restore\n")
#
#    def send_email(self, result, error_message=None):
#        '''
#        Send a message to the appropriate users.
#        If result is False (failure) then error message will contain the reason.
#        
#        @param result:
#        @param error_message:
#        '''
#        log.debug("send_email: ", result, error_message)
#        if result:
#            message_text = "Restore to folder %s completed." % (self.destfolder)
#
#            subject = "Restore Completed"
#        else:
#            message_text = "Restore FAILED\n\nERROR: %s" % (error_message)
#            subject = "Restore FAILED"
#
#        log.debug("Starting mail send")
#        try:
#            sendemail.sendemail(subject, message_text)
#        except Exception as e:
#            print("Unable to email results: %s" % str(e))
#
#        log.trace("send_email completed")
#
#
#
#    def find_offline_files(self, path, date):
#        #    Called to start the search. We dont know if this is a file or folder.
#        #    Get details. 
#        #    We make sure the file is as it was on the given date.
#        log.trace("find_offline_files", path)
#        versions = self.db.list_versions_file(path, build=False)
#        #    Last is the most recent
#        if len(versions) == 0:
#            raise Exception("%s has never been backed up" % path)
#
#        #    Find the right version of the file.
#        if date is None:
#            #    Get the most recent
#            version = versions[-1]
#        elif len(versions) == 1 and versions[0].type is None:
#            #    We have a folder that itself has not been backed up (no versions) but 
#            #    its subfolders most likely have.
#            version = versions[0]
#        else:
#            #    We want to find the OLDEST version BEFORE the given date.
#            #    That will be the file as it was on that date.
#            version = None
#            for v in versions:
#                if v.mod_time <= date:
#                    version = v
#                else:
#                    #    Gone too far.
#                    break
#            log.debug("VERSION SEARCH date=%s found version %s versions available %s" % \
#                      (str(date), 
#                       str(version), 
#                       ", ".join([str(v) for v in versions])))
#            if version is None:
#                log.debug("File did not exist on the given date", path)
#                #    This file did not exist on the given date.
#                return
#            
#        if version.type == 'F':
#            self.restore_list.append(backupitem(version.fs_id, version.run_id, version.name, path))
#        elif version.type == 'D' or version.type is None:
#            if version.type == 'D':
#                self.restore_list.append(backupitem(version.fs_id, version.run_id, version.name, path))
#            #    Now wander through the directory contents
#            contents = self.db.list_dir(path, build=False)
#            for name, item in contents.iteritems():
#                newpath = os.path.join(path, name)
#                self.find_offline_files(newpath, date)
#            
#
#
#    def recurse_offline_files(self, folder, date):
#        log.trace("Recurse_offline_files:", folder)
#        #    Add it to the list
#        #    Get a list of folder contents
#        contents = self.db.list_dir(folder, build=False)
#        for name, item in contents.iteritems():
#            #        if its a file:
#            if item.type == "F":
#                #            add it on
#                path = os.path.join(folder, item.name)
#                self.restore_list.append(backupitem(item.fs_id, item.run_id, item.name, path))
#            #   if its a folder and not norecurse:
#            elif (item.type == "D" or item.type == None) and not self.norecurse:
#                #            add it on.
#                path = os.path.join(folder, item.name)
#                self.restore_list.append(backupitem(item.fs_id, item.run_id, item.name, path))
#                #            call find_offline_files for it.
#                self.recurse_offline_files(path)
#
#
