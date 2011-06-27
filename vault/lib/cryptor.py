# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
    Cryptographic routines using OpenSSL libraries
'''

import ctypes
import os
import threading
import base64

import evp
from buffer import Buffer

BufferSize=102400
    

class CipherError(evp.SSLError):
    pass

def encrypt_file(password, src, dest=None):
    '''
    Encrypt a given file. If a destination path is not given,
    the original file is overwritten.
    
    The encryption is OpenSSL compatible (with -md sha256)
    
    @param password:
    @param src:
    @param dest:
    '''
    crypt = EncryptStream(password)
    _crypt_file(crypt, src, dest)
    return 0    
        
def decrypt_file(password, src, dest=None):
    '''
    Decrypt a given file. If a destination path is not given,
    the original file is overwritten.
    
    The file to be decrypted must be OpenSSL compatible (with -md sha256).
    
    @param password:
    @param src:
    @param dest:
    '''
    crypt = DecryptStream(password)
    _crypt_file(crypt, src, dest)
    return 0

def _crypt_file(crypt, src, dest):
    if isinstance(src, basestring):
        input = open(src, "rb")
    else:
        input = src
    if isinstance(dest, basestring):
        output = open(dest, "wb")
    else:
        output = dest

    #    Start up a thread to copy data from the
    #    crypt object to the dest file object.
    #    Otherwise reading could block if the file is small.
    thd = CopyThread(crypt, output)
    thd.start()
    try:
        data = input.read(BufferSize)
        while data:
            crypt.write(data)
            data = input.read(BufferSize)

        if isinstance(src, basestring):
            input.close()
    finally:
        #    When this happens, the thread should stop. 
        #    So we *make sure* the close happens.
        crypt.close()
    #    Wait for the copier to complete
    thd.join()

    if isinstance(dest, basestring):
        output.close()
        

def encrypt_string(password, data):
    """Encrypts the given data, raising CipherError on failure.

    This uses AES256 to encrypt and strengthens the given
    passphrase using SHA256.
    
    The data is encrypted ina form that can be decrypted by OpenSSL.
    It has 16 bytes at the front containing "Salted__" + Salt.
    
    Note that to decrypt with OpenSSL, you must use the "-md sha256" flag,
    because openSSL uses MD5 to convert a key to passphrase by default. 

    Usage:
        >>> pw = b"mypassword"
        >>> enc = cipher.encrypt(password, data)
        >>> cipher.decrypt(password, enc) == data
        True
    """
    crypt = EncryptStream(password)
    crypt.write(data)
    crypt.close()
    return crypt.read()


def decrypt_string(password, data):
    """Decrypts the given data, raising CipherError on failure.

    This uses AES256 to decrypt and strengthens the given
    passphrase using SHA256.
    
    The data must be in the OpenSSL for - that is it has 
    16 bytes at the front containing "Salted__" + Salt.
    
    Note that to encrypt with OpenSSL, you must use the "-md sha256" flag,
    because openSSL uses MD5 to convert a key to passphrase by default. 

    Usage:
        >>> pw = b"mypassword"
        >>> enc = cipher.encrypt(password, data)
        >>> cipher.decrypt(password, enc) == data
        True
    """   
    crypt = DecryptStream(password)
    crypt.write(data)
    crypt.close()
    return crypt.read()

def encrypt_string_base64(password, data):
    if not data or not password:
        return data
    return base64.b64encode(encrypt_string(password, data))

def decrypt_string_base64(password, data):
    if not data or not password:
        return data
    return decrypt_string(password, base64.b64decode(data))

class CopyThread(threading.Thread):
    def __init__(self, src, dest):
        threading.Thread.__init__(self)
        self.src = src
        self.dest = dest
    def run(self):
        data = self.src.read(BufferSize)
        while data:
            self.dest.write(data)
            data = self.src.read(BufferSize)
        self.src.close()
        self.dest.close()
        
class Crypter(Buffer):
    '''
    The base class for a set of encryption/decryption file-like objects.
    They use OpenSSL libraries, and create data that can be decrypted
    by OpenSSL on the command line (as long as you remember to use
    the "-md sha256' flag)
    
    It uses aes-256-cbc for encryption
    and sha256 for key generation.
    
    It is threadsafe - in that you can read and write to this
    from different threads.
    '''
    def __init__(self, password):
        Buffer.__init__(self)
        
        if not len(password):
            raise CipherError("Password cannot be blank")
        self.password = password

        # build and initialize the context
        self.ctx = evp.EVP_CIPHER_CTX_new()
        if not self.ctx:
            raise CipherError("Could not create encryption context")
        evp.EVP_CIPHER_CTX_init(self.ctx)

        # get the cipher object
        cipher_object = evp.EVP_aes_256_cbc()
        if not cipher_object:
            raise CipherError("Could not create cipher object")

        # finish the context and cipher object
        if not evp.EVP_EncryptInit_ex(self.ctx, cipher_object, None, None, None):
            raise CipherError("Could not initialize encryption context")


            
    def create_key(self, password, salt=None):
        '''
        Create a key and IV for a given password.
        If the salt is given, it is used. Otherwise a new random
        salt is created.
        
        Returns key, salt, iv
        @param pw:
        @param salt:
        '''
        if salt != None and len(salt) != 8:
            raise CipherError("Invalid salt, must be None or length 8")
        # add the hash
        evp.OpenSSL_add_all_digests()
        # build the key buffer
        key = ctypes.create_string_buffer(32)
        iv = ctypes.create_string_buffer(16)
        # either take the existing salt or build a new one
        if not salt:
            salt = os.urandom(8)
        # get the hash
        evp_hash = evp.EVP_get_digestbyname("sha256")
        if not evp_hash:
            raise CipherError("Could not create hash object")
        # fill the key
        if not evp.EVP_BytesToKey(evp.EVP_aes_256_cbc(), evp_hash, salt, 
                                  password, len(password), 1, key, iv):
            raise CipherError("Could not strengthen key")
        # go home
        return key.raw, salt, iv



class EncryptStream(Crypter):
    def __init__(self, passphrase):
        Crypter.__init__(self, passphrase)

        # strengthen the password into an honest-to-goodness key
        self.key, self.salt, self.iv = self.create_key(passphrase)
        # initialize the encryption operation
        if not evp.EVP_EncryptInit_ex(self.ctx, None, None, self.key, self.iv):
            raise CipherError("Failed to set key/iv")

        super(EncryptStream, self).write("Salted__" + self.salt)
        
    def write(self, data):
        # build the output buffer
        buf = ctypes.create_string_buffer(len(data) + 16)
        written = ctypes.c_int(0)

        # update
        if not evp.EVP_EncryptUpdate(self.ctx, buf, ctypes.byref(written), data, len(data)):
            raise CipherError("Could not update ciphertext")
        super(EncryptStream, self).write(buf.raw[:written.value])
        
    def close(self):
        #    Called by the writer when there is no more data
        #    Also could be called by the reader when it has been returned no data
        
        if self.closed:
            return 
        final = ctypes.c_int(0)    
        #    Put the last of the data into the output buffer
        buf = ctypes.create_string_buffer(16)
        if not evp.EVP_EncryptFinal_ex(self.ctx, buf, ctypes.byref(final)):
            raise CipherError("Could not finalize ciphertext")
        super(EncryptStream, self).write(buf.raw[:final.value])
        super(EncryptStream, self).close()

class DecryptStream(Crypter):
    def __init__(self, password):
        Crypter.__init__(self, password)
        
        #    We can't initialize the decryption operation until we get
        #    the salt, which is used to create the key
        self.input_buffer = ""
        self.initialized = False
        
    def write(self, data):
        if not self.initialized:
            self.input_buffer += data
            #    have we got enough to extract the salt?
            if len(self.input_buffer) < 16:
                return
            if self.input_buffer[:8] != "Salted__":
                raise CipherError("Invalid decrypt data - missing header")
            self.salt = self.input_buffer[8:16]
            
            #    Now we can generate the keys and initialize the decryptor
            self.key, _, self.iv = self.create_key(self.password, self.salt)
            
            if not evp.EVP_DecryptInit_ex(self.ctx, None, None, self.key, self.iv):
                raise CipherError("Failed to initialize decryptor")
            self.initialized = True
            #    Return the rest of the input data to be decrypted
            data = self.input_buffer[16:]
            
        # build the output buffer
        buf = ctypes.create_string_buffer(len(data) + 16)
        written = ctypes.c_int(0)
        
        # update
        if not evp.EVP_DecryptUpdate(self.ctx, buf, ctypes.byref(written), data, len(data)):
            raise CipherError("Could not update plaintext")
        super(DecryptStream, self).write(buf.raw[:written.value])

    def close(self):
        #    Called by the writer when there is no more data
        #    Also could be called by the reader when it has been returned no data
        
        if self.closed:
            return 
        final = ctypes.c_int(0)    
        #    Put the last of the data into the output buffer
        buf = ctypes.create_string_buffer(16)
        if not evp.EVP_DecryptFinal_ex(self.ctx, buf, ctypes.byref(final)):
            raise CipherError("Could not finalize plaintext")
        super(DecryptStream, self).write(buf.raw[:final.value])
        super(DecryptStream, self).close()
       
        