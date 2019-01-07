import wx
import wx.lib.scrolledpanel as scrolled
import random

SCHEDULE_ITEM_W = 200
SCHEDULE_ITEM_H = 50



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

        self.ScheduleViewPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(1350, 600), pos=(0, 130),
                                                                style=wx.SIMPLE_BORDER)
        self.ScheduleViewPanel.SetupScrolling()
        self.ScheduleViewPanel.SetBackgroundColour('#CCCCCC')




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

        self.ScheduleViewPanel.Destroy()
        self.ScheduleViewPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(1350, 650), pos=(0, 130),
                                                                    style=wx.SIMPLE_BORDER)
        self.ScheduleViewPanel.SetBackgroundColour('#CCCCCC')

        weekDays = ['월', '화', '수', '목', '금']
        weekColors = ['#00FFFF', '#FFFF00', '#00FF00', '#FFAAFF', '#FFFFAA']
        for i in range(len(weekDays)) :
            wday = wx.StaticText(self.ScheduleViewPanel, -1, weekDays[i], pos=(SCHEDULE_ITEM_W + SCHEDULE_ITEM_W*self.CoreData.nClassRooms*i,0), size=(SCHEDULE_ITEM_W * self.CoreData.nClassRooms, SCHEDULE_ITEM_H))
            wday.SetBackgroundColour(weekColors[i])

            for  j in range(self.CoreData.nClassRooms) :
                room = wx.StaticText(self.ScheduleViewPanel, -1, '강의실 - ' + str(j+1),
                              pos=(SCHEDULE_ITEM_W + 1 + SCHEDULE_ITEM_W * self.CoreData.nClassRooms * i + SCHEDULE_ITEM_W*j, SCHEDULE_ITEM_H+1),
                              size=(SCHEDULE_ITEM_W-2, SCHEDULE_ITEM_H-2))
                room.SetBackgroundColour(weekColors[i])


        for i in range(11) :
            wx.StaticText(self.ScheduleViewPanel, -1, str(i+1)+" 교시",
                          pos=(0, SCHEDULE_ITEM_H*(i+2)+SCHEDULE_ITEM_H*0.05),
                          size=(SCHEDULE_ITEM_W, SCHEDULE_ITEM_H*0.9))

        #for i in range(6):  # 5 days a week
        #    wx.StaticLine(self.ScheduleViewPanel, -1, wx.Point(SCHEDULE_ITEM_W+SCHEDULE_ITEM_W*self.CoreData.nClassRooms*i, 0), size=(-1, SCHEDULE_ITEM_W*12), style=wx.LI_VERTICAL)

        for i in range(10):  # 10 class hours
            wx.StaticLine(self.ScheduleViewPanel, -1, wx.Point(0, SCHEDULE_ITEM_H*2 + (i) * SCHEDULE_ITEM_H), size=(1150, -1), style=wx.LI_HORIZONTAL)

        self.scheduleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ScheduleViewPanel.SetSizer(self.scheduleSizer)
        self.scheduleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scheduleSizer.AddSpacer(5*SCHEDULE_ITEM_W*(self.CoreData.nClassRooms) + SCHEDULE_ITEM_W)
        self.ScheduleViewPanel.SetSizer(self.scheduleSizer)
        self.ScheduleViewPanel.SetupScrolling()



        self.genome.printInfo()

        if e is not None:
            e.Skip() # for multiple event handlers