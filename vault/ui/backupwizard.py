# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import os

from lib import const
from lib.backup import Backup, update_crontab
from lib.config import Config
from lib import wizard
from lib import dlg
import app

#    Do last!
from lib.logger import Logger
log = Logger('ui')


#####################################################################################
#
#    Disaster Recovery
#
#####################################################################################


def wiz_execute(wiz):
    log.debug("Executing backup creation wizard")
    config = Config.get_config()    
    name = wiz.fields["name"].value
    path = wiz.fields["folderpath"].value
    excl = []
    for typ in config.file_types.iterkeys():
        if wiz.fields['excl-'+typ].value:
            excl.append(typ)
    store = wiz.fields["store"].value
    
    b = Backup(name)
    b.active = True
    b.include_folders = [path]
    b.include_packages = True
    b.exclude_types = excl
    b.store = store
    b.excrypt = False
    b.sched_type = "daily/weekly"
    b.sched_times = "19:00/Sun"    
    b.verify = False
    b.notify_msg = True
    b.notify_email = False
    b.shutdown_after = False
    
    config.backups[name] = b
    config.save()
    update_crontab(config.backups)
    
    

    dlg.Info(wiz, _("Your backup has been successfully created."))
    app.broadcast_update()
        




def do_backup_wizard(parent):
    config = Config.get_config()
    wiz = wizard.Wizard(parent, _("Backup Creation Wizard"),
                 _("Welcome to the backup creation wizard.\n"
                    "\n"
                    "The first time you use The Vault, you need to define\n"
                    "what you want backed up and where to. This wizard will guide you\n"
                    "through the creation of your backup."),
                 _("We are now ready to create the backup."), wiz_execute, icon="images/storage.png")

    #    Name
    page = wizard.Page(wiz, _("Backup Name"))
    wizard.TextField(page, "name", _("What shall we call this backup?"),
                 default=None if not const.Debug else "TestName")
    #    Type of Folder
    page = wizard.Page(wiz, _("Backup What Folder"))
    wizard.DirEntryField(page, "folderpath", _("What folder should be backed up"), must_exist=True,
                 default=None if not const.Debug else os.path.join(const.RunDir, "files"))


    #    Exclude File Types
    names = [key for key in config.file_types.iterkeys()]
    names.sort()
    page = wizard.Page(wiz, _("Excluded Files"))
    wizard.LabelField(page, "excl", _("Select which file types to *exclude* from the backup"))
    for name in names:
        wizard.CheckField(page, "excl-"+name, None, name,
                          default=None if not const.Debug else False)
        
    page = wizard.Page(wiz, _("Store"))
    print(config.storage.keys())
    wizard.OptionsField(page, "store", _("Which store should this be saved to?"),
                 config.storage.keys())

    #    Run the wizard
    wiz.run()
