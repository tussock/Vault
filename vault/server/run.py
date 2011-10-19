# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import os
import sys
import tarfile
from datetime import datetime, timedelta
import tempfile
import fnmatch
import gzip
import subprocess
import gettext
_ = gettext.gettext

from lib import const
from lib.config import Config
from lib.db import DB
from store.streamer import StreamOut
from store.storebase import StoreFullException
from lib import cryptor      #@UnresolvedImport
from lib import utils
from lib import sendemail
from lib import locking      #@UnresolvedImport
from verify import Verify
#    Do this last!
from lib.logger import Logger
log = Logger("server")



class Run():
    def __init__(self, name, type, options):
        '''
        Prepare to run a backup event
        
        @param name: name of the backup
        @param type: type (Full/Incr)
        @param type: dry_run
        
        If dry_run is True, then we will print the files we *would have* backed
        up to stdout.
        
        '''
        self.type = type
        self.dry_run = options.dry_run
        self.options = options
        self.config = Config.get_config()

        try:
            self.backup = self.config.backups[name]
        except:
            raise Exception(_("Backup is missing or corrupt. Please reconfigure backup."))

        try:
            #    Get a fresh store (a copy of the config version
            self.store = self.config.storage[self.backup.store].copy()
        except:
            raise Exception(_("Storage definition is missing. Please reconfigure backup."))

        self.db = DB()
        self.start_time = None
        self.nfiles = None
        self.nfolders = None
        self.bytes = None
        self.run_id = None
        self.backup_folder = None

        #    Make sure there are no other backups running of this name
        self.lock = locking.InterProcessLock(name="Vault-%s" % self.backup.name)

        #    Build a quick file exclusion list, to speed up exclusion checking
        self.excl_ext = self.build_excl_exts()
        log.debug("Exclusion List:", ",".join(self.excl_ext))


    def run(self):
        '''
        Execute the backup
        '''
        try:
            self.lock.acquire()
        except:
            msg = _("Backup '%s' is already running. New backup run cannot start") \
                    % (self.backup.name)

            if not self.dry_run:
                #    Since this is a real backup, we create the run, write to the log and fail immediately.
                self.db.start_run(self.backup.name, self.backup.store, self.type, datetime.now())
                self.db.save_message(msg)
                self.db.update_run_status(const.StatusFailed)
            else:
                #    We dont need to do anything for a dry run. The message will
                #    be returned to the user.
                pass
            raise Exception(msg)

        #    We have the lock now...
        try:
            self.orig_type = self.type
            self.check_old_backups()
            self.do_backup()
        finally:
            self.lock.release()

    def check_old_backups(self):
        '''
        We have got the lock, but if there was a crash, there may be a "running"
        state backup left behind. Note that we *know* its not running because
        the lock is gone.
        
        Check for it and fail it if there is.
        '''
        log.debug("Checking for dead backups")
        runs = self.db.runs(self.backup.name)
        runs = [run for run in runs if run.status == const.StatusRunning]

        #    It looks like there is a run that is still running.
        for run in runs:
            log.warn("A prior run crashed. Cleaning up %s/%s" % (run.name, run.start_time_str))
            #    Get the store
            log.debug("Attempting to delete remote run data")
            try:
                self.store.delete_run_data(run)
            except:
                pass
            #    Delete the entries in the database (but not the failed run itself)
            #    This means the messages will persist, so we can see the usage.
            log.debug("Attempting to delete DB run data")
            self.db.delete_run_versions(self.run_id)
            #    Update the status
            log.debug("Setting status to failed and logging")
            self.db.execute("update runs set status = ? where run_id = ?", (const.StatusFailed, run.run_id))
            self.db.execute("insert into messages (run_id, message, time) values (?, ?, ?)",
                            (run.run_id, _("Backup run crashed. It was cleaned up."),
                             datetime.now().strftime(const.DateTimeFormat)))


        #        If there are *no* full backups in the history, then this run MUST be a full,
        #        even if an incremental is requested. Actually a request for incremental will
        #        grab all files anyway, but still... lets make the name match the contents.
        runs = self.db.runs(self.backup.name)
        full_count = len([run for run in runs
                            if run.type == const.FullBackup and
                            run.status == const.StatusSuccess])
        log.debug("Full backups: %d" % full_count)
        if full_count == 0 and self.type != const.FullBackup:
            log.debug("Resetting type to Full")
            self.type = const.FullBackup


    def do_backup(self)      :
        self.start_time = datetime.now()
        self.nfiles = 0
        self.nfolders = 0
        self.bytes = 0
        success = False
        message = ""

        self.backup_folder = os.path.join(self.backup.name, self.start_time.strftime(const.DateTimeFormat) + " " + self.type)
        if not self.dry_run:
            self.run_id = self.db.start_run(self.backup.name, self.backup.store, self.type, self.start_time)
            msg = _("Backup {backup}/{type} begins").format(backup=self.backup.name, type=self.type)
            if self.dry_run:
                msg += _(" (Dry Run)")
            log.info(msg)
            self.db.save_message(msg)
            if self.orig_type != self.type:
                #    The backup type was switched
                self.db.save_message(_("NOTE: Backup type switched to {newtype} from {oldtype}").format(
                                                        newtype=self.type, oldtype=self.orig_type))

        #    After here we have a run set up in the database, and can begin logging errors.
        try:
            self.prepare_store()

            #    Prepare output/destinations/encryption
            self.prepare_output()
            try:
                #    Now we actually DO the backup, for each listed folder
                for folder in self.backup.include_folders:
                    self.recursive_backup_folder(folder)

                log.debug("Committing saved fs entries...")
                self.db.fs_saved_commit()

                log.debug("Closing...")
                self.close_output(success=True)
            #raise Exception("Test Exception")
            except Exception as e:
                log.warn("Exception during backup:", str(e))
                #    We are going to fail. But we need to try and close
                #    whatever we can. Closing may fail, but in this case
                #    we ignore that error.
                try:
                    self.close_output(success=False)
                except:
                    pass
                raise e

            if self.backup.verify and not self.dry_run:
                log.info("Starting verify phase")
                self.db.save_message(_("Backup verification started"))
                v = Verify(self.backup.name, self.start_time)
                v.run()
                self.db.save_message(_("Backup verification succeeded"))
