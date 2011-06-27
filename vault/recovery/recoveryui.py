# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

import gettext
_ = gettext.gettext

###########################################################################
## Class RecoveryWindow
###########################################################################

class RecoveryWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("Disaster Recovery"), pos = wx.DefaultPosition, size = wx.Size( 389,338 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer88 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText89 = wx.StaticText( self, wx.ID_ANY, _("Backup Details"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText89.Wrap( -1 )
		self.m_staticText89.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer88.Add( self.m_staticText89, 0, wx.ALL, 3 )
		
		bSizer89 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText90 = wx.StaticText( self, wx.ID_ANY, _("Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText90.Wrap( -1 )
		bSizer89.Add( self.m_staticText90, 0, wx.ALL, 3 )
		
		cboBackupChoices = []
		self.cboBackup = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), cboBackupChoices, 0 )
		self.cboBackup.SetSelection( 0 )
		bSizer89.Add( self.cboBackup, 0, wx.ALL, 3 )
		
		self.lblStatus = wx.StaticText( self, wx.ID_ANY, _("Last Backup:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblStatus.Wrap( -1 )
		self.lblStatus.SetFont( wx.Font( 8, 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer89.Add( self.lblStatus, 0, wx.ALL, 3 )
		
		self.m_staticText92 = wx.StaticText( self, wx.ID_ANY, _("Master Password"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92.Wrap( -1 )
		bSizer89.Add( self.m_staticText92, 0, wx.ALL, 3 )
		
		self.txtPassword = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 250,-1 ), wx.TE_PASSWORD )
		bSizer89.Add( self.txtPassword, 0, wx.ALL, 3 )
		
		bSizer88.Add( bSizer89, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticline9 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer88.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 3 )
		
		self.m_staticText93 = wx.StaticText( self, wx.ID_ANY, _("Destination"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )
		self.m_staticText93.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer88.Add( self.m_staticText93, 0, wx.ALL, 3 )
		
		bSizer90 = wx.BoxSizer( wx.VERTICAL )
		
		self.radOriginal = wx.RadioButton( self, wx.ID_ANY, _("Original Location"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer90.Add( self.radOriginal, 0, wx.ALL|wx.EXPAND, 3 )
		
		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.radAlternate = wx.RadioButton( self, wx.ID_ANY, _("Alternate Location"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.radAlternate, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3 )
		
		self.dirAlternate = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _("Select a folder"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
		bSizer91.Add( self.dirAlternate, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 3 )
		
		bSizer90.Add( bSizer91, 1, wx.EXPAND, 0 )
		
		bSizer88.Add( bSizer90, 0, wx.EXPAND|wx.LEFT, 20 )
		
		self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer88.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 3 )
		
		bSizer92 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer92.AddSpacer( ( 0, 0), 1, wx.EXPAND, 3 )
		
		self.btnRecover = wx.Button( self, wx.ID_ANY, _("Recover Files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.btnRecover, 0, wx.ALL, 3 )
		
		self.btnClose = wx.Button( self, wx.ID_ANY, _("Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.btnClose, 0, wx.ALL, 3 )
		
		bSizer88.Add( bSizer92, 0, wx.EXPAND, 3 )
		
		self.SetSizer( bSizer88 )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cboBackup.Bind( wx.EVT_CHOICE, self.onBackup )
		self.radOriginal.Bind( wx.EVT_RADIOBUTTON, self.onDestination )
		self.radAlternate.Bind( wx.EVT_RADIOBUTTON, self.onDestination )
		self.btnRecover.Bind( wx.EVT_BUTTON, self.onRecover )
		self.btnClose.Bind( wx.EVT_BUTTON, self.onClose )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onBackup( self, event ):
		event.Skip()
	
	def onDestination( self, event ):
		event.Skip()
	
	
	def onRecover( self, event ):
		event.Skip()
	
	def onClose( self, event ):
		event.Skip()
	

