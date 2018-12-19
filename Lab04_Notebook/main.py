import wx

class TestNoteBook(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 500))
        panel = wx.Panel(self)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        leftpanel = wx.Panel(panel)
        notebook = wx.Notebook(leftpanel)
        posterpage = wx.Panel(notebook)
        listpage = wx.Panel(notebook)
        notebook.AddPage(posterpage, 'posters')
        notebook.AddPage(listpage, 'list')
        hsizer.Add(leftpanel, 1, wx.EXPAND)
        rightpanel = wx.Panel(panel)
        hsizer.Add(rightpanel, 1, wx.EXPAND)

        ##### Added code (
        leftpanel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        leftpanel_sizer.Add(notebook, 1, wx.EXPAND)
        leftpanel.SetSizer(leftpanel_sizer)

        rightpanel.SetBackgroundColour('blue') # not needed, to distinguish rightpanel from leftpanel
        ##### Added code )

        panel.SetSizer(hsizer)


app = wx.App()
frame = TestNoteBook(None, -1, 'notebook')
frame.Show()
app.MainLoop()