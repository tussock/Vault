# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
'''

@author: paul
'''

import os

from storebase import StoreBase
from lib import const
from lib import passphrase
from lib.cryptor import decrypt_string_base64, encrypt_string_base64
import gdata.docs.data
import gdata.docs.client

#    Do this last!
from lib.logger import Logger
log = Logger("io")


class GoogleStore(StoreBase):
    def __init__(self, name="__dummy__", limit="", auto_manage=False,
                 collection="__dummy__", login="__dummy__", password="__dummy__"):
        StoreBase.__init__(self, name, limit, auto_manage)

        #    We dont create large files for dropbox.
        log.trace("GoogleStore.init", name, limit, auto_manage, root, login, password)
        if const.Debug:
            self.split_size = 500 * 1024
        else:
            self.split_size = 100 * 1024 * 1024

        if collection == "":
            raise Exception(_("collection cannot be blank"))
        if not name or not password:
            raise Exception("Name and password cannot be blank")
        self.collection = collection
        self.login = login
        self._password = password
        self.pre_save()
        for attr in ["collection", "login", "password_c"]:
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

    def copy(self):
        '''
        Used by the persistence system to initialize a new FolderStore
        
        Returns a fully initialized duplicate of self.

        '''
        log.trace("Copy constructor")
        return GoogleStore(self.name, self.limit, self.auto_manage, self.root, self.login, self.password)

    def __str__(self):
        return "PATH: %s" % self.root

    def _connect(self):
#        config = auth.SimpleOAuthClient(server, port, request_token_url, access_token_url, authorization_url)
        log.debug("Connecting...")
        try:
            app_title = 'kereru-%s-v%s' % (const.PackageName, const.Version)
            self.client = gdata.docs.client.DocsClient(source=app_title)
            self.client.ssl = True
            self.client.ClientLogin(self.login, self.password, app_title)

            log.debug("Connected. Making root")
        #    If the bucket exists... this wont fail
        except Exception as e:
            if hasattr(e, "error_message"):
                raise Exception(e.error_message)
            else:
                raise

    def _disconnect(self):
        self.client = None

    def _send(self, src, dest):
        folder, filename = os.path.split(dest)
        entry = self.client.Upload(src, filename, content_type='application/msword', folder_or_uri=folder)
        print('Document now accessible online at:', entry.GetAlternateLink().href)

    def _get(self, src, dest):
        raise NotImplemented()
        entry = self.client.GetDoc(src)
        self.client.Export(entry, dest)

    def _make_dir(self, folder):
        #    Google will happily make multiple copies of any folder or file with
        #    the same name. So we need to check for existence first
        if self._exists(folder):
            return
        if folder in ["", ".", "/"]:
            path = self.root
        else:
            path = utils.join_paths(self.root, folder)
        new_folder = self.client.Create(gdata.docs.data.FOLDER_LABEL, path)

    def _remove_file(self, path):
        raise NotImplemented()

    def _remove_dir(self, path):
        if path in ["", ".", "/"]:
            #    Remove root folder.
            pass
        raise NotImplementedError()
        dir = path
        if dir[-1] != "/":
            dir += "/"
        raise NotImplementedError()

    #    Its more efficient to use this exists method.
    def _exists(self, path):
        if folder in ["", ".", "/"]:
            items = client.GetDocList(uri='/feeds/default/private/full/folder%3Aroot/contents')
            #does the collection exist
        else:
            path = utils.join_paths(self.root, folder)
        raise NotImplementedError()

    def _list(self, dir):
        raise NotImplementedError()

    def _listkeys(self, dir):
        raise NotImplementedError()

    def _size(self, path):
        raise NotImplementedError()

