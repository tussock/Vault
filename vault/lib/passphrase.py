'''
Created on 17/05/2011

@author: paul
'''
import os

import const
import utils
from cryptor import encrypt_string_base64, decrypt_string_base64

####################################################################
#
#    The Master Passphrase
#
####################################################################
#    The system passphrase is stored here.
PassphraseFile = os.path.join(const.ConfigDir, "masterpwd")
try:
    hid = os.popen("hostid").read().strip()
except:
    print("Except 1")
    hid = None
if not hid:
    #    This will be used to shroud the master password.
    hid = "the_Master!!"

try:
    crypt_passphrase = open(PassphraseFile).read()
    #    Make sure its still secure
    utils.secure_file(PassphraseFile)    
except:
    #    Doesn't exist!
    crypt_passphrase = ""
    
try:
    passphrase = decrypt_string_base64(hid, crypt_passphrase)
except:
    passphrase = "" 


def set_passphrase(value):
    global hid
    global passphrase
    passphrase = value
    with open(PassphraseFile, "w") as f:
        f.write(encrypt_string_base64(hid, passphrase))
    #    Make sure its still secure
    utils.secure_file(PassphraseFile)
        

def delete_passphrase():
    #    Not really a good way to do it... just setting blank
    set_passphrase("")

