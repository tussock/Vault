# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import os
import sys
import tarfile
from collections import namedtuple


from lib import const
from lib import passphrase
from lib.config import Config
from lib.db import DB
from store.streamer import StreamIn
from lib import sendemail
from lib import cryptor      #@UnresolvedImport


#    Do this last!
from lib.logger import Logger
log = Logger("server")

backupitem = namedtuple("backupitem", "fs_id run_id name path")



class Restore():
    def __init__(self, destfolder, files, date, options):
        '''
        Prepare to run a backup event
        
        '''
        self.destfolder = destfolder
        self.files = files
        self.date = date
        self.dry_run = options.dry_run
        self.norecurse = options.norecurse
        self.options = options
        self.config = Config.get_config()

        #    Prepare fields for the run
        self.tarfile = None
        self.nfiles = 0
        self.nfolders = 0
        self.start_time = None
        #    This holds the complete list of files to be restored.
        #    It could be large... 
        self.restore_list = []

        #    Check the parameters
        if not os.path.isdir(destfolder):
            raise Exception(_("Destination folder does not exist"))

        self.db = DB()
        log.trace("Created restore object:")


    def run(self):
        '''
        Execute the restore
        '''
        log.info("Starting restore")
        for path in self.files:
            try:
                self.find_offline_files(path, self.date)
            except:
                log.warn("Given file/folder has never been backed up (%s)" % path)
                sys.stderr.write("Given file/folder has never been backed up (%s)\n" % path)
        log.info("%d files to be restored" % len(self.restore_list))

        #    Now find all the runs (using a set so they are unique) then sort so we go from the oldest run forwards. 
        #    TODO! NOTE: some folders wont have a run because they haven't been backed up.
        #    But we still need to create them as intermediate paths.
        run_ids = set([item.run_id for item in self.restore_list if item.run_id])
        log.debug("Runs:", run_ids)
        run_ids = list(run_ids)
        run_ids.sort()

        #    Now we have to do this one run at a time as we may have to connect to each run's store.
        runs = self.db.runs()
        for run_id in run_ids:
            try:
                #    DB stores full unicode, tar stores FS encodings.
                #    Generate a list using the current encoding (utf-8 usually). 
                paths_in_run = set([item.path.encode() for item in self.restore_list if item.run_id == run_id])
                log.debug("In Run", run_id, "looking for files", paths_in_run)
                #    Stream in the tar file, looking for one of these files.
                #    Where will we put it? In destfolder+path
                #    Find the run
                run = [run for run in runs if run.run_id == run_id][0]
                backup = self.config.backups[run.name]
                #    Get a fresh copy of the store
                store = self.config.storage[run.store].copy()
                folder = run.folder
                log.debug("folder", folder, "run", run, "backup", backup, "store", store)
                self.prepare_input(folder, run, backup, store)
                tarinfo = self.tarfile.next()
                while tarinfo and paths_in_run:
                    #    tarinfo.name always has the leading pathsep removed 
                    #    We need to add it back in for comparison
                    path = os.sep + tarinfo.name
                    log.trace("Current tar file", path)
                    if path in paths_in_run:
                        if self.dry_run:
                            print("Restore %s" % path)
                        else:
                            self.tarfile.extract(tarinfo, self.destfolder)
                            log.debug("Extracted", path, "to", self.destfolder)
                            paths_in_run.remove(path)
                    tarinfo = self.tarfile.next()
                self.close_input(backup)
                #    What files didn't get restored?
                if len(paths_in_run) > 0:
                    sys.stderr.write("Failed to restore files:\n")
                    for file in paths_in_run:
                        sys.stderr.write(file + "\n")
            except Exception as e:
                #    Any exception during this run? We note it but still continue
                sys.stderr.write("Failed during read from Backup. %s Error: '%s', continuing...\n" % (str(run), str(e)))
            # TODO! Check for files that weren't found.

        if self.options.message:
            try:
                log.debug("Notifying user")
                from lib.dlg import Notify
                Notify(const.AppTitle, _("Restore is complete"))
            except:
                #    Probably no-one logged in
                log.debug("Unable to notify. No-one logged in?")
        if self.options.email:
            try:
                log.debug("Emailing user")
                self.send_email(True)
            except Exception as e:
                log.debug("Failed to email: ", str(e))
        if self.options.shutdown:
            log.debug("Shutting down")
            os.system("shutdown -P +2")

