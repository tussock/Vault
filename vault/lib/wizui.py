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
## Class Wizard
###########################################################################

class Wizard ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("Wizard Title"), pos = wx.DefaultPosition, size = wx.Size( 640,401 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer87 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel23 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel23.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		self.m_panel23.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		bSizer88 = wx.BoxSizer( wx.VERTICAL )
		
		self.txtPageTitle = wx.StaticText( self.m_panel23, wx.ID_ANY, _("Page Title"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtPageTitle.Wrap( -1 )
		self.txtPageTitle.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer88.Add( self.txtPageTitle, 0, wx.ALL|wx.EXPAND, 10 )
		
		self.m_panel23.SetSizer( bSizer88 )
		self.m_panel23.Layout()
		bSizer88.Fit( self.m_panel23 )
		bSizer87.Add( self.m_panel23, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.pnlPages = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer92 = wx.BoxSizer( wx.VERTICAL )
		
		self.pnlPages.SetSizer( bSizer92 )
		self.pnlPages.Layout()
		bSizer92.Fit( self.pnlPages )
		bSizer87.Add( self.pnlPages, 1, wx.EXPAND |wx.ALL, 20 )
		
		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer91.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnQuit = wx.Button( self, wx.ID_ANY, _("Quit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.btnQuit, 0, wx.ALL, 3 )
		
		self.btnBack = wx.Button( self, wx.ID_ANY, _("Back"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.btnBack, 0, wx.ALL, 3 )
		
		self.btnForward = wx.Button( self, wx.ID_ANY, _("Forward"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.btnForward, 0, wx.ALL, 3 )
		
		self.btnFinish = wx.Button( self, wx.ID_ANY, _("Finish"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.btnFinish, 0, wx.ALL, 3 )
		
		bSizer87.Add( bSizer91, 0, wx.EXPAND, 3 )
		
		self.SetSizer( bSizer87 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnQuit.Bind( wx.EVT_BUTTON, self.onQuit )
		self.btnBack.Bind( wx.EVT_BUTTON, self.onBack )
		self.btnForward.Bind( wx.EVT_BUTTON, self.onForward )
		self.btnFinish.Bind( wx.EVT_BUTTON, self.onFinish )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onQuit( self, event ):
		event.Skip()
	
	def onBack( self, event ):
		event.Skip()
	
	def onForward( self, event ):
		event.Skip()
	
	def onFinish( self, event ):
		event.Skip()
	

###########################################################################
## Class IntroPage
###########################################################################

class IntroPage ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		m_radioBox1Choices = [ _("Radio Button"), _("Option 1"), _("Option 2"), _("Option 3") ]
		self.m_radioBox1 = wx.RadioBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_ROWS )
		self.m_radioBox1.SetSelection( 0 )
		bSizer7.Add( self.m_radioBox1, 0, wx.ALL, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn1 = wx.RadioButton( self, wx.ID_ANY, _("RadioBtn"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_radioBtn1, 0, wx.ALL, 5 )
		
		self.m_radioBtn2 = wx.RadioButton( self, wx.ID_ANY, _("RadioBtn"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_radioBtn2, 0, wx.ALL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
		self.m_filePicker1 = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, _("Select a file"), u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer8.Add( self.m_filePicker1, 0, wx.ALL, 5 )
		
		self.m_dirPicker1 = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _("Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer8.Add( self.m_dirPicker1, 0, wx.ALL, 5 )
		
		
		bSizer8.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer7.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer7 )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class TextPanel
###########################################################################

class TextPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 304,83 ), style = wx.TAB_TRAVERSAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.label = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label.Wrap( -1 )
		bSizer7.Add( self.label, 0, wx.ALL, 3 )
		
		self.field = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.field, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.SetSizer( bSizer7 )
		self.Layout()
	
	def __del__( self ):
		pass
	

