#!../venv/Scripts/python.exe
# -*- coding: utf-8 -*-

# simple.py

import wx

app = wx.App()

frame = wx.Frame(None, style= wx.SYSTEM_MENU | wx.CAPTION |	 wx.CLOSE_BOX)
frame.Show()

app.MainLoop()