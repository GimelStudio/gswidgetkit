import wx

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

from gswidgetkit import NumberField, EVT_NUMBERFIELD, EVT_NUMBERFIELD_CHANGE
from gswidgetkit.icons import TEST_ICON


class TestAppFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1100, 600))
        self.SetBackgroundColour(wx.Colour("#464646"))

        sz = wx.BoxSizer(wx.VERTICAL)

        ctrl1 = NumberField(self, default_value=10, label="Resolution",
                            min_value=0, max_value=25, suffix="px")
        ctrl2 = NumberField(self, default_value=98, label="Opacity",
                            min_value=0, max_value=100, suffix="%")

        ctrl3 = NumberField(self, default_value=0, label="Radius",
                            min_value=0, max_value=10, suffix="", show_p=False)

        ctrl4 = NumberField(self, default_value=50, label="X:",
                            min_value=0, max_value=100, suffix="", show_p=False)
        ctrl5 = NumberField(self, default_value=13, label="Y:",
                            min_value=0, max_value=100, suffix="", show_p=False)

        sz.Add(ctrl1, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl2, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl3, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl4, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl5, flag=wx.EXPAND | wx.ALL, border=6)

        self.Bind(EVT_NUMBERFIELD_CHANGE, self.OnFieldChange, ctrl1)
        self.Bind(EVT_NUMBERFIELD, self.OnField, ctrl1)

        self.SetSizer(sz)

    def OnFieldChange(self, event):
        print("->", event.value)

    def OnField(self, event):
        print("->", event.value)


if __name__ == "__main__":
    app = wx.App(False)
    frame = TestAppFrame(None, wx.ID_ANY, "GS Widgetkit Demo")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
