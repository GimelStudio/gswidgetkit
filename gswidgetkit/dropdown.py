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
import wx.lib.agw.flatmenu as flatmenu
from wx.lib.newevent import NewCommandEvent

from .utils import GetTextExtent
from .icons import ICON_DROPDOWN_ARROW

# Max number of items that can be added to the menu is 100
DROPDOWNMENU_ITEM_IDS = wx.NewIdRef(100)

# Create new event for selecting dropdown item
dropdown_cmd_event, EVT_DROPDOWN = NewCommandEvent()


class DropDown(wx.Control):
    def __init__(self, parent, items, default, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, *args,**kwargs):
        wx.Control.__init__(self, parent, id, pos, size, style, *args, **kwargs)
        self.parent = parent
        self.items = items
        self.default = default
        self.value = default
        self.longest_str = max(items, key=len)  # Longest string in the choices

        self.buffer = None
        self.padding_x = 20
        self.padding_y = 10

        self.mouse_in = False
        self.mouse_down = False
        self.focused = False

        self.menuidmapping = {}

        # Init menu
        self.CreateMenu()

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
        dc.SetTextForeground("#ffffff")
        dc.SetPen(wx.TRANSPARENT_PEN)

        w, h = self.GetSize()
        lbl_w, lbl_h = GetTextExtent(self.GetValue())

        if self.mouse_down:
            dc.SetBrush(wx.Brush(wx.Colour("#5680C2")))
        elif self.mouse_in:
            dc.SetBrush(wx.Brush(wx.Colour("#4C4C4C")))
        else:
            dc.SetBrush(wx.Brush(wx.Colour("#333333")))

        dc.DrawRoundedRectangle(0, 0, w, h, 4)
        dc.DrawText(self.GetValue(), self.padding_x, int((h/2) - (lbl_h/2)))
        dc.DrawBitmap(ICON_DROPDOWN_ARROW.GetBitmap(), (w-28), int((h/2) - (lbl_h/2) - 2))

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
        self.OnClick()
        self.UpdateDrawing()

    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of the control
        based on the label size, the bitmap size and the current font.
        """
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        dc = wx.ClientDC(self)
        dc.SetFont(font)

        val_text_w, val_text_h = dc.GetTextExtent(self.longest_str)

        totalwidth = val_text_w + self.padding_x + 65

        totalheight = val_text_h + self.padding_y

        best = wx.Size(totalwidth, totalheight)

        # Cache the best size so it doesn't need to be calculated again,
        # at least until some properties of the window change
        self.CacheBestSize(best)

        return best

    def SetValue(self, value):
        self.value = value

    def GetValue(self):
        return self.value

    def ComputeMenuPos(self, menu):
        y = self.GetSize()[1] + self.GetScreenPosition()[1] + 3
        x = self.GetScreenPosition()[0]
        return wx.Point(x, y)

    def OnClick(self):
        pos = self.ComputeMenuPos(self.dropdown_menu)
        self.dropdown_menu.Popup(pos, self)

    def SendDropdownSelectEvent(self):
        wx.PostEvent(self, dropdown_cmd_event(id=self.GetId(), value=self.GetValue()))

    def CreateMenu(self):
        self.dropdown_menu = flatmenu.FlatMenu()

        i = 0
        for item in self.items:
            menu_item = flatmenu.FlatMenuItem(self.dropdown_menu,
                                              DROPDOWNMENU_ITEM_IDS[i],
                                              item, "", wx.ITEM_NORMAL)
            self.dropdown_menu.AppendItem(menu_item)
            self.menuidmapping[DROPDOWNMENU_ITEM_IDS[i]] = item

            self.Bind(wx.EVT_MENU, self.OnSelectMenuItem, id=DROPDOWNMENU_ITEM_IDS[i])
            i += 1

    def OnSelectMenuItem(self, event):
        self.SetValue(self.menuidmapping[event.GetId()])
        self.SendDropdownSelectEvent()
        self.UpdateDrawing()
