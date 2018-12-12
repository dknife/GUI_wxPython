import wx

import constant
import os



class TabRoomInfo(wx.Panel):

    def __init__(self, parent, coreData):
        wx.Panel.__init__(self, parent)

        # data
        self.CoreData = coreData
        parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnTabClicked)

    def OnTabClicked(self, e):

        print(self.CoreData.nProfessors)
        print(self.CoreData.nClassRooms)

