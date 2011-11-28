# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import os
from collections import namedtuple
import tempfile
import shutil

import gui
from lib.db import DB
from lib import dlg
from lib.config import Config
from lib import const
from rundetailswindow import RunDetailsWindow
from runrestorewindow import RunRestoreWindow
from packagewindow import PackageWindow
from recoverconfig import do_recover
from rebuilddb import do_rebuilddb
from lib import utils
from lib import cryptor
#    Do last!
from lib.logger import Logger
log = Logger('ui')


node_info = namedtuple('node_info', 'parent_id fs_id type expanded path')
DummyTreeNode = "__dummy__"

class RestorePanel(gui.RestorePanel):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        log.info("***RestorePanel.init")

        gui.RestorePanel.__init__(self, parent)
        self.db = DB()
        self.config = Config.get_config()
        self.images = wx.ImageList(16, 16)
        self.images.Add(
                        wx.Bitmap(os.path.join(const.PixmapDir, "folder.png"), 
                                  wx.BITMAP_TYPE_PNG)
                        )
        self.images.Add(
                        wx.Bitmap(os.path.join(const.PixmapDir, "document.png"), 
                                  wx.BITMAP_TYPE_PNG)
                        )
        self.fs_tree.SetImageList(self.images)
        #    Looks better if this is blank.
        self.set_selected_file("")
        self.force_rebuild()

        self.image = wx.Bitmap(os.path.join(const.PixmapDir, "review.png"))
        self.title = _("Restore")

        #    Ensure the right page is showing
        self.nb_restore.SetSelection(0)
        log.trace("Done RestorePanel.init")

    def prepare_static_data(self):
        #    Load all runs for the date slider
        self.runs = self.db.runs()

        self.date_slider.SetMin(0)
        log.debug("Date Slider: %d runs" % len(self.runs))
        if len(self.runs) in [0, 1]:
            #    Cannot set a slider with 0 or 1 positions. So disable it.
            self.date_slider.Enable(False)
            self.date_slider.SetMax(1)
            self.date_slider.SetValue(0)
        else:
            self.date_slider.SetMax(len(self.runs) - 1)
            self.date_slider.SetValue(len(self.runs) - 1)
            self.date_slider.Enable(True)

        self.cboBackup.Clear()
        self.cboBackup.AppendItems([name for name in self.config.backups.iterkeys()])
        if self.cboBackup.Count > 0:
            self.cboBackup.SetSelection(0)

    def force_rebuild(self):
        log.debug("Forcing complete rebuild")
        self.displayed_run = None
        self.prepare_static_data()
        #    Prepare the tree
        self.fs_tree.DeleteAllItems()
        self.root_node = self.fs_tree.AddRoot(text="/", image=0)
        self.fs_tree.SetItemPyData(self.root_node, node_info(0, 0, "D", False, "/"))
        self.expand_node(self.root_node)
        self.onSliderScroll(None)
        self.pnlRestore.Layout()

    def update_data(self):
        # TODO! This could be dangerously time consuming!
        self.prepare_static_data()
        self.onSliderScroll(None)
        self.rebuild_tree()
        self.pnlRestore.Layout()

    def get_current_run(self):
        if len(self.runs) == 0:
            return None
        if len(self.runs) == 1:
            return self.runs[0]

        idx = self.date_slider.GetValue()
        if idx >= len(self.runs):
            raise Exception("Invalid date slider position")
        return self.runs[idx]

    def expand_node(self, parent_node):
        log.trace("expand_node", parent_node)
        run = self.get_current_run()
        if not run:
            return
        #    Get the folder - which is in data
        parent_info = self.fs_tree.GetItemPyData(parent_node)
        log.debug("expanding node", parent_info)
        if parent_info.expanded:
            log.debug("Already expanded")
            return
        if parent_info.type == "F":
            log.debug("File node (no children)")
            return
        #    Clean out the dummy sub-node
        self.fs_tree.DeleteChildren(parent_node)

        #    Now add the subnodes (Only up to the currently selected run
        files = self.db.list_dir_id(parent_info.fs_id, run_id=run.run_id)
        for name, item in files.iteritems():
            if parent_info.fs_id == 0 and name == "/":
                continue
            #    The type may be None because this could be a folder that
            #    we log, but dont back up.
            type = item.type
            if type is None:
                type = "D"
            #    We dont add in deleted files
            if type != "X":
                node_name = utils.display_escape(name)
                new_node = self.fs_tree.AppendItem(parent_node, node_name, image=0 if type == "D" else 1)
                new_info = node_info(parent_info.fs_id, item.fs_id, type, False, os.path.join(parent_info.path, name))
                log.debug("New node: ", new_info)
                self.fs_tree.SetItemPyData(new_node, new_info)
                #    For any folders, add a dummy sub-node so we can expand it later
                if type == "D":
                    self.fs_tree.AppendItem(new_node, DummyTreeNode)

        #    Update the parent node to show that its been expanded.
        upd_info = node_info(parent_info.parent_id, parent_info.fs_id, parent_info.type, True, parent_info.path)
        self.fs_tree.SetItemPyData(parent_node, upd_info)
        self.fs_tree.SortChildren(parent_node)

