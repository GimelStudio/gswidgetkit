# ----------------------------------------------------------------------------
# GS Widget Kit Copyright 2021 by Noah Rahm and contributors
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
from wx.lib.newevent import NewCommandEvent
import wx.lib.agw.cubecolourdialog as colordialog

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

try:
    from .icons import ICON_BRUSH_CHECKERBOARD
except:
    from icons import ICON_BRUSH_CHECKERBOARD

button_cmd_event, EVT_BUTTON = NewCommandEvent()


class ColorPickerButton(wx.Control):
    def __init__(self, parent, id=wx.ID_ANY, label="", default=(213, 219, 213, 177),
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER, 
                 *args, **kwargs):
        wx.Control.__init__(self, parent, id, pos, size, style, *args, **kwargs)

        self.parent = parent

        self.cur_color = default

        self.label = label
        self.padding = (10, 20, 10, 20)
        self.outer_padding = 4
 
        self.buffer = None
        self.size = None

        self.mouse_in = False
        self.mouse_down = False
        self.focused = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
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
        dc.SetPen(wx.TRANSPARENT_PEN)

        w, h = self.GetSize()

        txt_w, txt_h = dc.GetTextExtent(self.label)

        txt_x = self.padding[3] + self.outer_padding
        txt_y = self.padding[0] + self.outer_padding

        txt_w = txt_w + self.padding[1] + self.padding[3]

        dc.SetBrush(wx.Brush(ICON_BRUSH_CHECKERBOARD.GetBitmap()))
        dc.DrawRoundedRectangle(txt_w+self.outer_padding, 
                                self.outer_padding, 
                                w-txt_w-self.outer_padding*2, 
                                h-(self.outer_padding*2), 4)

        dc.SetBrush(wx.Brush(wx.Colour(self.cur_color)))
        dc.DrawRoundedRectangle(txt_w+self.outer_padding, 
                                self.outer_padding, 
                                w-txt_w-self.outer_padding*2, 
                                h-(self.outer_padding*2), 4)

        # Text color
        if self.mouse_down or self.focused or self.mouse_in:
            dc.SetTextForeground(wx.Colour("#fff"))
        else:
            dc.SetTextForeground(wx.Colour("#e9e9e9"))

        # Draw text
        dc.DrawText(self.label, int(txt_x), int(txt_y))

    def OnSetFocus(self, event):
        self.focused = True
        self.Refresh()

    def OnKillFocus(self, event):
        self.focused = False
        self.Refresh()

    def OnMouseEnter(self, event):
        self.mouse_in = True
        self.UpdateDrawing()

    def OnMouseLeave(self, event):
        self.mouse_in = False
        self.UpdateDrawing()

    def OnMouseDown(self, event):
        self.mouse_down = True
        self.SetFocus()
        self.UpdateDrawing()

    def OnMouseUp(self, event):
        self.mouse_down = False
        self.ShowDialog()
        self.SendButtonEvent()
        self.UpdateDrawing()

    def SendButtonEvent(self):
        wx.PostEvent(self, button_cmd_event(id=self.GetId(), value=self.cur_color))

    def ShowDialog(self):
        self.color_data = wx.ColourData()
        self.color_data.SetColour(self.cur_color)
        self.color_dialog = colordialog.CubeColourDialog(None, self.color_data)
        if self.color_dialog.ShowModal() == wx.ID_OK:
            self.color_data = self.color_dialog.GetColourData()
            self.cur_color = self.color_data.GetColour()
        self.color_dialog.Destroy()

    def DoGetBestSize(self):
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

        dc = wx.ClientDC(self)
        dc.SetFont(font)

        txt_w, txt_h = dc.GetTextExtent(self.label)

        size = (self.padding[3] + txt_w + self.padding[1] + self.outer_padding*2,
                self.padding[0] + txt_h + self.padding[2] + self.outer_padding*2)

        return wx.Size(size)


if __name__ == "__main__":
    class TestAppFrame(wx.Frame):
        def __init__(self, *args, **kwds):
            kwds["style"] = wx.DEFAULT_FRAME_STYLE
            wx.Frame.__init__(self, *args, **kwds)
            self.SetSize((900, 400))
            self.SetBackgroundColour(wx.Colour("#464646"))

            sz = wx.BoxSizer(wx.VERTICAL)

            ctrl1 = ColorPickerButton(self, label="Background Color:")
            ctrl2 = ColorPickerButton(self, label="Highlight Color:", 
                                        default=(0, 54, 78, 215))
            ctrl3 = ColorPickerButton(self, label="Text Color:", 
                                        default=(255, 255, 255, 255))

            sz.Add(ctrl1, flag=wx.EXPAND, border=20)
            sz.Add(ctrl2, flag=wx.EXPAND, border=20)
            sz.Add(ctrl3, flag=wx.EXPAND, border=20)

            self.Bind(EVT_BUTTON, self.OnColorChosen, ctrl1)
            self.Bind(EVT_BUTTON, self.OnColorChosen, ctrl2)
            self.Bind(EVT_BUTTON, self.OnColorChosen, ctrl3)

            self.SetSizer(sz)

        def OnColorChosen(self, event):
            print("Color selected: ", event.value)

    app = wx.App(False)
    frame = TestAppFrame(None, wx.ID_ANY, "Color Picker")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
    