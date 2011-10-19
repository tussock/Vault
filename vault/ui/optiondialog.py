# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.



import gui

#    Do last!
from lib.logger import Logger
log = Logger('ui')

class OptionDialog(gui.OptionDialog):
    '''
    classdocs
    '''


    def __init__(self, parent, message, caption, option, default=False):
        '''
        Constructor
        '''
        gui.OptionDialog.__init__(self, parent)
        self.SetTitle(caption)
        self.lblMessage.SetLabel(message)
        self.chkOption.SetLabel(option)
        self.chkOption.SetValue(default)
        self.Fit()


#    def onOk(self, event):
#        log.debug("OK")
#
#    def onCancel(self, event):
#        log.debug("Cancel")
