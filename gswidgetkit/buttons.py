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

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

button_cmd_event, EVT_BUTTON = NewCommandEvent()


class Button(wx.Control):
    def __init__(self, parent, id=wx.ID_ANY, label="", bmp=None, center=True, 
                pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER, 
                *args, **kwargs):
        wx.Control.__init__(self, parent, id, pos, size, style, *args, **kwargs)

        self.parent = parent

        # Add spaces around a button with text
        if label != "":
            self.label = " {} ".format(label)
            self.padding = (10, 20, 10, 20)
        else:
            # Icon button
            self.label = label
            self.padding = (10, 10, 10, 10)
              
        self.buffer = None
        self.center = center
        self.size = None
        self.bmp = bmp

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

        if self.mouse_down:
            dc.SetBrush(wx.Brush(wx.Colour("#5680C2")))

        elif self.mouse_in:
            dc.SetBrush(wx.Brush(wx.Colour("#4C4C4C")))

        else:
            dc.SetBrush(wx.Brush(wx.Colour("#333333")))

        dc.DrawRoundedRectangle(0, 0, w, h, 4)

        txt_w, txt_h = dc.GetTextExtent(self.label)

        if self.bmp is not None:
            bmp = self.bmp
            bmp_w, bmp_h = bmp[0].GetSize()
            position = bmp[1]
        else:
            bmp = False

        if bmp:

            if position == 'left':
                if self.center:
                    bmp_x = (w - txt_w - bmp_w) / 2
                    bmp_y = (h - bmp_h) / 2

                    txt_x = (w - txt_w - bmp_w) / 2 + bmp_w
                    txt_y = (h - txt_h) / 2
                else:
                    bmp_x = self.padding[3]
                    bmp_y = self.padding[0]

                    txt_x = self.padding[3] + bmp_w
                    if bmp_h > txt_h:
                        txt_y = (bmp_h - txt_h) / 2 + self.padding[0]
                    else:
                        txt_y = self.padding[0]

            if position == 'right':
                if self.center:
                    bmp_x = (w - txt_w - bmp_w) / 2 + txt_w
                    bmp_y = (h - bmp_h) / 2

                    txt_x = (w - txt_w - bmp_w) / 2
                    txt_y = (h - txt_h) / 2
                else:
                    bmp_x = self.padding[3] + txt_w
                    bmp_y = self.padding[0]

                    txt_x = self.padding[3]
                    if bmp_h > txt_h:
                        txt_y = (bmp_h - txt_h) / 2 + self.padding[0]
                    else:
                        txt_y = self.padding[0]

            elif position == 'top':
                if self.center:
                    bmp_x = (w - bmp_w) / 2
                    bmp_y = (h - bmp_h - txt_h) / 2

                    txt_x = (w - txt_w) / 2
                    txt_y = (h - bmp_h - txt_h) / 2 + bmp_h
                else:
                    if bmp_w > txt_w:
                        bmp_x = self.padding[3]
                        bmp_y = self.padding[0]

                        txt_x = (bmp_w - txt_w) / 2 + self.padding[3]
                        txt_y = self.padding[0] + bmp_h
                    else:
                        bmp_x = (txt_w - bmp_w) / 2 + self.padding[3]
                        bmp_y = self.padding[0]

                        txt_x = self.padding[3]
                        txt_y = self.padding[0] + bmp_h

            elif position == 'bottom':
                if self.center:
                    bmp_x = (w - bmp_w) / 2
                    bmp_y = (h - txt_h - bmp_h) / 2 + txt_h

                    txt_x = (w - txt_w) / 2
                    txt_y = (h - txt_h - bmp_h) / 2
                else:
                    if bmp_w > txt_w:
                        bmp_x = self.padding[3]
                        bmp_y = self.padding[0] + txt_h

                        txt_x = (bmp_w - txt_w) / 2 + self.padding[3]
                        txt_y = self.padding[0]
                    else:
                        bmp_x = (txt_w - bmp_w) / 2 + self.padding[3]
                        bmp_y = self.padding[0] + txt_h

                        txt_x = self.padding[3]
                        txt_y = self.padding[0]

            dc.DrawBitmap(bmp[0], int(bmp_x), int(bmp_y))
        else:
            if self.center:
                txt_x = (w - txt_w) / 2
                txt_y = (h - txt_h) / 2
            else:
                txt_x = self.padding[3]
                txt_y = self.padding[0]

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
        self.SendButtonEvent()
        self.UpdateDrawing()

    def SendButtonEvent(self):
        wx.PostEvent(self, button_cmd_event(id=self.GetId(), value=0))

    def DoGetBestSize(self):
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

        dc = wx.ClientDC(self)
        dc.SetFont(font)

        txt_w, txt_h = dc.GetTextExtent(self.label)

        if self.bmp is not None:
            bmp = self.bmp
            bmp_w, bmp_h = bmp[0].GetSize()
            position = bmp[1]
        else:
            bmp = False

        if bmp:
            if position == 'left' or position == 'right':
                if bmp_h > txt_h:
                    size = (self.padding[3] + bmp_w + txt_w + self.padding[1],
                            self.padding[0] + bmp_h + self.padding[2])
                else:
                    size = (self.padding[3] + bmp_w + txt_w + self.padding[1],
                            self.padding[0] + txt_h + self.padding[2])
            else:
                if bmp_w > txt_w:
                    size = (self.padding[3] + bmp_w + self.padding[1],
                            self.padding[0] + bmp_h + txt_h + self.padding[2])
                else:
                    size = (self.padding[3] + txt_w + self.padding[1],
                            self.padding[0] + bmp_h + txt_h + self.padding[2])
        else:
            size = (self.padding[3] + txt_w + self.padding[1],
                    self.padding[0] + txt_h + self.padding[2])

        return wx.Size(size)


class TestAppFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((900, 400))

        sz = wx.BoxSizer(wx.VERTICAL)

        ctrl1 = Button(self, label="Contrast", 
                        bmp=(wx.Bitmap('test_icon.png'), 'left'))
        ctrl2 = Button(self, label="Render Image")
        ctrl3 = Button(self, label="Contrast", 
                        bmp=(wx.Bitmap('test_icon.png'), 'top'))
        ctrl4 = Button(self, label="", 
                        bmp=(wx.Bitmap('test_icon.png'), 'left'))

        sz.Add(ctrl1, flag=wx.EXPAND, border=20)
        sz.Add(ctrl2, border=20)
        sz.Add(ctrl3, border=20)
        sz.Add(ctrl4, border=20)

        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl1)
        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl2)
        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl3)
        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl4)

        self.SetSizer(sz)

    def OnButtonClick(self, event):
        print("button clicked")


if __name__ == "__main__":
    app = wx.App(False)
    frame = TestAppFrame(None, wx.ID_ANY, "Buttons")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()