#                self.do_verify()

            #    Messaging...
            #    If its a dry run, the command line specifies messaging.
            #    Otherwise both the command line AND backup spec do.
            if not self.dry_run:
                self.db.update_run_status(const.StatusSuccess)
            message = _("Backup {server}/{backup}/{type} completed").format(
                                                            server=utils.get_hostname(), 
                                                            backup=self.backup.name, 
                                                            type=self.type)
            if self.dry_run:
                message += " " + _("(Dry Run)")
            success = True
            if not self.dry_run:
                self.db.save_message(message)

        except Exception as e:
            log.error("Exception in backup. Recording. ", e)
            message = _("Backup {server}/{backup}/{type} failed. {error}").format(
                                                            server=utils.get_hostname(), 
                                                            backup=self.backup.name, 
                                                            type=self.type, 
                                                            error=str(e))
            success = False
            if not self.dry_run:
                self.db.update_run_status(const.StatusFailed)

                #    After a failed backup - we must remove the backup data because it 
                #    cannot be trusted.
                run = self.db.run_details(self.run_id)
                #    Delete the remote data
                log.debug("Attempting to delete remote run data")
                self.store.delete_run_data(run)
                #    Delete the entries in the database (but not the failed run itself)
                #    This means the messages will persist, so we can see the usage.
                log.debug("Attempting to delete DB run data")
                self.db.delete_run_versions(self.run_id)

                self.db.save_message(message)

        if self.options.message or (self.backup.notify_msg and not self.dry_run):
            try:
                from lib.dlg import Notify
                Notify(const.AppTitle, message)
            except Exception as e:
                #    This one is not really an error... there is probably no-one logged in.
                msg = _("Unable to send notification message (no-one logged in)")
                if not self.dry_run:
                    self.db.save_message(message)
                log.info(msg)

        if self.options.email or (self.backup.notify_email and not self.dry_run):
            try:
                self.send_email(success, message)
            except Exception as e:
                msg = _("Unable to email notification message: {error}").format(
                                                error=str(e))
                if not self.dry_run:
                    self.db.save_message(message)
                log.error(msg)
        if self.options.shutdown or (self.backup.shutdown_after and not self.dry_run):
            try:
                cmd = ["zenity", "--question",
                       "--ok-label", _("Shutdown Now"),
                       "--cancel-label", _("Cancel Shutdown"),
                       "--text",
                       _("Backup {backup} complete. Computer will shut down in 2 minutes").format(backup=self.backup.name),
                       "--timeout", "120"]
                status = subprocess.call(cmd)
                log.debug("Shutdown query. status=%d" % status)
                if status == 0 or status == 5:
                    subprocess.Popen("shutdown -P now")
            except Exception as e:
                msg = _("Unable to shutdown PC: {error}").format(
                                                error=str(e))
                if not self.dry_run:
                    self.db.save_message(message)
                log.error(msg)

    def send_email(self, result, head):

        '''
        Send a message to the appropriate users.
        If result is False (failure) then error message will contain the reason.
        
        @param result:
        @param error_message:
        '''
        log.debug("send_email: ", result, head)
        if result:
            message_text = head + \
                    _("\n\nStatistics:\n    {files} files backed up.\n    "
                      "{folders} folders backed up.\n    {size} copied.\n"
                      ).format(files=self.nfiles, folders=self.nfolders, size=utils.readable_form(self.bytes))

            subject = _("Backup {server}/{backup}/{type} completed").format(server=utils.get_hostname(), backup=self.backup.name, type=self.type)
        else:
            message_text = head
            subject = _("Backup {server}/{backup}/{type} failed").format(server=utils.get_hostname(), backup=self.backup.name, type=self.type)

        if not self.options.dry_run:
            messages = "    " + "\n    ".join([message.time + " " + message.message for message in self.db.run_messages(self.run_id)])
            message_text += _("\nBackup messages:\n") + messages
        else:
            message_text = "\n"

        log.debug("Starting mail send")
        try:
            sendemail.sendemail(subject, message_text)
        except Exception as e:
            msg = _("Unable to email results. {error}").format(error=str(e))
            if not self.dry_run:
                self.db.save_message(msg)
            else:
                print(msg)

        log.trace("send_email completed")



    def backup_packages(self):
        '''
        Build the package list. Then send to the backup server
        '''
        log.info("Backing up packages")
        package_list = utils.get_packages()
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write("\n".join(package_list))
        f.close()

        self.copy_file(f.name, const.PackageFile)
        os.remove(f.name)


    def copy_file(self, path, name=None):
        log.debug("CopyFile: ", path, name)
        if not name:
            name = os.path.basename(path)
        if self.dry_run:
            print(utils.escape(name))
            sys.stdout.flush()
        else:
            if self.backup.encrypt:
                if name:
                    name = name + ".enc"    #    Otherwise left as None
                enc_path = path + ".enc"
                cryptor.encrypt_file(self.config.data_passphrase, path, enc_path)
                self.store.send(enc_path, os.path.join(self.backup_folder, name))
                os.remove(enc_path)
            else:
                self.store.send(path, os.path.join(self.backup_folder, name))


    def build_excl_exts(self):
        list = []
        for name in self.backup.exclude_types:
            try:
                for ext in self.config.file_types[name]:
                    list.append(ext)
            except:
                self.db.save_message(_("Exclusion Type %s is no longer recongnised. Ignored.") % name)
        return list

    def list_to_unicode(self, l):
        return [utils.path_to_unicode(p) for p in l]




    def recursive_backup_folder(self, root):
        '''
        Backup a folder and all its sub-folders.
        This routine REQUIRES an absolute path.
        
        @param folder:
        '''
        log.trace("recursive_backup_folder", root)
        #    Before we interact with the FS - convert to utf-8
        root = root.encode('utf-8')
        if len(root) == 0:
            raise Exception(_("Backup_folder called on empty folder name"))
        if root[0] != "/":
            raise Exception(_("Backup_folder requires absolute paths"))
        for folder, local_folders, local_files in os.walk(root):
            #    Lets get everything to unicode
