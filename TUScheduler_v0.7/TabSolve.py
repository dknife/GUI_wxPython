import wx
import wx.lib.scrolledpanel as scrolled

import random

class Chromosome:
    def __init__(self, nClassRooms):
        self.weekday = random.randint(0,4)
        self.room = random.randint(0,nClassRooms-1)
        self.hour = random.randint(0,9)

    def printInfo(self):
        print(self.weekday, self.room, self.hour)

class Genome:
    def __init__(self, nClassUnits, nClassRooms):
        self.chromosome = [Chromosome(nClassRooms) for i in range(nClassUnits) ]

    def printInfo(self):
        for i in range(0, len(self.chromosome)) :
            self.chromosome[i].printInfo()

class TimeTable(scrolled.ScrolledPanel):
    def __init__(self, parent):

        scrolled.ScrolledPanel.__init__(self, parent, -1)

        button1 = wx.Button(parent, label="Button 1", pos=(0, 50), size=(50, 50))
        button2 = wx.Button(parent, label="Button 2", pos=(0, 100), size=(50, 50))
        button3 = wx.Button(parent, label="Button 3", pos=(0, 150), size=(50, 50))
        button4 = wx.Button(parent, label="Button 4", pos=(0, 200), size=(50, 50))
        button5 = wx.Button(parent, label="Button 5", pos=(0, 250), size=(50, 50))
        button6 = wx.Button(parent, label="Button 6", pos=(0, 300), size=(50, 50))
        button7 = wx.Button(parent, label="Button 7", pos=(0, 350), size=(50, 50))
        button8 = wx.Button(parent, label="Button 8", pos=(0, 400), size=(50, 50))

        bSizer = wx.BoxSizer(wx.VERTICAL)
        bSizer.Add(button1, 0, wx.ALL, 5)
        bSizer.Add(button2, 0, wx.ALL, 5)
        bSizer.Add(button3, 0, wx.ALL, 5)
        bSizer.Add(button4, 0, wx.ALL, 5)
        bSizer.Add(button5, 0, wx.ALL, 5)
        bSizer.Add(button6, 0, wx.ALL, 5)
        bSizer.Add(button7, 0, wx.ALL, 5)
        bSizer.Add(button8, 0, wx.ALL, 5)

        parent.SetSizer(bSizer)
        self.SetupScrolling()

class TabSolve(wx.Panel):

    def __init__(self, parent, coreData):
        wx.Panel.__init__(self, parent)

        self.genome = Genome(0,0)

        self.parent = parent
        self.parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnTabClicked)
        self.CoreData = coreData

        self.Msg_DataDone = wx.StaticText(self, -1, "시간표 생성 가능 여부", (100, 50))
        self.CreateButton = wx.Button(self, -1, "시간표 생성", pos=(300,45), size=(100,30))
        self.CreateButton.Bind(wx.EVT_BUTTON, self.OnCreate)
        self.Msg_ProfInfo = wx.StaticText(self, -1, "교수정보", (100, 90))

        panel2 = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(1400, 300), pos=(0, 150),
                                                    style=wx.SIMPLE_BORDER)


        self.scheduleView = TimeTable(panel2)
        panel2.SetupScrolling()
        panel2.SetBackgroundColour('#00FFFF')


    def OnCreate(self, e):
        self.genome = Genome(len(self.CoreData.ClassUnits), self.CoreData.nClassRooms)

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

        self.genome.printInfo()

        if e is not None:
            e.Skip() # for multiple event handlers