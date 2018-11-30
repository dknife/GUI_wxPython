import wx

import constant

class ClassData():
    def __init__(self, parent,  i, pos):
        nHoursChoices = ['1', '2', '3', '4']
        GradeChoices = ['1', '2', '3', '4']
        XCoord = constant.CLASS_NAME_INDENT + constant.COMBOBOXSIZE + i * constant.CLASSDATASIZE

        self.ClassName = wx.TextCtrl(parent, -1, "", (XCoord,  pos[1]), size=(constant.CLASSNAMESIZE, constant.WIDGET_H))
        self.Hours = wx.ComboBox(parent, -1, "", (XCoord + constant.CLASSNAMESIZE, pos[1]), choices=nHoursChoices, size=(constant.COMBOBOXSIZE, constant.WIDGET_H))
        self.Grade = wx.ComboBox(parent, -1, "", (XCoord + constant.CLASSNAMESIZE+constant.COMBOBOXSIZE, pos[1]), choices=GradeChoices, size=(constant.COMBOBOXSIZE, constant.WIDGET_H))

        #self.ClassName.SetLabel("hello")
    def remove(self):
        self.ClassName.Hide()
        self.Hours.Hide()
        self.Grade.Hide()


class ProfInfo():
    def __init__(self, parent, i, x, y):
        message = str(i) + "번째 교수님: "
        self.parent = parent
        self.pos = (x,y)
        self.Label = wx.StaticText(parent, -1, message, (x,y))
        self.Name = wx.TextCtrl(parent, -1, "", (x+constant.PROF_NAME_INDENT, y), size=(constant.PROFNAMEWIDTH,constant.WIDGET_H))
        nClassChoices = ['1', '2', '3','4', '5', '6', '7', '8', '9', '10']
        self.nClass = 0

        self.nClassCombo = wx.ComboBox(parent, pos=(x+constant.PROF_NCLASS_INDENT, y), choices=nClassChoices, style=wx.CB_READONLY)
        self.nClassCombo.Bind(wx.EVT_COMBOBOX, self.OnSelectNClass)
        self.ClassArr = []

    def OnSelectNClass(self, e):
        for i in range(self.nClass) :
            self.ClassArr[i].remove()

        del self.ClassArr
        self.ClassArr = []

        self.nClass = int(e.GetString())


        for i in range(self.nClass):
            self.ClassArr.append(ClassData(self.parent, i, (self.pos[0] + constant.CLASSGAP, self.pos[1])))

    def remove(self):
        self.Label.Hide()
        self.Name.Hide()
        self.nClassCombo.Hide()



class TabBasicInfo(wx.Panel):
    def __init__(self, parent):

        # data
        self.nProfessors = 0
        self.ProfInfoArr = []
        self.nClassRoom = 0


        wx.Panel.__init__(self, parent)

        wx.StaticText(self, -1, "기본정보 입력", (constant.XSTART, constant.WIDGET_H))
        wx.StaticText(self, -1, "시간표 작성 대상 교수님의 수는?", (constant.XSTART, constant.NUMBERQUESTION_Y))
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        cb = wx.ComboBox(self, pos=(constant.XSTART+230, constant.NUMBERQUESTION_Y), choices=numbers, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)

        wx.StaticText(self, -1, "사용 가능한 실습실의 수는?", (constant.XSTART+400, constant.NUMBERQUESTION_Y))
        classroomnumbers = ['1', '2', '3', '4', '5']
        cbClassRoom = wx.ComboBox(self, pos=(constant.XSTART+400+200, constant.NUMBERQUESTION_Y), choices=classroomnumbers, style=wx.CB_READONLY)
        cbClassRoom.Bind(wx.EVT_COMBOBOX, self.OnClassRoomSelect)


        self.labelName = wx.StaticText(self, -1, "성함", (constant.XSTART+constant.PROF_NAME_INDENT, constant.DATA_CATEGORY_LINE))
        self.labelName = wx.StaticText(self, -1, "과목수", (constant.XSTART+constant.PROF_NCLASS_INDENT, constant.DATA_CATEGORY_LINE))

        for i in range(8) :
            self.labelName = wx.StaticText(self, -1, "과목명", (constant.XSTART+constant.CLASS_NAME_INDENT+constant.COMBOBOXSIZE+i*constant.CLASSDATASIZE, constant.DATA_CATEGORY_LINE))
            self.labelName = wx.StaticText(self, -1, "시수", (constant.XSTART+constant.CLASS_NAME_INDENT+constant.COMBOBOXSIZE+constant.CLASSNAMESIZE+i*constant.CLASSDATASIZE, constant.DATA_CATEGORY_LINE))
            self.labelName = wx.StaticText(self, -1, "학년", (constant.XSTART+constant.CLASS_NAME_INDENT+constant.COMBOBOXSIZE+constant.CLASSNAMESIZE+constant.COMBOBOXSIZE+i*constant.CLASSDATASIZE, constant.DATA_CATEGORY_LINE))


    def OnClassRoomSelect(self, e):

        self.nClassRoom = int(e.GetString())


        for i in range(self.nProfessors):
            self.ProfInfoArr.append(ProfInfo(self, i+1, constant.XSTART, constant.DATA_CATEGORY_LINE + 50 +i*constant.PROF_DATA_GAP))

    def OnSelect(self, e):

        for i in range(self.nProfessors) :
            self.ProfInfoArr[i].remove()

        del self.ProfInfoArr
        self.ProfInfoArr = []

        self.nProfessors = int(e.GetString())


        for i in range(self.nProfessors):
            self.ProfInfoArr.append(ProfInfo(self, i+1, constant.XSTART, 150+i*50))

    def PrintInfo(self):

        print("실습실 :", self.nClassRoom)


