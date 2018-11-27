import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(800, 600))

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.panel = wx.Panel(self)

        self.panel.SetBackgroundColour("gray")

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.LoadImages()

        vbox.Add(self.mincol, wx.ID_ANY, wx.LEFT | wx.ALL, 5)
        vbox.Add(self.bardejov, wx.ID_ANY, wx.LEFT | wx.ALL, 5)
        vbox.Add(self.rotunda, wx.ID_ANY, wx.LEFT | wx.ALL, 5)

        self.panel.SetSizer(vbox)


    def LoadImages(self):

        self.mincol = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))

        self.bardejov = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))

        self.rotunda = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))


def main():

    app = wx.App()
    ex = Example(None, title='Sizer')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()