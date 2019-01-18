import wx

import constant
import os


class AvailableTimeTab(wx.Panel):
    def __init__(self, parent, name=''):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.panel = wx.Panel(self, size=(1280,600))
        self.panel.SetBackgroundColour(wx.Colour(210, 210, 210))
        self.name = name
        self.label1 = wx.StaticText(self.panel, -1, name + "에 대해 수업을 배정할 수 없는 시간을 체크하세요", (50,20))

        self.unavailable =[[],[],[],[],[]]
        self.classTimes = [[],[],[],[],[]]
        week = ['월', '화', '수', '목', '금']
        for i in range(5):  # 5 days a week
            wx.StaticText(self.panel, -1, week[i], (200+i*230, 50))

        self.ln = wx.StaticLine(self.panel, -1, wx.Point(50, 80), size=(1150, -1), style=wx.LI_HORIZONTAL)

        for i in range(6): # 5 days a week
            wx.StaticLine(self.panel, -1, wx.Point(50+(i)*230, 80), size=(-1, 400), style=wx.LI_VERTICAL)

        for i in range(10): # 10 class hours
            wx.StaticLine(self.panel, -1, wx.Point(50, 80+(i+1)*40), size=(1150, -1), style=wx.LI_HORIZONTAL)


        for i in range(5) : # 5 days a week
            for j in range(10) : # 10 class hours
                timeText = wx.StaticText(self.panel, -1, str(j+1)+"교시 - " + str(9+j) + ":00", (100+i*230, 100+j*40))
                self.classTimes[i].append(timeText)

        for i in range(5) : # 5 days a week
            for j in range(10) : # 10 class hours
                checkbox = wx.CheckBox(self.panel, -1, label="", pos=(200+i*230, 100+j*40))
                self.unavailable[i].append(checkbox)
                checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheck)

    def OnCheck(self, e):
        for i in range(5) : # 5 days a week
            for j in range(10) : # 10 class hours
                if self.unavailable[i][j].GetValue() is True:
                    self.classTimes[i][j].SetForegroundColour(wx.Colour(255,0,0))
                else:
                    self.classTimes[i][j].SetForegroundColour(wx.Colour(0, 0, 0))
        self.Refresh()

    def setName(self, name):
        self.name = name
        self.label1.SetLabel(name + "에 대해 수업을 배정할 수 없는 시간을 체크하세요")

class TabRoomInfo(wx.Panel):

    def __init__(self, parent, coreData):
        wx.Panel.__init__(self, parent)

        # data
        self.CoreData = coreData
        self.parent = parent
        parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnTabClicked)

        self.nb = wx.Notebook(self, pos=(50,50), size=(1280,600))

        self.GradeTabs = []
        self.ProfTabs = []
        self.RoomTabs = []

        for i in range(4):
            newTab = AvailableTimeTab(self.nb, str(i+1)+'학년')
            self.GradeTabs.append(newTab)
            self.nb.AddPage(self.GradeTabs[i], str(i + 1) + "학년")


    def OnTabClicked(self, e):
        if self.parent is not e.GetEventObject() :
            return

        nProfTabs = len(self.ProfTabs)
        if nProfTabs < self.CoreData.nProfessors :
            for i in range(nProfTabs, self.CoreData.nProfessors):
                newTab = AvailableTimeTab(self.nb, self.CoreData.ProfInfo[i].Name.GetValue()+" 교수님")
                self.ProfTabs.append(newTab)
                self.nb.InsertPage(4+i, self.ProfTabs[i], self.CoreData.ProfInfo[i].Name.GetValue())
        elif nProfTabs > self.CoreData.nProfessors :
            for i in range(self.CoreData.nProfessors, nProfTabs):
                self.nb.DeletePage(4+self.CoreData.nProfessors)
            self.ProfTabs[self.CoreData.nProfessors:] = []


        nRoomTabs = len(self.RoomTabs)
        if nRoomTabs < self.CoreData.nClassRooms:
            for i in range(nRoomTabs, self.CoreData.nClassRooms):
                newTab = AvailableTimeTab(self.nb, "강의실 " + str(i + 1))
                self.RoomTabs.append(newTab)
                self.nb.AddPage(self.RoomTabs[i], "강의실 " + str(i + 1))
        elif nRoomTabs > self.CoreData.nClassRooms:
            for i in range(self.CoreData.nClassRooms, nRoomTabs):
                self.nb.DeletePage(4+self.CoreData.nProfessors+self.CoreData.nClassRooms)
            self.RoomTabs[self.CoreData.nClassRooms:] = []

        for i in range(self.CoreData.nProfessors):
            self.ProfTabs[i].setName(self.CoreData.ProfInfo[i].Name.GetValue() + " 교수님")
            self.nb.SetPageText(i+4, self.CoreData.ProfInfo[i].Name.GetValue())

        if e is not None:
            e.Skip() # for multiple event handlers
