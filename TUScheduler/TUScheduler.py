import wx



# Define the tab content as classes:
import TabIntro
import TabBasicInfo


class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is the second tab", (20, 20))

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="동명대학교 게임공학과 시간표 작성기")
        self.SetSize((1400,1024))

        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # Create the tab windows
        self.tabIntro = TabIntro.TabIntro(nb)
        self.tabBasic = TabBasicInfo.TabBasicInfo(nb)
        tab2 = TabTwo(nb)



        # Add the windows to tabs and name them.
        nb.AddPage(self.tabIntro, "초기화면")
        nb.AddPage(self.tabBasic, "기본정보 입력")
        nb.AddPage(tab2, "Tab 2")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()