#!/usr/bin/python

# customdialog1.py

import wx

class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(350,300))

        sizer =  self.CreateTextSizer('My Buttons')
        sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL, 5)
        sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL, 5)
        sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL, 5)
        sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL|wx.ALIGN_CENTER, 5)
        sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(550,500))

        panel = wx.Panel(self, -1)
        wx.Button(panel, 1, 'Show Custom Dialog', (100,100))
        self.Bind (wx.EVT_BUTTON, self.OnShowCustomDialog, id=1)

    def OnShowCustomDialog(self, event):
        dia = MyDialog(self, -1, 'buttons')
        dia.ShowModal()
        dia.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'customdialog1.py')
        frame.Show(True)
        frame.Centre()
        return True

app = MyApp(0)
app.MainLoop()
