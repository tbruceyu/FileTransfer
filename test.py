# -*- coding: cp936 -*-
import  wx
import win32api
import win32con
class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mCheckBoxes = {}
        self.mCheckBoxes["PopWindow"] = wx.CheckBox(self, 1, "Pop Window", (35, 40), (150, 20))
        self.mCheckBoxes["BackupMode"] = wx.CheckBox(self, 2, "Backup mode", (35, 60), (150, 20))
        self.mCheckBoxes["RunOnStartup"] = wx.CheckBox(self, 3, "Run on startup", (35, 80), (150, 20))
        self.mStartButton = wx.Button(self, 1, "Start", pos=(0, 100))
        self.mStopButton = wx.Button(self, 2, "Stop", pos=(90, 100))
        self.mStopButton.Disable()
        self.Bind(wx.EVT_BUTTON, self.onStartClick, self.mStartButton)
        self.Bind(wx.EVT_BUTTON, self.onStopClick, self.mStopButton)
    def onStartClick(self, event):
        for (key, checkBox) in self.mCheckBoxes.items():
            checkBox.Disable()
        self.mStartButton.Disable()
        self.mStopButton.Enable()
        #self.button.SetLabel("Clicked")
    def onStopClick(self, event):
        for (key, checkBox) in self.mCheckBoxes.items():
            checkBox.Enable()
        self.mStartButton.Enable()
        self.mStopButton.Disable()

class TaskBarIcon(wx.TaskBarIcon):
    ID_Play = wx.NewId()
    ID_About = wx.NewId()
    ID_Minshow=wx.NewId()
    ID_Maxshow=wx.NewId()
    ID_Closeshow=wx.NewId()

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='resource/wx.ico', type=wx.BITMAP_TYPE_ICO), 'system panel')
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnPlay, id=self.ID_Play)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnMinshow, id=self.ID_Minshow)
        self.Bind(wx.EVT_MENU, self.OnMaxshow, id=self.ID_Maxshow)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()

    def OnPlay(self, event):
        wx.MessageBox('a demo', 'demo')

    def OnAbout(self,event):
        wx.MessageBox('demo', 'about')

    def OnMinshow(self,event):
        self.frame.Iconize(True)


    def OnMaxshow(self,event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()
        self.frame.Maximize(True)

    def OnCloseshow(self,event):
        self.frame.Close(True)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_Play, 'display')
        menu.Append(self.ID_Minshow, 'mix')
        menu.Append(self.ID_Maxshow, 'max')
        menu.Append(self.ID_About, 'about')
        menu.Append(self.ID_Closeshow, 'exit')
        return menu


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Checkbox Example',
                size=(200, 300))
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        self.taskBarIcon = TaskBarIcon(self)
        panel = MainPanel(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)

    def OnHide(self, event):
        self.Hide()
    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()
    def OnClose(self, event):
        self.taskBarIcon.Destroy()
        self.Destroy()


def RunOnStartup():
    key =  win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                    "Software\Microsoft\Windows\CurrentVersion\Run",
                    0,
                    win32con.KEY_ALL_ACCESS
                    )
    #SetValueEx(env,"FileTransferPC",0,REG_SZ,"")
    win32api.RegSetValueEx(key,'FileTransferPC',0,win32con.REG_SZ,'D:\\Program Files\\Console2\\Console.exe')
    print ("create_mvn_env ok!")
if __name__ == '__main__':
    app = wx.App()
    #RunOnStartup()
    frame = MainFrame()
    frame.Centre()
    app.MainLoop()
