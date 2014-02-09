# -*- coding: cp936 -*-
import wx
class TaskBarIcon(wx.TaskBarIcon):
    ID_Play = wx.NewId()
    ID_About = wx.NewId()
    ID_Minshow=wx.NewId()
    ID_Maxshow=wx.NewId()
    ID_Closeshow=wx.NewId()

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='wx.ico', type=wx.BITMAP_TYPE_ICO), 'ϵͳ������ʾ!')  #wx.icoΪicoͼ���ļ�
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick) #�������˫��
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
        wx.MessageBox('python ʵ�ֳ���ϵͳ���̵�һ����ʾ������ʾ��python2.6������ͨ��!', '��ʾ')

    def OnAbout(self,event):
        wx.MessageBox('ϵͳ������ʾV1.0 python2.x!', '����')

    def OnMinshow(self,event):
        self.frame.Iconize(True)


    def OnMaxshow(self,event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()
        self.frame.Maximize(True) #�����ʾ

    def OnCloseshow(self,event):
        self.frame.Close(True)

    # �Ҽ��˵�
    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_Play, '��ʾ')
        menu.Append(self.ID_Minshow, '��С��')
        menu.Append(self.ID_Maxshow, '���')
        menu.Append(self.ID_About, '����')
        menu.Append(self.ID_Closeshow, '�˳�')
        return menu

class Frame(wx.Frame):
    def __init__(
            self, parent=None, id=wx.ID_ANY, title='TaskBarIcon', pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)


        self.SetIcon(wx.Icon('wx.ico', wx.BITMAP_TYPE_ICO))
        panel = wx.Panel(self, wx.ID_ANY)
        staticText = wx.StaticText(panel,wx.ID_ANY,label=u'HELLO WORLD', pos=wx.Point(88, 152), size=wx.Size(200, 100))
        staticText.SetFont(wx.Font(26, wx.SWISS, wx.NORMAL, wx.NORMAL,False, u'Tahoma'))
        staticText.SetForegroundColour(wx.Colour(255, 0, 0))


        sizer = wx.BoxSizer()
        sizer.Add(staticText, -1,wx.TOP|wx.LEFT,200)
        panel.SetSizer(sizer)
        self.taskBarIcon = TaskBarIcon(self)



        # ���¼�
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy) # ������С��ʱ������OnIconfiy,ע��Wx�����ϵ���С����ť���������¼��� wx.EVT_ICONIZE,��������û�ж���ʲôwx.EVT_MINIMIZE,������󻯣��и�wx.EVT_MAXIMIZE��

    def OnHide(self, event):
        self.Hide()
    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()
    def OnClose(self, event):
        self.taskBarIcon.Destroy()
        self.Destroy()

def TestFrame():
    app = wx.PySimpleApp()
    frame = Frame(size=(640, 480))
    frame.Centre()
    frame.Show()
    app.MainLoop()
if __name__ == '__main__':
    TestFrame()