#            local_folders = self.list_to_unicode(local_folders)
#            local_files = self.list_to_unicode(local_files)
            log.debug("os.walk", folder, local_folders, local_files)
            #    First: Check if this is specifically excluded
            if self.check_exclusion(folder):
                log.info("Excluding Dir:", folder)
                continue

            log.info("Backing up folder: %s" % folder)

#            local_files.sort()
#            local_folders.sort()

            #    Get the data on this folder from the db
            db_files = self.db.list_dir(folder)
            log.debug("Backing up folder", folder)
            log.debug("local files:", local_files)
            log.debug("local folders:", local_folders)
            log.debug("DB files:", db_files)

            for local_file in local_files:
                try:
                    local_path = os.path.join(folder, local_file)
                    if self.check_backup(local_path, local_file, db_files):
                        self.do_backup_file(folder, local_file)
                except StoreFullException as e:
                    log.error(str(e))
                    raise e
                except Exception as e:
                    log.warn("Skipping file %s: %s" % (local_file, str(e)))

            #    Convert to unicode for checks below...
            local_folders = self.list_to_unicode(local_folders)
            local_files = self.list_to_unicode(local_files)
            #    Have backed up all the local files. Now look for DB files
            #    that exist, but are not local (i.e. they have been deleted)
            #    Make sure we are only looking for 'F' and 'D' (ignore 'X')
            for db_file in db_files.itervalues():
                try:
                    uname = utils.path_to_unicode(db_file.name)
                    if db_file.type in ['D', 'F'] and not uname in local_files and not uname in local_folders:
                        self.do_backup_deleted(folder, db_file.name)
                except Exception as e:
                    log.warn("Ignoring exception logging deleted file %s: %s" % (db_file.name, e))

            for local_folder in local_folders:
                try:
                    local_path = os.path.join(folder, local_folder)
                    if self.check_backup(local_path, local_folder, db_files):
                        self.do_backup_folder(folder, local_folder)
                except Exception as e:
                    log.warn("Ignoring exception backing up folder %s: %s" % (local_path, e))

