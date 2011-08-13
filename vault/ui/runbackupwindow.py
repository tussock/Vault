# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


import wx
import subprocess
import thread
import threading
import time
import os

import gui
from lib import const
from lib.config import Config
from lib import dlg
import app
#    Do last!
from lib.logger import Logger
log = Logger('ui')


class RunBackupWindow(gui.RunBackupWindow):
    '''
    classdocs
    '''


    def __init__(self, parent, backup_name):
        '''
        Constructor
        '''
        gui.RunBackupWindow.__init__(self, parent)
        log.trace("Starting up a run backup window")
        
        self.config = Config.get_config()

        self.cboBackup.AppendItems(self.config.backups.keys())
        self.cboBackup.SetStringSelection(backup_name)

        self.status(_("Idle"))

        self.lock = threading.Lock()
        self.proc = None
        self.btnStop.Enable(False)
        self.pnlDryRun.Hide()
        self.Layout()
        self.Fit()
        self.Show()

        icon = wx.Icon(os.path.join(const.PixmapDir, "storage.png"), wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)
        

    def onStart(self, event):
        bname = self.cboBackup.GetStringSelection()
        if not bname:
            dlg.Info(self, _("Please select a backup"))
            return
        #    Get a copy of the list
        options = list(const.ServerProgram)
        if self.chkMessage.GetValue():
            options.append("--message")
        if self.chkEmail.GetValue():
            options.append("--email")
        if self.chkShutdown.GetValue():
            options.append("--shutdown")
        if self.chkDryRun.GetValue():
            options.append("--dry-run")

        #    Start up the backup process
        options.append("backup")
        options.append("--full" if self.radFull.GetValue() else "--incremental")
        options.append(bname)


        if self.chkDryRun.GetValue():
            self.txtFiles.Clear()
            self.done = False
            self.lines = []

            #    Start the dry run process...
            log.debug("Starting subprocess", options)
            self.proc = subprocess.Popen(options,
                                         stdout=subprocess.PIPE
                                         )
            #    We need a thread to collect the (possibly large)
            #    data streamed from this sub-process.
            thread.start_new_thread(self.do_dry_run, (self.proc,))
            #    This process takes the streamed data and displays it.
            #    Must run in this thread.
            wx.CallLater(250, self.do_display_output)
            #    Now set up the display.
            self.status(_("Running..."))
            self.pnlDryRun.Show()
            self.Layout()
            self.Fit()
            self.btnStart.Enable(False)
            self.btnStop.Enable(True)
        else:
            log.debug("Starting", options)
            subprocess.Popen(options)
            wx.CallLater(2000, app.broadcast_update)
            dlg.Info(self, _("Backup '{backup}' has been started\nYou can view it's progress in the History Window").format(backup=bname))
            self.Close()


    def onClose(self, event):
        self.Close()

    def onStop(self, event):
        self.stop()

##################################################################
#
#    Dry Run Functions
#
##################################################################

    def do_dry_run(self, proc):
        """Threaded routine to capture output from the subprocess.
        Since this can only be done safely in a blocking mode... we 
        use a thread.
        
        Places the data in a list (with a lock for protection).
        It gets picked up by the timed callback (running in the 
        UI thread) for placing in the display list.
        """
        log.debug("Dry Run.")
        while proc.poll() is None:
            #    This can block
            output = proc.stdout.readline()
            if len(output) > 0:
                with self.lock:
                    self.lines.append(output)
                    log.trace("Pushing ", output)
        #    Capture anything left over
        log.debug("Capturing left over")
        output = proc.communicate()[0]
        if len(output) > 0:
            with self.lock:
                self.lines.append(output)
                log.trace("Pushing ", output)
        self.done = True

    def do_display_output(self):
        with self.lock:
            if len(self.lines) > 0:
                for line in self.lines:
                    log.trace("Popping ", line)
                    self.txtFiles.AppendText(line)
                self.lines = []
        self.txtFiles.Refresh()
        if not self.done:
            wx.CallLater(250, self.do_display_output)
        else:
            self.status("Finished")
            self.btnStart.Enable(True)
            self.btnStop.Enable(False)

##################################################################
#
#    Utilities
#
##################################################################

    def stop(self):
        #check its running
        if not self.proc is None and self.proc.poll() is None:
            self.status(_("Stopping..."))
            self.proc.terminate()
            #    Give it 1 second. then kill!!!
            t = time.time() + 1
            while time.time() < t:
                time.sleep(0.1)
                if self.proc.poll():
                    #    Its dead
                    break
            if self.proc.poll() is None:
                #    Still running...
                self.proc.kill()
        self.status(_("Stopped"))
        self.btnStart.Enable(True)
        self.btnStop.Enable(False)

    def status(self, msg):
        self.statusBar.SetFields([msg])
        self.statusBar.Refresh()