##################################################################
#
#    Event Handlers
#
##################################################################
    def onRefresh(self, event):
        self.force_rebuild()

    def onTreeItemExpanding(self, event):
        log.trace("onTreeItemExpanding")
        item = event.GetItem()
        self.expand_node(item)

    def onTreeSelChanged(self, event):
        log.trace("onTreeSelChanged")
        item = event.GetItem()
        print(item)
        info = self.fs_tree.GetItemPyData(item)
        self.set_selected_file(info.path)

    def onSliderScroll(self, event):
        #    Get the run
        log.trace("Slider Scroll")
        run = self.get_current_run()
        if not run:
            self.date_label.SetLabel("")
            self.time_label.SetLabel("")
            self.pnlRestore.Layout()
            self.lblTreeTitle.SetLabel("No backups have run yet.")
            return

        date = run.start_time
        self.date_label.SetLabel(date.strftime(const.ShortDateFormat))
        self.time_label.SetLabel(date.strftime(const.ShortTimeFormat))
        self.pnlRestore.Layout()
        self.date_slider.SetToolTipString(date.strftime(const.ShortDateTimeFormat))
        self.lblTreeTitle.SetLabel("File System as at " + date.strftime(const.ShortDateTimeFormat))

        self.rebuild_tree()

    def onRunDetails(self, event):
        run = self.get_current_run()
        if not run:
            return
        dummy = RunDetailsWindow(self, run)

    def onRestore(self, event):
        sel = self.fs_tree.GetSelection()
        data = self.fs_tree.GetItemPyData(sel)
        dummy = RunRestoreWindow(self, data.path)

    def onReload(self, event):
        #    Reload the configuration
        do_recover(self)

    def onRebuild(self, event):
        #    Rebuild the local database of saved files.
        do_rebuilddb(self)

    def onRestoreTab(self, event):
        #    Refresh the restore tab, then switch to it...
        self.onRefresh(event)
        self.nb_restore.SetSelection(0)

    def onShowPackages(self, event):
        #    Fetch the package list from the last run of the selected backup
        if self.cboBackup.Count == 0:
            return
        #    Get the backup and store
        bname = self.cboBackup.GetStringSelection()
        backup = self.config.backups[bname]
        store = self.config.storage[backup.store].copy()
        #    Figure out the last run
        runs = self.db.runs(bname)
        if len(runs) == 0:
            dlg.Info(self, _("The selected backup has not run"))
            return

        #    last is the most recent
        run = runs[-1]
        #    Get the folder
        folder = os.path.join(bname, run.start_time_str + ' ' + run.type)
        src = os.path.join(folder, const.PackageFile)

        if backup.encrypt:
            src = src + const.EncryptionSuffix
        workfolder = tempfile.mkdtemp()
        store.connect()
        store.copy_from(src, workfolder)
        store.disconnect()
        package_path = os.path.join(workfolder, const.PackageFile)
        if backup.encrypt:
            crypt_path = package_path + const.EncryptionSuffix
            cryptor.decrypt_file(self.config.data_passphrase, crypt_path, package_path)

        package_list = open(package_path).read().split('\n')
        #    Cleanup
        shutil.rmtree(workfolder)

        win = PackageWindow(self, package_list)

    def onSelectedFileSize(self, event):
        self.update_truncated_text(self.lblSelectedFile)
