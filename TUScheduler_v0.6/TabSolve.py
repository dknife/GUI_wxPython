import wx

class TabSolve(wx.Panel):

    def __init__(self, parent, coreData):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnTabClicked)
        self.CoreData = coreData



        self.Msg_DataDone = wx.StaticText(self, -1, "시간표 생성 가능 여부", (100, 50))
        self.CreateButton = wx.Button(self, -1, "시간표 생성", pos=(300,45), size=(100,30))
        self.Msg_ProfInfo = wx.StaticText(self, -1, "교수정보", (100, 90))

    def OnTabClicked(self, e):
        if self.parent is not e.GetEventObject():
            return

        self.CoreData.tabBasic.OnSetData(None)

        if self.CoreData.bClassDataFinished is True:
            self.Msg_DataDone.SetLabel("시간표를 생성할 수 있습니다.")
            self.Msg_DataDone.SetForegroundColour((0, 0, 255))
            self.CreateButton.Show()
        else :
            self.Msg_DataDone.SetLabel("강의 개설 정보가 완성되지 않아 시간표 생성이 불가능합니다. \"기본정보 입력\" 탭을 눌러 기본정보를 완성하십시오.")
            self.Msg_DataDone.SetForegroundColour((255, 0, 0))
            self.CreateButton.Hide()

        msg = "교수님 수: " + str(self.CoreData.nProfessors) + "       강의실 수:" + str(self.CoreData.nClassRooms) + "\n교수 리스트 -- "
        for i in range(self.CoreData.nProfessors) :
            msg = msg + self.CoreData.ProfInfo[i].Name.GetValue() + " 교수님 | "
        self.Msg_ProfInfo.SetLabel(msg)


        if e is not None:
            e.Skip() # for multiple event handlers