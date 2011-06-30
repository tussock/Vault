# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
'''

@author: paul
'''

from storebase import StoreBase
from lib import const
from lib import passphrase
from lib.cryptor import decrypt_string_base64, encrypt_string_base64
import boto 

#    Do this last!
from lib.logger import Logger
log = Logger("io")


class S3Store(StoreBase):
    def __init__(self, name="__dummy__", limit="", auto_manage=False, 
                 bucket="__dummy__", key="", secret_key=""):
        StoreBase.__init__(self, name, limit, auto_manage)
        
        #    We dont create large files for dropbox.
        log.trace("S3Store.init", name, limit, auto_manage, bucket, key, secret_key)
        if const.Debug:
            self.split_size = 500 * 1024
        else:
            self.split_size = 100 * 1024 * 1024
     
        if bucket == "":
            raise Exception(_("bucket cannot be blank"))

        self.bucket = bucket
        self.bucket = bucket
        self._key = key
        self._secret_key = secret_key
        self.pre_save()
        for attr in ["bucket", "key_c", "secret_key_c"]:
            self._persistent.append(attr)
        
        

    def pre_save(self):
        self.key_c = encrypt_string_base64(passphrase.passphrase, self._key) 
        self.secret_key_c = encrypt_string_base64(passphrase.passphrase, self._secret_key) 
    def post_load(self):
        self._key = decrypt_string_base64(passphrase.passphrase, self.key_c) 
        self._secret_key = decrypt_string_base64(passphrase.passphrase, self.secret_key_c) 

    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, value):
        self._key = value

    @property
    def secret_key(self):
        return self._secret_key
    
    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value
        
    

    def copy(self):
        '''
        Used by the persistence system to initialize a new FolderStore
        
        Returns a fully initialized duplicate of self.

        '''
        log.trace("Copy constructor")
        return S3Store(self.name, self.limit, self.auto_manage, self.bucket, self.key, self.secret_key)

    def __str__(self):
        return "PATH: %s" % self.bucket

    def _connect(self):
#        config = auth.SimpleOAuthClient(server, port, request_token_url, access_token_url, authorization_url)
        log.debug("Connecting...")
        try:
            if self.key != "" and self.secret_key != "":
                #    We will be providing a key. If not, we will assume that boto.conf is set up
                try:
                    #    This may already exist.
                    boto.config.add_section("Credentials")
                except:
                    pass
                boto.config.set("Credentials", 'aws_access_key_id', self.key)
                boto.config.set("Credentials", 'aws_secret_access_key', self.secret_key)
            self.s3 = boto.connect_s3()
    
            log.debug("Connected. Making bucket")
        #    If the bucket exists... this wont fail
            self.s3.create_bucket(self.bucket)
            self.s3_bucket = self.s3.get_bucket(self.bucket)
        except Exception as e:
            if hasattr(e, "error_message"):
                raise Exception(e.error_message)
            else:
                raise

    def _disconnect(self):
        self.s3 = None
        self.s3_bucket = None

    def _send(self, src, dest):
        key = self.s3_bucket.new_key(dest)
        with open(src, "rb") as fd:
            key.set_contents_from_file(fd)
    
    def _get(self, src, dest):
        key = self.s3_bucket.get_key(src)
        with open(dest, "wb") as fd:
            key.get_contents_to_file(fd)
                
    def _make_dir(self, folder):
        if folder in ["", "/", "."]:
            return
        
        #    Folders are not required in S3
        return
        #    We need to create something so that exists and remove work.
        key = self.s3_bucket.new_key(folder)
        key.set_contents_from_string('DIR')
    
    def _remove_file(self, path):
        key = self.s3_bucket.get_key(path)
        if key:
            key.delete()
        else:
            raise Exception("Attempting to delete a non-existent file")

    def _remove_bucket(self):
        keys = self.s3_bucket.get_all_keys()
        for key in keys:
            key.delete()
        self.s3_bucket.delete()
        self.s3_bucket = None
        self.disconnect()
        
    def _remove_dir(self, path):
        if path == "" or path == ".":
            self._remove_bucket()
            return
            
        dir = path
        if dir[-1] != "/":
            dir += "/"
        #    Get a list of all subkeys
        list = self._listkeys(dir)
        for key in list:
            key.delete()
        key = self.s3_bucket.get_key(path)
        if key:
            key.delete()
        

    #    Its more efficient to use this exists method.
    def exists(self, path):
        if not self.connected:
            self.connect()
        key = self.s3_bucket.get_key(path)
        return key != None

    def _list(self, dir):
        keys = self._listkeys(dir)
        len_dir = len(dir)
        #    Copy the names into contents. One will be the folder, 
        #    and will be blank when we remove the folder
        contents = [key.name[len_dir+1:] for key in keys if key.name[len_dir+1:] != ""]
        return contents

    def _listkeys(self, dir):
        if dir[-1] != "/":
            dir += "/"
        keys = self.s3_bucket.list(dir)
        return keys
    
    def size(self, path):
        key = self.s3_bucket.get_key(path)
        return key.size
        