##################################################################
#
#    Utilities
#
##################################################################

    def set_selected_file(self, text):
        """
        We dont want the SelectedFile expanding, nor do we want it resizing.
        
        We save the full text in the HelpText field.
        We set the text to a reduced text field that will fit.
        """
        self.lblSelectedFile.SetToolTipString(text)
        self.update_truncated_text(self.lblSelectedFile)
        
    def update_truncated_text(self, field):
        dc = wx.ClientDC(field)
        maxWidth = self.lblSelectedFile.GetSize().x
        tt = field.GetToolTip()
        text = tt.GetTip() if tt else ""
        newText = self.truncate_text(dc, text, maxWidth)
        if newText == None:
            newText = ""
        self.lblSelectedFile.SetLabel(newText)
        
    def truncate_text(self, dc, text, maxWidth):
        """
        Truncates a given string to fit given width size. if the text does not fit
        into the given width it is truncated to fit. the format of the fixed text
        is <truncate text ..>.
        """
    
        textLen = len(text)
        tempText = text
        rectSize = maxWidth
    
        fixedText = ""
    
        textW, textH = dc.GetTextExtent(text)
    
        if rectSize >= textW:
            return text
    
        # The text does not fit in the designated area,
        # so we need to truncate it a bit
        suffix = "..."
        border = 5
        w, h = dc.GetTextExtent(suffix)
        rectSize -= w
    
        for i in xrange(textLen, -1, -1):
    
            textW, textH = dc.GetTextExtent(tempText)
            if rectSize >= textW + border:
                fixedText = tempText
                fixedText += suffix
                return fixedText
    
            tempText = tempText[:-1]         

    def rebuild_tree(self):
        #    The date has changed.
        #    We correct the tree for the current date.
        #    Assume a number of nodes are visible/created
        #        1: if that node was not backed up in the run (or prior) then delete it
        #            unless that node has never been backed up (i.e we just record its FS position)
        #        2: if that node changed type, fix it
        #        3: if a new node should be added, add it.
        #    We must do this for all loaded nodes, not just visible.

        run = self.get_current_run() #self.runs[self.date_slider.GetValue()]
        if not run:
            return
        if run != self.displayed_run:
            log.info("Rebuilding tree for run:", run)
            self.rebuild_node(run, self.root_node)
            log.debug("Done rebuild tree")
            self.displayed_run = run
        else:
            log.debug("Already showing this run.")

    def rebuild_node(self, run, node):
        '''
        Given a node, we want to correct it's state as at the given run.
        We do this as non-destructively as possible, so that the tree remains
        in shape.
        
        We are correcting the CHILDREN of the current node, so if the node is
        a leaf - we quit (it should have been corrected when correcting its parent)
        
        @param run:
        @type run:
        @param node:
        @type node:
        '''
        node_data = self.fs_tree.GetItemPyData(node)
        #    If this is NOT a folder node, exit.
        if node_data.type != "D":
            log.debug("Node not directory")
            return
        #    If this node has not been expanded, exit
        if not node_data.expanded:
            log.debug("Node not expanded")
            return
        log.debug("rebuild_node", run, node, node_data)

        #    From the DB, get all fs entries under the current one
        dbentries = self.db.list_dir_id(node_data.fs_id, run.run_id)
        if not dbentries:
            #    This node has no children
            self.fs_tree.DeleteChildren(node)
            log.debug("Node has no children")
            return