#        sys.stdout.write("Completed restore\n")

    def send_email(self, result, error_message=None):
        '''
        Send a message to the appropriate users.
        If result is False (failure) then error message will contain the reason.
        
        @param result:
        @param error_message:
        '''
        log.debug("send_email: ", result, error_message)
        message_text = _("Restore of\n    %s\nto folder\n    %s\n%s") % \
                ("\n    ".join(self.files), self.destfolder, _("succeeded") if result else _("failed"))
        if result:
            subject = _("Restore Completed")
        else:
            message_text += _("Error was %s") % (error_message)
            subject = _("Restore FAILED")

        log.debug("Starting mail send")
        try:
            sendemail.sendemail(subject, message_text)
        except Exception as e:
            print("Unable to email results: %s" % str(e))

        log.trace("send_email completed")



    def find_offline_files(self, path, date):
        #    Called to start the search. We dont know if this is a file or folder.
        #    Get details. 
        #    We make sure the file is as it was on the given date.
        log.trace("find_offline_files", path)
        versions = self.db.list_versions_file(path, build=False)
#        for version in versions:
#            print(version)
        #    Last is the most recent
        if len(versions) == 0:
            raise Exception(_("%s has never been backed up") % path)

        #    Find the right version of the file.
        if date is None:
            #    Get the most recent
            version = versions[-1]
        elif len(versions) == 1 and versions[0].type is None:
            #    We have a folder that itself has not been backed up (no versions) but 
            #    its subfolders most likely have.
            version = versions[0]
        else:
            #    We want to find the OLDEST version BEFORE the given date.
            #    That will be the file as it was on that date.
            version = None
            for v in versions:
                if v.mod_time <= date:
                    version = v
                else:
                    #    Gone too far.
                    break
            log.debug("VERSION SEARCH date=%s found version %s versions available %s" % \
                      (str(date),
                       str(version),
                       ", ".join([str(v) for v in versions])))
            if version is None:
                log.debug("File did not exist on the given date", path)
                #    This file did not exist on the given date.
                return

        if version.type == 'F':
            self.restore_list.append(backupitem(version.fs_id, version.run_id, version.name, path))
        elif version.type == 'D' or version.type is None:
            if version.type == 'D':
                self.restore_list.append(backupitem(version.fs_id, version.run_id, version.name, path))
            #    Now wander through the directory contents
            contents = self.db.list_dir(path, build=False)
            for name in contents.iterkeys():
                if name != "/":
                    newpath = os.path.join(path, name)
                    self.find_offline_files(newpath, date)



    def recurse_offline_files(self, folder, date):
        log.trace("Recurse_offline_files:", folder)
        #    Add it to the list
        #    Get a list of folder contents
        contents = self.db.list_dir(folder, build=False)
        for item in contents.itervalues():
            #        if its a file:
            if item.type == "F":
                #            add it on
                path = os.path.join(folder, item.name)
                self.restore_list.append(backupitem(item.fs_id, item.run_id, item.name, path))
            #   if its a folder and not norecurse:
            elif (item.type == "D" or item.type == None) and not self.norecurse:
                #            add it on.
                path = os.path.join(folder, item.name)
                self.restore_list.append(backupitem(item.fs_id, item.run_id, item.name, path))
                #            call find_offline_files for it.
                self.recurse_offline_files(path)

    def prepare_input(self, folder, run, backup, store):
        '''
        Open the tar file.
        Connect the output of the tar to either:
        a) the storage handler
        b) to encryption (openssl), THEN the storage handler
        
        '''
        log.trace("Setting up input processes")

        #    If we are using an external save command, we do nothing here
        if self.dry_run:
            log.info("No input processes: Dry run")
            return

        #    Set up the encryptor 
        if backup.encrypt:
            log.debug("Creating crypto object")
            self.crypto = cryptor.DecryptStream(passphrase.passphrase)
        else:
            self.crypto = cryptor.Buffer()

        #    Set up the storage handler
        log.debug("Starting storage thread")

        self.store_thread = StreamIn(self.crypto, store, folder)
        self.store_thread.start()

        #    Now set up the tar file which will feed all this
        log.debug("Connecting tar object")
        self.tarfile = tarfile.open(mode="r|gz", fileobj=self.crypto, bufsize=const.BufferSize)

        log.trace("Completed input preparation")

    def close_input(self, backup):
        log.trace("Closing output managers")
        #    If we are using an external save command, we do nothing here
        if self.dry_run:
            log.info("No output managers: Dry Run")
            return

        try:
            self.tarfile.close()
            self.crypto.close()
            #    Now we are ready to wait for the storage. 
            #    Force the store close... We may be stopping early
            #    for efficiency reasons.
            self.store_thread.join()
            if self.store_thread.error:
                raise self.store_thread.error

        except Exception as e:
            log.debug("Ignoring errors during close (%s)" % str(e))
            pass
        log.debug("All input closed")

