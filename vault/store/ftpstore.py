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
from threading import Thread, RLock
from ftplib import FTP, FTP_TLS
import time
import ssl

from storebase import *
from lib import utils
from lib import const
from lib import passphrase
from lib.cryptor import decrypt_string_base64, encrypt_string_base64


#    Do this last!
from lib.logger import Logger
log = Logger("io")



class FTPStreamer(Thread):
    def __init__(self, ftp, path, mode):
        Thread.__init__(self, name="FTPWorker")
        log.trace("FTPStreamer init", ftp, path, mode)
        self.ftp = ftp
        self.path = path
        self.mode = mode

        self.lock = RLock()
        self.buffer = []
        self.bufsize = 0
        self.done = False
        self.error = None

    def run(self):
        '''
        This is a file-like threaded object.
        It performs a single file transfer.
        
        It assumes the FTP object is already connected.
        1) Start up a storbinary call
        2) the FTP object then reads from self. We block that read if there
            is no data available
        3) At the same time, the backup producer (TAR'd, ZIP'd, (possibly) ENCRYPTED 
            stream of data is written to this object. As this data becomes
            available, this object hands it to the FTP Server.
            I dont allow the write to get too far ahead, so I can block
            the write.

        '''
        try:
            if self.mode == ioWriting:
                log.info("Starting storbinary call for", self.path)
                self.ftp.storbinary("STOR " + self.path, self)
            else:
                log.info("Starting retrbinary call for", self.path)
                self.ftp.retrbinary("RETR " + self.path, self.write)
        except Exception as e:
            self.error = IOError(str(e))
            log.debug("Exception in FTPWorker", self.error)
        self.done = True
        log.trace("FTPWorker.run complete")




    def read(self, size= -1):
        log.trace("FTPWorker.read", size)
        #    Wait until there is data OR we have been told to stop.
        while self.bufsize == 0 and not self.done and not self.error:
            time.sleep(0.01)

        if self.error:
            raise self.error

        if self.bufsize == 0 and self.done:
            log.info("Read finished. No data and done set.")
            return ""

        self.lock.acquire()
        try:
            #    Return all the data we have (up to size)
            buf = "".join(self.buffer)
            log.debug("Returning %d bytes to FTP" % len(buf))
            self.buffer = []
            self.bufsize = 0
            return buf
        finally:
            self.lock.release()


    def close(self):
        log.trace("FTPWorker.close")
        self.done = True


    def write(self, bytes):
        '''
        Some other thread passes bytes to us to write to 
        the FTP endpoint. We queue it up for transmission
        
        @param bytes:
        '''
        log.trace("Writing data to FTP queue")
        #    If we have too much data pending... we wait (watch for errors)
        while self.bufsize > const.BufferSize and not self.error:
            time.sleep(0.01)

        if self.error:
            raise self.error

        #    lock before changing the queue or bufsize
        self.lock.acquire()
        try:
            #    Add these bytes to the buffer
            self.buffer.append(bytes)
            self.bufsize += len(bytes)
            log.debug("Added %d bytes to FTP queue" % len(bytes))
        finally:
            self.lock.release()
            


class FTPStore(StoreBase):
    def __init__(self, name="__dummy__", limit="", auto_manage=False,
                 ip="127.0.0.1", root="store", login="__dummy__", password="__dummy__", sftp=True):
        StoreBase.__init__(self, name, limit, auto_manage)


        if ip == "":
            raise Exception("Server address cannot be blank")
        if login == "" or password == "":
            raise Exception("Login name and password cannot be blank")
        if type(sftp) != bool:
            raise Exception("SFTP must be True or False")

        self.ip = ip
        self.root = root
        self.login = login
        self._password = password
        self.sftp = sftp
        self.folder_stack = []
        self._password = password
        self.pre_save()        
        for attr in ["ip", "root", "login", "password_c", "sftp"]:
            self._persistent.append(attr)


    def pre_save(self):
        self.password_c = encrypt_string_base64(passphrase.passphrase, self._password) 
    def post_load(self):
        self._password = decrypt_string_base64(passphrase.passphrase, self.password_c) 

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = value
        

    def __str__(self):
        return "FTP: %s@%s/%s %s" % (self.login, self.ip, self.root, str(self.sftp))

    def copy(self):
        log.trace("FTPStore Copy Constructor")
        return FTPStore(self.name, self.limit, self.auto_manage, self.ip, self.root, self.login, self.password, self.sftp)


