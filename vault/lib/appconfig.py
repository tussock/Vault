# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
from __future__ import division, with_statement, print_function

'''
This module contains a function that will build a config object for the Vault project.


'''
#    OS imports
import os

#    APP imports
from lib import const
from lib.backup import Backup
from store.folderstore import FolderStore

#    Do last!
from lib.logger import Logger
log = Logger('library')

def build_config(conf):
    #    This is called to build a default config object
    #    It is used the first time this application is run.
    log.info("Building new config object")

    conf.version = 1
    conf.file_types = {_("Images"): ["jpg", "jpeg", "raw",
                                     "cr2", "png", "gif", "dng", "tiff",
                                        "tif", "bmp", "svg", "ppm", "psd"],
                     _("Videos"): ["avi", "mpg", "mpeg", "mp4", "mov", "m4v", "vob", "wmv", "flv"],
                     _("Music"): ["mp3", "aac", "ogg", "flac", "wav", "wma", "mpa"],
                     _("Programs"): ["bin", "dll", "exe", "com", "lib"]
                     }

    conf.storage = {}
    store = FolderStore(_("System Backup Folder"), "", False, os.path.join(const.DataDir, "vault-store"))
    conf.storage[store.name] = store

    conf.backups = {}

    b = Backup(_("Home"))
    b.include_folders = ["/home"]
    b.active = False
    b.include_packages = True
    b.store = store.name
    b.notify_msg = True
    conf.backups[b.name] = b

    conf.mail_server = ""
    conf.mail_port = 25
    conf.mail_ssl = False
    conf.mail_auth = False
    conf.mail_login = ""
    conf.mail_password_c = ""
    conf.mail_from = ""
    conf.mail_to = ""


    if const.Debug:

        #    If we are debugging, we create debug store and backup objects
        store = FolderStore("TestStore", "20MB", True,
                        os.path.join(const.RunDir, "store"))
        conf.storage[store.name] = store


        b = Backup("test")
        b.include_folders = [os.path.join(const.RunDir, "files")]
        b.include_packages = True
        b.exclude_types = ["Videos", "Programs"]
        b.exclude_patterns = ["*/not"]
        b.store = store.name
        b.notify_msg = True
        b.encrypt = True
        conf.backups[b.name] = b

        #    DEBUG - reset the store and include folders
        conf.backups["Home"].store = store.name
        conf.backups["Home"].include_folders = [os.path.join(const.RunDir, "files")]


def check_version(conf):
    if not hasattr(conf, "version"):
        version = 0
    else:
        version = conf.version
    log.debug("Config at version", version)

    if version == 0:
        #    Upgrade from version 0 to version 1
        #    New backup manager.
        log.warn("Upgrading configuration from 0 to 1")
        conf.version = 1

    #    if version == 1:
        #    Here will go any changes from version 1 to 2
        #    obj.version = 2

    if version != conf.version:
        conf.save()
