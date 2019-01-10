import wx
import wx.lib.scrolledpanel as scrolled
import random

SCHEDULE_ITEM_W = 100
SCHEDULE_ITEM_H = 50




class Chromosome:
    def __init__(self, nClassRooms):
        self.weekday = random.randint(0,4)
        self.room = random.randint(0,nClassRooms-1)
        self.hour = random.randint(0,8)

    def printInfo(self):
        print(self.weekday, self.room, self.hour)

class Genome:
    def __init__(self, nClassUnits, nClassRooms):
        self.chromosome = [Chromosome(nClassRooms) for i in range(nClassUnits) ]

    def printInfo(self):
        for i in range(0, len(self.chromosome)) :
            self.chromosome[i].printInfo()


class GeneticEvolver:
    def __init__(self, coreData, nPopulation, maxGeneration):
        self.Generation = 0
        self.nPopulation = nPopulation
        self.maxGeneration = maxGeneration

        self.solutionFound = False
        self.CoreData = coreData
        self.GenePool = [Genome(len(self.CoreData.ClassUnits), self.CoreData.nClassRooms) for i in range(nPopulation) ]
        self.Fitness = [ 0.0 ] * nPopulation
        self.BestFitness = -1000000000000000
        self.BestIdx = -1


    def nextGen(self):
        if self.Generation >= self.maxGeneration :
            return

        for i in range(self.nPopulation):
            self.ShuffleGene()

        self.Generation = self.Generation + 1
        for i in range(self.nPopulation) :
            self.Fitness[i] = self.ComputeFitness(self.GenePool[i], self.CoreData)

        # rearrange
        half = int(self.nPopulation/2)
        quater = int(self.nPopulation/4)
        randomOffset = random.randrange(0, quater)

        for i in range(half) :
            offset = (randomOffset+i)%int(half)
            j = self.nPopulation-1-offset
            if self.Fitness[j]>self.Fitness[i]  : # swap
                self.SwapGene(i,j)
                t = self.Fitness[i]
                self.Fitness[i] =self.Fitness[j]
                self.Fitness[j] = t

        # crossover here
        for i in range(0, half, 2) :
            child = self.CrossOver(i, i+1)
            for idx in range(len(self.CoreData.ClassUnits)):
                self.GenePool[half+1+int(i/2)].chromosome[idx] = child[idx]

        # mutate
        for i in range(half+quater, self.nPopulation) :
            self.Mutate(i)


        for i in range(self.nPopulation) :
            self.Fitness[i] = self.ComputeFitness(self.GenePool[i], self.CoreData)

        # Finding the best gene
        self.bestFit = -10000000000.0
        self.bestIdx = -1
        for i in range(0, self.nPopulation):
            if self.Fitness[i] > self.bestFit :
                self.bestFit = self.Fitness[i]
                self.bestIdx = i

    def ShuffleGene(self):
        i = random.randrange(0, self.nPopulation)
        j = random.randrange(0, self.nPopulation)
        if i != j :
            self.SwapGene(i,j)


    def SwapGene(self,i, j):
        iGene = self.GenePool[i].chromosome
        jGene = self.GenePool[j].chromosome
        t = iGene
        self.GenePool[i].chromosome = jGene
        self.GenePool[j].chromosome = t


    def Select(self, a, b, max):
        rVal = random.randrange(0, 10001) % 2
        if rVal == 0 :
            return a%max
        elif rVal == 1 :
            return b%max
        elif rVal == 2:
            return int((a+b)/2)
        else :
            return ((a+b)*rVal*rVal)%max

    def CrossOver(self, i, j):
        iGene = self.GenePool[i].chromosome
        jGene = self.GenePool[j].chromosome
        child = [Chromosome(self.CoreData.nClassRooms) for i in range(len(self.CoreData.ClassUnits))]
        for idx in range(len(iGene)):
            child[idx].weekday = self.Select(iGene[idx].weekday, jGene[idx].weekday, 5)
            child[idx].room = self.Select(iGene[idx].room, jGene[idx].room, self.CoreData.nClassRooms)
            child[idx].hour = self.Select(iGene[idx].hour, jGene[idx].hour, 10-self.CoreData.ClassUnits[idx][4])
        return child

    def Mutate(self, i):
        iGene = self.GenePool[i].chromosome
        for idx in range(len(iGene)):
            rVal = random.randrange(0, 10001)
            iGene[idx].weekday = (iGene[idx].weekday + rVal)%5
            rVal = random.randrange(0, 10001)
            iGene[idx].room = (iGene[idx].room + rVal)%self.CoreData.nClassRooms
            rVal = random.randrange(0, 10001)
            iGene[idx].hour = (iGene[idx].hour + rVal) % (10 - self.CoreData.ClassUnits[idx][4])




    def ComputeFitness(self, gene, data):
        fitness  = 0.0
        slots =  [-1] * 2 * 10 * data.nClassRooms * 5 # 10 hours in nClassRooms for 5 days
        # fitness check slots setting and overlapping test
        for i in range(len(data.ClassUnits)):  # for each chromosome
            day = gene.chromosome[i].weekday
            room = gene.chromosome[i].room
            hour = gene.chromosome[i].hour

            credits = data.ClassUnits[i][4]
            profId = data.ClassUnits[i][0]
            grade = data.ClassUnits[i][5]

            for h in range(hour, hour + credits):

                if h <= 9:
                    idx1 = day * (2 * 10 * data.nClassRooms) + room * (2 * 10) + (h) * 2
                    idx2 = day * (2 * 10 * data.nClassRooms) + room * (2 * 10) + (h) * 2 + 1
                    curID = slots[idx1]
                    if curID >= 0 :
                        fitness -= 10
                    else:
                        slots[idx1] = profId
                        slots[idx2] = grade
                else:
                    #print("night")
                    fitness -= 10

        # professor and grade check
        return fitness


