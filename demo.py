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

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

from gswidgetkit import (NumberField, EVT_NUMBERFIELD,
                         EVT_NUMBERFIELD_CHANGE, NativeTextCtrl,
                         TextCtrl, ColorPickerButton, EVT_BUTTON,
                         Button, CheckBox, ToolTip)
from gswidgetkit.icons import ICON_TEST


class TestAppFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((600, 800))
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

        ctrl6 = TextCtrl(self, value="", style=wx.BORDER_SIMPLE,
                            placeholder="", size=(-1, 24))
        ctrl7 = NativeTextCtrl(self, size=(-1, 26))

        ctrl8 = ColorPickerButton(self, label="Background Color:")
        ctrl9 = ColorPickerButton(self, label="Highlight Color:",
                                    default=(0, 54, 78, 215))
        ctrl10 = ColorPickerButton(self, label="Text Color:",
                                    default=(255, 255, 255, 255))

        ctrl11 = Button(self, label="Contrast",
                        bmp=(ICON_TEST.GetBitmap(), 'left'))
        ToolTip("Contrast", """Adjusts the degree of difference between the lightest
and darkest parts of a picture.""", target=ctrl11, footer="Shortcut: Ctrl+S")

        ctrl12 = Button(self, label="Render Image")
        ctrl13 = Button(self, label="Contrast",
                        bmp=(ICON_TEST.GetBitmap(), 'top'))
        ctrl14 = Button(self, label="Choose Layer",
                        bmp=(ICON_TEST.GetBitmap(), 'left'))

        sz2 = wx.BoxSizer(wx.HORIZONTAL)

        ctrl15 = Button(self, label="",
                        bmp=(ICON_TEST.GetBitmap(), 'left'))
        ctrl16 = Button(self, label="",
                        bmp=(ICON_TEST.GetBitmap(), 'left'))
        ctrl17 = Button(self, label="",
                        bmp=(ICON_TEST.GetBitmap(), 'left'))
        ctrl18 = Button(self, label="",
                        bmp=(ICON_TEST.GetBitmap(), 'left'))

        ctrl19 = CheckBox(self, label="Auto Render")

        sz2.Add(ctrl15, flag=wx.EXPAND | wx.ALL, border=6)
        sz2.Add(ctrl16, flag=wx.EXPAND | wx.ALL, border=6)
        sz2.Add(ctrl17, flag=wx.EXPAND | wx.ALL, border=6)
        sz2.Add(ctrl18, flag=wx.EXPAND | wx.ALL, border=6)
        sz2.Add(ctrl19, flag=wx.EXPAND | wx.ALL, border=6)

        sz.Add(ctrl1, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl2, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl3, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl4, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl5, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl6, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl7, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl8, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl9, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl10, flag=wx.EXPAND | wx.ALL, border=6)

        sz.Add(ctrl11, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl12, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl13, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(ctrl14, flag=wx.EXPAND | wx.ALL, border=6)
        sz.Add(sz2, border=20)

        self.SetSizer(sz)

        # Events
        self.Bind(EVT_NUMBERFIELD_CHANGE, self.OnFieldChange, ctrl1)
        self.Bind(EVT_NUMBERFIELD, self.OnField, ctrl1)
        self.Bind(EVT_BUTTON, self.OnColorChosen, ctrl8)
        self.Bind(EVT_BUTTON, self.OnColorChosen, ctrl9)
        self.Bind(EVT_BUTTON, self.OnColorChosen, ctrl10)
        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl11)
        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl12)
        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl13)
        self.Bind(EVT_BUTTON, self.OnButtonClick, ctrl14)


    def OnFieldChange(self, event):
        print("->", event.value)

    def OnField(self, event):
        print("->", event.value)

    def OnColorChosen(self, event):
        print("Color selected: ", event.value)

    def OnButtonClick(self, event):
        print("Button clicked: ", event.GetId())


if __name__ == "__main__":
    app = wx.App(False)
    frame = TestAppFrame(None, wx.ID_ANY, "GS Widgetkit Demo")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
