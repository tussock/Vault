#!/usr/bin/env python

# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
'''
Setup Application Goals:

a) Copy the whole application into /usr/lib/vault/vault (by default)
b) Copy the vault and vault_svr script into /usr/bin
c) Copy the documentation file into /usr/share/doc/vault/en
d) Copy the vault.xml, legal.xml, fdl-appendix.xml, images/* into /usr/share/gnome/help/vault/C
    (other translations go into /usr/share/gnome/help/vault/<country code>)
e) Man pages copied to /usr/share/man/man1
    
'''
import os
import glob
import fnmatch
from distutils.core import setup
import distutils.command.install


# Boolean: running as root?
ROOT = os.geteuid() == 0
# For Debian packaging it could be a fakeroot so reset flag to prevent execution of
# system update services for Mime and Desktop registrations.
# The debian/vault.postinst script must do those.
if not os.getenv("FAKEROOTKEY") == None:
    print "NOTICE: Detected execution in a FakeRoot so disabling calls to system update services."
    ROOT = False
    

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



#    Taken from the quodlibet setup.py. Creates the right install list
def recursive_include(dir, pre, ext):
    all = []
    old_dir = os.getcwd()
    os.chdir(dir)
    for path, dirs, files in os.walk(pre):
        for file in files:
            if file.split('.')[-1] in ext:
                all.append(os.path.join(path, file))
    os.chdir(old_dir)
    return all

from vault.lib import const

PACKAGES = ["vault", "vault.store", "vault.store.dropbox", "vault.ui", "vault.server", "vault.lib", "vault.recovery"]

OS_FILES = [
     # XDG application description
     ('share/applications', ['bin/vault.desktop']),
     # XDG application icon
     ('share/pixmaps', ['pixmaps/vault.png']),
     # Application working icons
     ('share/vault/pixmaps', glob.glob('pixmaps/*.png')),
     # man-page ("man 1 vault")
     ('share/man/man1',['help/C/vault.1']),
     ('share/man/man1',['help/C/vault_svr.1']),
     # doc, in-ap help
     ("share/gnome/help/vault/C", glob.glob('help/C/*.xml')),
     
     ("share/omf/vault", ["help/vault.omf"]),
]
# Find all the translations
locale_files = []
for filepath in glob.glob("vault/i18n/*/LC_MESSAGES/*"):
    filepath = filepath.replace('vault/', '')
    locale_files.append(filepath)
    

setup(
    name = const.PackageName,
    version = const.Version,
    description = const.Description,
    author = 'Paul Reddy',
    author_email = 'paul@kereru.org',
    maintainer = "Paul Reddy",
    maintainer_email = "paul@kereru.org",
    license = "GPL",
    platforms = "UNIX",
    keywords = ["backup", "encryption", "archive", "recovery"],
    url = 'http://www.kereru.org/vault',
    packages = PACKAGES,
    package_data = { 'vault': ["recovery/recoveryui.fbp", 
                               "ui/gui.fbp",
                               "lib/wizui.fbp"
                               ] + locale_files },
                      
    data_files = OS_FILES,
    
    long_description = read('README'),
    scripts = ["bin/vault", "bin/vault_svr"],
    classifiers = [
                 "Development Status :: 4 - Beta",
                 "Environment :: X11 Applications :: Gnome",
                 "Intended Audience :: End Users/Desktop",
                 "Intended Audience :: System Administrators",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Operating System :: POSIX :: Linux",
                 "Programming Language :: Python",
                 "Topic :: System :: Archiving :: Backup"
    ],

)
    
if ROOT and dist != None:
    # update the XDG .desktop file database
    try:
        sys.stdout.write('Updating the .desktop file database.\n')
        subprocess.call(["update-desktop-database"])
    except:
        sys.stderr.write(FAILED)
    sys.stdout.write("\n-----------------------------------------------")
    sys.stdout.write("\nInstallation Finished!")
    sys.stdout.write("\nRun The Vault by typing 'vault' or through the System|Administration menu.")
    sys.stdout.write("\n-----------------------------------------------\n")

 

