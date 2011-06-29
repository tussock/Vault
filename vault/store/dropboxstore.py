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
 
from storebase import *
from lib import const
from lib import utils
from lib.buffer import Buffer 
from lib import passphrase  
from lib.cryptor import decrypt_string_base64, encrypt_string_base64
from dropbox import auth, client    

#    Do this last!
from lib.logger import Logger
log = Logger("io") 


auth_config = {}
auth_config['server'] = "api.dropbox.com"
auth_config['content_server'] = "api-content.dropbox.com"
auth_config['port'] = "80"
auth_config['dropbox_root'] = "dropbox"    # 'sandbox' or 'dropbox'

auth_config['request_token_url'] = "https://api.dropbox.com/0/oauth/request_token"
auth_config['access_token_url'] = "https://api.dropbox.com/0/oauth/access_token"
auth_config['authorization_url'] = "https://www.dropbox.com/0/oauth/authorize"
auth_config['trusted_access_token_url'] = "https://api.dropbox.com/0/token"

class DropBoxWriter(Thread, Buffer):
    def __init__(self, db_store, path):
        self.db_store = db_store
        self.path = path
        self.folder, self.filename = os.path.split(path)

        Thread.__init__(self)
        Buffer.__init__(self, name=self.filename)
        self.error = None
        
   
    def run(self):
        log.debug("Starting put_file", self.path)
        try:
            ret = self.db_store.db_client.put_file(self.db_store.db_root, self.folder, self)
            log.debug("Completed put_file", ret.__dict__)
        except Exception as e:
            log.error("Exception in put thread", str(e))
            self.error = e
            
               
        
class DropBoxStore(StoreBase):
    def __init__(self, name="__dummy__", limit="", auto_manage=False, 
                 root="store", login="__dummy__", password="__dummy__",
                 app_key="__dummy__", app_secret_key="__dummy__"):
        StoreBase.__init__(self, name, limit, auto_manage)
        
        #    We dont create large files for dropbox.
        log.trace("DropBoxStore.init", name, limit, auto_manage, root, login, password)
        if const.Debug:
            self.split_size = 500 * 1024
        else:
            self.split_size = 100 * 1024 * 1024
     
        if login == "" or password == "" or app_key == "" or app_secret_key == "":
            raise Exception(_("login, password and app_keys cannot be blank"))

        self.root = root
        if len(self.root) == 0 or self.root[0] != "/":
            self.root = "/" + self.root
        self.login = login
        self._password = password
        self._app_key = app_key
        self._app_secret_key = app_secret_key
        self.pre_save()
        for attr in ["root", "login", "password_c", "app_key_c", "app_secret_key_c"]:
            self._persistent.append(attr)
        
        

    def pre_save(self):
        self.password_c = encrypt_string_base64(passphrase.passphrase, self._password) 
        self.app_key_c = encrypt_string_base64(passphrase.passphrase, self._app_key) 
        self.app_secret_key_c = encrypt_string_base64(passphrase.passphrase, self._app_secret_key) 
    def post_load(self):
        self._password = decrypt_string_base64(passphrase.passphrase, self.password_c) 
        self._app_key = decrypt_string_base64(passphrase.passphrase, self.app_key_c) 
        self._app_secret_key = decrypt_string_base64(passphrase.passphrase, self.app_secret_key_c) 

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = value
        
    @property
    def app_key(self):
        return self._app_key
    
    @app_key.setter
    def app_key(self, value):
        self._app_key = value
        
    @property
    def app_secret_key(self):
        return self._app_secret_key
    
    @app_secret_key.setter
    def app_secret_key(self, value):
        self._app_secret_key = value
        
     

    def copy(self):
        '''
        Used by the persistence system to initialize a new DropBoxStore
        
        Returns a fully initialized duplicate of self.

        '''
        log.trace("Copy constructor")
        return DropBoxStore(self.name, self.limit, self.auto_manage, self.root, 
                            self.login, self.password, self.app_key, self.app_secret_key)

    def __str__(self):
        return "PATH: %s" % self.root
    
    