class TabSolve(wx.Panel):

    def __init__(self, parent, coreData):
        wx.Panel.__init__(self, parent)

        self.bRunning = False

        self.parent = parent
        self.parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnTabClicked)
        self.CoreData = coreData

        self.Msg_DataDone = wx.StaticText(self, -1, "시간표 생성 가능 여부", (100, 50))
        self.CreateButton = wx.Button(self, -1, "시간표 생성", pos=(300,45), size=(100,30))
        self.CreateButton.Bind(wx.EVT_BUTTON, self.OnCreateSchedule)
        self.Msg_ProfInfo = wx.StaticText(self, -1, "교수정보", (100, 90))

        self.ScheduleViewPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(1350, 600), pos=(0, 130),
                                                                style=wx.SIMPLE_BORDER)
        self.ScheduleViewPanel.SetupScrolling()
        self.ScheduleViewPanel.SetBackgroundColour('#CCCCCC')

        self.Bind(wx.EVT_IDLE, self.OnIdle)


    def OnIdle(self, e):
        if self.bRunning:
            self.evolover.nextGen()
            self.drawScheduleFrame()
            self.drawGenome(self.evolover.GenePool[self.evolover.bestIdx], self.ScheduleViewPanel)
            #print('best gene fitness = ', self.evolover.bestFit, self.evolover.bestIdx)
            if self.evolover.Generation >= self.evolover.maxGeneration :
                self.bRunning = False


    def OnCreateSchedule(self, e):
        self.evolover = GeneticEvolver(self.CoreData, 500, 100)
        self.bRunning = True


    def drawGenome(self, gene, panel):

        profColors = [
            '#DDDDDD','#CCCCFF','#CCFFCC','#FFCCCC','#FFFFCC','#CCFFFF','#FFCCFF','#FFFFFF','#CFADFC','#DFEABC'
        ]
        for i in range(len(gene.chromosome)) :
            day = gene.chromosome[i].weekday
            room = gene.chromosome[i].room
            hour = gene.chromosome[i].hour
            profId = self.CoreData.ClassUnits[i][0]
            name = self.CoreData.ClassUnits[i][1]
            className = self.CoreData.ClassUnits[i][3]
            credits = self.CoreData.ClassUnits[i][4]
            grade = self.CoreData.ClassUnits[i][5]

            unit = wx.StaticText(panel, -1, className+"\n"+name +"\n"+str(grade)+"학년/"+str(credits)+"시간",
                          pos=(SCHEDULE_ITEM_W + 10 + SCHEDULE_ITEM_W*self.CoreData.nClassRooms*day + SCHEDULE_ITEM_W*room, SCHEDULE_ITEM_H*2 + hour*SCHEDULE_ITEM_H),
                          size=(SCHEDULE_ITEM_W - 10, SCHEDULE_ITEM_H * credits))
            line = wx.StaticText(panel, -1, '',
                                 pos=(
                                 SCHEDULE_ITEM_W + SCHEDULE_ITEM_W * self.CoreData.nClassRooms * day + SCHEDULE_ITEM_W * room,
                                 SCHEDULE_ITEM_H * 2 + hour * SCHEDULE_ITEM_H),
                                 size=(10, SCHEDULE_ITEM_H * credits))
            unit.SetBackgroundColour(profColors[profId%10])
            line.SetBackgroundColour(profColors[(profId+2) % 10])
            unit.SetTransparent(0.75)
            unit.Wrap(2)



    def drawScheduleFrame(self):
        self.ScheduleViewPanel.Destroy()
        self.ScheduleViewPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(1350, 650), pos=(0, 130),
                                                                    style=wx.SIMPLE_BORDER)
        self.ScheduleViewPanel.SetBackgroundColour('#CCCCCC')

        weekDays = ['월', '화', '수', '목', '금']
        weekColors = ['#00FFFF', '#FFFF00', '#00FF00', '#FFAAFF', '#FFFFAA']
        for i in range(len(weekDays)):
            wday = wx.StaticText(self.ScheduleViewPanel, -1, weekDays[i],
                                 pos=(SCHEDULE_ITEM_W + SCHEDULE_ITEM_W * self.CoreData.nClassRooms * i, 0),
                                 size=(SCHEDULE_ITEM_W * self.CoreData.nClassRooms, SCHEDULE_ITEM_H))
            wday.SetBackgroundColour(weekColors[i])

            for j in range(self.CoreData.nClassRooms):
                room = wx.StaticText(self.ScheduleViewPanel, -1, '강의실 - ' + str(j + 1),
                                     pos=(
                                     SCHEDULE_ITEM_W + 1 + SCHEDULE_ITEM_W * self.CoreData.nClassRooms * i + SCHEDULE_ITEM_W * j,
                                     SCHEDULE_ITEM_H + 1),
                                     size=(SCHEDULE_ITEM_W - 2, SCHEDULE_ITEM_H - 2))
                room.SetBackgroundColour(weekColors[i])

        for i in range(10):
            wx.StaticText(self.ScheduleViewPanel, -1, str(i + 1) + " 교시\n"+str(9+i)+":00 - " + str(10+i) + ":00",
                          pos=(0, SCHEDULE_ITEM_H * (i + 2) + SCHEDULE_ITEM_H * 0.05),
                          size=(SCHEDULE_ITEM_W, SCHEDULE_ITEM_H * 0.9))

        # for i in range(6):  # 5 days a week
        #    wx.StaticLine(self.ScheduleViewPanel, -1, wx.Point(SCHEDULE_ITEM_W+SCHEDULE_ITEM_W*self.CoreData.nClassRooms*i, 0), size=(-1, SCHEDULE_ITEM_W*12), style=wx.LI_VERTICAL)

        for i in range(11):  # 10 class hours
            wx.StaticLine(self.ScheduleViewPanel, -1, wx.Point(0, SCHEDULE_ITEM_H * 2 + (i) * SCHEDULE_ITEM_H),
                          size=(SCHEDULE_ITEM_W * 5 * self.CoreData.nClassRooms + SCHEDULE_ITEM_W, -1), style=wx.LI_HORIZONTAL)

        self.scheduleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ScheduleViewPanel.SetSizer(self.scheduleSizer)
        self.scheduleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scheduleSizer.AddSpacer(5 * SCHEDULE_ITEM_W * (self.CoreData.nClassRooms) + SCHEDULE_ITEM_W)
        self.ScheduleViewPanel.SetSizer(self.scheduleSizer)
        self.ScheduleViewPanel.SetupScrolling()


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

        self.drawScheduleFrame()


        if e is not None:
            e.Skip() # for multiple event handlers