#########################################################
#
#    FTP implementation of a streaming interface.
#
#########################################################

    def open(self, path, mode):
        if not self.connected:
            self.connect()
        if "w" in mode:
            self.io_state = ioWriting
            #    Make sure the dest folder exists
            dir, _ = os.path.split(path)
            self.make_dir(dir)
        else:
            self.io_state = ioReading
        
        self.io_path = os.path.join(self.root, path)
                    
        self.io_fd = FTPStreamer(self.ftp, self.io_path, self.io_state)
        self.io_fd.start()
        #    Now we wait for some data, or an error
        if self.io_state == ioReading:
            log.debug("In open - waiting for data or error")
            while self.io_fd.bufsize == 0 and not self.io_fd.error:
                time.sleep(0.01)
            if self.io_fd.error:
                log.debug("Got exception", str(self.io_fd.error))
                raise self.io_fd.error
            log.debug("Got data")

        return self
        
    def seek(self, offset, whence):
        pass
        
    def tell(self):
        return 0
    
    def close(self):
        self.io_fd.close()
        self.io_fd.join()
        self.io_state = ioClosed
        if self.io_fd.error:
            log.error("Raising exception from FTPWorker", self.io_fd.error)
            raise Exception(str(self.io_fd.error))
        
        
###################################################################################
#
#    Implementation Of The Store API
#
###################################################################################
    def _connect(self):
        '''
        Creates a connected and authenticated FTP object.
        Raises an exception if that ftp object cannot be connected.
        '''
        try:
            self.ftp = None
            if self.sftp:
                log.debug("Connect SFTP")
                self.ftp = FTP_TLS()
                self.ftp.ssl_version = ssl.PROTOCOL_SSLv23
            else:
                log.debug("Connect FTP")
                self.ftp = FTP()
            self.ftp.connect(self.ip, timeout=const.FTPTimeout)
            if self.sftp:
                self.ftp.login(self.login, self.password, secure=True)
                self.ftp.prot_p()
            else:
                self.ftp.login(self.login, self.password)
        except Exception as e:
            #    We failed connection and/or login, so FORCE close
            log.debug("Exception during connect and login")
            if self.ftp:
                self.ftp.close()
            self.ftp = None
            raise Exception("Failed to connect or log in (%s)" % str(e))


    def _disconnect(self):
        if self.ftp:
            self.ftp.close()
        
    def _send(self, src, dest):
        dest = utils.join_paths(self.root, dest)
        fd = open(src, "rb")
        try:
            self.ftp.storbinary("STOR " + dest, fd)
        finally:
            fd.close()
                
        
    def _get(self, src, dest):
        src = utils.join_paths(self.root, src)
        
        fd = open(dest, "wb")
        try:
            self.ftp.retrbinary("RETR " + src, fd.write)
        finally:        
            fd.close()

    def _make_dir(self, folder):
        '''
        Create a folder on the FTP service.
        If its relative, the folder is made relative to cwd.
        Otherwise its absolute.
        
        We do it by attempting to create every folder in the chain.
        '''

        folder = utils.join_paths(self.root, folder)
        self._pushd(".")
        try:
            #    Get all the anscestor paths.
            paths = utils.ancestor_paths(folder)
            for path in paths:
                if not path in ["", ".", "..", "/"]:
                    try:
                        #    If we can't chdir, then we try to build
                        self._pushd(path)
                        self._popd()
                    except:
                        #    If we fail to build - we fail 
                        self.ftp.mkd(path)
        finally:
            self._popd()


    def _remove_file(self, path):
        path = utils.join_paths(self.root, path)
        self.ftp.delete(path)

    def _remove_dir(self, path):
        if path in ["", ".", "/"]:
            path = self.root
        else:
            path = utils.join_paths(self.root, path)
        self._recurse_delete(path)


    def _list(self, path="."):
        path = utils.join_paths(self.root, path)
        #    Save the folder
        self._pushd(path)
        try:
            contents = self.ftp.nlst()
        finally:
            self._popd()    #    Restore the working folder
        return contents

    def _size(self, path):
        path = utils.join_paths(self.root, path)
        self.ftp.sendcmd("TYPE i")         
        size = self.ftp.size(path)
        return size

###################################################################################
#
#    Internal Routines
#
###################################################################################

    def _pushd(self, folder):
        wd = self.ftp.pwd()
        self.folder_stack.append(wd)
        self.ftp.cwd(folder)

    def _popd(self):
        if len(self.folder_stack) == 0:
            raise Exception("Folder stack is empty in popd")
        wd = self.folder_stack.pop()
        self.ftp.cwd(wd)

    def _recurse_delete(self, folder):
        '''
        Internal recursive delete.
        Requires a full path
        
        @param folder:
        @type folder:
        '''
        #    Get a list of files
        self._pushd(folder)
        try:
            files = self.ftp.nlst()
            for d in files:
                try:
                    self.ftp.delete(d)
                except:
                    #    Probably a folder, so lets recurse
                    #    If the failure had another cause - the exception will bubble up.
                    self._recurse_delete(d)
            #    The folder should now be empty.
            #    Exceptions will bubble this up.
        finally:
            self._popd()
        #    Attempt to delete the folder itself
        self.ftp.rmd(folder)



