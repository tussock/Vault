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
import sys
from threading import Thread, RLock
import time 


#    Import FTP. Figure out where TLS is coming from
import ftplib
use_paramiko = not hasattr(ftplib, "FTP_TLS")
if use_paramiko:
    from ftplib import FTP
    import paramiko
else:
    from ftplib import FTP, FTP_TLS


from storebase import *
from lib import utils
from lib import const 


#    Do this last!
from lib.logger import Logger 
log = Logger("io") 

log.debug("Use Paramiko: ", "yes" if use_paramiko else "no")



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

if use_paramiko:
    class ParamikoFTPStreamer(FTPStreamer):
        def run(self):
            '''
            This is an encrypted file-like threaded object.
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
                    log.info("Starting sftp put call for", self.path)
                    fd = self.ftp.open(self.path, "w+")
                    try:
                        data = self.read(const.BufferSize)
                        while data:
                            log.debug("FTP read %d bytes", len(data))
                            fd.write(data)
                            data = self.read(const.BufferSize)
                    finally:
                        fd.close()
                else:
                    log.info("Starting sftp get call for", self.path)
                    fd = self.ftp.open(self.path, "r")
                    try:
                        data = fd.read(const.BufferSize)
                        while data:
                            log.debug("FTP read %d bytes", len(data))
                            self.write(data)
                            data = fd.read(const.BufferSize)
                    finally:
                        fd.close()
            except Exception as e:
                self.error = IOError(str(e))
                log.debug("Exception in ParamikoFTPStreamer", self.error)
            self.done = True
            log.trace("ParamikoFTPStreamer.run complete")
                 


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
        self.password = password
        self.sftp = sftp
        self.folder_stack = []
        for attr in ["ip", "root", "login", "password", "sftp"]:
            self._persistent.append(attr)

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
            dir, dummy = os.path.split(path)
            self.make_dir(dir)
        else:
            self.io_state = ioReading

        self.io_path = os.path.join(self.root, path)
        
        if self.sftp and use_paramiko:
            #    We dont have FTP_TLS AND we need the encryption. We will be using paramiko
            self.io_fd = ParamikoFTPStreamer(self.ftp, self.io_path, self.io_state)
        else:
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
            self.transport = None
            if self.sftp:
                if use_paramiko:
                    log.debug("Connect SFTP paramiko version=", paramiko.__version__,
                              "id", self.login, 
                              "addr", self.ip, 
                              "python version", sys.version)
#                    paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)                    
#                    self.transport = paramiko.SSHClient()
#                    log.debug("Have transport")
#                    self.transport.connect(str(self.ip), 
#                                           username=str(self.login), 
#                                           password=str(self.password))
#                    log.debug("Connected")
#                    self.ftp = self.transport.open_sftp()
                    self.transport = paramiko.Transport((self.ip, 22))
                    log.debug("Have transport")
                    self.transport.connect(username=self.login, password=self.password)
                    log.debug("Connected")
                    self.ftp = paramiko.SFTPClient.from_transport(self.transport)
                    
                    log.debug("Connected and ready to go")
                else:
                    log.debug("Connect SFTP")
                    self.ftp = FTP_TLS()
                    self.ftp.connect(self.ip, timeout=const.FTPTimeout)
                    self.ftp.login(self.login, self.password, secure=True)
                    self.ftp.prot_p()
            else:
                log.debug("Connect FTP")
                self.ftp = FTP()
                self.ftp.connect(self.ip, timeout=const.FTPTimeout)
                self.ftp.login(self.login, self.password)
        except Exception as e:
            #    We failed connection and/or login, so FORCE close
            log.debug("Exception during connect and login: ", str(e))
            self._disconnect
            raise Exception("Failed to connect or log in (%s)" % str(e))


    def _disconnect(self):
        if self.ftp:
            self.ftp.close()
            self.ftp = None
        if self.transport:
            self.transport.close()
            self.transport = None

    def _send(self, src, dest):
        dest = utils.join_paths(self.root, dest)
        with open(src, "rb") as ifd:
            if self.sftp and use_paramiko:
                log.info("Starting sftp.paramiko put call src", src, "dest", dest)
                ofd = self.ftp.open(dest, "w+")
                try:
                    data = ifd.read(const.BufferSize)
                    while data:
                        log.debug("FTP read %d bytes", len(data))
                        ofd.write(data)
                        data = ifd.read(const.BufferSize)
                finally:
                    ofd.close()
            else:
                self.ftp.storbinary("STOR " + dest, ifd)


    def _get(self, src, dest):
        src = utils.join_paths(self.root, src)

        with open(dest, "wb") as ofd:
            if self.sftp and use_paramiko:
        
                ifd = self.ftp.open(src, "r")
                try:
                    data = ifd.read(const.BufferSize)
                    while data:
                        log.debug("FTP read %d bytes", len(data))
                        ofd.write(data)
                        data = ifd.read(const.BufferSize)
                finally:
                    ifd.close()
            else:
                self.ftp.retrbinary("RETR " + src, ofd.write)

    def _make_dir(self, folder):
        '''
        Create a folder on thel FTP service.
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
                        if self.sftp and use_paramiko:
                            self.ftp.mkdir(path)
                        else:
                            self.ftp.mkd(path)
        finally:
            self._popd()


    def _remove_file(self, path):
        path = utils.join_paths(self.root, path)
        if self.sftp and use_paramiko:
            self.ftp.remove(path)
        else:
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
            if self.sftp and use_paramiko:
                contents = self.ftp.listdir()
            else:
                contents = self.ftp.nlst()
        finally:
            self._popd()    #    Restore the working folder
        return contents

    def _size(self, path):
        path = utils.join_paths(self.root, path)
        if self.sftp and use_paramiko:
            stat = self.ftp.stat(path)
            size = stat.st_size
        else:
            self.ftp.sendcmd("TYPE i")
            size = self.ftp.size(path)
        return size

###################################################################################
#
#    Internal Routines
#
###################################################################################

    def _pushd(self, folder):
        if self.sftp and use_paramiko:
            wd = self.ftp.getcwd()
        else:
            wd = self.ftp.pwd()
        self.folder_stack.append(wd)
        if self.sftp and use_paramiko:
            self.ftp.chdir(folder)
        else:
            self.ftp.cwd(folder)
                    
    def _popd(self):
        if len(self.folder_stack) == 0:
            raise Exception("Folder stack is empty in popd")
        wd = self.folder_stack.pop()
        if self.sftp and use_paramiko:
            self.ftp.chdir(wd)
        else:
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
            if self.sftp and use_paramiko:
                files = self.ftp.listdir()
            else:
                files = self.ftp.nlst()
            for d in files:
                try:
                    if self.sftp and use_paramiko:
                        self.ftp.remove(d)
                    else:
                        self.ftp.delete(d)
                except:
                    #    Probably a folder, so lets recurse
                    #    If the failure had another cause - the exception will bubble up.
                    self._recurse_delete(d)
            #    The folder should now be empty.
            #    Exceptions will bubble this up.
        except Exception as e:
            log.debug("NList exception", str(e))
            raise e
        finally:
            self._popd()
        #    Attempt to delete the folder itself
        if self.sftp and use_paramiko:
            self.ftp.rmdir(folder)
        else:
            self.ftp.rmd(folder)


