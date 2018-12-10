import wx

import constant

class ClassData():
    def __init__(self, parent,  i, pos):
        nHoursChoices = ['1', '2', '3', '4']
        GradeChoices = ['1', '2', '3', '4']
        XCoord = constant.CLASS_NAME_INDENT + constant.COMBOBOXSIZE + i * constant.CLASSDATASIZE

        self.label1 = wx.StaticText(parent, -1, "과목명", (XCoord,  pos[1]-18))
        self.ClassName = wx.TextCtrl(parent, -1, "", (XCoord,  pos[1]), size=(constant.CLASSNAMESIZE, constant.WIDGET_H))
        self.label2 = wx.StaticText(parent, -1, "시수", (XCoord + constant.CLASSNAMESIZE, pos[1]-18))
        self.Hours = wx.ComboBox(parent, -1, "", (XCoord + constant.CLASSNAMESIZE, pos[1]), choices=nHoursChoices, size=(constant.COMBOBOXSIZE, constant.WIDGET_H))
        self.Hours.SetValue('0')
        self.label3 = wx.StaticText(parent, -1, "학년", (XCoord + constant.CLASSNAMESIZE+constant.COMBOBOXSIZE, pos[1]-18))
        self.Grade = wx.ComboBox(parent, -1, "", (XCoord + constant.CLASSNAMESIZE+constant.COMBOBOXSIZE, pos[1]), choices=GradeChoices, size=(constant.COMBOBOXSIZE, constant.WIDGET_H))
        self.Grade.SetValue('0')
        self.Theory = wx.CheckBox(parent, -1, label="이론수업", pos=(XCoord,  pos[1]+25))
        self.Multi = wx.ComboBox(parent, -1, "", (XCoord+constant.CLASSNAMESIZE, pos[1] + 25), choices=nHoursChoices, size=(constant.COMBOBOXSIZE, constant.WIDGET_H))
        #wx.CheckBox(parent, -1, label="분반", pos=(XCoord+constant.CLASSNAMESIZE, pos[1] + 25))
        self.ln = wx.StaticLine(parent, -1, wx.Point(XCoord, pos[1] + 43), size=(constant.CLASSDATASIZE*0.9,-1), style=wx.LI_HORIZONTAL)

    def remove(self):
        self.ClassName.Hide()
        self.Hours.Hide()
        self.Grade.Hide()
        self.label1.Hide()
        self.label2.Hide()
        self.label3.Hide()
        self.Theory.Hide()
        self.Multi.Hide()
        self.ln.Hide()


class ProfInfo():
    def __init__(self, parent, i, x, y):
        message ="교수"+str(i)+":"
        self.parent = parent
        self.pos = (x,y)
        self.Label = wx.StaticText(parent, -1, message, (x,y))
        self.Name = wx.TextCtrl(parent, -1, "", (x+constant.PROF_NAME_INDENT, y), size=(constant.PROFNAMEWIDTH,constant.WIDGET_H), style=wx.TE_PROCESS_ENTER)

        nClassChoices = ['1', '2', '3','4', '5', '6', '7', '8', '9', '10']
        self.nClass = 0

        self.nClassCombo = wx.ComboBox(parent, pos=(x+constant.PROF_NCLASS_INDENT, y), choices=nClassChoices, style=wx.CB_READONLY)
        self.nClassCombo.Bind(wx.EVT_COMBOBOX, self.OnSelectNClass)
        self.ClassArr = []



    def OnSelectNClass(self, e):

        nClassInput = int(e.GetString())
        if nClassInput == self.nClass: return
        elif nClassInput < self.nClass:
            for i in range(nClassInput, self.nClass) :
                self.ClassArr[i].remove()
            del self.ClassArr[nClassInput:self.nClass]
            self.nClass = nClassInput
        elif nClassInput > self.nClass:
            for i in range(self.nClass, nClassInput):
                self.ClassArr.append(ClassData(self.parent, i, (self.pos[0] + constant.CLASSGAP, self.pos[1])))
            self.nClass = nClassInput

    def remove(self):
        for i in range(0, self.nClass):
            self.ClassArr[i].remove()
        del self.ClassArr
        self.nClass = 0
        self.Label.Hide()
        self.Name.Hide()
        self.nClassCombo.Hide()



