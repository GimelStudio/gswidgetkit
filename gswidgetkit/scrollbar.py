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
from wx.lib.scrolledpanel import ScrolledPanel


class SuperScrolledWindow(wx.Window):
    """
    SuperScrolledWindow
     - A hacky attempt at replacing native scrollbars.
     - This is the general layout of the window.
        w = ScrolledPanel
        v = Vertical Scrollbar area
        h = Horizontal Scrollbar area
         ______
        | w | |
        |___|v|
        |_h_|_|

    :param parent: wx.Window
    :param wid: window ID
    :param pos: tuple
    :param size: tuple
    :param: style: wx.TAB_TRAVERSAL + whatever else
    :param name: window name
    """
    def __init__(self, parent: wx.Window, wid=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TAB_TRAVERSAL, name="SuperScrolledWindow"):
        super(SuperScrolledWindow, self).__init__(parent=parent, id=wid, pos=pos, style=style, size=size, name=name)
        # Attributes
        self.rate_x = 20
        self.rate_y = 20
        self._vbar_w = 10
        self._vbar_h = 0
        self._vscroll_hover = False
        self._hbar_h = 10
        self._hbar_w = 0
        self._hscroll_hover = False

        # Colors - updated in .setup() based on ScrolledPanel background color
        self._colour_normal = parent.GetBackgroundColour()
        self._colour_hover = wx.Colour(self._colour_normal).ChangeLightness(ialpha=115)
        self._colour_bar = "#8a8a8a"
        self._colour_bar_hover = wx.Colour(self._colour_bar).ChangeLightness(ialpha=115)

        # Base Sizer
        self._sizer_meta = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self._sizer_meta)

        # ScrolledPanel - hide the native scrollbars
        self._scrolled_panel = ScrolledPanel(parent=self)
        self._scrolled_panel.ShowScrollbars(horz=wx.SHOW_SB_NEVER, vert=wx.SHOW_SB_NEVER)

        # Vertical Scrollbar
        self._vscroll = wx.Window(parent=self, name='vscroll', size=(self._vbar_w, self.GetSize()[1]))
        self._vscroll.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # Horizontal Scrollbar
        self._hscroll = wx.Window(parent=self, name='hscroll', size=(self.GetSize()[0], self._hbar_h))
        self._hscroll.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # Main Sizer that holds the internal ScrolledPanel
        self._sizer_main = wx.BoxSizer(wx.VERTICAL)
        self._sizer_meta.Add(self._sizer_main, proportion=1, flag=wx.EXPAND)
        # Add the ScrolledPanel
        self._sizer_main.Add(self._scrolled_panel, proportion=1, flag=wx.EXPAND)
        # Add Horzontal Scrollbar below ScrolledPanel
        self._sizer_main.Add(self._hscroll, proportion=0, flag=wx.EXPAND)
        # Add Vertical Scrollbar to the right of the ScrolledPanel. This arrangement expands the VScroll to the
        # entire height of the client area.
        self._sizer_meta.Add(self._vscroll, proportion=0, flag=wx.EXPAND)

    def __calc_bar_sizes(self):
        v = ((self._vscroll.GetClientSize()[1] / self._scrolled_panel.GetVirtualSize()[1]) *
             self._vscroll.GetClientSize()[1]) + self._hbar_h + self.rate_y

        h = ((self._hscroll.GetClientSize()[0] / self._scrolled_panel.GetVirtualSize()[0]) *
             self._hscroll.GetClientSize()[0]) + self._vbar_w + self.rate_x

        self._vbar_h = max(v, self.rate_y)
        self._hbar_w = max(h, self.rate_x)

        self._vscroll.Refresh()
        self._hscroll.Refresh()

    def __on_scrollwin(self, event):
        if event.GetOrientation() == wx.VERTICAL and self._vscroll.IsShown() and self._vscroll.IsEnabled():
            self._vscroll.Refresh()

        elif event.GetOrientation() == wx.HORIZONTAL and self._hscroll.IsShown() and self._hscroll.IsEnabled():
            self._hscroll.Refresh()

        event.Skip()

    def __on_paint(self, event):
        # Get the scrollbars' x and y positions in relation to the size of the scrollbar sizes
        x, y = self._scrolled_panel.CalcScrolledPosition(self._scrolled_panel.GetViewStart())
        y = y*-1*(self._scrolled_panel.GetClientSize()[1] / self._scrolled_panel.GetVirtualSize()[1])
        x = x*-1*(self._scrolled_panel.GetClientSize()[0] / self._scrolled_panel.GetVirtualSize()[0])

        if event.EventObject == self._vscroll and self._vscroll.IsShown() and self._vscroll.IsEnabled():
            dc = wx.BufferedPaintDC(self._vscroll)
            dc.Clear()
            dc = wx.GCDC(dc)

            if not self._vscroll_hover:
                dc.SetPen(wx.Pen(self._colour_bar, 1, wx.PENSTYLE_TRANSPARENT))
                dc.SetBrush(wx.Brush(self._colour_bar, wx.BRUSHSTYLE_SOLID))

            else:
                dc.SetPen(wx.Pen(self._colour_hover, 1, wx.PENSTYLE_TRANSPARENT))
                dc.SetBrush(wx.Brush(self._colour_hover, wx.BRUSHSTYLE_SOLID))
                # Highlight scrollbar background
                dc.DrawRectangle(x=0, y=0, width=self._vbar_w, height=self._vscroll.GetSize()[1])

                dc.SetPen(wx.Pen(self._colour_bar_hover, 1, wx.PENSTYLE_TRANSPARENT))
                dc.SetBrush(wx.Brush(self._colour_bar_hover, wx.BRUSHSTYLE_SOLID))

            # Draw the bar
            dc.DrawRoundedRectangle(x=0, y=y, width=self._vbar_w, height=self._vbar_h, radius=1)

        elif event.EventObject == self._hscroll and self._hscroll.IsShown() and self._hscroll.IsEnabled():
            dc = wx.BufferedPaintDC(self._hscroll)
            dc.Clear()
            dc = wx.GCDC(dc)

            if not self._hscroll_hover:
                dc.SetPen(wx.Pen(self._colour_bar, 1, wx.PENSTYLE_TRANSPARENT))
                dc.SetBrush(wx.Brush(self._colour_bar, wx.BRUSHSTYLE_SOLID))

            else:
                dc.SetPen(wx.Pen(self._colour_hover, 1, wx.PENSTYLE_TRANSPARENT))
                dc.SetBrush(wx.Brush(self._colour_hover, wx.BRUSHSTYLE_SOLID))
                # Highlight scrollbar background
                dc.DrawRectangle(x=0, y=0, width=self._hscroll.GetSize()[0], height=self._hbar_w)

                dc.SetPen(wx.Pen(self._colour_bar_hover, 1, wx.PENSTYLE_TRANSPARENT))
                dc.SetBrush(wx.Brush(self._colour_bar_hover, wx.BRUSHSTYLE_SOLID))

            dc.DrawRoundedRectangle(x=x, y=0, width=self._hbar_w, height=self._hbar_h, radius=1)

        event.Skip()

    def __on_mouse(self, event: [wx.MouseEvent, wx.Event]):
        mx, my = event.GetPosition()
        if event.EventObject == self._vscroll:
            if self._vscroll.IsEnabled() and self._vscroll.IsShown():
                if event.LeftIsDown():
                    self._vscroll_hover = True
                    if not self._vscroll.HasCapture():
                        # Capture the mouse to retain dragging outside scrollbar area
                        self._vscroll.CaptureMouse()
                    # Get the position of the mouse relative to the virtual size of the main window
                    y = my*(self._scrolled_panel.GetVirtualSize()[1] / self._vscroll.GetClientSize()[1])
                    # Convert pixels to units by dividing by the scroll rate
                    self._scrolled_panel.Scroll(-1, int(y // self.rate_y))

                elif event.LeftUp():
                    if mx < 0 or mx > self._vbar_w or my < 0 or my > self._vscroll.GetClientSize()[1]:
                        self._vscroll_hover = False
                    if self._vscroll.HasCapture():
                        # Release the mouse when left-click goes up
                        self._vscroll.ReleaseMouse()

                elif event.GetWheelRotation() > 0:
                    # Scroll down by 3 units
                    # (This is the same number of units as a scrolling in the window. Don't know why.)
                    self._scrolled_panel.Scroll(-1, max(0, self._scrolled_panel.GetViewStart()[1] - 3))

                elif event.GetWheelRotation() < 0:
                    # Scroll up by 3 units
                    self._scrolled_panel.Scroll(-1, self._scrolled_panel.GetViewStart()[1] + 3)

                self._vscroll.Refresh()

        elif event.EventObject == self._hscroll:
            if self._hscroll.IsEnabled() and self._hscroll.IsShown():
                # Get the position of the mouse relative to the virtual size of the main window
                x = mx*(self._scrolled_panel.GetVirtualSize()[0] / self._hscroll.GetClientSize()[0])
                if event.LeftIsDown():
                    self._hscroll_hover = True
                    if not self._hscroll.HasCapture():
                        self._hscroll.CaptureMouse()
                    # Convert pixels to units by dividing by the scroll rate
                    self._scrolled_panel.Scroll(int(x // self.rate_x), -1)

                elif event.LeftUp():
                    if my < 0 or my > self._hbar_h or mx < 0 or mx > self._hscroll.GetClientSize()[0]:
                        self._hscroll_hover = False
                    if self._hscroll.HasCapture():
                        self._hscroll.ReleaseMouse()

                elif event.GetWheelRotation() > 0:
                    # Scroll right by 3 units
                    self._scrolled_panel.Scroll(self._scrolled_panel.GetViewStart()[0] + 3, -1)

                elif event.GetWheelRotation() < 0:
                    # Scroll up left 3 units
                    self._scrolled_panel.Scroll(max(0, self._scrolled_panel.GetViewStart()[0] - 3), -1)

                self._hscroll.Refresh()

        event.Skip()

    def __on_size(self, event):
        if self._vscroll.IsEnabled():
            # Show/Hide Vertical Scrollbar
            if self._scrolled_panel.GetVirtualSize()[1] <= self.GetClientSize()[1]:
                self._vscroll.Show(False)
            else:
                self._vscroll.Show(True)

        if self._hscroll.IsEnabled():
            # Show/Hide Horizontal Scrollbar
            if self._scrolled_panel.GetVirtualSize()[0] <= self.GetClientSize()[0]:
                self._hscroll.Show(False)
            else:
                self._hscroll.Show(True)

        wx.CallAfter(self.__calc_bar_sizes)
        event.Skip()

    def __on_enter_window(self, event):
        if event.EventObject == self._vscroll:
            if self._vscroll.IsEnabled() and self._vscroll.IsShown():
                self._vscroll_hover = True
                self._vscroll.Refresh()

        elif event.EventObject == self._hscroll:
            if self._hscroll.IsEnabled() and self._hscroll.IsShown():
                self._hscroll_hover = True
                self._hscroll.Refresh()

        event.Skip()

    def __on_leave_window(self, event):
        if event.EventObject == self._vscroll:
            if self._vscroll.IsEnabled() and self._vscroll.IsShown():
                self._vscroll_hover = False
                self._vscroll.Refresh()

        elif event.EventObject == self._hscroll:
            if self._hscroll.IsEnabled() and self._hscroll.IsShown():
                self._hscroll_hover = False
                self._hscroll.Refresh()

        event.Skip()

    def __update_colors(self):
        self._colour_normal = self._scrolled_panel.GetBackgroundColour()

        if wx.Colour(self._colour_normal).GetLuminance() >= 0.5:
            self._colour_bar = wx.Colour(self._colour_normal).ChangeLightness(ialpha=80)
            self._colour_bar_hover = wx.Colour(self._colour_bar).ChangeLightness(ialpha=70)
            self._colour_hover = wx.Colour(self._colour_normal).ChangeLightness(ialpha=85)
        else:
            self._colour_bar = wx.Colour(self._colour_normal).ChangeLightness(ialpha=120)
            self._colour_bar_hover = wx.Colour(self._colour_bar).ChangeLightness(ialpha=130)
            self._colour_hover = wx.Colour(self._colour_normal).ChangeLightness(ialpha=115)

        self.SetBackgroundColour(self._colour_normal)
        self.SetForegroundColour(self._scrolled_panel.GetForegroundColour())
        self._hscroll.SetBackgroundColour(self._colour_normal)
        self._vscroll.SetBackgroundColour(self._colour_normal)

    def scroll(self, x: int, y: int):
        """
        Overloaded function to scroll to a given point. This is in units, not pixels.

        :param x: units in horizontal direction
        :param y, units in vertical direction.
        """
        self._scrolled_panel.Scroll((x, y))
        self._vscroll.Refresh()
        self._hscroll.Refresh()

    def get_panel(self) -> ScrolledPanel:
        """
        Get the ScrolledPanel object to place all widgets.
        """
        return self._scrolled_panel

    def set_colors(self, bg: [str, wx.Colour] = None, fg: [str, wx.Colour] = None):
        """
        Set the panel background and foreground colors. This will update the scrollbar colors.

        :param bg: background color
        :param fg: foreground color
        """
        if bg is not None:
            self._scrolled_panel.SetBackgroundColour(bg)

        if fg is not None:
            self._scrolled_panel.SetForegroundColour(fg)

        self.__update_colors()
        self.Update()
        self.Refresh()

    def setup(self, scroll_x=True, scroll_y=True, rate_x=20, rate_y=20, scroll_to_top=True, scroll_into_view=False):
        """
        Setup up the Scrollbars after adding widgets. Same inputs as ScrolledPanel.SetupScrolling().

        :param scroll_x: Enable horizontal scrolling
        :param scroll_y: Enable vertical scrolling
        :param rate_x: Horizontal scroll rate
        :param rate_y: Vertical scroll rate
        :param scroll_to_top: Scroll to the top left after initialization
        :param scroll_into_view: Scroll children into view when activated
        """
        self.rate_x = rate_x
        self.rate_y = rate_y

        if not scroll_x:
            self._hscroll.Enable(enable=False)
            self._hscroll.Show(show=False)

        if not scroll_y:
            self._vscroll.Enable(enable=False)
            self._vscroll.Show(show=False)

        # Setup Scrollbars
        self._scrolled_panel.EnableScrolling(xScrolling=scroll_x, yScrolling=scroll_y)
        self._scrolled_panel.SetupScrolling(scroll_x=scroll_x, scroll_y=scroll_y, rate_x=rate_x, rate_y=rate_y,
                                            scrollToTop=scroll_to_top, scrollIntoView=scroll_into_view)

        # Update Colors
        self.__update_colors()

        # Binds
        self.Bind(event=wx.EVT_SIZE, handler=self.__on_size)
        self._scrolled_panel.Bind(event=wx.EVT_SCROLLWIN, handler=self.__on_scrollwin)
        self._vscroll.Bind(event=wx.EVT_PAINT, handler=self.__on_paint)
        self._hscroll.Bind(event=wx.EVT_PAINT, handler=self.__on_paint)
        self._vscroll.Bind(event=wx.EVT_MOUSE_EVENTS, handler=self.__on_mouse)
        self._hscroll.Bind(event=wx.EVT_MOUSE_EVENTS, handler=self.__on_mouse)
        self._vscroll.Bind(event=wx.EVT_ENTER_WINDOW, handler=self.__on_enter_window)
        self._hscroll.Bind(event=wx.EVT_ENTER_WINDOW, handler=self.__on_enter_window)
        self._vscroll.Bind(event=wx.EVT_LEAVE_WINDOW, handler=self.__on_leave_window)
        self._hscroll.Bind(event=wx.EVT_LEAVE_WINDOW, handler=self.__on_leave_window)

        wx.CallAfter(self.__calc_bar_sizes)



if __name__ == '__main__':

    class TestFrame(wx.Frame):
        def __init__(self, parent=None, title='Test SuperScrolledWindow', style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP):
            super(TestFrame, self).__init__(parent=parent, title=title, style=style, size=(350, 350))

            # Frame setup
            self.SetBackgroundColour("#FFFFFF")
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(sizer)

            # # SuperScrolledWindow
            self.ssw = SuperScrolledWindow(parent=self)
            sizer.Add(self.ssw, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

            # Get ScrolledPanel and add stuff
            self.panel = self.ssw.get_panel()
            self.panel.SetBackgroundColour("#FFFFFF")
            self.panel.SetForegroundColour("#000000")
            self.main_sizer = wx.GridBagSizer(vgap=5, hgap=5)
            self.panel.SetSizer(self.main_sizer)

            self.init_panel()

            # Setup up scrolling
            self.ssw.setup(scroll_x=True, scroll_y=True, rate_x=20, rate_y=20, scroll_to_top=True,
                           scroll_into_view=False)

            # Add a pointless button on the frame
            self._mode = 'light'
            self._btn_mode = wx.Button(parent=self, label='Dark Mode', name='mode')
            sizer.Add(self._btn_mode, flag=wx.ALL, border=10)

            self.Layout()
            self.Fit()
            self.SetInitialSize((300, 300))

            self.Bind(event=wx.EVT_BUTTON, handler=self.__on_button)

        def __on_button(self, event):
            if event.EventObject.GetName() == "scroll_me":
                self.ssw.scroll(x=20, y=20)

            elif event.EventObject.GetName() == 'mode':
                if self._mode == 'light':
                    self._btn_mode.SetLabel(label='Light Mode')
                    self._mode = 'dark'
                    self.ssw.set_colors(bg="#212121", fg="#FFFFFF")
                else:
                    self._btn_mode.SetLabel(label='Dark Mode')
                    self._mode = 'light'
                    self.ssw.set_colors(bg="#FFFFFF", fg="#000000")

            event.Skip()

        def init_panel(self):
            """
            Add stuff...
            """
            text1 = wx.StaticText(parent=self.panel, label="words words words. these are words. blah blah blah "
                                                           "this is a long statictext to take up room. words words "
                                                           "words. these are words. i know words. these are words")
            text1.Wrap(200)
            self.main_sizer.Add(text1, pos=(0, 0), flag=wx.ALL, border=5)

            btn1 = wx.Button(parent=self.panel, label="Scroll Me", name="scroll_me")
            self.main_sizer.Add(btn1, pos=(0, 1), flag=wx.ALL, border=5)

            for x in range(4):
                for y in range(4):
                    p = wx.Panel(parent=self.panel, size=(100, 100))
                    p.SetBackgroundColour("#85e97a")
                    self.main_sizer.Add(p, pos=(x+1, y+1), flag=wx.ALL, border=5)

            self.panel.Layout()

    app = wx.App(False)
    frame = TestFrame()

    frame.Show()

    app.MainLoop()
    app.ExitMainLoop()
    app.Destroy()
