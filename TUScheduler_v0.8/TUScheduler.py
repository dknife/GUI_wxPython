import wx



# Define the tab content as classes:
import TabIntro
import TabBasicInfo
import TabRoomInfo
import TabSolve # notebook page for solving the problem for generating the schedule


class CoreData:
    def __init__(self):
        self.bClassDataFinished = False
        self.nProfessors = 0
        self.nClassRooms = 0
        self.ClassUnits = []
        self.ProfInfo = []
        self.tabBasic = None
        self.tabAvailability = None


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="동명대학교 게임공학과 시간표 작성기")
        self.SetSize((1400,1024))

        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        self.CoreData = CoreData()
        # Create the tab windows
        self.tabIntro = TabIntro.TabIntro(nb)
        self.CoreData.tabBasic = self.tabBasic = TabBasicInfo.TabBasicInfo(nb, self.CoreData)
        self.CoreData.tabAvailability = self.tabRooms = TabRoomInfo.TabRoomInfo(nb, self.CoreData)
        self.tabSolve = TabSolve.TabSolve(nb, self.CoreData)


        # Add the windows to tabs and name them.
        nb.AddPage(self.tabIntro, "초기화면")
        nb.AddPage(self.tabBasic, "기본정보 입력")
        nb.AddPage(self.tabRooms, "강의불가 시간 입력")
        nb.AddPage(self.tabSolve, "강의 시간표 생성")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()