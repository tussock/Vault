# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Created on Dec 2, 2009

@author: paul
'''

import wx
import gettext
_ = gettext.gettext
import wizui

#    Do last!
from lib.logger import Logger
log = Logger('library')


WizardField_Entry = 1
WizardField_Radio = 2
WizardField_Checkbox = 3

class ValidationException(Exception):
    pass





class Wizard(wizui.Wizard):
    """A wizard class.
    
    You need to add pages to the wizard.
    The first page ([0]) and last page (len(pages)+1) arew autogenerated
    """
    def __init__(self, parent, title, intro_message, final_message, callback=None, size=(600, 400), icon=None):
        wizui.Wizard.__init__(self, parent)
        self.SetTitle(title)
        self.SetMinSize(size)
        self.SetMaxSize(size)
        self.callback = callback
        
        self.parent = parent
        self.page_no = 0
        self.pages = []
        self.fields = {}

        #    Intro page
        page = Page(self, _("Introduction"))
        LabelField(page, "__intro__", intro_message)

        #    Final page
        page = Page(self, _("Completion"))
        LabelField(page, "__final__", final_message)
        
        if not icon is None:
            icon_obj = wx.Icon(icon, wx.BITMAP_TYPE_ANY)
            self.SetIcon(icon_obj)
        
        

        
    def add_page(self, page):
        #    If we have 2 or more pages, then we always add to one before the end
        #    Because the end is the Finalization page.
        if len(self.pages) >= 2:
            self.pages.insert(len(self.pages)-1, page)
        else:
            self.pages.append(page)
        self.pnlPages.GetSizer().Add(page, proportion=0, flag= wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=0) 
        
    def add_field(self, field):
        self.fields[field.tag] = field

    def run(self):

        self.page_no = 0
        self.show_current_page()
        self.Show()
        
    def show_current_page(self):
        #    Setup the buttons
        self.btnBack.Enable(self.page_no >= 1)
        self.btnForward.Show(self.page_no < len(self.pages)-1)
        self.btnFinish.Show(self.page_no == len(self.pages)-1)

        #    Show the correct page
        for page in self.pages:
            page.Hide()
        page = self.pages[self.page_no]
        page.Show()

        #    Set the page title
        self.txtPageTitle.SetLabel(page.title)
        
        #    Finally we ensure all control and buttons are properly laid out
        self.Layout()
        self.Refresh()
        
        
    def onForward(self, event):
        page = self.pages[self.page_no]
        if page.check_cb and not page.check_cb(self):
            return
        self.page_no += 1
        page = self.pages[self.page_no]
        while page.show_cb and not page.show_cb(self) and self.page_no < len(self.pages)-1:
            self.page_no += 1
            page = self.pages[self.page_no]
        self.show_current_page()
    
    def onBack(self, event):
        self.page_no -= 1
        page = self.pages[self.page_no]
        while page.show_cb and not page.show_cb(self) and self.page_no > 0:
            self.page_no -= 1
            page = self.pages[self.page_no]
        self.show_current_page()
    
    def onQuit(self, event):
        dlg = wx.MessageDialog(self, _("Are you sure you want to quit the wizard?"), _("Confirm Quit"), wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Close()
    
    def onFinish(self, event):
        if self.callback:
            self.callback(self)
        self.Close()
        
class Page(wx.Panel):
    def __init__(self, wizard, title, show_cb=None, check_cb=None):
        '''
        
        @param wizard:
        @param title:
        @param show_cb: A function that must return true, otherwise FORWARD and BACKWARD will skip this page
        @param check_cb: A function that must return true before you can move FORWARD off this page
        '''
        wx.Panel.__init__(self, wizard.pnlPages)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.title = title
        self.wizard = wizard
        self.fields = {}
        self.wizard.add_page(self)
        self.Hide()
        self.show_cb = show_cb
        self.check_cb = check_cb

    def add_control(self, control):
        self.sizer.Add(control, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=1)
        
    def add_field(self, field):
        if field.tag in self.fields:
            raise Exception("All wizard fields must have a unique tag")
        self.fields[field.tag] = field
        self.wizard.add_field(field)     
        
    def add_spacer(self):
        self.sizer.AddStretchSpacer() 

class Field(object):
    def __init__(self, page, tag):
        self.page = page
        self.tag = tag

class LabelField(Field):
    def __init__(self, page, tag, label):
        Field.__init__(self, page, tag)
        self.label = wx.StaticText(page)
        self.label.SetLabel(label)
        page.add_control(self.label)
        page.add_field(self)
        
    @property
    def value(self):
        return self.label.GetLabel()

class CheckField(Field):
    def __init__(self, page, tag, prompt=None, checklabel="", default=None):
        Field.__init__(self, page, tag)
        
        #    Set up the label
        if prompt:
            self.label = wx.StaticText(page)
            self.label.SetLabel(prompt)
            page.add_control(self.label)

        #    Set up the Check Box
        self.check = wx.CheckBox(page, label=checklabel)
        page.add_control(self.check)
        if not default is None:
            self.value = default
            
        page.add_field(self)
        
    @property
    def value(self):
        return self.check.GetValue()
    @value.setter
    def value(self, v):
        self.check.SetValue(v)

class OptionsField(Field):
    def __init__(self, page, tag, prompt, choices, default=None):
        Field.__init__(self, page, tag)
        
        self.choices = choices
        #    Set up the label
        self.label = wx.StaticText(page)
        self.label.SetLabel(prompt)
        page.add_control(self.label)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.box = wx.RadioBox(parent = page,
                       choices=self.choices,
                       majorDimension=3)
        self.sizer.Add(self.box, 
                       flag=wx.RA_SPECIFY_COLS | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                       border=3) 
        page.add_control(self.sizer)
        if not default:
            idx = 0
        else:
            idx = self.choices.index(default)
        self.box.SetSelection(idx)
        
        page.add_field(self)

    @property
    def value(self):
        return self.box.GetStringSelection()
    @value.setter
    def value(self, v):
        idx = self.choices.index(v)
        if idx < 0:
            raise Exception("Choice value not found")
        self.box.SetSelection(idx)
        
        
class TextField(Field):
    def __init__(self, page, tag, prompt, width=250, default=None):
        Field.__init__(self, page, tag)
        
        #    Set up the label
        self.label = wx.StaticText(page)
        self.label.SetLabel(prompt)
        page.add_control(self.label)

        #    Set up the text field
        self.text = wx.TextCtrl(page)
        self.text.SetSizeHints(width, -1, width, -1)
        page.add_control(self.text)

        if not default is None:
            self.value = default

        page.add_field(self)

        
    @property
    def value(self):
        return self.text.GetValue()

    @value.setter
    def value(self, v):
        self.text.SetValue(v)

class PasswordField(TextField):
    def __init__(self, page, tag, prompt, width=250, default=None):
        TextField.__init__(self, page, tag, prompt, width, default)    
        self.text.SetWindowStyle(wx.TE_PASSWORD)

class FileEntryField(Field):
    def __init__(self, page, tag, prompt, width=250, must_exist=False, default=None):
        Field.__init__(self, page, tag)
        
        #    Set up the label
        self.label = wx.StaticText(page)
        self.label.SetLabel(prompt)
        page.add_control(self.label)

        #    Set up the text field
        self.path = wx.FilePickerCtrl(page)
        self.path.SetSizeHints(width, -1, width, -1)
        self.path.SetStyle(wx.FLP_FILE_MUST_EXIST)
        page.add_control(self.path) 
        if not default is None:
            self.value = default

        page.add_field(self)

        
    @property
    def value(self):
        return self.path.GetPath()
    @value.setter
    def value(self, v):
        self.path.SetPath(v)

class DirEntryField(Field):
    def __init__(self, page, tag, prompt, must_exist=False, default=None):
        Field.__init__(self, page, tag)
        
        #    Set up the label
        self.label = wx.StaticText(page)
        self.label.SetLabel(prompt)

        page.add_control(self.label)

        #    Set up the text field
        self.path = wx.DirPickerCtrl(page)
        if must_exist:
            self.path.SetExtraStyle(wx.DIRP_DIR_MUST_EXIST)
        page.add_control(self.path)
        if not default is None:
            self.value = default

        page.add_field(self)

        
    @property
    def value(self):
        return self.path.GetPath()
    @value.setter
    def value(self, v):
        self.path.SetPath(v)
    

class ButtonField(Field):
    def __init__(self, page, tag, prompt, callback, args=None):
        Field.__init__(self, page, tag)
        
        self.callback = callback
        self.args = args
        #    Set up the button
        self.button = wx.Button(page, label=prompt)
        self.button.Bind(wx.EVT_BUTTON, self.do_callback)
        page.add_control(self.button)

    def do_callback(self, event):
        if self.args is None:
            self.callback(self.page.wizard)
        else:
            self.callback(self.page.wizard, self.args)
        
        


##################################################################################
#        Testing Code
##################################################################################
def cb(page):
    if page[0] == "a":
        raise ValidationException("The value 'a' is illegal")

def final_cb(wiz):
    pass

def run_test(wizard):
    dlg = wx.MessageDialog(None, "Test Run", "Run", wx.OK)
    dlg.ShowModal()
    dlg.Destroy()
        


def change_cb(widget, field, page, wizard):
    print("got cb from field %s: value = %s" % (field.name, str(field.get_value())))
    
def check_cb(wiz):
    if wiz.fields["checkcb"].value == "option 3":
        return True
    import dlg
    dlg.Warn(wiz, "You must choose option 3", "Choice")
    return False

if __name__ == "__main__":
    app = wx.App()

    wiz = Wizard(None, "Test Title Wizard", "Welcome to the test test wizard.", 
                 "We are now ready to complete the wizard", final_cb)
    
    #    Type of storage
    page = Page(wiz, "Wizard page 1")
    OptionsField(page, "optionsfield", "Which of these options",
                 ["option 1", "option 2"])
    
    #    Type of storage
    page = Page(wiz, "Wizard page 1b")
    OptionsField(page, "manyoptionsfield", "Which of these options",
                 ["option 1", "option 2", "option 3", "option 4",
                   "option 5", "option 6", "option 7"])    
    
    #    Check the check callback
    page = Page(wiz, "You can only move forward if you select option 3", check_cb=check_cb)
    OptionsField(page, "checkcb", "Pick an option",
                 ["option 1", "option 2", "option 3", "option 4",
                   "option 5", "option 6", "option 7"])    
    
    #    Folder storage
    page = Page(wiz, "Page 2 Information", show_cb=lambda wiz: wiz.fields["optionsfield"].value == "option 1")
    DirEntryField(page, "folderpath", "Select a path", must_exist=True)
    
    #    FTP Storage
    page = Page(wiz, "Page 3 information", show_cb=lambda wiz: wiz.fields["optionsfield"].value == "option 2")
    TextField(page, "text", "Some text")
    CheckField(page, "check", "What option", "yes")
    ButtonField(page, "tester", "test", run_test)
    
    #    Run the wizard
    wiz.run()
    
    app.MainLoop()
