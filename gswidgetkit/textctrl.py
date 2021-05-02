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
from wx import stc


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