#            #    At the completion of a folder - we update the DB storage usage
            if not self.dry_run:
                self.bytes, self.hash = self.store_thread.get_hash()
                self.db.update_run_stats(self.bytes, self.nfiles, self.nfolders, self.backup.include_packages, self.hash)

    def lof_record(self, folder, name, type, mod_time=None, size=None):
        #    Save the entry in the LOF
        log.trace("lof_record", folder, name)
        if folder != self.lof_folder:
            self.lof.write("\n%s\n" % utils.escape(folder))
            self.lof_folder = folder
        self.lof.write("%s,%s" % (type, utils.escape(name)))
        if mod_time:
            self.lof.write(',%s,%d' % (mod_time, size))
        self.lof.write("\n")


    def check_exclusion(self, path):
        _, ext = os.path.splitext(path)
        ext = ext[1:].lower()           #    Remove the '.'
        #    Is this file excluded by type
        if ext in self.excl_ext:
            return True

        #    Is this file excluded by filename/folder/glob
        ancestors = utils.ancestor_paths(path)
        #log.debug("Ancestor Pathlist:", ",".join(ancestors))
        for patt in self.backup.exclude_patterns:
            for path in ancestors:
                if fnmatch.fnmatch(path, patt):
                    return True

        return False



    def check_backup(self, path, basename, db_files):
        log.trace("check_backup", path, basename)
        #    Check for exclusions
        if self.check_exclusion(path):
            log.debug("Excluding", path)
            return False

        #    If this is a full backup, then its included
        if self.type == const.FullBackup:
            log.debug("Include", path, "because full backup")
            return True

        #    Its an incremental - check timestamps.
        #    Find it in the database...
        if not basename in db_files:
            log.debug("Include", path, "because new file")
            return True

        db_file = db_files[basename]
        #    Was the last entry a delete? If so, its back and we back it up
        if db_file.type == 'X':
            log.debug("Include", path, "because file was deleted")
            return True

        if db_file.mod_time == None:
            #    The last version record for this file must have been removed.
            #    This can happen when the storage is too small for a complete
            #    cycle of FULL and INCREMENTALS. The FULL has been deleted and
            #    so there are FS entries, but no version entries.
            return True

        #    Check the timestamp
        #local_modtime = self.get_file_time_str(path)
        local_modtime = datetime.fromtimestamp(os.path.getmtime(path))
        #    The file datetime is to the nearest microsecond. The DB time is not.
        local_modtime -= timedelta(microseconds=local_modtime.microsecond)
        log.debug("MOD TIME CHECK: db: %s local: %s" % (str(db_file.mod_time), str(local_modtime)))
        if local_modtime > db_file.mod_time:
            log.debug("Include", path, "because changed")
            return True

        #    Check if the type has changed
        log.debug("TYPE CHECK: db type = %s isfile=%d" % (db_file.type, os.path.isfile(path)))
        if db_file.type == 'F' and not os.path.isfile(path):
            log.debug("Include", path, "because changed type")
            return True
        if db_file.type == 'D' and not os.path.isdir(path):
            log.debug("Include", path, "because changed type")
            return True

        #    One extra check - just in case. Only for files
        if db_file.type == 'F':
            size = os.path.getsize(path)
            log.debug("SIZE CHECK: db: %s local: %s" % (db_file.size, size))
            if size != db_file.size:
                log.debug("Include", path, "because changed size")
                return True

        return False

    def get_file_time_str(self, path):
        return datetime.fromtimestamp(os.path.getmtime(path)).strftime(const.DateTimeFormat)

    def do_backup_file(self, folder, name):
        log.trace("do_backup_file", folder, name)
        path = os.path.join(folder, name)
        if self.dry_run:
            print("F - %s" % utils.escape(path))
            sys.stdout.flush()
            return

        #    Add it to the tar
        try:
            #    What's the encoding on the file?
            upath = utils.path_to_unicode(path)
            uname = utils.path_to_unicode(name)
            ufolder = utils.path_to_unicode(folder)
            #    Due to issues with encoding... I'll open the file myself and pass to tar
            with open(path, "rb") as f:
                info = self.tarfile.gettarinfo(arcname=upath, fileobj=f)
                self.tarfile.addfile(info, f)
            #self.tarfile.addfile(name=path, recursive=False)

            mod_time = self.get_file_time_str(path)
            size = os.path.getsize(path)
            type = 'F'
            self.db.fs_saved(upath, mod_time, size, type)
            self.nfiles += 1

            #    Save the entry in the LOF
            self.lof_record(ufolder, uname, "F", mod_time, size)

        except Exception as e:
            #    If the exception is in the store - we crash and burn
            #    as we cannot save
            if self.store_thread.error:
                raise self.store_thread.error

            #    Otherwise log it and keep going...
            msg = "Unable to backup %s: %s" % (path, str(e))
            self.db.save_message(msg)
            log.warn(msg)

    def do_backup_folder(self, folder, name):
        log.trace("do_backup_folder", folder, name)
        path = os.path.join(folder, name)
        if self.dry_run:
            print("D - %s" % utils.escape(path))
            sys.stdout.flush()
            return

        #    We dont need to add it to the 
        try:
            self.tarfile.add(name=path, recursive=False)
            mod_time = self.get_file_time_str(path)
            size = 0
            type = 'D'
            self.db.fs_saved(path, mod_time, size, type)
            self.nfolders += 1

            #    Save the entry in the LOF
            self.lof_record(folder, name, "D", mod_time, size)
        except Exception as e:
            log.warn("Exception backing up folder %s: %s" % (path, str(e)))
            #    If the exception is in the store - we crash and burn
            #    as we cannot save
            if self.store_thread.error:
                raise self.store_thread.error

            #    Otherwise log it and keep going...
            msg = "Unable to backup %s: %s" % (path, str(e))
            self.db.save_message(msg)
            log.warn(msg)

    def do_backup_deleted(self, folder, name):
        path = os.path.join(folder, name)
        if self.dry_run:
            print("X - %s" % utils.escape(path))
            sys.stdout.flush()
            return
        try:
            log.debug("FILE/FOLDER DELETED:", name)
            self.db.fs_deleted(path)
            #    We keep track of deletions
            self.lof_record(folder, name, "X")
        except Exception as e:
            #    If the exception is in the store - we crash and burn
            #    as we cannot save
            if self.store_thread.error:
                raise self.store_thread.error

            #    Otherwise log it and keep going...
            msg = "Unable to backup %s: %s" % (path, str(e))
            self.db.save_message(msg)
            log.warn(msg)


    def prepare_store(self):
        #    Test that the storage is available (this will connect and disconnect)
        self.store.test()

        #    Connect to the store
        self.store.connect()

        try:
            log.info("Preparing store")
            #    Ensure the store is properly marked and configured.
            self.store.setup_store()

            if self.backup.include_packages:
                self.backup_packages()

            #    Backup the configuration
            self.copy_file(const.ConfigFile, const.ConfigName)
        finally:
            self.store.disconnect()


    def prepare_output(self):
        '''
        Open the tar file.
        Connect the output of the tar to either:
        a) the storage handler
        b) to encryption (openssl), THEN the storage handler
        
        '''
        log.trace("Setting up output processes")

        #    If we are using an external save command, we do nothing here
        if self.dry_run:
            log.info("No output processes: Dry run")
            return

        #    Set up the encryptor (use TEE for now)
        self.crypt_proc = None
        if self.backup.encrypt:
            log.debug("Creating crypto stream")

            self.crypto = cryptor.EncryptStream(self.config.data_passphrase)

        else:
            self.crypto = cryptor.Buffer()

        #    Set up the storage handler
        log.debug("Starting storage thread")

        self.store_thread = StreamOut(self.crypto, self.store, self.backup_folder)
        self.store_thread.start()

        #    Now set up the tar file which will feed all this
        log.debug("Connecting tar object")
        self.tarfile = tarfile.open(mode="w|gz", fileobj=self.crypto, format=tarfile.PAX_FORMAT, encoding="utf-8",
                                    dereference=False, bufsize=const.BufferSize)

        #    Now set up a zipped temp file to record the list of files/folders saved
        tmp = tempfile.NamedTemporaryFile(delete=False)
        self.lof = gzip.GzipFile(tmp.name, mode="wb", compresslevel=9)
        tmp.close()
        #    Used to keep track of the current folder
        self.lof_folder = ""

        log.trace("Completed output preparation")

    def close_output(self, success):
        '''
        Close as much as we can. This means we may need to ignore some
        errors as we go to ensure everything gets closed.
        
        If success is True, then we have been successful up to this point.
        '''
        log.trace("Closing output managers")
        #    If we are using an external save command, we do nothing here
        if self.dry_run:
            log.info("No output managers: Dry Run")
            return
        #    First exception will be returned.
        error = None
        try:
            self.tarfile.close()
            #    Tar object tries to write after delete. Seems that in an error state,
            #    we get more data after the crypto pipe is closed.
            #    Its an ignorable error, that only occurs when output write fails.
#            del self.tarfile            
        except Exception as e:
            if not error:
                error = e
        try:
            #    Must manually close this (tarfile wont
            #    close a file_obj
            self.crypto.close()
        except Exception as e:
            if not error:
                error = e
        try:
            #    Now we are ready to wait for the storage.
            self.store_thread.join()
            if self.store_thread.error:
                msg = _("Error saving backup: %s") % str(self.store_thread.error)
                log.error(msg)
                self.db.save_message(msg)
                raise self.store_thread.error
        except Exception as e:
            #    This one we will propogate
            error = e
        try:
            self.lof.close()
            if not error and success:
                #    Send the lof only on success
                self.copy_file(self.lof.name, const.LOFFile)
            os.remove(self.lof.name)
        except Exception as e:
            if not error:
                error = e
        try:

            self.store.disconnect()

            #    Update run data, ONLY if this was successful.
            if not error and success:
                self.bytes, self.hash = self.store_thread.get_hash()
                self.db.update_run_stats(self.bytes, self.nfiles, self.nfolders, self.backup.include_packages, self.hash)
        except Exception as e:
            if not error:
                error = e

        log.debug("All output closed. ")
        if error:
            raise error
