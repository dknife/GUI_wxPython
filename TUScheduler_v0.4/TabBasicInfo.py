import wx
import constant
import os

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
        self.label4= wx.StaticText(parent, -1, "분반", (XCoord+constant.CLASSNAMESIZE, pos[1] + 25))
        self.Multi = wx.ComboBox(parent, -1, "", (XCoord+constant.CLASSNAMESIZE+30, pos[1] + 25), choices=nHoursChoices, size=(constant.COMBOBOXSIZE, constant.WIDGET_H))
        self.Multi.SetValue('1')
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
        self.label4.Hide()
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

        self.nClassCombo = wx.ComboBox(parent, pos=(x+constant.PROF_NCLASS_INDENT, y), size=(50,20), choices=nClassChoices, style=wx.CB_READONLY)
        self.nClassCombo.SetValue('0')
        self.nClassCombo.Bind(wx.EVT_COMBOBOX, self.OnSelectNClass)
        self.ClassArr = []



    def OnSelectNClass(self, e):

        nClassInput = int(e.GetString())
        if nClassInput == self.nClass: return
        elif nClassInput < self.nClass:
            for i in range(nClassInput, self.nClass) :
                self.ClassArr[i].remove()
            del self.ClassArr[nClassInput:self.nClass]
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

    def __init__(self, parent, coreData):
        # data
        self.nProfessors = 0
        self.ProfInfoArr = []
        self.nClassRooms = 0
        self.ClassUnits = []
        self.bDataGebSuccess = False
        self.CoreData = coreData


        wx.Panel.__init__(self, parent)

        wx.StaticText(self, -1, "기본정보 입력", (constant.XSTART, constant.WIDGET_H))
        wx.StaticText(self, -1, "시간표 작성 대상 교수님의 수는?", (constant.XSTART, constant.NUMBERQUESTION_Y))
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        self.cbNProf = wx.ComboBox(self, pos=(constant.XSTART+230, constant.NUMBERQUESTION_Y), choices=numbers, style=wx.CB_READONLY)
        self.cbNProf.SetValue('0')
        self.cbNProf.Bind(wx.EVT_COMBOBOX, self.OnSelect)

        wx.StaticText(self, -1, "사용 가능한 실습실의 수는?", (constant.XSTART+400, constant.NUMBERQUESTION_Y))
        classroomnumbers = ['1', '2', '3', '4', '5']
        self.cbClassRoom = wx.ComboBox(self, pos=(constant.XSTART+400+200, constant.NUMBERQUESTION_Y), choices=classroomnumbers, style=wx.CB_READONLY)
        self.cbClassRoom.SetValue('0')
        self.cbClassRoom.Bind(wx.EVT_COMBOBOX, self.OnClassRoomSelect)

        self.labelName = wx.StaticText(self, -1, "성함", (constant.XSTART+constant.PROF_NAME_INDENT, constant.DATA_CATEGORY_LINE))
        self.labelName = wx.StaticText(self, -1, "과목수                   * 이론수업은 실습실이 아닌 일반 강의실로 배정해도 무방한 강의입니다.",
                                       (constant.XSTART+constant.PROF_NCLASS_INDENT, constant.DATA_CATEGORY_LINE))

        self.StoreDataButton = wx.Button(self, wx.ID_ANY, "현재 입력 저장", pos=(constant.XSTART + 100, constant.WIDGET_H-10), size=(200, 30), style=0)
        self.StoreDataButton.Bind(wx.EVT_BUTTON, self.OnStoreData)
        self.LoadDataButton = wx.Button(self, wx.ID_ANY, "불러오기", pos=(constant.XSTART + 300, constant.WIDGET_H-10), size=(200, 30), style=0)
        self.LoadDataButton.Bind(wx.EVT_BUTTON, self.OnLoadData)

        self.ClassInfoMsg = wx.StaticText(self, -1, "개설 강의 정보 미생성", (constant.XSTART, constant.DATA_CATEGORY_LINE+50))

        parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnSetData)

    def OnClassRoomSelect(self, e):

        self.nClassRooms = int(e.GetString())
        self.CoreData.nClassRooms = self.nClassRooms
        

    def OnLoadData(self, e):

        openFileDialog = wx.FileDialog(self, "Load Class Data:", ".", "", "class units data (*.cud)|*.cud", wx.FD_OPEN)

        openFileDialog.ShowModal()
        filePath = openFileDialog.GetPath()
        openFileDialog.Destroy()

        if filePath is '': return

        size = os.path.getsize(filePath)
        if size == 0 :
            msg = "파일의 내용이 없습니다."
            self.ClassInfoMsg.SetLabel(msg)
            self.ClassInfoMsg.SetForegroundColour((255, 0, 0))
            return
        else:
            print(size)

        file = open(filePath, "r")
        nProf = int(next(file).rstrip())
        nClassRoom = int(next(file))
        self.cbNProf.SetValue(str(nProf))
        self.nClassRooms = nClassRoom
        self.CoreData.nClassRooms = self.nClassRooms
        self.cbClassRoom.SetValue(str(nClassRoom))

        if nProf<1:
            msg = "파일 읽기 오류: 교수 수를 찾을 수 없습니다"
            self.ClassInfoMsg.SetLabel(msg)
            self.ClassInfoMsg.SetForegroundColour((255, 0, 0))

        # remove current class units
        for i in range(self.nProfessors) :
            self.ProfInfoArr[i].remove()
        del self.ProfInfoArr
        self.ProfInfoArr = []
        self.nProfessors = nProf
        self.CoreData.nProfessors = nProf

        for i in range(0, nProf):
            self.ProfInfoArr.append(ProfInfo(self, i+1, constant.XSTART, constant.DATA_CATEGORY_LINE+50+i*constant.PROF_DATA_GAP))
            name = next(file).rstrip()
            self.ProfInfoArr[i].Name.SetValue(name)
            nClass = int(next(file))
            self.ProfInfoArr[i].nClass = nClass
            self.ProfInfoArr[i].nClassCombo.SetValue(str(nClass))
            for j in range(0, nClass) :
                self.ProfInfoArr[i].ClassArr.append(ClassData(self, j, (self.ProfInfoArr[i].pos[0] + constant.CLASSGAP, self.ProfInfoArr[i].pos[1])))
                self.ProfInfoArr[i].ClassArr[j].ClassName.SetValue(next(file).rstrip())
                hours = int(next(file))
                self.ProfInfoArr[i].ClassArr[j].Hours.SetValue(str(hours))
                grade = int(next(file))
                self.ProfInfoArr[i].ClassArr[j].Grade.SetValue(str(grade))
                theory = int(next(file))
                if theory == 0:
                    self.ProfInfoArr[i].ClassArr[j].Theory.SetValue(False)
                else:
                    self.ProfInfoArr[i].ClassArr[j].Theory.SetValue(True)
                multi = int(next(file))
                self.ProfInfoArr[i].ClassArr[j].Multi.SetValue(str(multi))

        self.ClassInfoMsg.SetPosition((constant.XSTART,constant.DATA_CATEGORY_LINE+30+self.nProfessors*constant.PROF_DATA_GAP + 20))

        self.OnSetData(None)

    def OnStoreData(self, e):

        if self.bDataGebSuccess is False:
            msg = "!!!! 강의 개설 데이터 생성이 완료되지 않았습니다. 저장 데이터는 임시정보입니다."
            self.ClassInfoMsg.SetLabel(msg)
            self.ClassInfoMsg.SetForegroundColour((255, 0, 0))

        openFileDialog = wx.FileDialog(self, "Save to file:", ".", "", "class units data (*.cud)|*.cud", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

        openFileDialog.ShowModal()
        filePath = openFileDialog.GetPath()
        openFileDialog.Destroy()

        if filePath is '': return

        f = open(filePath, "w")
        f.write(str(self.nProfessors)+"\n")
        f.write(str(self.nClassRooms)+"\n")

        for i in range(self.nProfessors) :
            f.write(self.ProfInfoArr[i].Name.GetValue()+"\n")
            f.write(str(self.ProfInfoArr[i].nClass) + "\n")
            for j in range(self.ProfInfoArr[i].nClass) :
                f.write(self.ProfInfoArr[i].ClassArr[j].ClassName.GetValue()+"\n")
                f.write(self.ProfInfoArr[i].ClassArr[j].Hours.GetValue()+"\n")
                f.write(self.ProfInfoArr[i].ClassArr[j].Grade.GetValue()+"\n")
                if self.ProfInfoArr[i].ClassArr[j].Theory.GetValue() is True :
                    f.write("1\n")
                else: f.write("0\n")
                f.write(self.ProfInfoArr[i].ClassArr[j].Multi.GetValue()+"\n")

        self.OnSetData(None)


    def OnSelect(self, e):

        nProfessorsInput = int(e.GetString())

        if nProfessorsInput == self.nProfessors:
            return
        elif nProfessorsInput < self.nProfessors :
            for i in range(nProfessorsInput, self.nProfessors) :
                self.ProfInfoArr[i].remove()
            del self.ProfInfoArr[nProfessorsInput:self.nProfessors]
        elif nProfessorsInput > self.nProfessors :
            for i in range(self.nProfessors, nProfessorsInput):
                self.ProfInfoArr.append(ProfInfo(self, i+1, constant.XSTART, constant.DATA_CATEGORY_LINE+50+i*constant.PROF_DATA_GAP))
        self.nProfessors = nProfessorsInput
        self.CoreData.nProfessors = self.nProfessors

        self.ClassInfoMsg.SetPosition((constant.XSTART,constant.DATA_CATEGORY_LINE+30+self.nProfessors*constant.PROF_DATA_GAP + 20))



    def OnSetData(self, e):

        print("setting current data")
        msg = "개설 강의 정보: "
        del self.ClassUnits
        self.ClassUnits = []
        self.bDataGebSuccess = True

        if self.nProfessors == 0 :
            self.bDataGebSuccess = False
            eMsg = "교수님 수가 입력되지 않았습니다."
        if self.nClassRooms == 0 :
            self.bDataGebSuccess = False
            eMsg = "실습실 수가 입력되지 않았습니다."
        else :
            for i in range(self.nProfessors) :
                name = self.ProfInfoArr[i].Name.GetValue()
                if name == '':
                    self.bDataGebSuccess = False
                    eMsg = "교수 성함이 입력되지 않았습니다"
                    break
                for j in range(self.ProfInfoArr[i].nClass) :
                    className = self.ProfInfoArr[i].ClassArr[j].ClassName.GetValue()
                    if className == '':
                        self.bDataGebSuccess = False
                        eMsg = name + "교수님의 " + str(j+1) + "번 째 과목명이 입력되지 않았습니다."
                        break
                    hours = int(self.ProfInfoArr[i].ClassArr[j].Hours.GetValue())
                    if hours == 0:
                        self.bDataGebSuccess = False
                        eMsg = name + "교수님의 " + str(j+1) + "번 째 과목 시수가 입력되지 않았습니다."
                        break
                    grade = int(self.ProfInfoArr[i].ClassArr[j].Grade.GetValue())
                    if grade == 0:
                        self.bDataGebSuccess = False
                        eMsg = name + "교수님의 " + str(j+1) + "번 째 과목 대상 학년이 입력되지 않았습니다."
                        break
                    if self.ProfInfoArr[i].ClassArr[j].Theory.GetValue() is True:
                        theory = 1
                    else : theory = 0
                    multi = int(self.ProfInfoArr[i].ClassArr[j].Multi.GetValue())
                    for classMulti in range(multi) :
                        self.ClassUnits.append([i, name, j, className, hours, grade, theory, classMulti])

                if self.bDataGebSuccess is not True:
                    break

        if self.bDataGebSuccess is True:
            msg = "강의 개설 성공 \n총 강의 개설 건수 = " + str(len(self.ClassUnits)) + "\n\n시간표 작성이 가능합니다. 강의 개설 불가 시간을 입력하세요."
            self.ClassInfoMsg.SetLabel(msg)
            self.ClassInfoMsg.SetForegroundColour((0,0,255))
            print(self.ClassUnits)
            self.CoreData.ClassUnits = self.ClassUnits
            self.CoreData.bClassDataFinished = True

        else:
            msg = "!!!! 강의 개설 실패 \n실패 메시지: " + eMsg + "\n\n 아직은 시간표 작성이 불가능합니다. 강의 기본 정보를 완성하세요."
            self.ClassInfoMsg.SetLabel(msg)
            self.ClassInfoMsg.SetForegroundColour((255,0,0))
            self.CoreData.bClassDataFinished = False

        self.CoreData.ProfInfo = self.ProfInfoArr

        if e is not None:
            e.Skip()

