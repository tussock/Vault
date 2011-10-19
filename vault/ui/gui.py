# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
from autowidthlist import AutoWidthListCtrl

import gettext
_ = gettext.gettext

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("The Vault"), pos = wx.DefaultPosition, size = wx.Size( 743,429 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.statusbar.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer30 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer85 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnQuit = wx.Button( self, wx.ID_ANY, _("Quit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer85.Add( self.btnQuit, 0, wx.ALL, 3 )
		
		
		bSizer85.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnAbout = wx.Button( self, wx.ID_ANY, _("About"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer85.Add( self.btnAbout, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.btnHelp = wx.Button( self, wx.ID_ANY, _("Show Help"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer85.Add( self.btnHelp, 0, wx.ALL, 3 )
		
		bSizer30.Add( bSizer85, 0, wx.EXPAND, 3 )
		
		self.SetSizer( bSizer30 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_SET_FOCUS, self.onSetFocus )
		self.btnQuit.Bind( wx.EVT_BUTTON, self.onQuit )
		self.btnAbout.Bind( wx.EVT_BUTTON, self.onAbout )
		self.btnHelp.Bind( wx.EVT_BUTTON, self.onHelp )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSetFocus( self, event ):
		event.Skip()
	
	def onQuit( self, event ):
		event.Skip()
	
	def onAbout( self, event ):
		event.Skip()
	
	def onHelp( self, event ):
		event.Skip()
	

###########################################################################
## Class OptionDialog
###########################################################################

class OptionDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("<title>"), pos = wx.DefaultPosition, size = wx.Size( 386,173 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer57 = wx.BoxSizer( wx.VERTICAL )
		
		self.lblMessage = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblMessage.Wrap( -1 )
		bSizer57.Add( self.lblMessage, 0, wx.ALL|wx.EXPAND, 10 )
		
		self.chkOption = wx.CheckBox( self, wx.ID_ANY, _("Check Me!"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer57.Add( self.chkOption, 0, wx.ALL|wx.EXPAND, 20 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		bSizer57.Add( m_sdbSizer1, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.SetSizer( bSizer57 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.onCancel )
		self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.onOk )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancel( self, event ):
		event.Skip()
	
	def onOk( self, event ):
		event.Skip()
	

###########################################################################
## Class OverviewPanel
###########################################################################

class OverviewPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 573,441 ), style = wx.TAB_TRAVERSAL )
		
		bSizer37 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText60 = wx.StaticText( self, wx.ID_ANY, _("System Overview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText60.Wrap( -1 )
		self.m_staticText60.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer37.Add( self.m_staticText60, 0, wx.ALL, 3 )
		
		statusSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
		statusSizer.AddGrowableCol( 1 )
		statusSizer.AddGrowableRow( 2 )
		statusSizer.SetFlexibleDirection( wx.BOTH )
		statusSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.imgStatus = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		statusSizer.Add( self.imgStatus, 0, wx.ALL, 3 )
		
		self.lblStatus = wx.StaticText( self, wx.ID_ANY, _("Status: Healthy"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblStatus.Wrap( -1 )
		self.lblStatus.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		statusSizer.Add( self.lblStatus, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		
		statusSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.lblMessages = wx.StaticText( self, wx.ID_ANY, _("Messages"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblMessages.Wrap( -1 )
		self.lblMessages.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		statusSizer.Add( self.lblMessages, 0, wx.ALL|wx.EXPAND, 3 )
		
		bSizer37.Add( statusSizer, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer37.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, _("Backups Overview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		self.m_staticText61.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer37.Add( self.m_staticText61, 0, wx.ALL, 3 )
		
		bSizer55 = wx.BoxSizer( wx.VERTICAL )
		
		self.lstBackups = AutoWidthListCtrl(self)
		
		#self.lstBackups.SetSingleStyle(wx.LC_NO_HEADER)
		self.lstBackups.SetSingleStyle(wx.LC_SORT_ASCENDING)
		self.lstBackups.SetBackgroundColour(wx.NullColour)
		
		self.lstBackups.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer55.Add( self.lstBackups, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.lblNoBackups = wx.StaticText( self, wx.ID_ANY, _("No backups have been defined"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.lblNoBackups.Wrap( -1 )
		self.lblNoBackups.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer55.Add( self.lblNoBackups, 0, wx.ALL, 3 )
		
		bSizer37.Add( bSizer55, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer37.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, _("Storage Overview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		self.m_staticText62.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer37.Add( self.m_staticText62, 0, wx.ALL, 3 )
		
		bSizer56 = wx.BoxSizer( wx.VERTICAL )
		
		self.lstStores = AutoWidthListCtrl(self)
		
		#self.lstStores.SetSingleStyle(wx.LC_NO_HEADER)
		self.lstStores.SetSingleStyle(wx.LC_SORT_ASCENDING)
		self.lstStores.SetBackgroundColour(wx.NullColour)
		
		self.lstStores.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer56.Add( self.lstStores, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.lblNoStores = wx.StaticText( self, wx.ID_ANY, _("No stores have been defined"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.lblNoStores.Wrap( -1 )
		self.lblNoStores.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer56.Add( self.lblNoStores, 0, wx.ALL, 5 )
		
		bSizer37.Add( bSizer56, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticline81 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer37.Add( self.m_staticline81, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText621 = wx.StaticText( self, wx.ID_ANY, _("Actions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText621.Wrap( -1 )
		self.m_staticText621.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer37.Add( self.m_staticText621, 0, wx.ALL, 5 )
		
		bSizer82 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer15 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer83 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnRefresh2 = wx.Button( self, wx.ID_ANY, _("Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer83.Add( self.btnRefresh2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.btnHistory = wx.Button( self, wx.ID_ANY, _("View History"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer83.Add( self.btnHistory, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticline13 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer83.Add( self.m_staticline13, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText115 = wx.StaticText( self, wx.ID_ANY, _("First Time Wizards:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText115.Wrap( -1 )
		bSizer83.Add( self.m_staticText115, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_button32 = wx.Button( self, wx.ID_ANY, _("Setup Storage"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer83.Add( self.m_button32, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_button33 = wx.Button( self, wx.ID_ANY, _("Setup Backup"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer83.Add( self.m_button33, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		fgSizer15.Add( bSizer83, 1, wx.EXPAND, 3 )
		
		bSizer82.Add( fgSizer15, 1, wx.EXPAND, 3 )
		
		bSizer37.Add( bSizer82, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.SetSizer( bSizer37 )
		self.Layout()
		
		# Connect Events
		self.btnRefresh2.Bind( wx.EVT_BUTTON, self.onRefresh )
		self.btnHistory.Bind( wx.EVT_BUTTON, self.onHistory )
		self.m_button32.Bind( wx.EVT_BUTTON, self.onSetupStore )
		self.m_button33.Bind( wx.EVT_BUTTON, self.onSetupBackup )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onRefresh( self, event ):
		event.Skip()
	
	def onHistory( self, event ):
		event.Skip()
	
	def onSetupStore( self, event ):
		event.Skip()
	
	def onSetupBackup( self, event ):
		event.Skip()
	

###########################################################################
## Class BackupPanel
###########################################################################

class BackupPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 717,457 ), style = wx.TAB_TRAVERSAL )
		
		bSizer33 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter3 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		self.m_splitter3.SetMinimumPaneSize( 180 )
		
		self.m_panel26 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer34 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText24 = wx.StaticText( self.m_panel26, wx.ID_ANY, _("Backups"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		self.m_staticText24.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer34.Add( self.m_staticText24, 0, wx.ALL|wx.EXPAND, 3 )
		
		lstItemsChoices = []
		self.lstItems = wx.ListBox( self.m_panel26, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,150 ), lstItemsChoices, wx.LB_SORT )
		bSizer34.Add( self.lstItems, 0, wx.ALL|wx.EXPAND, 3 )
		
		gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.btnDelete = wx.Button( self.m_panel26, wx.ID_ANY, _("Delete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnDelete, 0, wx.ALL, 3 )
		
		self.btnNew = wx.Button( self.m_panel26, wx.ID_ANY, _("Add New"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnNew, 0, wx.ALIGN_RIGHT|wx.ALL, 3 )
		
		self.btnRun = wx.Button( self.m_panel26, wx.ID_ANY, _("Run..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnRun, 0, wx.ALL, 3 )
		
		self.btnHistory = wx.Button( self.m_panel26, wx.ID_ANY, _("History"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnHistory, 0, wx.ALIGN_RIGHT|wx.ALL, 3 )
		
		bSizer34.Add( gSizer3, 0, wx.EXPAND, 3 )
		
		self.m_panel26.SetSizer( bSizer34 )
		self.m_panel26.Layout()
		bSizer34.Fit( self.m_panel26 )
		self.m_panel27 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.nbBackup = wx.Notebook( self.m_panel27, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pnlGeneralTab = wx.Panel( self.nbBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer42 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText39 = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("General"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )
		self.m_staticText39.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer42.Add( self.m_staticText39, 0, wx.ALL, 3 )
		
		fgSizer2 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText311 = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("Name:"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText311.Wrap( -1 )
		fgSizer2.Add( self.m_staticText311, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer87 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtName = wx.TextCtrl( self.pnlGeneralTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer87.Add( self.txtName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.lblName = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("Static Name"), wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		self.lblName.Wrap( -1 )
		bSizer87.Add( self.lblName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		fgSizer2.Add( bSizer87, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 3 )
		
		self.m_staticText81 = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("Status:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )
		fgSizer2.Add( self.m_staticText81, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkActive = wx.CheckBox( self.pnlGeneralTab, wx.ID_ANY, _("Active/Enabled"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.chkActive, 0, wx.ALL, 5 )
		
		bSizer42.Add( fgSizer2, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText40 = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("Backup What Folders"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		self.m_staticText40.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer42.Add( self.m_staticText40, 0, wx.ALL, 3 )
		
		fgSizer4 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText32 = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("Folders:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		fgSizer4.Add( self.m_staticText32, 0, wx.ALL, 3 )
		
		bSizer412 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer95 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtFolders = wx.TextCtrl( self.pnlGeneralTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.txtFolders.SetMinSize( wx.Size( -1,100 ) )
		
		bSizer95.Add( self.txtFolders, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		self.btnAddFolder = wx.BitmapButton( self.pnlGeneralTab, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer95.Add( self.btnAddFolder, 0, wx.ALL, 5 )
		
		bSizer412.Add( bSizer95, 1, wx.EXPAND, 3 )
		
		self.m_staticText95 = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("Type one folder per line, or click \"+\" to use a folder selector."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText95.Wrap( -1 )
		self.m_staticText95.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer412.Add( self.m_staticText95, 0, wx.ALL, 5 )
		
		fgSizer4.Add( bSizer412, 1, wx.EXPAND, 3 )
		
		self.m_staticText34 = wx.StaticText( self.pnlGeneralTab, wx.ID_ANY, _("Packages:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		fgSizer4.Add( self.m_staticText34, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkPackages = wx.CheckBox( self.pnlGeneralTab, wx.ID_ANY, _("Include list of installed packages"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.chkPackages, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		
		fgSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 3 )
		
		bSizer42.Add( fgSizer4, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlGeneralTab.SetSizer( bSizer42 )
		self.pnlGeneralTab.Layout()
		bSizer42.Fit( self.pnlGeneralTab )
		self.nbBackup.AddPage( self.pnlGeneralTab, _("General"), True )
		self.pnlExcludeTab = wx.Panel( self.nbBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer43 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText41 = wx.StaticText( self.pnlExcludeTab, wx.ID_ANY, _("Exclude File Types"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		self.m_staticText41.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer43.Add( self.m_staticText41, 0, wx.ALL, 3 )
		
		bSizer411 = wx.BoxSizer( wx.VERTICAL )
		
		lstExcludeTypesChoices = [ _("Images"), _("Videos"), _("Programs") ];
		self.lstExcludeTypes = wx.CheckListBox( self.pnlExcludeTab, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), lstExcludeTypesChoices, wx.LB_SORT )
		self.lstExcludeTypes.SetMinSize( wx.Size( -1,100 ) )
		
		bSizer411.Add( self.lstExcludeTypes, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.lblDestDetails112 = wx.StaticText( self.pnlExcludeTab, wx.ID_ANY, _("File types may be adjusted in Configuration | File Types."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblDestDetails112.Wrap( -1 )
		self.lblDestDetails112.SetFont( wx.Font( 8, 74, 93, 90, False, "Sans" ) )
		
		bSizer411.Add( self.lblDestDetails112, 0, wx.ALL, 3 )
		
		bSizer43.Add( bSizer411, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText42 = wx.StaticText( self.pnlExcludeTab, wx.ID_ANY, _("Exclude Files/Folder Patterns"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		self.m_staticText42.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer43.Add( self.m_staticText42, 0, wx.ALL, 3 )
		
		bSizer4121 = wx.BoxSizer( wx.VERTICAL )
		
		self.txtExcludePatterns = wx.TextCtrl( self.pnlExcludeTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 250,-1 ), wx.TE_MULTILINE )
		self.txtExcludePatterns.SetMinSize( wx.Size( -1,100 ) )
		
		bSizer4121.Add( self.txtExcludePatterns, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.lblDestDetails11 = wx.StaticText( self.pnlExcludeTab, wx.ID_ANY, _("Enter paths and patterns for files/folders to exclude - one per line.\n* - matches any path\n? - matches any character\n[letters] - matches any one of the letters\n[!letters] = matches any character not in letters.\nExample: */Trash matches the Trash folder, and therefore also excludes all subfolders."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblDestDetails11.Wrap( -1 )
		self.lblDestDetails11.SetFont( wx.Font( 8, 74, 93, 90, False, "Sans" ) )
		
		bSizer4121.Add( self.lblDestDetails11, 0, wx.ALL, 3 )
		
		bSizer43.Add( bSizer4121, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlExcludeTab.SetSizer( bSizer43 )
		self.pnlExcludeTab.Layout()
		bSizer43.Fit( self.pnlExcludeTab )
		self.nbBackup.AddPage( self.pnlExcludeTab, _("Exclude"), False )
		self.pnlStoreTab = wx.Panel( self.nbBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer75 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText50 = wx.StaticText( self.pnlStoreTab, wx.ID_ANY, _("Store To:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText50.Wrap( -1 )
		self.m_staticText50.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer75.Add( self.m_staticText50, 0, wx.ALL, 3 )
		
		bSizer76 = wx.BoxSizer( wx.HORIZONTAL )
		
		cboStoreChoices = []
		self.cboStore = wx.Choice( self.pnlStoreTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboStoreChoices, 0 )
		self.cboStore.SetSelection( 0 )
		bSizer76.Add( self.cboStore, 0, wx.ALL, 3 )
		
		bSizer75.Add( bSizer76, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText501 = wx.StaticText( self.pnlStoreTab, wx.ID_ANY, _("Protect Backup Files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText501.Wrap( -1 )
		self.m_staticText501.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer75.Add( self.m_staticText501, 0, wx.ALL, 3 )
		
		self.chkEncrypt = wx.CheckBox( self.pnlStoreTab, wx.ID_ANY, _("Encrypt data"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer75.Add( self.chkEncrypt, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 23 )
		
		self.lblDestDetails1111 = wx.StaticText( self.pnlStoreTab, wx.ID_ANY, _("Encryption will use the master password (see the Configuration panel)."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblDestDetails1111.Wrap( -1 )
		self.lblDestDetails1111.SetFont( wx.Font( 8, 74, 93, 90, False, "Sans" ) )
		
		bSizer75.Add( self.lblDestDetails1111, 0, wx.LEFT, 23 )
		
		self.chkVerify = wx.CheckBox( self.pnlStoreTab, wx.ID_ANY, _("Verify data after backup"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer75.Add( self.chkVerify, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 23 )
		
		self.lblDestDetails111 = wx.StaticText( self.pnlStoreTab, wx.ID_ANY, _("Note that verification will slow down the backup"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblDestDetails111.Wrap( -1 )
		self.lblDestDetails111.SetFont( wx.Font( 8, 74, 93, 90, False, "Sans" ) )
		
		bSizer75.Add( self.lblDestDetails111, 0, wx.LEFT, 23 )
		
		self.pnlStoreTab.SetSizer( bSizer75 )
		self.pnlStoreTab.Layout()
		bSizer75.Fit( self.pnlStoreTab )
		self.nbBackup.AddPage( self.pnlStoreTab, _("Storage"), False )
		self.pnlScheduleTab = wx.Panel( self.nbBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer66 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1111 = wx.StaticText( self.pnlScheduleTab, wx.ID_ANY, _("Simple Backup Schedule"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1111.Wrap( -1 )
		self.m_staticText1111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer66.Add( self.m_staticText1111, 0, wx.ALL, 3 )
		
		bSizer93 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer951 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.radSchedDailyWeekly = wx.RadioButton( self.pnlScheduleTab, wx.ID_ANY, _("Save changes daily at"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		bSizer951.Add( self.radSchedDailyWeekly, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboTime1Choices = [ _("7:00pm") ]
		self.cboTime1 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboTime1Choices, 0 )
		self.cboTime1.SetSelection( 0 )
		bSizer951.Add( self.cboTime1, 0, wx.ALL, 3 )
		
		self.m_staticText106 = wx.StaticText( self.pnlScheduleTab, wx.ID_ANY, _("Save all weekly on"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText106.Wrap( -1 )
		bSizer951.Add( self.m_staticText106, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboDay1Choices = [ _("Sunday") ]
		self.cboDay1 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboDay1Choices, 0 )
		self.cboDay1.SetSelection( 0 )
		bSizer951.Add( self.cboDay1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer93.Add( bSizer951, 0, wx.EXPAND, 0 )
		
		bSizer9512 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.radSchedDailyMonthly = wx.RadioButton( self.pnlScheduleTab, wx.ID_ANY, _("Save changes daily at"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9512.Add( self.radSchedDailyMonthly, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboTime2Choices = [ _("7:00pm") ]
		self.cboTime2 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboTime2Choices, 0 )
		self.cboTime2.SetSelection( 0 )
		bSizer9512.Add( self.cboTime2, 0, wx.ALL, 3 )
		
		self.m_staticText1062 = wx.StaticText( self.pnlScheduleTab, wx.ID_ANY, _("Save all monthly on"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1062.Wrap( -1 )
		bSizer9512.Add( self.m_staticText1062, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboMonthDay2Choices = [ _("1") ]
		self.cboMonthDay2 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboMonthDay2Choices, 0 )
		self.cboMonthDay2.SetSelection( 0 )
		bSizer9512.Add( self.cboMonthDay2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer93.Add( bSizer9512, 1, wx.EXPAND, 5 )
		
		bSizer9511 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.radSchedHourlyWeekly = wx.RadioButton( self.pnlScheduleTab, wx.ID_ANY, _("Save changes hourly.  Save all weekly on"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9511.Add( self.radSchedHourlyWeekly, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboDay3Choices = [ _("Sunday") ]
		self.cboDay3 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboDay3Choices, 0 )
		self.cboDay3.SetSelection( 0 )
		bSizer9511.Add( self.cboDay3, 0, wx.ALL, 3 )
		
		self.m_staticText1061 = wx.StaticText( self.pnlScheduleTab, wx.ID_ANY, _("at"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1061.Wrap( -1 )
		bSizer9511.Add( self.m_staticText1061, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboTime3Choices = [ _("7:00pm") ]
		self.cboTime3 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboTime3Choices, 0 )
		self.cboTime3.SetSelection( 0 )
		bSizer9511.Add( self.cboTime3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer93.Add( bSizer9511, 0, wx.EXPAND, 0 )
		
		bSizer95112 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.radSchedNoneDaily = wx.RadioButton( self.pnlScheduleTab, wx.ID_ANY, _("Save all daily at"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer95112.Add( self.radSchedNoneDaily, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboTime4Choices = [ _("7:00pm") ]
		self.cboTime4 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboTime4Choices, 0 )
		self.cboTime4.SetSelection( 0 )
		bSizer95112.Add( self.cboTime4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer93.Add( bSizer95112, 1, wx.EXPAND, 5 )
		
		bSizer951121 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.radSchedNoneWeekly = wx.RadioButton( self.pnlScheduleTab, wx.ID_ANY, _("Save all weekly on"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer951121.Add( self.radSchedNoneWeekly, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboDay5Choices = [ _("Sunday") ]
		self.cboDay5 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboDay5Choices, 0 )
		self.cboDay5.SetSelection( 0 )
		bSizer951121.Add( self.cboDay5, 0, wx.ALL, 3 )
		
		self.m_staticText106111 = wx.StaticText( self.pnlScheduleTab, wx.ID_ANY, _("at"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText106111.Wrap( -1 )
		bSizer951121.Add( self.m_staticText106111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboTime5Choices = [ _("7:00pm") ]
		self.cboTime5 = wx.Choice( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboTime5Choices, 0 )
		self.cboTime5.SetSelection( 0 )
		bSizer951121.Add( self.cboTime5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer93.Add( bSizer951121, 1, wx.EXPAND, 5 )
		
		self.m_staticline7 = wx.StaticLine( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer93.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 3 )
		
		bSizer66.Add( bSizer93, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText1121 = wx.StaticText( self.pnlScheduleTab, wx.ID_ANY, _("Advanced Backup Schedule"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1121.Wrap( -1 )
		self.m_staticText1121.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer66.Add( self.m_staticText1121, 0, wx.ALL, 3 )
		
		bSizer95111 = wx.BoxSizer( wx.VERTICAL )
		
		self.radSchedAdvanced = wx.RadioButton( self.pnlScheduleTab, wx.ID_ANY, _("Use Crontab Entries"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer95111.Add( self.radSchedAdvanced, 0, wx.ALL, 3 )
		
		self.pnlAdvanced = wx.Panel( self.pnlScheduleTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer15 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText111 = wx.StaticText( self.pnlAdvanced, wx.ID_ANY, _("Backup Changes:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		fgSizer15.Add( self.m_staticText111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtCronIncr = wx.TextCtrl( self.pnlAdvanced, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer15.Add( self.txtCronIncr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText112 = wx.StaticText( self.pnlAdvanced, wx.ID_ANY, _("Backup Everything:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText112.Wrap( -1 )
		fgSizer15.Add( self.m_staticText112, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtCronFull = wx.TextCtrl( self.pnlAdvanced, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer15.Add( self.txtCronFull, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		
		fgSizer15.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText110 = wx.StaticText( self.pnlAdvanced, wx.ID_ANY, _("Crontab format is \"min hour dayofmonth month dayofweek\"\nFor example: \"30 5 * * *\" runs every day at 5:30 am.\nLeave blank to disable. See help for more details."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText110.Wrap( -1 )
		self.m_staticText110.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer15.Add( self.m_staticText110, 0, wx.ALL, 5 )
		
		self.pnlAdvanced.SetSizer( fgSizer15 )
		self.pnlAdvanced.Layout()
		fgSizer15.Fit( self.pnlAdvanced )
		bSizer95111.Add( self.pnlAdvanced, 1, wx.EXPAND|wx.LEFT, 25 )
		
		bSizer66.Add( bSizer95111, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlScheduleTab.SetSizer( bSizer66 )
		self.pnlScheduleTab.Layout()
		bSizer66.Fit( self.pnlScheduleTab )
		self.nbBackup.AddPage( self.pnlScheduleTab, _("Schedule"), False )
		self.pnlNotification = wx.Panel( self.nbBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer59 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText63 = wx.StaticText( self.pnlNotification, wx.ID_ANY, _("After The Backup Completes"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )
		self.m_staticText63.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer59.Add( self.m_staticText63, 0, wx.ALL, 3 )
		
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		self.chkNotifyMsg = wx.CheckBox( self.pnlNotification, wx.ID_ANY, _("Show a system notification"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer61.Add( self.chkNotifyMsg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkNotifyEmail = wx.CheckBox( self.pnlNotification, wx.ID_ANY, _("Send an email"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer61.Add( self.chkNotifyEmail, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkShutdown = wx.CheckBox( self.pnlNotification, wx.ID_ANY, _("Shutdown the computer"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer61.Add( self.chkShutdown, 0, wx.ALL, 3 )
		
		bSizer59.Add( bSizer61, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlNotification.SetSizer( bSizer59 )
		self.pnlNotification.Layout()
		bSizer59.Fit( self.pnlNotification )
		self.nbBackup.AddPage( self.pnlNotification, _("Notification"), False )
		
		bSizer26.Add( self.nbBackup, 1, wx.EXPAND |wx.ALL, 3 )
		
		bSizer94 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnSave = wx.Button( self.m_panel27, wx.ID_ANY, _("Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer94.Add( self.btnSave, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 3 )
		
		self.btnRevert = wx.Button( self.m_panel27, wx.ID_ANY, _("Revert"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer94.Add( self.btnRevert, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer26.Add( bSizer94, 0, wx.EXPAND, 0 )
		
		self.m_panel27.SetSizer( bSizer26 )
		self.m_panel27.Layout()
		bSizer26.Fit( self.m_panel27 )
		self.m_splitter3.SplitVertically( self.m_panel26, self.m_panel27, 180 )
		bSizer33.Add( self.m_splitter3, 1, wx.EXPAND, 3 )
		
		self.SetSizer( bSizer33 )
		self.Layout()
		
		# Connect Events
		self.lstItems.Bind( wx.EVT_LISTBOX, self.onItemSelected )
		self.btnDelete.Bind( wx.EVT_BUTTON, self.onDelete )
		self.btnNew.Bind( wx.EVT_BUTTON, self.onNew )
		self.btnRun.Bind( wx.EVT_BUTTON, self.onRun )
		self.btnHistory.Bind( wx.EVT_BUTTON, self.onHistory )
		self.btnAddFolder.Bind( wx.EVT_BUTTON, self.onAddFolder )
		self.radSchedDailyWeekly.Bind( wx.EVT_RADIOBUTTON, self.onBackupSchedule )
		self.radSchedDailyMonthly.Bind( wx.EVT_RADIOBUTTON, self.onBackupSchedule )
		self.radSchedHourlyWeekly.Bind( wx.EVT_RADIOBUTTON, self.onBackupSchedule )
		self.radSchedNoneDaily.Bind( wx.EVT_RADIOBUTTON, self.onBackupSchedule )
		self.radSchedNoneWeekly.Bind( wx.EVT_RADIOBUTTON, self.onBackupSchedule )
		self.radSchedAdvanced.Bind( wx.EVT_RADIOBUTTON, self.onBackupSchedule )
		self.chkNotifyMsg.Bind( wx.EVT_CHECKBOX, self.onNotifyMsg )
		self.chkNotifyEmail.Bind( wx.EVT_CHECKBOX, self.onNotifyEmail )
		self.btnSave.Bind( wx.EVT_BUTTON, self.onSave )
		self.btnRevert.Bind( wx.EVT_BUTTON, self.onRevert )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onItemSelected( self, event ):
		event.Skip()
	
	def onDelete( self, event ):
		event.Skip()
	
	def onNew( self, event ):
		event.Skip()
	
	def onRun( self, event ):
		event.Skip()
	
	def onHistory( self, event ):
		event.Skip()
	
	def onAddFolder( self, event ):
		event.Skip()
	
	def onBackupSchedule( self, event ):
		event.Skip()
	
	
	
	
	
	
	def onNotifyMsg( self, event ):
		event.Skip()
	
	def onNotifyEmail( self, event ):
		event.Skip()
	
	def onSave( self, event ):
		event.Skip()
	
	def onRevert( self, event ):
		event.Skip()
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 180 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	

###########################################################################
## Class RunBackupWindow
###########################################################################

class RunBackupWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("Run Backup Window"), pos = wx.DefaultPosition, size = wx.Size( 587,501 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer43 = wx.BoxSizer( wx.VERTICAL )
		
		self.label1 = wx.StaticText( self, wx.ID_ANY, _("Backup"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label1.Wrap( -1 )
		self.label1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer43.Add( self.label1, 0, wx.ALL, 5 )
		
		fgSizer7 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText48 = wx.StaticText( self, wx.ID_ANY, _("Name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText48.Wrap( -1 )
		fgSizer7.Add( self.m_staticText48, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboBackupChoices = []
		self.cboBackup = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboBackupChoices, 0 )
		self.cboBackup.SetSelection( 0 )
		fgSizer7.Add( self.cboBackup, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText45 = wx.StaticText( self, wx.ID_ANY, _("Type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )
		fgSizer7.Add( self.m_staticText45, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer431 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.radFull = wx.RadioButton( self, wx.ID_ANY, _("Full"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer431.Add( self.radFull, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.radIncr = wx.RadioButton( self, wx.ID_ANY, _("Changes"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer431.Add( self.radIncr, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		fgSizer7.Add( bSizer431, 0, wx.EXPAND, 3 )
		
		self.m_staticText91 = wx.StaticText( self, wx.ID_ANY, _("After Finished:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )
		fgSizer7.Add( self.m_staticText91, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer92 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.chkMessage = wx.CheckBox( self, wx.ID_ANY, _("Show message"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.chkMessage, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkEmail = wx.CheckBox( self, wx.ID_ANY, _("Send email"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.chkEmail, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkShutdown = wx.CheckBox( self, wx.ID_ANY, _("Shutdown computer"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.chkShutdown, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		fgSizer7.Add( bSizer92, 1, wx.EXPAND, 5 )
		
		self.m_staticText90 = wx.StaticText( self, wx.ID_ANY, _("Dry Run:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText90.Wrap( -1 )
		fgSizer7.Add( self.m_staticText90, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkDryRun = wx.CheckBox( self, wx.ID_ANY, _("Enable"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer7.Add( self.chkDryRun, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		
		fgSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText107 = wx.StaticText( self, wx.ID_ANY, _("A dry run will execute a backup without actually copying any files\nor changing the system. It shows what *would* happen if this backup ran."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText107.Wrap( -1 )
		self.m_staticText107.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer7.Add( self.m_staticText107, 0, wx.ALL, 5 )
		
		bSizer43.Add( fgSizer7, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlDryRun = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer91 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText46 = wx.StaticText( self.pnlDryRun, wx.ID_ANY, _("List Of Files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )
		self.m_staticText46.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer91.Add( self.m_staticText46, 0, wx.ALL, 5 )
		
		bSizer441 = wx.BoxSizer( wx.VERTICAL )
		
		self.txtFiles = wx.TextCtrl( self.pnlDryRun, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer441.Add( self.txtFiles, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText99 = wx.StaticText( self.pnlDryRun, wx.ID_ANY, _("D = Directory; F = File; X = Deleted"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText99.Wrap( -1 )
		self.m_staticText99.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer441.Add( self.m_staticText99, 0, wx.ALL, 5 )
		
		bSizer91.Add( bSizer441, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlDryRun.SetSizer( bSizer91 )
		self.pnlDryRun.Layout()
		bSizer91.Fit( self.pnlDryRun )
		bSizer43.Add( self.pnlDryRun, 1, wx.EXPAND |wx.ALL, 0 )
		
		bSizer44 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer44.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnStart = wx.Button( self, wx.ID_ANY, _("Start"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer44.Add( self.btnStart, 0, wx.ALL, 3 )
		
		self.btnStop = wx.Button( self, wx.ID_ANY, _("Stop"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer44.Add( self.btnStop, 0, wx.ALL, 3 )
		
		self.btnClose = wx.Button( self, wx.ID_ANY, _("Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer44.Add( self.btnClose, 0, wx.ALL, 3 )
		
		bSizer43.Add( bSizer44, 0, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer43 )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnStart.Bind( wx.EVT_BUTTON, self.onStart )
		self.btnStop.Bind( wx.EVT_BUTTON, self.onStop )
		self.btnClose.Bind( wx.EVT_BUTTON, self.onClose )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onStart( self, event ):
		event.Skip()
	
	def onStop( self, event ):
		event.Skip()
	
	def onClose( self, event ):
		event.Skip()
	

###########################################################################
## Class RestorePanel
###########################################################################

class RestorePanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 517,367 ), style = wx.TAB_TRAVERSAL )
		
		bSizer50 = wx.BoxSizer( wx.VERTICAL )
		
		self.nb_restore = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pnlRestore = wx.Panel( self.nb_restore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer53 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer95 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblTreeTitle = wx.StaticText( self.pnlRestore, wx.ID_ANY, _("File System"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblTreeTitle.Wrap( -1 )
		self.lblTreeTitle.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer95.Add( self.lblTreeTitle, 0, wx.ALL, 3 )
		
		
		bSizer95.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer53.Add( bSizer95, 0, wx.EXPAND, 3 )
		
		self.fs_tree = wx.TreeCtrl( self.pnlRestore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT )
		bSizer53.Add( self.fs_tree, 1, wx.ALL|wx.EXPAND, 3 )
		
		bSizer94 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button40 = wx.Button( self.pnlRestore, wx.ID_ANY, _("Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer94.Add( self.m_button40, 0, wx.ALL, 3 )
		
		self.btnRestore = wx.Button( self.pnlRestore, wx.ID_ANY, _("Restore File/Folder..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer94.Add( self.btnRestore, 0, wx.ALL, 3 )
		
		self.lblSelectedFile = wx.StaticText( self.pnlRestore, wx.ID_ANY, _("<selected file>"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblSelectedFile.Wrap( -1 )
		bSizer94.Add( self.lblSelectedFile, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer53.Add( bSizer94, 0, wx.EXPAND, 3 )
		
		bSizer51.Add( bSizer53, 1, wx.EXPAND, 3 )
		
		bSizer52 = wx.BoxSizer( wx.VERTICAL )
		
		self.date_label = wx.StaticText( self.pnlRestore, wx.ID_ANY, _("Selected Date"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.date_label.Wrap( -1 )
		bSizer52.Add( self.date_label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 0 )
		
		self.time_label = wx.StaticText( self.pnlRestore, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.time_label.Wrap( -1 )
		bSizer52.Add( self.time_label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 0 )
		
		self.m_staticline3 = wx.StaticLine( self.pnlRestore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer52.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self.pnlRestore, wx.ID_ANY, _("Oldest"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		self.m_staticText56.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer52.Add( self.m_staticText56, 0, wx.ALIGN_CENTER_HORIZONTAL, 3 )
		
		self.date_slider = wx.Slider( self.pnlRestore, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_VERTICAL )
		bSizer52.Add( self.date_slider, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText55 = wx.StaticText( self.pnlRestore, wx.ID_ANY, _("Latest"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText55.Wrap( -1 )
		self.m_staticText55.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer52.Add( self.m_staticText55, 0, wx.ALIGN_CENTER_HORIZONTAL, 3 )
		
		self.m_staticline4 = wx.StaticLine( self.pnlRestore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer52.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.btnRunDetails = wx.Button( self.pnlRestore, wx.ID_ANY, _("Run Details"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer52.Add( self.btnRunDetails, 0, wx.ALL, 5 )
		
		bSizer51.Add( bSizer52, 0, wx.EXPAND, 3 )
		
		self.pnlRestore.SetSizer( bSizer51 )
		self.pnlRestore.Layout()
		bSizer51.Fit( self.pnlRestore )
		self.nb_restore.AddPage( self.pnlRestore, _("Restore Files/Folders"), True )
		self.pnlRecovery = wx.Panel( self.nb_restore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer93 = wx.BoxSizer( wx.VERTICAL )
		
		self.lblTreeTitle1 = wx.StaticText( self.pnlRecovery, wx.ID_ANY, _("Method 1: Rebuild Local Database"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblTreeTitle1.Wrap( -1 )
		self.lblTreeTitle1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer93.Add( self.lblTreeTitle1, 0, wx.ALL, 3 )
		
		bSizer931 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText104 = wx.StaticText( self.pnlRecovery, wx.ID_ANY, _("Step 1: Retrieve a copy of the backup configuration from *any* recently used store."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText104.Wrap( -1 )
		self.m_staticText104.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer931.Add( self.m_staticText104, 0, wx.ALL, 3 )
		
		self.btnReload = wx.Button( self.pnlRecovery, wx.ID_ANY, _("Step 1: Fetch Configuration"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer931.Add( self.btnReload, 0, wx.ALL, 3 )
		
		self.m_staticline9 = wx.StaticLine( self.pnlRecovery, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer931.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.m_staticText94 = wx.StaticText( self.pnlRecovery, wx.ID_ANY, _("Step 2: Once the configuration has been fetched, The Vault can rebuild a complete\ncopy of the backup database, which includes information about all backed up files."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText94.Wrap( -1 )
		self.m_staticText94.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer931.Add( self.m_staticText94, 0, wx.ALL, 3 )
		
		self.btnRebuild = wx.Button( self.pnlRecovery, wx.ID_ANY, _("Step 2: Rebuild Database"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer931.Add( self.btnRebuild, 0, wx.ALL, 3 )
		
		self.m_staticline10 = wx.StaticLine( self.pnlRecovery, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer931.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.m_staticText941 = wx.StaticText( self.pnlRecovery, wx.ID_ANY, _("Step 3: Use the \"Restore Flies/Folders\" tab to recover your files and folders."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText941.Wrap( -1 )
		self.m_staticText941.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer931.Add( self.m_staticText941, 0, wx.ALL, 3 )
		
		self.btnRestoreTab = wx.Button( self.pnlRecovery, wx.ID_ANY, _("Step 3: Switch To Restore Tab"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer931.Add( self.btnRestoreTab, 0, wx.ALL, 3 )
		
		bSizer93.Add( bSizer931, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.lblTreeTitle11 = wx.StaticText( self.pnlRecovery, wx.ID_ANY, _("Method 2: Run Recover Application"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblTreeTitle11.Wrap( -1 )
		self.lblTreeTitle11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer93.Add( self.lblTreeTitle11, 0, wx.ALL, 3 )
		
		bSizer9311 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText901 = wx.StaticText( self.pnlRecovery, wx.ID_ANY, _("Every store has an emergency recovery application inside its root folder. \nRun that program (recover.py) to restore all backup data from that store. \nThis is better suited to local stores (e.g. USB drives) that can be easily mounted."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText901.Wrap( -1 )
		self.m_staticText901.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer9311.Add( self.m_staticText901, 0, wx.ALL, 3 )
		
		bSizer93.Add( bSizer9311, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlRecovery.SetSizer( bSizer93 )
		self.pnlRecovery.Layout()
		bSizer93.Fit( self.pnlRecovery )
		self.nb_restore.AddPage( self.pnlRecovery, _("Disaster Recovery"), False )
		self.pnlPackages = wx.Panel( self.nb_restore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer951 = wx.BoxSizer( wx.VERTICAL )
		
		self.lblTreeTitle12 = wx.StaticText( self.pnlPackages, wx.ID_ANY, _("Restore All Packages/Software"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblTreeTitle12.Wrap( -1 )
		self.lblTreeTitle12.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer951.Add( self.lblTreeTitle12, 0, wx.ALL, 5 )
		
		bSizer9312 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1041 = wx.StaticText( self.pnlPackages, wx.ID_ANY, _("If one of your backups includes \"Backup Packages\", then\nthe vault can automatically restore all software (packages)\nin one go.\n\nPlease choose a Backup to fetch the package list from."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1041.Wrap( -1 )
		self.m_staticText1041.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer9312.Add( self.m_staticText1041, 0, wx.ALL, 3 )
		
		bSizer99 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText120 = wx.StaticText( self.pnlPackages, wx.ID_ANY, _("Backup:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText120.Wrap( -1 )
		bSizer99.Add( self.m_staticText120, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboBackupChoices = [ _("asdf"), _("asdfasdf") ]
		self.cboBackup = wx.Choice( self.pnlPackages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboBackupChoices, 0 )
		self.cboBackup.SetSelection( 0 )
		self.cboBackup.SetMinSize( wx.Size( 150,-1 ) )
		
		bSizer99.Add( self.cboBackup, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer9312.Add( bSizer99, 0, wx.EXPAND, 3 )
		
		self.m_staticline91 = wx.StaticLine( self.pnlPackages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer9312.Add( self.m_staticline91, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText942 = wx.StaticText( self.pnlPackages, wx.ID_ANY, _("Click the \"Show Missing Packages\" button to fetch the backed\nup package list and to compare it will the currently installed list."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText942.Wrap( -1 )
		self.m_staticText942.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer9312.Add( self.m_staticText942, 0, wx.ALL, 3 )
		
		self.btnShowPackages = wx.Button( self.pnlPackages, wx.ID_ANY, _("Show Missing Packages"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9312.Add( self.btnShowPackages, 0, wx.ALL, 3 )
		
		bSizer951.Add( bSizer9312, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlPackages.SetSizer( bSizer951 )
		self.pnlPackages.Layout()
		bSizer951.Fit( self.pnlPackages )
		self.nb_restore.AddPage( self.pnlPackages, _("Restore Packages"), False )
		
		bSizer50.Add( self.nb_restore, 1, wx.EXPAND |wx.ALL, 3 )
		
		self.SetSizer( bSizer50 )
		self.Layout()
		
		# Connect Events
		self.fs_tree.Bind( wx.EVT_TREE_ITEM_EXPANDING, self.onTreeItemExpanding )
		self.fs_tree.Bind( wx.EVT_TREE_SEL_CHANGED, self.onTreeSelChanged )
		self.m_button40.Bind( wx.EVT_BUTTON, self.onRefresh )
		self.btnRestore.Bind( wx.EVT_BUTTON, self.onRestore )
		self.date_slider.Bind( wx.EVT_SCROLL, self.onSliderScroll )
		self.btnRunDetails.Bind( wx.EVT_BUTTON, self.onRunDetails )
		self.btnReload.Bind( wx.EVT_BUTTON, self.onReload )
		self.btnRebuild.Bind( wx.EVT_BUTTON, self.onRebuild )
		self.btnRestoreTab.Bind( wx.EVT_BUTTON, self.onRestoreTab )
		self.btnShowPackages.Bind( wx.EVT_BUTTON, self.onShowPackages )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onTreeItemExpanding( self, event ):
		event.Skip()
	
	def onTreeSelChanged( self, event ):
		event.Skip()
	
	def onRefresh( self, event ):
		event.Skip()
	
	def onRestore( self, event ):
		event.Skip()
	
	def onSliderScroll( self, event ):
		event.Skip()
	
	def onRunDetails( self, event ):
		event.Skip()
	
	def onReload( self, event ):
		event.Skip()
	
	def onRebuild( self, event ):
		event.Skip()
	
	def onRestoreTab( self, event ):
		event.Skip()
	
	def onShowPackages( self, event ):
		event.Skip()
	

###########################################################################
## Class RunRestoreWindow
###########################################################################

class RunRestoreWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("Restore Files"), pos = wx.DefaultPosition, size = wx.Size( 497,307 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer81 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText84 = wx.StaticText( self, wx.ID_ANY, _("Folders"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText84.Wrap( -1 )
		self.m_staticText84.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer81.Add( self.m_staticText84, 0, wx.ALL, 5 )
		
		fgSizer13 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer13.AddGrowableCol( 1 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText86 = wx.StaticText( self, wx.ID_ANY, _("File/Folder To Restore:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText86.Wrap( -1 )
		fgSizer13.Add( self.m_staticText86, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtSource = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer13.Add( self.txtSource, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText861 = wx.StaticText( self, wx.ID_ANY, _("Destination Folder:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText861.Wrap( -1 )
		fgSizer13.Add( self.m_staticText861, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.cboDest = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _("Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		fgSizer13.Add( self.cboDest, 0, wx.ALL, 3 )
		
		bSizer81.Add( fgSizer13, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText90 = wx.StaticText( self, wx.ID_ANY, _("Options:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText90.Wrap( -1 )
		self.m_staticText90.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer81.Add( self.m_staticText90, 0, wx.ALL, 5 )
		
		bSizer82 = wx.BoxSizer( wx.VERTICAL )
		
		self.chkNoRecurse = wx.CheckBox( self, wx.ID_ANY, _("Do not restore sub-folders"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.chkNoRecurse, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkNotify = wx.CheckBox( self, wx.ID_ANY, _("Notify me by desktop message when complete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.chkNotify, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkEmail = wx.CheckBox( self, wx.ID_ANY, _("Notify me by email when complete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.chkEmail, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkShutdown = wx.CheckBox( self, wx.ID_ANY, _("Shutdown the computer afterwards"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.chkShutdown, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer81.Add( bSizer82, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.btnStart = wx.Button( self, wx.ID_ANY, _("Start"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.btnStart, 0, wx.ALL, 5 )
		
		self.SetSizer( bSizer81 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnStart.Bind( wx.EVT_BUTTON, self.onStart )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onStart( self, event ):
		event.Skip()
	

###########################################################################
## Class RunDetailsWindow
###########################################################################

class RunDetailsWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("Backup Run Details"), pos = wx.DefaultPosition, size = wx.Size( 604,467 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer54 = wx.BoxSizer( wx.VERTICAL )
		
		self.nbDetails = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pnlOverview = wx.Panel( self.nbDetails, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		self.lstDetails = wx.ListCtrl( self.pnlOverview, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_NO_HEADER|wx.LC_REPORT )
		bSizer61.Add( self.lstDetails, 1, wx.ALL|wx.EXPAND, 20 )
		
		self.pnlOverview.SetSizer( bSizer61 )
		self.pnlOverview.Layout()
		bSizer61.Fit( self.pnlOverview )
		self.nbDetails.AddPage( self.pnlOverview, _("Overview"), False )
		self.pnlFiles = wx.Panel( self.nbDetails, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer58 = wx.BoxSizer( wx.VERTICAL )
		
		self.lstFiles = wx.ListCtrl( self.pnlFiles, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer58.Add( self.lstFiles, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.pnlAllFiles = wx.Panel( self.pnlFiles, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer581 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText62 = wx.StaticText( self.pnlAllFiles, wx.ID_ANY, _("Only the first 200 files are shown because displaying\nthe full list could take a while.  Do you want to see\nall the files?"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		bSizer581.Add( self.m_staticText62, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		
		bSizer581.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnAllFiles = wx.Button( self.pnlAllFiles, wx.ID_ANY, _("Display All Files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer581.Add( self.btnAllFiles, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.pnlAllFiles.SetSizer( bSizer581 )
		self.pnlAllFiles.Layout()
		bSizer581.Fit( self.pnlAllFiles )
		bSizer58.Add( self.pnlAllFiles, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.pnlFiles.SetSizer( bSizer58 )
		self.pnlFiles.Layout()
		bSizer58.Fit( self.pnlFiles )
		self.nbDetails.AddPage( self.pnlFiles, _("Files"), True )
		self.pnlMessages = wx.Panel( self.nbDetails, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer59 = wx.BoxSizer( wx.VERTICAL )
		
		self.lstMessages = wx.ListCtrl( self.pnlMessages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer59.Add( self.lstMessages, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.pnlMessages.SetSizer( bSizer59 )
		self.pnlMessages.Layout()
		bSizer59.Fit( self.pnlMessages )
		self.nbDetails.AddPage( self.pnlMessages, _("Messages"), False )
		
		bSizer54.Add( self.nbDetails, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer54 )
		self.Layout()
		self.m_statusBar4 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnAllFiles.Bind( wx.EVT_BUTTON, self.onAllFiles )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onAllFiles( self, event ):
		event.Skip()
	

###########################################################################
## Class StoragePanel
###########################################################################

class StoragePanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 718,507 ), style = wx.TAB_TRAVERSAL )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 180 )
		
		self.pnlList = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText21 = wx.StaticText( self.pnlList, wx.ID_ANY, _("Storage"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetFont( wx.Font( 11, 74, 90, 92, False, "Sans" ) )
		
		bSizer21.Add( self.m_staticText21, 0, wx.ALL, 3 )
		
		lstItemsChoices = []
		self.lstItems = wx.ListBox( self.pnlList, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,150 ), lstItemsChoices, wx.LB_SORT )
		bSizer21.Add( self.lstItems, 0, wx.ALL|wx.EXPAND, 3 )
		
		gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.btnDelete = wx.Button( self.pnlList, wx.ID_ANY, _("Delete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnDelete, 0, wx.ALL, 3 )
		
		self.btnNew = wx.Button( self.pnlList, wx.ID_ANY, _("Add New"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnNew, 0, wx.ALIGN_RIGHT|wx.ALL, 3 )
		
		self.btnTest = wx.Button( self.pnlList, wx.ID_ANY, _("Test"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnTest, 0, wx.ALL, 3 )
		
		bSizer21.Add( gSizer3, 0, wx.EXPAND, 3 )
		
		self.pnlList.SetSizer( bSizer21 )
		self.pnlList.Layout()
		bSizer21.Fit( self.pnlList )
		self.pnlDetails = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText43 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("General"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )
		self.m_staticText43.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer26.Add( self.m_staticText43, 0, wx.ALL, 3 )
		
		fgSizer6 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer6.AddGrowableCol( 1 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText24 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Name:"), wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText24.Wrap( -1 )
		fgSizer6.Add( self.m_staticText24, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.pnlName = wx.Panel( self.pnlDetails, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer85 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtName = wx.TextCtrl( self.pnlName, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer85.Add( self.txtName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		self.lblName = wx.StaticText( self.pnlName, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblName.Wrap( -1 )
		bSizer85.Add( self.lblName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		self.pnlName.SetSizer( bSizer85 )
		self.pnlName.Layout()
		bSizer85.Fit( self.pnlName )
		fgSizer6.Add( self.pnlName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 0 )
		
		bSizer26.Add( fgSizer6, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText42 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Storage Space"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		self.m_staticText42.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer26.Add( self.m_staticText42, 0, wx.ALL, 3 )
		
		fgSizer1111 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer1111.AddGrowableCol( 1 )
		fgSizer1111.SetFlexibleDirection( wx.BOTH )
		fgSizer1111.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )
		
		self.m_staticText5711 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Auto Manage:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5711.Wrap( -1 )
		fgSizer1111.Add( self.m_staticText5711, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.chkAutoManage = wx.CheckBox( self.pnlDetails, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.chkAutoManage, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText53 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Limit to:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText53.Wrap( -1 )
		bSizer41.Add( self.m_staticText53, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtLimitSize = wx.TextCtrl( self.pnlDetails, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		bSizer41.Add( self.txtLimitSize, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboLimitUnitsChoices = []
		self.cboLimitUnits = wx.Choice( self.pnlDetails, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboLimitUnitsChoices, 0 )
		self.cboLimitUnits.SetSelection( 0 )
		bSizer41.Add( self.cboLimitUnits, 0, wx.ALL, 3 )
		
		fgSizer1111.Add( bSizer41, 1, wx.EXPAND, 3 )
		
		
		fgSizer1111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 3 )
		
		self.m_staticText47 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("If selected, old backups will automatically be\nremoved as required, and the total space used\nrestricted to the limit."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		self.m_staticText47.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer1111.Add( self.m_staticText47, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText111 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Contents:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		fgSizer1111.Add( self.m_staticText111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.lblContentDetails = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("not available"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblContentDetails.Wrap( -1 )
		self.lblContentDetails.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer1111.Add( self.lblContentDetails, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer26.Add( fgSizer1111, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.txtStoreTypeName = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Storage Connection"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtStoreTypeName.Wrap( -1 )
		self.txtStoreTypeName.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer26.Add( self.txtStoreTypeName, 0, wx.ALL, 3 )
		
		self.nbStoreType = wx.Choicebook( self.pnlDetails, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
		self.pnlFolder = wx.Panel( self.nbStoreType, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer78 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText51 = wx.StaticText( self.pnlFolder, wx.ID_ANY, _("Local Folder Details"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		self.m_staticText51.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer78.Add( self.m_staticText51, 0, wx.ALL, 3 )
		
		fgSizer16 = wx.FlexGridSizer( 2, 3, 0, 0 )
		fgSizer16.AddGrowableCol( 1 )
		fgSizer16.SetFlexibleDirection( wx.BOTH )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText109 = wx.StaticText( self.pnlFolder, wx.ID_ANY, _("Path:"), wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText109.Wrap( -1 )
		fgSizer16.Add( self.m_staticText109, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtFolderPath = wx.TextCtrl( self.pnlFolder, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer16.Add( self.txtFolderPath, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.btnFolderChoose = wx.Button( self.pnlFolder, wx.ID_ANY, _("Choose..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer16.Add( self.btnFolderChoose, 0, wx.ALL, 3 )
		
		bSizer78.Add( fgSizer16, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlFolder.SetSizer( bSizer78 )
		self.pnlFolder.Layout()
		bSizer78.Fit( self.pnlFolder )
		self.nbStoreType.AddPage( self.pnlFolder, _("Local Folder"), False )
		self.pnlFTP = wx.Panel( self.nbStoreType, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer781 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText511 = wx.StaticText( self.pnlFTP, wx.ID_ANY, _("FTP Server Details"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511.Wrap( -1 )
		self.m_staticText511.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer781.Add( self.m_staticText511, 0, wx.ALL, 3 )
		
		fgSizer11 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer11.AddGrowableCol( 1 )
		fgSizer11.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText57 = wx.StaticText( self.pnlFTP, wx.ID_ANY, _("Server Address:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText57.Wrap( -1 )
		fgSizer11.Add( self.m_staticText57, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtFTPAddress = wx.TextCtrl( self.pnlFTP, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer11.Add( self.txtFTPAddress, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.lblRoot = wx.StaticText( self.pnlFTP, wx.ID_ANY, _("Root Folder:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblRoot.Wrap( -1 )
		fgSizer11.Add( self.lblRoot, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtFTPRoot = wx.TextCtrl( self.pnlFTP, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer11.Add( self.txtFTPRoot, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText58 = wx.StaticText( self.pnlFTP, wx.ID_ANY, _("Use SFTP:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText58.Wrap( -1 )
		fgSizer11.Add( self.m_staticText58, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkSFTP = wx.CheckBox( self.pnlFTP, wx.ID_ANY, _("(Encryption. Strongly recommended)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chkSFTP.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.chkSFTP, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText59 = wx.StaticText( self.pnlFTP, wx.ID_ANY, _("Login ID:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText59.Wrap( -1 )
		fgSizer11.Add( self.m_staticText59, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtFTPLogin = wx.TextCtrl( self.pnlFTP, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer11.Add( self.txtFTPLogin, 0, wx.ALL, 3 )
		
		self.m_staticText60 = wx.StaticText( self.pnlFTP, wx.ID_ANY, _("Password:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText60.Wrap( -1 )
		fgSizer11.Add( self.m_staticText60, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtFTPPass = wx.TextCtrl( self.pnlFTP, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_PASSWORD )
		bSizer111.Add( self.txtFTPPass, 0, wx.ALL, 3 )
		
		self.btnFTPHidePassword = wx.Button( self.pnlFTP, wx.ID_ANY, _("Show"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.btnFTPHidePassword, 0, wx.ALL, 3 )
		
		fgSizer11.Add( bSizer111, 1, wx.EXPAND, 5 )
		
		bSizer781.Add( fgSizer11, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlFTP.SetSizer( bSizer781 )
		self.pnlFTP.Layout()
		bSizer781.Fit( self.pnlFTP )
		self.nbStoreType.AddPage( self.pnlFTP, _("FTP Server"), False )
		self.pnlShare = wx.Panel( self.nbStoreType, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7811 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText5111 = wx.StaticText( self.pnlShare, wx.ID_ANY, _("Server Share"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5111.Wrap( -1 )
		self.m_staticText5111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer7811.Add( self.m_staticText5111, 0, wx.ALL, 3 )
		
		fgSizer111 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer111.AddGrowableCol( 1 )
		fgSizer111.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer111.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText571 = wx.StaticText( self.pnlShare, wx.ID_ANY, _("Local Path:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText571.Wrap( -1 )
		fgSizer111.Add( self.m_staticText571, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtShareRoot = wx.TextCtrl( self.pnlShare, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.txtShareRoot, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.btnShareChoose = wx.Button( self.pnlShare, wx.ID_ANY, _("Choose..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.btnShareChoose, 0, wx.ALL, 3 )
		
		fgSizer111.Add( bSizer101, 1, wx.EXPAND, 5 )
		
		self.m_staticText591 = wx.StaticText( self.pnlShare, wx.ID_ANY, _("Mount Cmd:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText591.Wrap( -1 )
		fgSizer111.Add( self.m_staticText591, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtShareMount = wx.TextCtrl( self.pnlShare, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer111.Add( self.txtShareMount, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText71 = wx.StaticText( self.pnlShare, wx.ID_ANY, _("Unmount Cmd:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		fgSizer111.Add( self.m_staticText71, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtShareUMount = wx.TextCtrl( self.pnlShare, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer111.Add( self.txtShareUMount, 0, wx.ALL|wx.EXPAND, 3 )
		
		bSizer7811.Add( fgSizer111, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlShare.SetSizer( bSizer7811 )
		self.pnlShare.Layout()
		bSizer7811.Fit( self.pnlShare )
		self.nbStoreType.AddPage( self.pnlShare, _("Server Share"), False )
		self.pnlDropBox = wx.Panel( self.nbStoreType, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7812 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText5112 = wx.StaticText( self.pnlDropBox, wx.ID_ANY, _("DropBox Details"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5112.Wrap( -1 )
		self.m_staticText5112.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer7812.Add( self.m_staticText5112, 0, wx.ALL, 3 )
		
		fgSizer112 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer112.AddGrowableCol( 1 )
		fgSizer112.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer112.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText592 = wx.StaticText( self.pnlDropBox, wx.ID_ANY, _("Login ID:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText592.Wrap( -1 )
		fgSizer112.Add( self.m_staticText592, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtDBLogin = wx.TextCtrl( self.pnlDropBox, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer112.Add( self.txtDBLogin, 0, wx.ALL, 3 )
		
		self.m_staticText601 = wx.StaticText( self.pnlDropBox, wx.ID_ANY, _("Password:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText601.Wrap( -1 )
		fgSizer112.Add( self.m_staticText601, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer110 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtDBPass = wx.TextCtrl( self.pnlDropBox, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_PASSWORD )
		bSizer110.Add( self.txtDBPass, 0, wx.ALL, 3 )
		
		self.btnDBHidePassword = wx.Button( self.pnlDropBox, wx.ID_ANY, _("Show"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer110.Add( self.btnDBHidePassword, 0, wx.ALL, 3 )
		
		fgSizer112.Add( bSizer110, 1, wx.EXPAND, 0 )
		
		self.lblRoot1 = wx.StaticText( self.pnlDropBox, wx.ID_ANY, _("Root Folder:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblRoot1.Wrap( -1 )
		fgSizer112.Add( self.lblRoot1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtDBRoot = wx.TextCtrl( self.pnlDropBox, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer112.Add( self.txtDBRoot, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText130 = wx.StaticText( self.pnlDropBox, wx.ID_ANY, _("Application Key:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText130.Wrap( -1 )
		fgSizer112.Add( self.m_staticText130, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtDBKey = wx.TextCtrl( self.pnlDropBox, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer112.Add( self.txtDBKey, 0, wx.ALL, 3 )
		
		self.m_staticText131 = wx.StaticText( self.pnlDropBox, wx.ID_ANY, _("Application Secret Key:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )
		fgSizer112.Add( self.m_staticText131, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtDBSecretKey = wx.TextCtrl( self.pnlDropBox, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer112.Add( self.txtDBSecretKey, 0, wx.ALL, 3 )
		
		
		fgSizer112.AddSpacer( ( 0, 0), 1, wx.EXPAND, 3 )
		
		bSizer94 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.url_dropbox_create = wx.HyperlinkCtrl( self.pnlDropBox, wx.ID_ANY, _("Click to create an account"), u"https://www.dropbox.com/register", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer94.Add( self.url_dropbox_create, 0, wx.ALL, 3 )
		
		self.m_staticText118 = wx.StaticText( self.pnlDropBox, wx.ID_ANY, _("(its free!)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText118.Wrap( -1 )
		bSizer94.Add( self.m_staticText118, 0, wx.ALL, 3 )
		
		fgSizer112.Add( bSizer94, 1, wx.EXPAND, 0 )
		
		bSizer7812.Add( fgSizer112, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlDropBox.SetSizer( bSizer7812 )
		self.pnlDropBox.Layout()
		bSizer7812.Fit( self.pnlDropBox )
		self.nbStoreType.AddPage( self.pnlDropBox, _("DropBox"), False )
		self.m_panel32 = wx.Panel( self.nbStoreType, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer78121 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText51121 = wx.StaticText( self.m_panel32, wx.ID_ANY, _("Amazon S3 Details"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51121.Wrap( -1 )
		self.m_staticText51121.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer78121.Add( self.m_staticText51121, 0, wx.ALL, 3 )
		
		fgSizer1121 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer1121.AddGrowableCol( 1 )
		fgSizer1121.SetFlexibleDirection( wx.BOTH )
		fgSizer1121.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5921 = wx.StaticText( self.m_panel32, wx.ID_ANY, _("Access Key ID:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5921.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText5921, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtAmazonKey = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		fgSizer1121.Add( self.txtAmazonKey, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText6011 = wx.StaticText( self.m_panel32, wx.ID_ANY, _("Secret Access Key ID:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6011.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText6011, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtAmazonSecretKey = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		fgSizer1121.Add( self.txtAmazonSecretKey, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.lblRoot11 = wx.StaticText( self.m_panel32, wx.ID_ANY, _("Bucket Name:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblRoot11.Wrap( -1 )
		fgSizer1121.Add( self.lblRoot11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtAmazonBucket = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.txtAmazonBucket, 0, wx.ALL|wx.EXPAND, 3 )
		
		
		fgSizer1121.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText134 = wx.StaticText( self.m_panel32, wx.ID_ANY, _("The bucket is a unique identifier for a set of data stored\non Amazon S3. It must be unique world wide. We suggest\nusing \"vault.your.email.address\". For example: \n    vault.myname.mailserver.com\n(note: '@' is not permitted in bucket names)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText134.Wrap( -1 )
		self.m_staticText134.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer1121.Add( self.m_staticText134, 0, wx.ALL, 5 )
		
		
		fgSizer1121.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer941 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.url_amazon_create = wx.HyperlinkCtrl( self.m_panel32, wx.ID_ANY, _("Click to create an account"), u"http://aws.amazon.com", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer941.Add( self.url_amazon_create, 0, wx.ALL, 3 )
		
		self.m_staticText1181 = wx.StaticText( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1181.Wrap( -1 )
		bSizer941.Add( self.m_staticText1181, 0, wx.ALL, 3 )
		
		fgSizer1121.Add( bSizer941, 1, wx.EXPAND, 5 )
		
		bSizer78121.Add( fgSizer1121, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_panel32.SetSizer( bSizer78121 )
		self.m_panel32.Layout()
		bSizer78121.Fit( self.m_panel32 )
		self.nbStoreType.AddPage( self.m_panel32, _("Amazon S3"), True )
		bSizer26.Add( self.nbStoreType, 0, wx.EXPAND|wx.LEFT, 20 )
		
		bSizer82 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnSave = wx.Button( self.pnlDetails, wx.ID_ANY, _("Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.btnSave, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.btnRevert = wx.Button( self.pnlDetails, wx.ID_ANY, _("Revert"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.btnRevert, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		
		bSizer82.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer26.Add( bSizer82, 0, wx.EXPAND, 3 )
		
		self.pnlDetails.SetSizer( bSizer26 )
		self.pnlDetails.Layout()
		bSizer26.Fit( self.pnlDetails )
		self.m_splitter2.SplitVertically( self.pnlList, self.pnlDetails, 180 )
		bSizer20.Add( self.m_splitter2, 1, wx.EXPAND, 3 )
		
		self.SetSizer( bSizer20 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_ENTER_WINDOW, self.onEnter )
		self.Bind( wx.EVT_KILL_FOCUS, self.onKillFocus )
		self.Bind( wx.EVT_LEAVE_WINDOW, self.onLeave )
		self.Bind( wx.EVT_SET_FOCUS, self.onSetFocus )
		self.lstItems.Bind( wx.EVT_LISTBOX, self.onItemSelected )
		self.btnDelete.Bind( wx.EVT_BUTTON, self.onDelete )
		self.btnNew.Bind( wx.EVT_BUTTON, self.onNew )
		self.btnTest.Bind( wx.EVT_BUTTON, self.onTest )
		self.chkAutoManage.Bind( wx.EVT_CHECKBOX, self.onAutoManage )
		self.txtLimitSize.Bind( wx.EVT_CHAR, self.onLimitChar )
		self.txtLimitSize.Bind( wx.EVT_KEY_UP, self.onLimitKey )
		self.btnFolderChoose.Bind( wx.EVT_BUTTON, self.onFolderChoose )
		self.btnFTPHidePassword.Bind( wx.EVT_BUTTON, self.onFTPHidePassword )
		self.btnShareChoose.Bind( wx.EVT_BUTTON, self.onShareChoose )
		self.btnDBHidePassword.Bind( wx.EVT_BUTTON, self.onDBHidePassword )
		self.url_dropbox_create.Bind( wx.EVT_HYPERLINK, self.onDropBoxClick )
		self.url_amazon_create.Bind( wx.EVT_HYPERLINK, self.onDropBoxClick )
		self.btnSave.Bind( wx.EVT_BUTTON, self.onSave )
		self.btnRevert.Bind( wx.EVT_BUTTON, self.onRevert )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onEnter( self, event ):
		event.Skip()
	
	def onKillFocus( self, event ):
		event.Skip()
	
	def onLeave( self, event ):
		event.Skip()
	
	def onSetFocus( self, event ):
		event.Skip()
	
	def onItemSelected( self, event ):
		event.Skip()
	
	def onDelete( self, event ):
		event.Skip()
	
	def onNew( self, event ):
		event.Skip()
	
	def onTest( self, event ):
		event.Skip()
	
	def onAutoManage( self, event ):
		event.Skip()
	
	def onLimitChar( self, event ):
		event.Skip()
	
	def onLimitKey( self, event ):
		event.Skip()
	
	def onFolderChoose( self, event ):
		event.Skip()
	
	def onFTPHidePassword( self, event ):
		event.Skip()
	
	def onShareChoose( self, event ):
		event.Skip()
	
	def onDBHidePassword( self, event ):
		event.Skip()
	
	def onDropBoxClick( self, event ):
		event.Skip()
	
	
	def onSave( self, event ):
		event.Skip()
	
	def onRevert( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 180 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

###########################################################################
## Class ConfigPanel
###########################################################################

class ConfigPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 531,478 ), style = wx.TAB_TRAVERSAL )
		
		bSizer74 = wx.BoxSizer( wx.VERTICAL )
		
		self.nb_config = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pnlSecurity = wx.Panel( self.nb_config, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer95 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText961 = wx.StaticText( self.pnlSecurity, wx.ID_ANY, _("Encryption:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText961.Wrap( -1 )
		self.m_staticText961.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer95.Add( self.m_staticText961, 0, wx.ALL, 5 )
		
		bSizer107 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer142 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer142.SetFlexibleDirection( wx.BOTH )
		fgSizer142.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText931 = wx.StaticText( self.pnlSecurity, wx.ID_ANY, _("Master Password:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText931.Wrap( -1 )
		fgSizer142.Add( self.m_staticText931, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer109 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtMasterPassword = wx.TextCtrl( self.pnlSecurity, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		self.txtMasterPassword.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer109.Add( self.txtMasterPassword, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.btnHidePassword = wx.Button( self.pnlSecurity, wx.ID_ANY, _("Show"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer109.Add( self.btnHidePassword, 0, wx.ALL, 5 )
		
		fgSizer142.Add( bSizer109, 1, wx.EXPAND, 5 )
		
		
		fgSizer142.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer103 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText132 = wx.StaticText( self.pnlSecurity, wx.ID_ANY, _("Strength:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText132.Wrap( -1 )
		bSizer103.Add( self.m_staticText132, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.strength = wx.Gauge( self.pnlSecurity, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,10 ), wx.GA_HORIZONTAL|wx.GA_SMOOTH )
		bSizer103.Add( self.strength, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		fgSizer142.Add( bSizer103, 1, wx.EXPAND, 5 )
		
		
		fgSizer142.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText134 = wx.StaticText( self.pnlSecurity, wx.ID_ANY, _("This master password is used to encrypt all remotely\nstored backup data, *if* you enable data encryption.\n\nWhatever you do... remember this password.\n\nWarning: If you change the master password, then\nall existing backup data will need to be deleted\n(i.e. you need to restart your backups)."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText134.Wrap( -1 )
		self.m_staticText134.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer142.Add( self.m_staticText134, 0, wx.ALL, 5 )
		
		
		fgSizer142.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnSavePassword = wx.Button( self.pnlSecurity, wx.ID_ANY, _("Save Change"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer142.Add( self.btnSavePassword, 0, wx.ALL, 3 )
		
		bSizer107.Add( fgSizer142, 1, wx.EXPAND, 5 )
		
		bSizer95.Add( bSizer107, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlSecurity.SetSizer( bSizer95 )
		self.pnlSecurity.Layout()
		bSizer95.Fit( self.pnlSecurity )
		self.nb_config.AddPage( self.pnlSecurity, _("Security"), True )
		self.pnlEmail = wx.Panel( self.nb_config, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer841 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText92 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Email Server"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92.Wrap( -1 )
		self.m_staticText92.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer841.Add( self.m_staticText92, 0, wx.ALL, 3 )
		
		bSizer75 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer14 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText93 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Mail Server:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )
		fgSizer14.Add( self.m_staticText93, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer85 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtMailServer = wx.TextCtrl( self.pnlEmail, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtMailServer.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer85.Add( self.txtMailServer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText103 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Port:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText103.Wrap( -1 )
		bSizer85.Add( self.m_staticText103, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtMailPort = wx.TextCtrl( self.pnlEmail, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer85.Add( self.txtMailPort, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		fgSizer14.Add( bSizer85, 1, wx.EXPAND, 5 )
		
		self.m_staticText104 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Use SSL:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText104.Wrap( -1 )
		fgSizer14.Add( self.m_staticText104, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.chkMailSSL = wx.CheckBox( self.pnlEmail, wx.ID_ANY, _("(Encryption. Strongly recommended)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chkMailSSL.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer14.Add( self.chkMailSSL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer75.Add( fgSizer14, 0, wx.EXPAND, 3 )
		
		bSizer841.Add( bSizer75, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticline8 = wx.StaticLine( self.pnlEmail, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer841.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.chkMailAuth = wx.CheckBox( self.pnlEmail, wx.ID_ANY, _("Use Authentication?"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.TAB_TRAVERSAL )
		self.chkMailAuth.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer841.Add( self.chkMailAuth, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer751 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer141 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer141.SetFlexibleDirection( wx.BOTH )
		fgSizer141.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText941 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Login:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText941.Wrap( -1 )
		fgSizer141.Add( self.m_staticText941, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtMailLogin = wx.TextCtrl( self.pnlEmail, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.txtMailLogin.SetMinSize( wx.Size( 150,-1 ) )
		
		fgSizer141.Add( self.txtMailLogin, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText951 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Password:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText951.Wrap( -1 )
		fgSizer141.Add( self.m_staticText951, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer112 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtMailPassword = wx.TextCtrl( self.pnlEmail, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD|wx.TAB_TRAVERSAL )
		self.txtMailPassword.SetMinSize( wx.Size( 150,-1 ) )
		
		bSizer112.Add( self.txtMailPassword, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.btnHideMailPassword = wx.Button( self.pnlEmail, wx.ID_ANY, _("Show"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer112.Add( self.btnHideMailPassword, 0, wx.ALL, 3 )
		
		fgSizer141.Add( bSizer112, 1, wx.EXPAND, 5 )
		
		bSizer751.Add( fgSizer141, 0, wx.EXPAND, 3 )
		
		bSizer841.Add( bSizer751, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticline9 = wx.StaticLine( self.pnlEmail, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer841.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText135 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Address"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText135.Wrap( -1 )
		self.m_staticText135.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer841.Add( self.m_staticText135, 0, wx.ALL, 5 )
		
		bSizer7511 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1411 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer1411.AddGrowableCol( 1 )
		fgSizer1411.SetFlexibleDirection( wx.BOTH )
		fgSizer1411.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText9411 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Send From:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9411.Wrap( -1 )
		fgSizer1411.Add( self.m_staticText9411, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtMailFrom = wx.TextCtrl( self.pnlEmail, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.txtMailFrom.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer1411.Add( self.txtMailFrom, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticText9511 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("Send To:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9511.Wrap( -1 )
		fgSizer1411.Add( self.m_staticText9511, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.txtMailTo = wx.TextCtrl( self.pnlEmail, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.txtMailTo.SetMinSize( wx.Size( 150,-1 ) )
		
		fgSizer1411.Add( self.txtMailTo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		
		fgSizer1411.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText140 = wx.StaticText( self.pnlEmail, wx.ID_ANY, _("You may enter multiple Send To addresses, separated by ';'"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText140.Wrap( -1 )
		self.m_staticText140.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		fgSizer1411.Add( self.m_staticText140, 0, wx.ALL, 3 )
		
		bSizer7511.Add( fgSizer1411, 0, wx.EXPAND, 3 )
		
		bSizer841.Add( bSizer7511, 0, wx.EXPAND|wx.LEFT, 20 )
		
		bSizer84 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnMailSave = wx.Button( self.pnlEmail, wx.ID_ANY, _("Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer84.Add( self.btnMailSave, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.btnEmailTest = wx.Button( self.pnlEmail, wx.ID_ANY, _("Test"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer84.Add( self.btnEmailTest, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer841.Add( bSizer84, 0, wx.EXPAND, 3 )
		
		self.pnlEmail.SetSizer( bSizer841 )
		self.pnlEmail.Layout()
		bSizer841.Fit( self.pnlEmail )
		self.nb_config.AddPage( self.pnlEmail, _("Notification Email"), False )
		self.pnlFileTypes = wx.Panel( self.nb_config, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer85 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText96 = wx.StaticText( self.pnlFileTypes, wx.ID_ANY, _("File Types:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText96.Wrap( -1 )
		self.m_staticText96.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer85.Add( self.m_staticText96, 0, wx.ALL, 5 )
		
		bSizer76 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self.pnlFileTypes, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 200 )
		
		self.pnlList = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		lstFileTypesChoices = []
		self.lstFileTypes = wx.ListBox( self.pnlList, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,100 ), lstFileTypesChoices, wx.LB_SORT )
		bSizer21.Add( self.lstFileTypes, 0, wx.ALL|wx.EXPAND, 3 )
		
		gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.btnDelete = wx.Button( self.pnlList, wx.ID_ANY, _("Delete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnDelete, 0, wx.ALL, 3 )
		
		self.btnNew = wx.Button( self.pnlList, wx.ID_ANY, _("Add New"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.btnNew, 0, wx.ALIGN_RIGHT|wx.ALL, 3 )
		
		bSizer21.Add( gSizer3, 0, wx.EXPAND, 3 )
		
		self.pnlList.SetSizer( bSizer21 )
		self.pnlList.Layout()
		bSizer21.Fit( self.pnlList )
		self.pnlDetails = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText43 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )
		self.m_staticText43.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer26.Add( self.m_staticText43, 0, wx.ALL, 3 )
		
		bSizer90 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtName = wx.TextCtrl( self.pnlDetails, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer90.Add( self.txtName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		self.lblName = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblName.Wrap( -1 )
		bSizer90.Add( self.lblName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		bSizer26.Add( bSizer90, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText42 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("File Extensions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		self.m_staticText42.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer26.Add( self.m_staticText42, 0, wx.ALL, 5 )
		
		bSizer84 = wx.BoxSizer( wx.VERTICAL )
		
		self.txtExtensions = wx.TextCtrl( self.pnlDetails, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_MULTILINE )
		bSizer84.Add( self.txtExtensions, 1, wx.ALL, 3 )
		
		self.m_staticText146 = wx.StaticText( self.pnlDetails, wx.ID_ANY, _("Enter the list of file extensions, \none per line. Do not include the '.'."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText146.Wrap( -1 )
		self.m_staticText146.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer84.Add( self.m_staticText146, 0, wx.ALL, 5 )
		
		bSizer26.Add( bSizer84, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.btnSave = wx.Button( self.pnlDetails, wx.ID_ANY, _("Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.btnSave, 0, wx.ALL, 3 )
		
		self.pnlDetails.SetSizer( bSizer26 )
		self.pnlDetails.Layout()
		bSizer26.Fit( self.pnlDetails )
		self.m_splitter2.SplitVertically( self.pnlList, self.pnlDetails, 200 )
		bSizer76.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		bSizer85.Add( bSizer76, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.pnlFileTypes.SetSizer( bSizer85 )
		self.pnlFileTypes.Layout()
		bSizer85.Fit( self.pnlFileTypes )
		self.nb_config.AddPage( self.pnlFileTypes, _("File Types"), False )
		
		bSizer74.Add( self.nb_config, 1, wx.EXPAND |wx.ALL, 3 )
		
		self.SetSizer( bSizer74 )
		self.Layout()
		
		# Connect Events
		self.txtMasterPassword.Bind( wx.EVT_CHAR, self.onMasterPasswordChar )
		self.btnHidePassword.Bind( wx.EVT_BUTTON, self.onHidePassword )
		self.btnSavePassword.Bind( wx.EVT_BUTTON, self.onSavePassword )
		self.chkMailSSL.Bind( wx.EVT_CHECKBOX, self.onSSL )
		self.chkMailAuth.Bind( wx.EVT_CHECKBOX, self.onMailAuth )
		self.btnHideMailPassword.Bind( wx.EVT_BUTTON, self.onHideMailPassword )
		self.btnMailSave.Bind( wx.EVT_BUTTON, self.onMailSave )
		self.btnEmailTest.Bind( wx.EVT_BUTTON, self.onMailTest )
		self.lstFileTypes.Bind( wx.EVT_LISTBOX, self.onFileType )
		self.btnDelete.Bind( wx.EVT_BUTTON, self.onDelete )
		self.btnNew.Bind( wx.EVT_BUTTON, self.onNew )
		self.txtName.Bind( wx.EVT_TEXT, self.onName )
		self.btnSave.Bind( wx.EVT_BUTTON, self.onSaveTypes )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onMasterPasswordChar( self, event ):
		event.Skip()
	
	def onHidePassword( self, event ):
		event.Skip()
	
	def onSavePassword( self, event ):
		event.Skip()
	
	def onSSL( self, event ):
		event.Skip()
	
	def onMailAuth( self, event ):
		event.Skip()
	
	def onHideMailPassword( self, event ):
		event.Skip()
	
	def onMailSave( self, event ):
		event.Skip()
	
	def onMailTest( self, event ):
		event.Skip()
	
	def onFileType( self, event ):
		event.Skip()
	
	def onDelete( self, event ):
		event.Skip()
	
	def onNew( self, event ):
		event.Skip()
	
	def onName( self, event ):
		event.Skip()
	
	def onSaveTypes( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 200 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

###########################################################################
## Class HistoryWindow
###########################################################################

class HistoryWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("History"), pos = wx.DefaultPosition, size = wx.Size( 707,462 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer95 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer94 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer93 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, _("Show History For Backup:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		bSizer93.Add( self.m_staticText111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		cboBackupChoices = []
		self.cboBackup = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cboBackupChoices, 0 )
		self.cboBackup.SetSelection( 0 )
		bSizer93.Add( self.cboBackup, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.m_staticline18 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer93.Add( self.m_staticline18, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.txtOrder = wx.StaticText( self, wx.ID_ANY, _("Order: Newest At Top"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtOrder.Wrap( -1 )
		bSizer93.Add( self.txtOrder, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.btnOrder = wx.Button( self, wx.ID_ANY, _("Switch"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer93.Add( self.btnOrder, 0, wx.ALL, 5 )
		
		self.m_staticline181 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer93.Add( self.m_staticline181, 0, wx.EXPAND |wx.ALL, 3 )
		
		
		bSizer93.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnRefresh = wx.Button( self, wx.ID_ANY, _("Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer93.Add( self.btnRefresh, 0, wx.ALL, 5 )
		
		bSizer94.Add( bSizer93, 0, wx.EXPAND, 3 )
		
		self.nb_history = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pnlRuns = wx.Panel( self.nb_history, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer96 = wx.BoxSizer( wx.VERTICAL )
		
		self.lstRuns = wx.ListCtrl( self.pnlRuns, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer96.Add( self.lstRuns, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.btnDetails = wx.Button( self.pnlRuns, wx.ID_ANY, _("Show Run Details"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer96.Add( self.btnDetails, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.pnlRuns.SetSizer( bSizer96 )
		self.pnlRuns.Layout()
		bSizer96.Fit( self.pnlRuns )
		self.nb_history.AddPage( self.pnlRuns, _("Runs"), True )
		self.pnlMessages = wx.Panel( self.nb_history, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer97 = wx.BoxSizer( wx.VERTICAL )
		
		self.lstMessages = wx.ListCtrl( self.pnlMessages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer97.Add( self.lstMessages, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.pnlMessages.SetSizer( bSizer97 )
		self.pnlMessages.Layout()
		bSizer97.Fit( self.pnlMessages )
		self.nb_history.AddPage( self.pnlMessages, _("Messages"), False )
		
		bSizer94.Add( self.nb_history, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer95.Add( bSizer94, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer95 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cboBackup.Bind( wx.EVT_CHOICE, self.onBackup )
		self.btnOrder.Bind( wx.EVT_BUTTON, self.onOrder )
		self.btnRefresh.Bind( wx.EVT_BUTTON, self.onRefresh )
		self.lstRuns.Bind( wx.EVT_LEFT_DCLICK, self.onLeftDClick )
		self.lstRuns.Bind( wx.EVT_LIST_COL_CLICK, self.onColClick )
		self.btnDetails.Bind( wx.EVT_BUTTON, self.onDetails )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onBackup( self, event ):
		event.Skip()
	
	def onOrder( self, event ):
		event.Skip()
	
	def onRefresh( self, event ):
		event.Skip()
	
	def onLeftDClick( self, event ):
		event.Skip()
	
	def onColClick( self, event ):
		event.Skip()
	
	def onDetails( self, event ):
		event.Skip()
	

###########################################################################
## Class AboutWindow
###########################################################################

class AboutWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 342,371 ), style = wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer90 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer91.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.imgAbout = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer91.Add( self.imgAbout, 0, wx.ALL, 5 )
		
		
		bSizer91.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer90.Add( bSizer91, 1, wx.EXPAND, 5 )
		
		self.lblTitle = wx.StaticText( self, wx.ID_ANY, _("Title"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblTitle.Wrap( -1 )
		self.lblTitle.SetFont( wx.Font( 14, 74, 90, 92, False, "Sans" ) )
		
		bSizer90.Add( self.lblTitle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 3 )
		
		self.lblSubTitle = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblSubTitle.Wrap( -1 )
		self.lblSubTitle.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer90.Add( self.lblSubTitle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.lblVersion = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblVersion.Wrap( -1 )
		bSizer90.Add( self.lblVersion, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 3 )
		
		self.lblCopyright = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblCopyright.Wrap( -1 )
		bSizer90.Add( self.lblCopyright, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 3 )
		
		
		bSizer90.AddSpacer( ( 5, 10), 0, 0, 0 )
		
		self.SetSizer( bSizer90 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_LEFT_UP, self.onLeftUp )
		self.imgAbout.Bind( wx.EVT_LEFT_UP, self.onLeftUp )
		self.lblTitle.Bind( wx.EVT_LEFT_UP, self.onLeftUp )
		self.lblSubTitle.Bind( wx.EVT_LEFT_UP, self.onLeftUp )
		self.lblVersion.Bind( wx.EVT_LEFT_UP, self.onLeftUp )
		self.lblCopyright.Bind( wx.EVT_LEFT_UP, self.onLeftUp )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onLeftUp( self, event ):
		event.Skip()
	
	
	
	
	
	

###########################################################################
## Class PackageWindow
###########################################################################

class PackageWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 483,378 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer98 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText112 = wx.StaticText( self, wx.ID_ANY, _("Missing Packages (Software)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText112.Wrap( -1 )
		self.m_staticText112.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer98.Add( self.m_staticText112, 0, wx.ALL, 3 )
		
		bSizer99 = wx.BoxSizer( wx.VERTICAL )
		
		lstSoftwareChoices = [ _("asdf") ];
		self.lstSoftware = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstSoftwareChoices, 0 )
		bSizer99.Add( self.lstSoftware, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.m_staticText114 = wx.StaticText( self, wx.ID_ANY, _("Uncheck any that you do not want installed, then click \"Begin Installation\"."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText114.Wrap( -1 )
		self.m_staticText114.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer99.Add( self.m_staticText114, 0, wx.ALL, 5 )
		
		self.btnBegin = wx.Button( self, wx.ID_ANY, _("Begin Installation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer99.Add( self.btnBegin, 0, wx.ALL, 3 )
		
		self.m_staticline12 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer99.Add( self.m_staticline12, 0, wx.EXPAND |wx.ALL, 3 )
		
		bSizer98.Add( bSizer99, 1, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticText113 = wx.StaticText( self, wx.ID_ANY, _("Installation Progress"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText113.Wrap( -1 )
		self.m_staticText113.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer98.Add( self.m_staticText113, 0, wx.ALL, 3 )
		
		bSizer100 = wx.BoxSizer( wx.VERTICAL )
		
		self.progress = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_SMOOTH )
		bSizer100.Add( self.progress, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.lblCurrentFile = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblCurrentFile.Wrap( -1 )
		bSizer100.Add( self.lblCurrentFile, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer98.Add( bSizer100, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.SetSizer( bSizer98 )
		self.Layout()
		self.m_statusBar4 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.lstSoftware.Bind( wx.EVT_LISTBOX, self.onCheckBox )
		self.lstSoftware.Bind( wx.EVT_LISTBOX_DCLICK, self.onCheckBox )
		self.lstSoftware.Bind( wx.EVT_CHECKLISTBOX, self.onCheckBox )
		self.btnBegin.Bind( wx.EVT_BUTTON, self.onBegin )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCheckBox( self, event ):
		event.Skip()
	
	
	
	def onBegin( self, event ):
		event.Skip()
	

###########################################################################
## Class ProgressDialog
###########################################################################

class ProgressDialog ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 348,91 ), style = wx.CAPTION|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_TOOL_WINDOW|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer93 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer16 = wx.FlexGridSizer( 1, 3, 0, 0 )
		fgSizer16.AddGrowableCol( 1 )
		fgSizer16.SetFlexibleDirection( wx.BOTH )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.lblMessage = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblMessage.Wrap( -1 )
		fgSizer16.Add( self.lblMessage, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		
		fgSizer16.AddSpacer( ( 30, 0), 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 0 )
		
		self.aniPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 32,32 ), wx.TAB_TRAVERSAL )
		fgSizer16.Add( self.aniPanel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		bSizer93.Add( fgSizer16, 1, wx.ALL|wx.EXPAND, 20 )
		
		self.SetSizer( bSizer93 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

