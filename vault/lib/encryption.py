# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
    OBSOLETE
    
    Encryption Routines
'''

import os
import subprocess

gOpenSSL = "/usr/bin/openssl"

def encrypt_file(pwd, clearfile, cryptfile=None):
    '''
    Encrypt the given clearfile to cryptfile using pwd.
    Uses openSSL and AES256 to perform the encryption.
    
    if cryptfile is None (not provided) then the encryption is inplace.
    It is done to a temp file and replaces clearfile afterwards
    
    @param clearfile:
    @param cryptfile:
    @param pwd:
    '''
    global gOpenSSL
    inplace = cryptfile == None
    if inplace:
        cryptfile = clearfile + ".enc"
        
    proc = subprocess.Popen(args=[gOpenSSL, "enc", "-aes256", "-pass", "stdin", "-in", clearfile, "-out", cryptfile],
                            stdin=subprocess.PIPE)
    ssl_stdin = proc.stdin
    ssl_stdin.write(pwd)
    ssl_stdin.write("\n")
    ret = proc.wait()
    #    If successful, and we are doing an inplace conversion, remove the source
    if ret==0 and inplace:
        os.remove(clearfile)
        os.rename(cryptfile, clearfile)
        
    return ret
    
def decrypt_file(pwd, cryptfile, clearfile=None):
    '''
    Decrypt the given cryptfile to clearfile using pwd.
    Uses openSSL to perform the decryption, and assumes the input file is AES256.
     
    @param cryptfile:
    @param clearfile:
    @param pwd:
    '''
    global gOpenSSL
    inplace = clearfile == None
    if inplace:
        clearfile = cryptfile + ".enc"
    proc = subprocess.Popen(args=[gOpenSSL, "enc", "-d", "-aes256", "-pass", "stdin", "-in", cryptfile, "-out", clearfile],
                            stdin=subprocess.PIPE)
    ssl_stdin = proc.stdin
    ssl_stdin.write(pwd)
    ssl_stdin.write("\n")
    ret = proc.wait()
    #    If successful, and we are doing an inplace conversion, remove the source
    if ret==0 and inplace:
        os.remove(cryptfile)
        os.rename(clearfile, cryptfile)
    return ret

