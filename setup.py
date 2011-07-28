#!/usr/bin/env python

# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
'''
Setup Application Goals:

a) Copy the whole application into /usr/lib/python2.7/dist-packages (by default)
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


PACKAGES = ["vault", "vault.store", "vault.store.dropbox", "vault.ui", "vault.server", "vault.lib", "vault.recovery"]

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
                      
#    package_dir = {'vault': 'vault'},
                
    package_data = {"vault": recursive_include("vault", ".", ("version", "png", "gif", "po")),
                    },
    data_files = [
                    #    Help files
                    ("share/gnome/help/vault/C", 
                        glob.glob('vault/help/C/*.xml')),
                    ("share/gnome/help/vault/C/images", 
                        glob.glob('vault/help/C/images/*.png')),
                    #    Application  
                    ("share/applications", 
                        ["vault/bin/vault.desktop"]),
                    ("share/pixmaps", ["vault/ui/images/vault.png"]),
                    ("share/omf/vault", ["vault/help/vault.omf"]),
                    ("share/man/man1", glob.glob("vault/help/C/*.1.gz")),
#                    ('share/icons/hicolor/16x16/apps', ['vault/ui/images/16x16/vault.png']),
#                    ('share/icons/hicolor/24x24/apps', ['vault/ui/images/24x24/vault.png']),
#                    ('share/icons/hicolor/32x32/apps', ['vault/ui/images/32x32/vault.png']),
#                    ('share/icons/hicolor/48x48/apps', ['vault/ui/images/48x48/vault.png']),
#                    ('share/icons/hicolor/64x64/apps', ['vault/ui/images/64x64/vault.png']),
#                    ('share/icons/hicolor/96x96/apps', ['vault/ui/images/96x96/vault.png']),
#                    ('share/icons/hicolor/128x128/apps', ['vault/ui/images/128x128/vault.png']),
#                    ('share/icons/hicolor/192x192/apps', ['vault/ui/images/192x192/vault.png']),
#                    ('share/icons/hicolor/256x256/apps', ['vault/ui/images/256x256/vault.png']),
                         
                  ],
    long_description = read('README'),
    scripts = ["vault/bin/vault", "vault/bin/vault_svr"],
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

 

