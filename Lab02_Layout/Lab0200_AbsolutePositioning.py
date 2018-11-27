import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(350, 300))

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.panel = wx.Panel(self)

        self.panel.SetBackgroundColour("gray")

        self.LoadImages()

        self.mincol.SetPosition((20, 20))
        self.bardejov.SetPosition((240, 20))
        self.rotunda.SetPosition((20, 200))


    def LoadImages(self):

        self.mincol = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))

        self.bardejov = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))

        self.rotunda = wx.StaticBitmap(self.panel, wx.ID_ANY,
            wx.Bitmap("quit.png", wx.BITMAP_TYPE_ANY))


def main():

    app = wx.App()
    ex = Example(None, title='Absolute positioning')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()