#    def open(self, path, mode):
#        if not self.connected:
#            self.connect()
#
#        self.io_path = os.path.join(self.root, path)
#        if "w" in mode:
#            self.io_state = ioWriting
#            #    Make sure the dest folder exists
#            dir, _ = os.path.split(path)
#            self.make_dir(dir)
#
#            self.io_fd = DropBoxWriter(self, self.io_path)
#            self.io_fd.start()
#        else:
#            self.io_state = ioReading
#            self.io_fd = self.db_client.get_file(self.db_root, self.io_path)
#            if self.io_fd.status != 200:
#                raise Exception("Failed to fetch file object")                   
#
#        return self
#
#
#    def close(self):
#        self.io_state = ioClosed
#        self.io_fd.close()
#        self.io_fd.join()
#    
#    def read(self, size=-1):
#        if self.io_state != ioReading:
#            raise Exception("Not opened for reading")
#        return self.io_fd.read(size)
#    
#    def write(self, data):
#        if self.io_state != ioWriting:
#            raise Exception("Not opened for writing")
#        self.io_fd.write(data)
#        
#    def seek(self, offset, whence=0):
#        pass
#        
#    def tell(self):
#        return 0
    


    def _connect(self):
#        config = auth.SimpleOAuthClient(server, port, request_token_url, access_token_url, authorization_url)
        log.debug("Connecting...")
        global auth_config
        auth_config['consumer_key'] = self.app_key
        auth_config['consumer_secret'] = self.app_secret_key
        self.dba = auth.Authenticator(auth_config)
        self.access_token = self.dba.obtain_trusted_access_token(str(self.login), str(self.password))
        log.debug("Got access token: ", self.access_token)
        self.db_client = client.DropboxClient(auth_config['server'], auth_config['content_server'], 
                                         auth_config['port'], self.dba, self.access_token)
        self.db_root = auth_config['dropbox_root']

        log.debug("Connected. Making root")

    def _disconnect(self):
        pass
        

    def _send(self, src, dest):
        #    Dropbox limitation - the final file name must match the source
        #    name. AND we cannot pass the final file name in.
        old_src = None
        dest_folder, dest_fname = os.path.split(dest)
        src_folder, src_fname = os.path.split(src)
        if dest_fname != src_fname:
            #    We need to rename src temporarily
            #    because the src name and final name MUST match
            #    We do this in a temporary folder beside its current location.
            old_src = src
            tmpfolder = tempfile.mkdtemp()
            src = os.path.join(tmpfolder, dest_fname)
            os.rename(old_src, src)
            log.debug("Fixed name", old_src, src)
        try:
            dest = utils.join_paths(self.root, dest_folder)
            with open(src, "rb") as fd:
                ret = self.db_client.put_file(self.db_root, dest, fd)
            if ret.status != 200:
                raise IOError("Unable to send file: " + ret.reason)
        finally:
            if old_src:
                #    Put the name back!
                os.rename(src, old_src)
                os.rmdir(tmpfolder)

    def _get(self, src, dest):
        src = utils.join_paths(self.root, src)
        with open(dest, "wb") as fd:
            fileobj = self.db_client.get_file(self.db_root, src)
            if fileobj.status != 200:
                raise IOError("Unable to get %s: %s" % (src, fileobj.reason))
            try:
                data = fileobj.read(const.BufferSize)
                while len(data) > 0:
                    fd.write(data)
                    data = fileobj.read(const.BufferSize)
            finally:
                fileobj.close()

    def _make_dir(self, folder):
        if folder in ["", "."]:
            path = self.root
        else:
            path = utils.join_paths(self.root, folder)
        self.db_client.file_create_folder(self.db_root, path)

    def _remove_file(self, path):
        if path in ["", ".", "/"]:
            path = self.root
        else:
            path = utils.join_paths(self.root, path)
        self.db_client.file_delete(self.db_root, path)

    def _remove_dir(self, path):
        self._remove_file(path)

    def _list(self, dir):
        if dir in ["", ".", "/"]:
            path = self.root
        else:
            path = utils.join_paths(self.root, dir)
        resp = self.db_client.metadata(self.db_root, path, file_limit=10000, list="true")
        ret = [os.path.basename(item["path"]) for item in resp.data["contents"]]
        return ret
    
    def _size(self, path):
        path = utils.join_paths(self.root, path)
        resp = self.db_client.metadata(self.db_root, path, list="false")
        return resp.data["bytes"]
        
