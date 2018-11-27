import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(800, 600))

        self.vbox = wx.BoxSizer(wx.HORIZONTAL)

        self.InitUI()
        self.Centre()

    def InitUI(self):
        menubar = wx.MenuBar()
        sizerMenu = wx.Menu()
        h_mi = wx.MenuItem(sizerMenu, wx.ID_ANY, '&Horizontal\tCtrl+H')
        v_mi = wx.MenuItem(sizerMenu, wx.ID_ANY, '&Vertical\tCtrl+V')
        q_mi = wx.MenuItem(sizerMenu, wx.ID_ANY, '&Quit\tCtrl+Q')
        sizerMenu.Append(h_mi)
        sizerMenu.Append(v_mi)
        sizerMenu.Append(q_mi)

        self.Bind(wx.EVT_MENU, self.OnHorizontal, h_mi)
        self.Bind(wx.EVT_MENU, self.OnVertical, v_mi)
        self.Bind(wx.EVT_MENU, self.OnQuit, q_mi)

        menubar.Append(sizerMenu, '&Sizer')
        self.SetMenuBar(menubar)


        self.panel = wx.Panel(self)


        self.panel.SetBackgroundColour("gray")



        self.LoadImages()

        self.vbox.Add(self.mincol, wx.ID_ANY, wx.LEFT | wx.ALL, 5)
        self.vbox.Add(self.bardejov, wx.ID_ANY, wx.LEFT | wx.ALL, 5)
        self.vbox.Add(self.rotunda, wx.ID_ANY, wx.LEFT | wx.ALL, 5)

        self.panel.SetSizer(self.vbox)


    def LoadImages(self):

        self.mincol = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))

        self.bardejov = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))

        self.rotunda = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))

    def OnQuit(self, e):
        self.Close()

    def OnHorizontal(self, e):
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)

    def OnVertical(self, e):
        self.vbox = wx.BoxSizer(wx.VERTICAL)


def main():

    app = wx.App()
    ex = Example(None, title='Sizer')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()