# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Created on Nov 10, 2010

@author: paul
'''

import os
import tempfile
import random
import string
from Queue import Queue
from threading import Thread
import re

from lib import const
from lib import utils
from lib.serializer import Serializer

#    Do this last!
from lib.logger import Logger
log = Logger("io")

cLimitRE = "([0-9]+([.][0-9]+)?)([MGT]B)"

class StoreFullException(Exception):
    pass
class StoreCannotDelete(Exception):
    pass

class DebugException(Exception):
    pass

ioClosed, ioReading, ioWriting = range(3)


class IOWorker(Thread):
    def __init__(self, store, queue):
        Thread.__init__(self,
                        name="%s %s" % (store.name, "IOWorker"))

        self.store = store
        self.queue = queue
        #    Crash NOW
        self.terminate = False
        #    When the queue is empty... stop
        self.finish = False
        self.error = None

    def run(self):
        while not self.terminate:
            try:
                work = None
                work = self.queue.get(True, 0.5)
            except:
                #    There was nothing to pick up...
                if self.finish:
                    break
                #    Otherwise we will keep trucking.
                #    But we dont put this in the try block above because 
                #    exceptions below are significant
            if work:
                try:
                    log.debug("Got some work", work)
                    path, dest_path = work
                    if self.store.debug_fail:
                        raise DebugException("FAIL TEST")
                    self.store.send(path, dest_path)
                    log.debug("Success sending work")
                except Exception as e:
                    log.error("Failed to send a file!")
                    self.error = e
                    #    If we can't sent it... fail. 
                    #    Send will retry (usually - can be overridden).
                    break
                finally:
                    try:
                        os.remove(path)
                    except:
                        pass

        #    We are finishing... So clean out the queue and clean up files
        log.debug("Cleaning up files and finishing")
        while not self.queue.empty():
            try:
                work = self.queue.get(True, 0)
                path, _ = work
                os.remove(path)
            except:
                pass
        log.debug("Threading stopping")




class StoreBase(Serializer):
    def __init__(self, name, limit, auto_manage):
        '''
        
        @param name: Name of this store
        @param limit: Either a blank string (no limit) OR
                        [0-9]+(MG|GB|TB)
        @auto_manage: should the space on this store be auto-managed?
            That means the space will be limited to "limit", and old
            runs deleted as required.
        '''
        #    Validate the data                    self.check_space()

        name = name.strip()
        if len(name) == 0:
            raise Exception("Name cannot be empty or consist of only blanks")


        self.name = name
        self.limit = limit
        self.auto_manage = auto_manage

        (total, _, _) = self.limit_details()
        #    If we are auto-managing, then the store must be big enough to be usable.
        #    Otherwise we just assume the store is infinite and let the user manually manage.
        if self.auto_manage and total < const.MinStoreSize:
            raise Exception("Store size must larger than " + utils.readable_form(const.MinStoreSize))

        #    These fields are all we are saving
        self._persistent = ["limit", "name", "auto_manage"]

        self._db = None
        self.connected = False
        self.queue = Queue(maxsize=const.QueueSize)
        self.io_worker = None
        #    For testing... causes a queued xmit to fail.
        self.debug_fail = False


    def __del__(self):
        if hasattr(self, "connected"):
            self.disconnect()
        else:
            #print("Delete called on incompletely constructed object")
            pass

    def copy(self):
        return StoreBase(self.name, self.limit, self.auto_manage)

    def get_hash(self):
        return self.total_bytes, self.hashobj.hexdigest()


    @property
    def db(self):
        '''
        We load the DB object on demand. Stores are created often,
        but they dont often connect to the DB.
        '''
        if not self._db:
            from lib.db import DB
            self._db = DB()
        return self._db


    def limit_details(self):
        '''
        Return the tuple of:
            number of bytes total
            number
            units
        So 1024MB would be returned as:
            1024*1024*1024
            1024
            MB
            
        '''
        log.trace("limit_details")
        if not self.auto_manage or not self.limit:
            return (0, 0, "MB")
        total, num, units = utils.from_readable_form(self.limit)
        log.trace("done limit_details", total, num, units)
        return (total, num, units)

    def current_usage(self):
        '''
        Returns a tuple detailing the current usage and space available.
        
        Tuple contents are: (size, used, available)
        
        If there is no limit (i.e. auto-manage is false), then size = None and avail = None,
        otherwise available = size - used.
        '''
        log.trace("current_usage")
        use = self.db.store_usage(self.name)

        if not self.auto_manage:
            ret = (None, use.size, None)
        else:
            size, _, _ = self.limit_details()
            if size == 0:
                avail = None
            else:
                avail = size - use.size
            ret = (size, use.size, avail)

        log.trace("done current_usage", ret)
        return ret


    def __str__(self):
        return self.name

    def test(self):
        '''
        Test whether this Storage is valid
        Raises an exception if there is a problem.
        '''
        log.info("Beginning Store Test")

        self.connect()
        #    Create a root dir to test from.
        #    There may be multiple simultaneous backups using it,
        #    and there may be multiple machines doing those backups.
        #    So we can't juts use locks. We use a large random number,
        #    and watch for anyone else using it.
        remotedir = "__test%s" % \
            ''.join(random.choice(string.letters + string.digits) for _ in xrange(10))

        if self.exists(remotedir):
            #    Uh oh... very unlikely but possible.
            raise Exception("Test folder in use")

        try:
            tempf = utils.maketempfile(256)
            temps = open(tempf).read()


            #    Create a remote folder
            log.debug("Building temp dir")
            self.make_dir(remotedir)
            if not self.exists(remotedir):
                raise Exception("Unable to create temporary test folder")

            #    Attempt to send 
            log.debug("Sending temp file")
            remotefile = self.send(tempf, remotedir + os.sep)

            #    Make sure it exists
            if not self.exists(remotefile):
                raise Exception("Cannot copy to remote folder")

            #    Get it back and check it is consistent
            contents = self.get_contents(remotefile)
            if contents != temps:
                raise Exception("Writing and reading a file fails")

            #    Attempt to delete (make sure we have delete permission
            self.remove_file(remotefile)
            if self.exists(remotefile):
                raise Exception("Unable to delete remote file")

        except Exception as e:
            raise Exception("Test of store '%s' failed (%s)" % (self.name, e))
        finally:
            #    Clean out the dir too
            if self.exists(remotedir):
                self.remove_dir(remotedir)
            if self.exists(remotedir):
                raise Exception("Unable to remove test dir")
            if os.path.exists(tempf):
                os.remove(tempf)
            self.disconnect()
        log.debug("Success! store test")

    def setup_store(self):
        log.debug("Preparing store. Checking marker")
        if not self.connected:
            self.connect()
        try:
            #    ENSURE the store has the special marker file
            if not self.exists(const.StoreMarkerFile):
                self.set_contents(const.StoreMarkerFile, "STORE")

            log.debug("Preparing store. Copying recovery files")
            #    ENSURE the store has the latest recovery program
            copy_recovery = True
            try:
                if self.exists(const.RecoveryFolder):
                    remote_version_file = os.path.join(const.RecoveryFolder, const.RecoveryVersionFile)
                    local_version_file = os.path.join(const.AppDir, "recovery", const.RecoveryVersionFile)
                    if self.exists(remote_version_file):
                        #    A regex to find the version line
                        test = re.compile("^__version__=.*")          
                        lines = self.get_contents(remote_version_file).splitlines() 
                        #    Find the first line that matches the above filter, then return whats
                        #    after the '='
                        remote_version = filter(test.search, lines)[0].split("=")[1].strip()
                        lines = open(local_version_file).read().splitlines()
                        local_version = filter(test.search, lines)[0].split("=")[1].strip()
                        log.debug("Recovery Version Check: Remote version: '%s' Local Version: '%s'" % (remote_version, local_version))
                        if int(remote_version) >= int(local_version):
                            copy_recovery = False
                else:
                    log.debug("No remote recovery. Sending...")

            except:
                #    Any exception means we update the recovery file
                pass
            if copy_recovery:
                log.debug("Copying recovery files to store")
                for name in const.RecoveryFiles:
                    self.send(os.path.join(const.AppDir, "recovery", name), const.RecoveryFolder + os.sep)
        except:
            raise



############################################################################
#
#    Data and space management
#
############################################################################
# TODO! Note that this is very inefficient.
    def check_space(self, bytes_written):
        '''
        Check if we have enough space to keep writing this run.
        If there isn't - we start deleting runs.

        Parameter is the amount of data written to the store, but not
        yet logged in the database.
        
        In the future:
        a) keep a cache of current usage. It only changes at the completion of a run
        b) Have a start-run and end-run call in the store, so we know when to refetch from the DB
        c) Then always use the cache.
        '''

        if not self.auto_manage:
            return

        #    Needs to VERY quickly check that we have enough space in the store
        #    We target keeping good headroom at all times, so we have plenty of space
        #    for the next buffer write.
        size, used, avail = self.current_usage()
        log.debug("CheckSpace size %d used %d avail %d total_bytes %d" % (size, used, avail, bytes_written))
        #    Check if the amount recorded as used in the DB, plus the amount currently being
        #    written, is bigger than allowed free space
        runs = self.db.store_runs(self.name)
        #    Remove any that are still running (we dont want to remove their space!)
        #    Note that we include FAILED runs - therefore they will eventually be removed.
        #    They dont take any space since their space has already been removed on failure.
        runs = [run for run in runs if run.status != const.StatusRunning]

        #    Note: we need to use a separate store connection for this action
        #    as our store may be busy writing.
        store = None
        try:
            while len(runs) > 0 and avail - bytes_written < const.MinSpaceAvail:
                log.info("CheckSpace: Running low! size %d, used %d, avail %d avail-total_bytes %d minspace %d" % (size, used, avail, avail - bytes_written, const.MinSpaceAvail))
                #    Pick the oldest (the first).
                oldest_run = runs[0]
                del runs[0]
                if not store:
                    #    Create and connect only if required.
                    store = self.copy()
                    store.connect()
                self.db.delete_run(oldest_run.run_id)
                store.delete_run_data(oldest_run)
                #    Now check again...
                size, used, avail = self.current_usage()
        finally:
            if store:
                store.disconnect()
        if avail - bytes_written < const.MinSpaceAvail:
            #    Uh oh.... we have exceeded our usage in this run. CRASH AND BURN
            log.error("Out of space on store")
            raise StoreFullException("Unable to free enough space for backup. Store too small. (size=%s)" % \
                        (utils.readable_form(size)))


    def delete_run_data(self, run):
        '''
        For a given run, all data associated with that run on the store is removed.
        
        It does this by recursively removing the folder representing that run.
        @param run:
        '''
        folder = run.folder;

        log.info("Deleting run folder. Folder=", folder)
        try:
            self.remove_dir(folder)
        except Exception as e:
            #    IF the run is in a failed state, then the folder wont exist. So we ignore the error.
            if run.status == const.StatusFailed:
                log.debug("Folder did not exist")
                pass
            else:
                #    We actually were unable to remove the data. THIS is an issue
                log.error("Deleting run data failed!")
                raise e

    def delete_backup_data(self, backup_name):
        '''
        Delete all runs for this backup.
        
        @param backup_name:
        '''
        self.remove_dir(backup_name)

    def delete_store_data(self):
        '''
        Delete this complete store. All data is removed, including
        all runs, and the store markers. It recursively removes the
        top level directory of the store.
        '''
        self.remove_dir(".")

############################################################################
#
#    Utility functions that use the core functions below
#
############################################################################
    def get_contents(self, src):
        '''
        Retrieve the contents of the given file.
        The contents are returned as a string.
        @param src:
        '''
        if not self.connected:
            self.connect()
        if not self.exists(src):
            raise IOError("File does not exist (%s)" % src)
        tempf = tempfile.NamedTemporaryFile(delete=False)
        try:
            tempf.close()
            self.get(src, tempf.name)
            return open(tempf.name, "r").read()
        finally:
            os.remove(tempf.name)

    def set_contents(self, dest, data):
        '''
        Set the contents of the given file from data passed in
        @param src:
        '''
        if not self.connected:
            self.connect()
        tempf = tempfile.NamedTemporaryFile(delete=False)
        try:
            tempf.write(data)
            tempf.close()
            self.send(tempf.name, dest)
        finally:
            os.remove(tempf.name)

    def remove(self, path):
        '''
        Attempt to remove path. Will raise StoreCannotDelete exception if
        it is unable to delete.
        
        Path can be a file or folder. 
        If it is a folder, the delete will be recursive (i.e. all sub-files/folders
            will also be removed.
            
        This calls remove_file and remove_dir to actually perform the deletion.
            
        @param path:
        '''
        if not self.exists(path):
            return
        try:
            self.remove_file(path)
            if self.exists(path):
                raise Exception()
        except:
            try:
                self.remove_dir(path)
                if self.exists(path):
                    raise Exception
            except:
                raise StoreCannotDelete(_("Unable to delete %s") % path)

############################################################################
#
#    File-like functions.
#
#        By default, these will read/write to a temporary
#        file, then use send/get. But they may be overwritten by a subclass
#        if there is a more efficient way (such as streaming (e.g. FTP)
#        Note that there are no retries when using a file-like interface
#        because the data disappears as soon as it is transmitted.
#
############################################################################

    def open(self, path, mode):
        if not self.connected:
            self.connect()


        if "w" in mode:
            self.io_fd = tempfile.NamedTemporaryFile(delete=False)
            self.io_path = self.io_fd.name
            self.io_state = ioWriting
            #    open a local temp file
            self.io_destpath = path
            #    Special non-blocking mode.
            #    Close will not wait for sending, but will use a thread.
            self.io_block = not ("q" in mode)
        else:
            self.io_state = ioReading
            #    Make a folder to put it
            self.io_folder = tempfile.mkdtemp()
            self.io_folder += os.sep
            #    Fetch the file into that folder. Get its name
            self.io_path = self.get(path, self.io_folder)
            self.io_fd = open(self.io_path, "rb")
            self.io_block = True
        return self

    def read(self, size= -1):
        if self.io_state != ioReading:
            raise Exception("Not opened for reading")
        return self.io_fd.read(size)

    def write(self, data):
        if self.io_state != ioWriting:
            raise Exception("Not opened for writing")
        self.io_fd.write(data)


    def seek(self, offset, whence):
        self.io_fd.seek(offset, whence)

    def tell(self):
        return self.io_fd.tell()

    def close(self):
        self.io_fd.close()
        if self.io_state == ioWriting:
            #    Send (may or may not block
            self.send(self.io_path, self.io_destpath, self.io_block)
        if self.io_block:
            #    If we blocked, then the file has gone. Clean up.
            os.remove(self.io_path)

        if self.io_state == ioReading:
            #    Clean up the temporary folder
            os.rmdir(self.io_folder)
        self.io_state = ioClosed

        #    IF we are not blocking, 
        #    and an io_worker has started AND its in an error state.
        #    Flush will clean up the error, clean up the worker
        #    and raise the error
        if not self.io_block and self.io_worker and self.io_worker.error:
            self.flush()



############################################################################
#
#    Non Blocking Transmit Interface
#
############################################################################

    def flush(self):
        try:
            if self.io_worker:
                log.debug("Waiting for worker to finish")
                self.io_worker.finish = True
                self.io_worker.join()

            #    IF we are not blocking, 
            #    and an io_worker has started AND its in an error state.
            if self.io_worker and self.io_worker.error:
                raise self.io_worker.error
        finally:
            #    The io worker is now dead.
            #    We may need to re-create it if more work 
            #    arrives in the future.
            self.io_worker = None

############################################################################
#
#    The Public interface
#
############################################################################

    def connect(self):
        '''
        Connect to a store. May be implemented in the subclass.
        
        Note that calling connect() when we are already connected is NOT an error.
        '''
        if self.connected:
            return
        self._connect()
        self.connected = True
        self.make_dir("")

    def disconnect(self):
        '''
        Disconnect from a store. May be implemented in the subclass.
        
        Note that calling disconnect when we are already disconnected is NOT an error.
        '''
        if not self.connected:
            return
        self.flush()
        self._disconnect()
        self.connected = False

    def send(self, src, dest, block=True):
        '''
        Send a file to the given location.
        Src must point to a file.
        IF dest ends in os.sep (i.e. the path component separator - '/' on linux):
            it will be created if it doesn't exist
            the final dest file name will be dest/basename(src)
        Otherwise
            dest MUST be the full file name
            the folder will be created as required.
        
        the actual filename will be returned.
        '''
        if not self.connected:
            self.connect()

        #    Do this first - so we know the dest path in case
        #    we have to return it early.
        if len(dest) == 0:
            dest = os.sep
        if dest[-1] == os.sep:
            folder = dest
            dest = os.path.join(folder, os.path.basename(src))
        else:
            folder = os.path.split(dest)[0]

        if not block:
            #    We use a thread to actually manage the send.
            log.debug("Queued writing")
            #    Make sure there is a worker.
            if not self.io_worker:
                log.debug("Starting worker")
                self.io_worker = IOWorker(self, self.queue)
                self.io_worker.start()
            #    This could block if the queue is full
            #    Before we put it into the queue, check that the
            #    ioworker is up and running and not in an error state
            if self.io_worker.error:
                raise self.io_worker.error
            if not self.io_worker.is_alive():
                raise Exception("IO Worker has died")
            self.queue.put((src, dest))
            return dest

        #    Make sure the folder exists
        self.make_dir(folder)

        retries = 0
        success = False
        while not success:
            try:
                log.debug("Storebase blocking send")
                self._send(src, dest)
                success = True
                log.debug("Storebase blocking send Success")
            except Exception as e:
                log.debug("Storebase blocking send Failed. attempt=", retries)
                self.disconnect()
                self.connect()
                retries += 1
                if retries > const.Retries:
                    raise e
        return dest


    def get(self, src, dest):
        '''
        Get a given file from the remote location
        
        The src MUST exist, and MUST be a file on the remote system
        IF dest ends in os.sep (i.e. the path component separator - '/' on linux):
            it will be created if it doesn't exist
            the final dest file name will be dest/basename(src)
        Otherwise
            dest MUST be the full file name
            the folder will be created as required.
        
        the actual filename will be returned.
        '''
        if not self.connected:
            self.connect()
        if dest[-1] == os.sep:
            folder = dest
            dest = os.path.join(folder, os.path.basename(src))
        else:
            folder = os.path.split(dest)[0]
        utils.makedirs(folder)
        retries = 0
        success = False
        while not success:
            try:
                self._get(src, dest)
                success = True
            except Exception as e:
                self.disconnect()
                self.connect()
                retries += 1
                if retries > const.Retries:
                    raise e
        return dest

    def make_dir(self, folder):
        '''
        Create a given directory.
        
        If the folder already exists, no error is raised.
        Any parent paths required to create folder will also
            be created.
        
        @param folder:
        @type folder:
        '''
        #    Make the folder.
        if not self.connected:
            self.connect()
        self._make_dir(folder)

    def remove_file(self, path):
        '''
        Called to remove a file from the remote system
        
        @param path:
        @type path:
        '''
        if not self.connected:
            self.connect()
        self._remove_file(path)

    def remove_dir(self, path):
        '''
        Called to remove a folder from the remote system.
        Note that this is a recursive operation, so all files and folders
        underneath will be deleted.
        
        @param path:
        @type path:
        '''
        if not self.connected:
            self.connect()
        self._remove_dir(path)

    def exists(self, path):
        '''
        Verify that the given file or folder exists.
        
        @param path:
        @type path:
        '''
        folder, filename = os.path.split(path)
        try:
            return filename in self.list(folder)
        except:
            #    Most likely the folder doesn't exist
            return False

    def list(self, folder="."):
        '''
        List the contents of the given dir
        
        @param path:
        @type path:
        '''
        if not self.connected:
            self.connect()
        return self._list(folder)

    def size(self, path):
        '''
        Return the size of the given file in bytes
        May not be implemented on all FTP servers (should be).
        
        If path is a folder, this will return 0.
        @param path:
        '''
        if not self.connected:
            self.connect()
        return self._size(path)

############################################################################
#
#    The subclassed interface
#
############################################################################


    def _connect(self):
        raise Exception("Unimplemented operation")
    def _dicconnect(self):
        raise Exception("Unimplemented operation")
    def _send(self, src, dest):
        raise Exception("Unimplemented operation")
    def _get(self, src, dest):
        raise Exception("Unimplemented operation")
    def _make_dir(self, folder):
        raise Exception("Unimplemented operation")
    def _remove_file(self, path):
        raise Exception("Unimplemented operation")
    def _remove_dir(self, path):
        raise Exception("Unimplemented operation")
    def _list(self, folder="."):
        raise Exception("Unimplemented operation")
    def _size(self, path):
        raise Exception("Unimplemented operation")

