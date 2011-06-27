# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
from __future__ import division, with_statement, print_function

'''
A class that holds all configuration values, plus supports
persistent savings via ".save()".

Also makes upgrades easy - just add any new values to this class's
__init__ function
'''

import os
import const

import utils
import serializer
import passphrase
from cryptor import encrypt_string_base64, decrypt_string_base64

#    Do last!
from lib.logger import Logger
log = Logger('library')


#    The global configuration object
_appconfig = None




class Config(serializer.Serializer):
    '''
    The class that holds configuration data
    We use a simple singleton - call the classmethod 
        get_config
    to get the config object rather than the constructor.
    The config object will be loaded if necessary, and
    the common one returned.
    
    If no config object exists, a new default config object
    will be created. 
    '''
    def __init__(self):
        pass

      
    @classmethod
    def get_config(cls):
        '''
        Get a reference to the global configuration object.
        If the config object hasn't been loaded, it is loaded.
        If the file doesn't exist, we build a default one.
        '''
        log.trace("Config.get_config", cls)
        global _appconfig
        if not _appconfig:
            try:
                #    Attempt to load it first
                _appconfig = cls.load(const.ConfigFile)
            except Exception as e:
                #    Can't load, so lets build
                log.debug("Failed load: error=", str(e))
                _appconfig = Config()
                import appconfig
                appconfig.build_config(_appconfig)
                _appconfig.post_load()
                _appconfig.save()
        log.trace("Returning", _appconfig)
        return _appconfig

    @classmethod
    def load(cls, path):
        log.debug("Config loading class", cls.__name__)
        
        if not os.path.isfile(path):
            raise IOError("File not found")
        
        obj = serializer.load(path)           
        
        #    Secure the path.
        utils.secure_file(const.ConfigFile)
            
        #    If we get to here, we have loaded the config.
        #    Now check for version upgrade
        import appconfig
        appconfig.check_version(obj)
        
        obj.post_load()
        return obj
    
    @property
    def mail_password(self):
        return self._mail_password
    
    @mail_password.setter
    def mail_password(self, value):
        self._mail_password = value
    

    def post_load(self):
        self.mail_password = decrypt_string_base64(passphrase.passphrase, self.mail_password_c)
        for store in self.storage.itervalues():
            if hasattr(store, "post_load"):
                store.post_load()
        
    def pre_save(self):
        self.mail_password_c = encrypt_string_base64(passphrase.passphrase, self.mail_password)
        for store in self.storage.itervalues():
            if hasattr(store, "pre_save"):
                store.pre_save()

    def save(self):
        global _appconfig
        try:
            utils.makedirs(const.ConfigDir)
            self.pre_save()
            serializer.save(const.ConfigFile, _appconfig)

            log.debug("Saved configuration")
            #    Ensure it is secured.
            utils.secure_file(const.ConfigFile)
                
        except Exception as e:
            log.error("Unable to save configuration: " + str(e))
            raise e