class TabBasicInfo(wx.Panel):

    def __init__(self, parent):
        # data
        self.nProfessors = 0
        self.ProfInfoArr = []
        self.nClassRoom = 0
        self.ClassUnits = []


        wx.Panel.__init__(self, parent)

        wx.StaticText(self, -1, "기본정보 입력", (constant.XSTART, constant.WIDGET_H))
        wx.StaticText(self, -1, "시간표 작성 대상 교수님의 수는?", (constant.XSTART, constant.NUMBERQUESTION_Y))
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        cb = wx.ComboBox(self, pos=(constant.XSTART+230, constant.NUMBERQUESTION_Y), choices=numbers, style=wx.CB_READONLY)
        cb.SetValue('0')
        cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)

        wx.StaticText(self, -1, "사용 가능한 실습실의 수는?", (constant.XSTART+400, constant.NUMBERQUESTION_Y))
        classroomnumbers = ['1', '2', '3', '4', '5']
        cbClassRoom = wx.ComboBox(self, pos=(constant.XSTART+400+200, constant.NUMBERQUESTION_Y), choices=classroomnumbers, style=wx.CB_READONLY)
        cbClassRoom.SetValue('1')
        cbClassRoom.Bind(wx.EVT_COMBOBOX, self.OnClassRoomSelect)

        self.labelName = wx.StaticText(self, -1, "성함(姓銜)", (constant.XSTART+constant.PROF_NAME_INDENT, constant.DATA_CATEGORY_LINE))
        self.labelName = wx.StaticText(self, -1, "과목수                   * 이론수업은 실습실이 아닌 일반 강의실로 배정해도 무방한 강의입니다.", (constant.XSTART+constant.PROF_NCLASS_INDENT, constant.DATA_CATEGORY_LINE))

        self.SetDataButton = wx.Button(self, wx.ID_ANY, "개설 강의 데이터 생성", pos=(constant.XSTART, constant.DATA_CATEGORY_LINE+50), size=(200, 40), style=0)
        self.SetDataButton.Bind(wx.EVT_BUTTON, self.OnSetData)
        self.ClassInfoMsg = wx.StaticText(self, -1, "개설 강의 정보 미생성", (constant.XSTART, constant.DATA_CATEGORY_LINE+50+50))

    def OnClassRoomSelect(self, e):

        self.nClassRoom = int(e.GetString())


    def OnSelect(self, e):

        nProfessorsInput = int(e.GetString())

        if nProfessorsInput == self.nProfessors:
            return
        elif nProfessorsInput < self.nProfessors :
            for i in range(nProfessorsInput, self.nProfessors) :
                self.ProfInfoArr[i].remove()
            del self.ProfInfoArr[nProfessorsInput:self.nProfessors]
            self.nProfessors = nProfessorsInput

        elif nProfessorsInput > self.nProfessors :
            for i in range(self.nProfessors, nProfessorsInput):
                self.ProfInfoArr.append(ProfInfo(self, i+1, constant.XSTART, constant.DATA_CATEGORY_LINE+50+i*constant.PROF_DATA_GAP))
            self.nProfessors = nProfessorsInput

        self.SetDataButton.SetPosition((constant.XSTART,constant.DATA_CATEGORY_LINE+50+self.nProfessors*constant.PROF_DATA_GAP))
        self.ClassInfoMsg.SetPosition((constant.XSTART,constant.DATA_CATEGORY_LINE+50+self.nProfessors*constant.PROF_DATA_GAP + 50))

    def OnSetData(self, e):

        msg = "개설 강의 정보: "
        del self.ClassUnits
        self.ClassUnits = []
        bSuccess = True

        if self.nProfessors == 0 :
            bSuccess = False
            eMsg = "교수님 수가 입력되지 않았습니다."
        else :
            for i in range(self.nProfessors) :
                name = self.ProfInfoArr[i].Name.GetValue()
                if name == '':
                    bSuccess = False
                    eMsg = "교수 성함이 입력되지 않았습니다"
                    break
                for j in range(self.ProfInfoArr[i].nClass) :
                    className = self.ProfInfoArr[i].ClassArr[j].ClassName.GetValue()
                    if className == '':
                        bSuccess = False
                        eMsg = name + "교수님의 " + str(j+1) + "번 째 과목명이 입력되지 않았습니다."
                        break
                    hours = int(self.ProfInfoArr[i].ClassArr[j].Hours.GetValue())
                    if hours == 0:
                        bSuccess = False
                        eMsg = name + "교수님의 " + str(j+1) + "번 째 과목 시수가 입력되지 않았습니다."
                        break
                    grade = int(self.ProfInfoArr[i].ClassArr[j].Grade.GetValue())
                    if grade == 0:
                        bSuccess = False
                        eMsg = name + "교수님의 " + str(j+1) + "번 째 과목 대상 학년이 입력되지 않았습니다."
                        break
                    if self.ProfInfoArr[i].ClassArr[j].Theory.GetValue() is True:
                        theory = 1
                    else : theory = 0
                    multi = self.ProfInfoArr[i].ClassArr[j].Multi.GetValue()
                    if multi is False:
                        self.ClassUnits.append([i, name, j, className, hours, grade, theory, 0])
                    else :
                        self.ClassUnits.append([i, name, j, className, hours, grade, theory, 0])
                        self.ClassUnits.append([i, name, j, className, hours, grade, theory, 1])

        if bSuccess is True:
            msg = "강의 개설 성공 \n총 강의 개설 건수 = " + str(len(self.ClassUnits)) + "\n"
            self.ClassInfoMsg.SetLabel(msg)
            self.ClassInfoMsg.SetForegroundColour((0,0,255))
        else:
            msg = "!!!! 강의 개설 실패 \n실패 메시지: " + eMsg
            self.ClassInfoMsg.SetLabel(msg)
            self.ClassInfoMsg.SetForegroundColour((255,0,0))