#        #    Get the child list - we have to get this in advance because our changes to
#        #    the tree will cause iterators to fail
#        (child, cookie) = self.fs_tree.GetFirstChild(node)

        #    For each of its children
        children_ids = []
        (child, cookie) = self.fs_tree.GetFirstChild(node)
        while child:
            children_ids.append(child)
            child, cookie = self.fs_tree.GetNextChild(node, cookie)

        for child in children_ids:
            #    Get information on this node.
            child_name = self.fs_tree.GetItemText(child)
            log.debug("Got ", child_name)
            child_data = self.fs_tree.GetItemPyData(child)
            if not child_data:
                raise Exception("Illegal: empty child node")

            log.debug("Visiting node:", child_name, child_data)
            #    Fix the node.
            #    If the node type is right, then we will leave it in.
            #    Get the DB node:
            try:
                if child_name in dbentries:
                    #    Exists in tree AND in DB. Make sure the types are right
                    db_data = dbentries[child_name]
                    if db_data.type == 'X':
                        log.debug("Type X = delete", child_name)
                        self.fs_tree.Delete(child)
                    elif db_data.type == 'D' and child_data.type == 'F':
                        new_info = node_info(db_data.parent_id, db_data.fs_id, db_data.type, False, os.path.join(node_data.path, child_name))
                        log.debug("New node: ", new_info)
                        self.fs_tree.SetItemPyData(child, new_info)
                        #    Adding a DIR node, so add a dummy to ensure it shows properly.
                        self.fs_tree.AppendItem(child, DummyTreeNode)
                        #    TODO. change the icon from dir to file.
                    elif db_data.type == 'F' and child_data.type == 'D':
                        #    Fix
                        new_info = node_info(db_data.parent_id, db_data.fs_id, db_data.type, False, os.path.join(node_data.path, child_name))
                        log.debug("New node: ", new_info)
                        self.fs_tree.SetItemPyData(child, new_info)
                        self.fs_tree.DeleteChildren(child)
                        #    TODO. change the icon from file to dir.
                    else:
                        #    The tree and DB nodes agree
                        pass
                    #    Check on the children
                    log.debug("Recursing")
                    self.rebuild_node(run, child)
                    log.debug("Completed node ", child_name)
                    #    This node has been completely fixed
                    del dbentries[child_name]
                else:   #    NOTE IN DB
                    log.debug("Entry no longer exists. Removing from tree")
                    self.fs_tree.Delete(child)
            except Exception as e:
                log.error("Exception on %s: %s" % (child_name, str(e)))
            #    Next node
        log.debug("Items Left:", dbentries)
        #    Now add any missing items back in
        for name, db_data in dbentries.iteritems():
            #    Special case - watch for root
            if db_data.fs_id == 0:
                continue
            if db_data.type is None:
                type = 'D'
            else:
                type = db_data.type

            if db_data.type == 'X':
                continue

            node_name = utils.display_escape(name)
            new_node = self.fs_tree.AppendItem(node, node_name, image=0 if type == "D" else 1)
            new_info = node_info(db_data.parent_id, db_data.fs_id, type, False, os.path.join(node_data.path, name))
            log.debug("New node: ", new_info)
            self.fs_tree.SetItemPyData(new_node, new_info)
            #    For any folders, add a dummy sub-node so we can expand it later
            if type == "D":
                self.fs_tree.AppendItem(new_node, DummyTreeNode)

        #    Ensure the nodes keep roughly the same position/order
        self.fs_tree.SortChildren(node)


    def get_path(self, node):
        '''
        Walk back up the tree to work out the full path for the current node
        
        @param node:
        '''
        if node == self.root_node:
            return "/"

        path = os.path.join(self.get_path(self.fs_tree.GetItemParent(node)),
                            self.fs_tree.GetItemText(node))
        return path


