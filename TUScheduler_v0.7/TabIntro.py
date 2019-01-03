import wx

class TabIntro(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        bitmapData = wx.Image('./images/intro.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmapData, (0, 0), (bitmapData.GetWidth(), bitmapData.GetHeight()))