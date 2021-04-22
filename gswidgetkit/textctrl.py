

import wx
from wx import stc

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass


class TextCtrl(stc.StyledTextCtrl):
    def __init__(self, parent, value="", placeholder="", scrollbar=False, style=0, *args, **kwargs):
        stc.StyledTextCtrl.__init__(self, parent, style=style | wx.TRANSPARENT_WINDOW, *args, **kwargs)

        if scrollbar is False:
            self.SetUseVerticalScrollBar(False)
            self.SetUseHorizontalScrollBar(False)
        self.SetCaretWidth(2)
        self.SetCaretForeground("#5680c2")
        self.SetMarginLeft(8)
        self.SetMarginRight(8)
        self.SetMarginWidth(1, 0)
        self.SetEOLMode(stc.STC_EOL_LF)
        self.SetLexer(stc.STC_LEX_NULL)
        self.SetIndent(4)
        self.SetUseTabs(False)
        self.SetTabWidth(4)
        self.SetValue(value)
        self.SetScrollWidth(self.GetSize()[0])
        self.SetScrollWidthTracking(True)
        self.SetSelBackground(True, "#242424")
        self.StyleSetBackground(stc.STC_STYLE_DEFAULT, wx.Colour("#333333"))
        self.StyleSetForeground(stc.STC_STYLE_DEFAULT, wx.Colour("#ffffff"))
        self.StyleSetFont(stc.STC_STYLE_DEFAULT, 
                          wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT))
        self.StyleClearAll()
        self.SetValue(value)


class NativeTextCtrl(wx.TextCtrl):
    def __init__(self, parent, value="", style=wx.BORDER_SIMPLE, *args, **kwargs):
        wx.TextCtrl.__init__(self, parent, value=value, style=style, *args, **kwargs)
        self.SetBackgroundColour(wx.Colour("#333333"))
        self.SetForegroundColour(wx.Colour("#fff"))


if __name__ == "__main__":

    class TestAppFrame(wx.Frame):
        def __init__(self, *args, **kwds):
            kwds["style"] = wx.DEFAULT_FRAME_STYLE
            wx.Frame.__init__(self, *args, **kwds)
            self.SetSize((900, 400))
            self.SetBackgroundColour(wx.Colour("#464646"))

            sz = wx.BoxSizer(wx.VERTICAL)

            ctrl1 = TextCtrl(self, value="", style=wx.BORDER_SIMPLE,
                             placeholder="", size=(-1, 24))
            ctrl2 = NativeTextCtrl(self, size=(-1, 26))

            sz.Add(ctrl1, flag=wx.EXPAND, border=20)
            sz.Add(ctrl2, flag=wx.EXPAND, border=20)

            self.SetSizer(sz)

    app = wx.App(False)
    frame = TestAppFrame(None, wx.ID_ANY, "Textctrl")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
