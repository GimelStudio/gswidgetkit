# ----------------------------------------------------------------------------
# gswidgetkit Copyright 2021 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

import wx
from wx import stc


class StyledTextCtrl(stc.StyledTextCtrl):
    def __init__(self, parent, value="", placeholder="", scrollbar=False,
                 style=0, bg_color="#333333", sel_color="#5680C2", *args, **kwargs):
        stc.StyledTextCtrl.__init__(self, parent, style=style | wx.TRANSPARENT_WINDOW, *args, **kwargs)

        if scrollbar is False:
            self.SetUseVerticalScrollBar(False)
            self.SetUseHorizontalScrollBar(False)
        self.SetCaretWidth(2)
        self.SetCaretForeground(sel_color)
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
        self.SetSelBackground(True, sel_color)
        self.StyleSetBackground(stc.STC_STYLE_DEFAULT, wx.Colour(bg_color))
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


class TextCtrl(wx.Control):
    def __init__(self, parent, default="", icon=None, size=wx.DefaultSize):
        wx.Control.__init__(self, parent, wx.ID_ANY, pos=wx.DefaultPosition,
                            size=size, style=wx.NO_BORDER)

        self.parent = parent
        self.focused = False
        self.mouse_in = False
        self.control_size = wx.DefaultSize
        self.buffer = None

        self.value = default
        self.icon = icon

        self.padding_x = 20
        self.padding_y = 30

        # Inner text ctrl
        self.textctrl = StyledTextCtrl(self, value=str(self.value),
                                       style=wx.BORDER_NONE, bg_color="#222222",
                                       sel_color="#5680C2", pos=(0, 0), size=(10, 24))

        self.textctrl.Bind(wx.EVT_KILL_FOCUS, self.OnMouseLeave)
        self.textctrl.Bind(wx.EVT_SET_FOCUS, self.OnFocused)
        self.textctrl.Bind(wx.EVT_CHAR_HOOK, self.OnKey)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, event):
        wx.BufferedPaintDC(self, self.buffer)

    def OnSize(self, event):
        size = self.GetClientSize()

        # Make sure size is at least 1px to avoid
        # strange "invalid bitmap size" errors.
        if size[0] < 1:
            size = (1, 1)
        self.buffer = wx.Bitmap(*size)
        self.UpdateDrawing()

    def UpdateDrawing(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc = wx.GCDC(dc)
        self.OnDrawBackground(dc)
        self.OnDrawWidget(dc)
        del dc  # need to get rid of the MemoryDC before Update() is called.
        self.Refresh()
        self.Update()

    def OnDrawBackground(self, dc):
        dc.SetBackground(wx.Brush(self.parent.GetBackgroundColour()))
        dc.Clear()

    def OnDrawWidget(self, dc):
        fnt = self.parent.GetFont()
        dc.SetFont(fnt)

        width = self.Size[0]
        height = self.Size[1]

        if self.mouse_in:
            dc.SetTextForeground("#ffffff")
            dc.SetPen(wx.Pen(wx.Colour("#5680C2"), 1))
            dc.SetBrush(wx.Brush(wx.Colour("#333333")))
            self.textctrl.StyleSetBackground(stc.STC_STYLE_DEFAULT, wx.Colour("#333333"))
        else:
            dc.SetTextForeground("#e9e9e9")
            dc.SetPen(wx.Pen(wx.Colour("#333333"), 1))
            dc.SetBrush(wx.Brush(wx.Colour("#222222")))
            self.textctrl.StyleSetBackground(stc.STC_STYLE_DEFAULT, wx.Colour("#222222"))
        dc.DrawRoundedRectangle(1, 1, width-1, height-1, 4)

        if self.icon != None:
            dc.DrawBitmap(self.icon, 8, int(self.Size[1]/2) - (self.icon.Height/2))

        # Update position of textctrl
        if self.icon == None:
            self.textctrl.SetPosition((2, (int(self.Size[1]/2) - 10)))
            self.textctrl.SetSize((int(self.Size[0]-4), 20))
        else:
            self.textctrl.SetPosition((self.icon.Width + 4, (int(self.Size[1]/2) - 10)))
            self.textctrl.SetSize((int(self.Size[0]-(self.icon.Width + 4)-4), 20))
        self.textctrl.SetCurrentPos(len(str(self.value)))
        self.textctrl.SelectNone()

    def OnKey(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.mouse_in = False
            self.focused = False
            self.textctrl.SetCurrentPos(len(str(self.value)))
            self.UpdateDrawing()
        else:
            event.Skip()

    def OnFocused(self, event):
        self.mouse_in = True
        event.Skip()
        self.UpdateDrawing()

    def OnSetFocus(self, event):
        self.focused = True
        self.textctrl.SetFocus()
        event.Skip()
        self.Refresh()

    def OnKillFocus(self, event):
        self.focused = False
        event.Skip()
        self.Refresh()

    def OnMouseLeave(self, event):
        self.mouse_in = False
        event.Skip()
        self.Refresh()
        self.UpdateDrawing()

    def AcceptsFocusFromKeyboard(self):
        """Overridden base class virtual."""
        return True

    def AcceptsFocus(self):
        """ Overridden base class virtual. """
        return True

    def HasFocus(self):
        """ Returns whether or not we have the focus. """
        return self.focused

    def GetValue(self):
        return self.value

    def SetValue(self, value):
        self.value = value
        self.textctrl.SetValue(value)

    def SetIcon(self, icon):
        self.icon = icon

    def SetFocus(self):
        self.textctrl.SetFocus()

    def DoGetBestSize(self):
        """
        Overridden base class virtual. Determines the best size of the control.
        """
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        dc = wx.ClientDC(self)
        dc.SetFont(font)

        # Calculate sizing
        totalwidth = self.padding_x + self.textctrl.GetSize()[0] + 130
        totalheight = self.textctrl.GetSize()[1] + self.padding_y

        best = wx.Size(totalwidth, totalheight)

        # Cache the best size so it doesn't need to be calculated again,
        # at least until some properties of the window change
        self.CacheBestSize(best)

        return best
