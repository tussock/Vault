# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import app
from lib import dlg
#    Do last!
from lib.logger import Logger
log = Logger('ui')

#    Edit States
ViewState, NewState = range(2)



class EditPanel():
    '''
    This class implements all the UI functionality, and expects its subclass
    to implement the worker functions (such as clear(), save() etc.
    '''
    
    def onNew(self, event):
        log.info("New!")
        self.state = NewState
        self.clear()
        self.txtName.SetFocus()   
        
    def onSave(self, event):
        try:
            self.save()
            self.state = ViewState
            self.update_state()
            self.lstItems.SetStringSelection(self.txtName.GetValue())
            #    Inform all other panels about the data change.
            app.broadcast_update()
        except Exception as e:
            dlg.Warn(self, str(e))
        

    def onItemSelected(self, event):
        #    Get the name to be showed
        name = self.lstItems.GetStringSelection()
        if len(name) == 0:
            return
        self.show(name)
        
    def onRevert(self, event):
        self.onItemSelected(event)


    def onDelete(self, event):
        #    Get the name to be showed
        name = self.lstItems.GetStringSelection()
        if len(name) == 0:
            return
        self.delete(name)        


        
    #   Abstract Classes Implemented By Subclass
    def save(self):
        pass
    def clear(self):
        pass
    def update_state(self):
        pass
    def show(self, name):
        pass