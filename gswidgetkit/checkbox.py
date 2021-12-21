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
#
# This file is edited code from wx.lib.checkbox
# (c) 2020 by Total Control Software
#
# ----------------------------------------------------------------------------

import wx
from .icons import (ICON_CHECKBOX_CHECKED, ICON_CHECKBOX_UNCHECKED,
                    ICON_CHECKBOX_FOCUSED)


class CheckBox(wx.Control):
    """ 
    Checkbox widget for selecting boolean values.

    :param wx.Window `parent`: parent window. Must not be ``None``.
    :param integer `id`: window identifier. A value of -1 indicates a default value.
    :param string `label`: the displayed checkbox label.
    """
    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="CheckBox"):
        wx.Control.__init__(self, parent, id, pos, size, style, validator, name)

        self.SYS_DEFAULT_GUI_FONT = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

        # Initialize our cool bitmaps.
        self.InitializeBitmaps()

        # Initialize the focus pen colour/dashes, for faster drawing later.
        self.InitializeColours()

        # Set default colors
        self.SetBackgroundColour(parent.GetBackgroundColour())
        self.SetForegroundColour(wx.Colour("#e9e9e9"))

        # By default, we start unchecked.
        self._checked = False

        # Set the spacing between the check bitmap and the label to 3 by default.
        # This can be changed using SetSpacing later.
        self._spacing = 6
        self._hasFocus = False

        # Ok, set the wx.PyControl label, its initial size (formerly known an
        # SetBestFittingSize), and inherit the attributes from the standard
        # wx.CheckBox .
        self.SetLabel(label)
        self.SetInitialSize(size)
        self.InheritAttributes()

        # Bind the events related to our control: first of all, we use a
        # combination of wx.BufferedPaintDC and an empty handler for
        # wx.EVT_ERASE_BACKGROUND (see later) to reduce flicker.
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # Since the paint event draws the whole widget, we will use
        # SetBackgroundStyle(wx.BG_STYLE_PAINT) and then
        # implementing an erase-background handler is not neccessary.
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        # Add a size handler to refresh so the paint wont smear when resizing.
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Then we want to monitor user clicks, so that we can switch our
        # state between checked and unchecked.
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        if wx.Platform == '__WXMSW__':
            # MSW Sometimes does strange things...
            self.Bind(wx.EVT_LEFT_DCLICK,  self.OnMouseClick)

        # We want also to react to keyboard keys, namely the space bar that can
        # toggle our checked state. Whether key-up or key-down is used is based
        # on platform.
        if 'wxMSW' in wx.PlatformInfo:
            self.Bind(wx.EVT_KEY_UP, self.OnKeyEvent)
        else:
            self.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvent)

        # Then, we react to focus event, because we want to draw a small
        # dotted rectangle around the text if we have focus.
        # This might be improved!!!
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


    def InitializeBitmaps(self):
        """ Initializes the check bitmaps. """

        # We keep 4 bitmaps for GenCheckBox, depending on the
        # checking state (Checked/UnChecked) and the control
        # state (Enabled/Disabled).

        self._bitmaps = {
            "CheckedEnable": _GetCheckedBitmap(self),
            "FocusedEnable": _GetFocusedBitmap(self),
            "UnCheckedEnable": _GetNotCheckedBitmap(self),
            "CheckedDisable": _GetCheckedImage(self).ConvertToDisabled().ConvertToBitmap(),
            "FocusedDisable": _GetFocusedImage(self).ConvertToDisabled().ConvertToBitmap(),
            "UnCheckedDisable": _GetNotCheckedImage(self).ConvertToDisabled().ConvertToBitmap()
            }

    def InitializeColours(self):
        """ Initializes the focus indicator pen. """

        textClr = self.GetForegroundColour()
        self.SYS_COLOUR_GRAYTEXT = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)

    def GetBitmap(self):
        """
        Returns the appropriated bitmap depending on the checking state
        (Checked/UnChecked) and the control state (Enabled/Disabled).
        """

        if self.IsEnabled():
            # So we are Enabled.
            if self.IsChecked():
                # We are Checked.
                return self._bitmaps["CheckedEnable"]
            elif self.HasFocus():
                return self._bitmaps["FocusedEnable"]
            else:
                # We are UnChecked.
                return self._bitmaps["UnCheckedEnable"]
        else:
            # Poor GenCheckBox, Disabled and ignored!
            if self.IsChecked():
                return self._bitmaps["CheckedDisable"]
            elif self.HasFocus():
                return self._bitmaps["FocusedDisable"]
            else:
                return self._bitmaps["UnCheckedDisable"]

    def SetLabel(self, label):
        """
        Sets the :class:`GenCheckBox` text label and updates the control's
        size to exactly fit the label plus the bitmap.

        :param `label`: Text to be displayed next to the checkbox.
        :type `label`: str
        """

        wx.Control.SetLabel(self, label)

        # The text label has changed, so we must recalculate our best size
        # and refresh ourselves.
        self.InvalidateBestSize()
        self.Refresh()

    def SetFont(self, font):
        """
        Sets the :class:`GenCheckBox` text font and updates the control's
        size to exactly fit the label plus the bitmap.

        :param `font`: Font to be used to render the checkboxs label.
        :type `font`: `wx.Font`
        """

        wx.Control.SetFont(self, font)

        # The font for text label has changed, so we must recalculate our best
        # size and refresh ourselves.
        self.InvalidateBestSize()
        self.Refresh()

    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of the control
        based on the label size, the bitmap size and the current font.
        """

        # Retrieve our properties: the text label, the font and the check
        # bitmap.
        label = self.GetLabel()
        font = self.GetFont()
        bitmap = self.GetBitmap()

        if not font:
            # No font defined? So use the default GUI font provided by the system.
            font = self.SYS_DEFAULT_GUI_FONT

        # Set up a wx.ClientDC. When you don't have a dc available (almost
        # always you don't have it if you are not inside a wx.EVT_PAINT event),
        # use a wx.ClientDC (or a wx.MemoryDC) to measure text extents.
        dc = wx.ClientDC(self)
        dc.SetFont(font)

        # Measure our label.
        textWidth, textHeight = dc.GetTextExtent(label)

        # Retrieve the check bitmap dimensions.
        bitmapWidth, bitmapHeight = bitmap.GetWidth(), bitmap.GetHeight()

        # Get the spacing between the check bitmap and the text.
        spacing = self.GetSpacing()

        # Ok, we're almost done: the total width of the control is simply
        # the sum of the bitmap width, the spacing and the text width,
        # while the height is the maximum value between the text width and
        # the bitmap width.
        totalWidth = bitmapWidth + spacing + textWidth
        totalHeight = max(textHeight, bitmapHeight)

        best = wx.Size(totalWidth, totalHeight)

        # Cache the best size so it doesn't need to be calculated again,
        # at least until some properties of the window change.
        self.CacheBestSize(best)

        return best

    def AcceptsFocusFromKeyboard(self):
        """ Overridden base class virtual. """

        # We can accept focus from keyboard, obviously.
        return True

    def AcceptsFocus(self):
        """ Overridden base class virtual. """

        # If it seems that wx.CheckBox does not accept focus with mouse, It does.
        # You just can't see the focus rectangle until there's
        # another keypress or navigation event (at least on some platforms.)
        return True  # This will draw focus rectangle always on mouse click.

    def HasFocus(self):
        """ Returns whether or not we have the focus. """

        # We just returns the _hasFocus property that has been set in the
        # wx.EVT_SET_FOCUS and wx.EVT_KILL_FOCUS event handlers.
        return self._hasFocus

    def SetForegroundColour(self, colour):
        """
        Overridden base class virtual.

        :param `colour`: Set the foreground colour of the checkboxs label.
        :type `colour`: `wx.Colour`
        """

        wx.Control.SetForegroundColour(self, colour)

        # We have to re-initialize the focus indicator per colour as it should
        # always be the same as the foreground colour.
        self.InitializeColours()
        self.Refresh()

    def SetBackgroundColour(self, colour):
        """
        Overridden base class virtual.

        :param `colour`: Set the background colour of the checkbox.
        :type `colour`: `wx.Colour`
        """

        wx.Control.SetBackgroundColour(self, colour)

        # We have to refresh ourselves.
        self.Refresh()

    def Enable(self, enable=True):
        """
        Enables/Disables :class:`GenCheckBox`.

        :param `enable`: Set the enabled state of the checkbox.
        :type `enable`: bool
        """

        wx.Control.Enable(self, enable)

        # We have to refresh ourselves, as our state changed.
        self.Refresh()

    def GetDefaultAttributes(self):
        """
        Overridden base class virtual.  By default we should use
        the same font/colour attributes as the native wx.CheckBox.
        """

        return wx.CheckBox.GetClassDefaultAttributes()

    def ShouldInheritColours(self):
        """
        Overridden base class virtual.  If the parent has non-default
        colours then we want this control to inherit them.
        """

        return True

    def SetSpacing(self, spacing):
        """
        Sets a new spacing between the check bitmap and the text.

        :param `spacing`: Set the amount of space between the checkboxs bitmap and text.
        :type `spacing`: int
        """

        self._spacing = spacing

        # The spacing between the check bitmap and the text has changed,
        # so we must recalculate our best size and refresh ourselves.
        self.InvalidateBestSize()
        self.Refresh()

    def GetSpacing(self):
        """ Returns the spacing between the check bitmap and the text. """

        return self._spacing

    def GetValue(self):
        """
        Returns the state of :class:`GenCheckBox`, True if checked, False
        otherwise.
        """

        return self._checked

    def IsChecked(self):
        """
        This is just a maybe more readable synonym for GetValue: just as the
        latter, it returns True if the :class:`GenCheckBox` is checked and False
        otherwise.
        """

        return self._checked

    def SetValue(self, state):
        """
        Sets the :class:`GenCheckBox` to the given state. This does not cause a
        ``wx.wxEVT_COMMAND_CHECKBOX_CLICKED`` event to get emitted.

        :param `state`: Set the value of the checkbox. True or False.
        :type `state`: bool
        """

        self._checked = state

        # Refresh ourselves: the bitmap has changed.
        self.Refresh()

    def OnKeyEvent(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` or ``wx.EVT_KEY_UP`` event (depending on
        platform) for :class:`GenCheckBox`.

        :param `event`: A `wx.KeyEvent` to be processed.
        :type `event`: `wx.KeyEvent`
        """

        if event.GetKeyCode() == wx.WXK_SPACE:
            # The spacebar has been pressed: toggle our state.
            self.SendCheckBoxEvent()
        else:
            event.Skip()

    def OnSetFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`GenCheckBox`.

        :param `event`: A `wx.FocusEvent` to be processed.
        :type `event`: `wx.FocusEvent`
        """

        self._hasFocus = True

        # We got focus, and we want a dotted rectangle to be painted
        # around the checkbox label, so we refresh ourselves.
        self.Refresh()

    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`GenCheckBox`.

        :param `event`: A `wx.FocusEvent` to be processed.
        :type `event`: `wx.FocusEvent`
        """

        self._hasFocus = False

        # We lost focus, and we want a dotted rectangle to be cleared
        # around the checkbox label, so we refresh ourselves.
        self.Refresh()

    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`GenCheckBox`.

        :param `event`: A `wx.SizeEvent` to be processed.
        :type `event`: `wx.SizeEvent`
        """
        self.Refresh()

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`GenCheckBox`.

        :param `event`: A `wx.PaintEvent` to be processed.
        :type `event`: `wx.PaintEvent`
        """

        # If you want to reduce flicker, a good starting point is to
        # use wx.BufferedPaintDC .
        # wx.AutoBufferedPaintDC would be marginally better.
        dc = wx.AutoBufferedPaintDC(self)

        # Is is advisable that you don't overcrowd the OnPaint event
        # (or any other event) with a lot of code, so let's do the
        # actual drawing in the Draw() method, passing the newly
        # initialized wx.AutoBufferedPaintDC .
        self.Draw(dc)

    def Draw(self, dc):
        """
        Actually performs the drawing operations, for the bitmap and
        for the text, positioning them centered vertically.

        :param `dc`: device context to use.
        :type `dc`: `wx.DC`
        """

        # Get the actual client size of ourselves.
        width, height = self.GetClientSize()

        if not width or not height:
            # Nothing to do, we still don't have dimensions!
            return

        # Initialize the wx.BufferedPaintDC, assigning a background
        # colour and a foreground colour (to draw the text).
        backColour = self.GetBackgroundColour()
        backBrush = wx.Brush(backColour, wx.SOLID)
        dc.SetBackground(backBrush)
        dc.Clear()

        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(self.SYS_COLOUR_GRAYTEXT)

        dc.SetFont(self.GetFont())

        # Get the text label for the checkbox, the associated check bitmap
        # and the spacing between the check bitmap and the text.
        label = self.GetLabel()
        bitmap = self.GetBitmap()
        spacing = self.GetSpacing()

        # Measure the text extent and get the check bitmap dimensions.
        textWidth, textHeight = dc.GetTextExtent(label)
        bitmapWidth, bitmapHeight = bitmap.GetWidth(), bitmap.GetHeight()

        # Position the bitmap centered vertically.
        bitmapXpos = 0
        bitmapYpos = (height - bitmapHeight) // 2

        # Position the text centered vertically.
        textXpos = bitmapWidth + spacing
        textYpos = (height - textHeight) // 2

        # Draw the bitmap on the DC.
        try:
            dc.DrawBitmap(bitmap, bitmapXpos, bitmapYpos, True)
        except Exception as exc:  # bitmap might be image and need converted. Ex: if disabled.
            dc.DrawBitmap(bitmap.ConvertToBitmap(), bitmapXpos, bitmapYpos, True)

        # Draw the text
        dc.DrawText(label, textXpos, textYpos)

        # Let's see if we have keyboard focus and, if this is the case,
        # we draw it a little lighter.
        if self.HasFocus():
            dc.DrawBitmap(bitmap, bitmapXpos, bitmapYpos, True)

    def OnMouseClick(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`GenCheckBox`.

        :param `event`: A `wx.MouseEvent` to be processed.
        :type `event`: `wx.MouseEvent`
        """

        if not self.IsEnabled():
            # Nothing to do, we are disabled.
            return

        self.SendCheckBoxEvent()
        event.Skip()

    def SendCheckBoxEvent(self):
        """ Actually sends the wx.wxEVT_COMMAND_CHECKBOX_CLICKED event. """

        # This part of the code may be reduced to a 3-liner code
        # but it is kept for better understanding the event handling.
        # If you can, however, avoid code duplication; in this case,
        # I could have done:
        #
        # self._checked = not self.IsChecked()
        # checkEvent = wx.CommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED,
        #                              self.GetId())
        # checkEvent.SetInt(int(self._checked))
        if self.IsChecked():

            # We were checked, so we should become unchecked.
            self._checked = False

            # Fire a wx.CommandEvent: this generates a
            # wx.wxEVT_COMMAND_CHECKBOX_CLICKED event that can be caught by the
            # developer by doing something like:
            # MyCheckBox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
            checkEvent = wx.CommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED,
                                         self.GetId())

            # Set the integer event value to 0 (we are switching to unchecked state).
            checkEvent.SetInt(0)

        else:

            # We were unchecked, so we should become checked.
            self._checked = True

            checkEvent = wx.CommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED,
                                         self.GetId())

            # Set the integer event value to 1 (we are switching to checked state).
            checkEvent.SetInt(1)

        # Set the originating object for the event (ourselves).
        checkEvent.SetEventObject(self)

        # Watch for a possible listener of this event that will catch it and
        # eventually process it.
        self.GetEventHandler().ProcessEvent(checkEvent)

        # Refresh ourselves: the bitmap has changed.
        self.Refresh()


def _GetCheckedBitmap(self):
    return ICON_CHECKBOX_CHECKED.GetBitmap()

def _GetCheckedImage(self):
    return _GetCheckedBitmap(self).ConvertToImage()

def _GetFocusedBitmap(self):
    return ICON_CHECKBOX_FOCUSED.GetBitmap()

def _GetFocusedImage(self):
    return _GetFocusedBitmap(self).ConvertToImage()

def _GetNotCheckedBitmap(self):
    return ICON_CHECKBOX_UNCHECKED.GetBitmap()

def _GetNotCheckedImage(self):
    return _GetNotCheckedBitmap(self).ConvertToImage()


def _GrayOut(anImage):
    """
    Convert the given image (in place) to a grayed-out version,
    appropriate for a 'disabled' appearance.

    :param `anImage`: A `wx.Image` to gray out.
    :type `anImage`: `wx.Image`
    :rtype: `wx.Bitmap`
    """

    factor = 0.7  # 0 < f < 1.  Higher Is Grayer

    if anImage.HasMask():
        maskColor = (anImage.GetMaskRed(), anImage.GetMaskGreen(), anImage.GetMaskBlue())
    else:
        maskColor = None

    data = map(ord, list(anImage.GetData()))

    for i in range(0, len(data), 3):
        pixel = (data[i], data[i + 1], data[i + 2])
        pixel = _MakeGray(pixel, factor, maskColor)

        for x in range(3):
            data[i + x] = pixel[x]

    anImage.SetData(''.join(map(chr, data)))

    return anImage.ConvertToBitmap()


def _MakeGray(rgbTuple, factor, maskColor):
    """
    Make a pixel grayed-out. If the pixel matches the maskcolor, it won't be
    changed.

    :type `rgbTuple`: red, green, blue 3-tuple
    :type `factor`: float
    :type `maskColor`: red, green, blue 3-tuple
    """
    r, g, b = rgbTuple
    if (r, g, b) != maskColor:
        return map(lambda x: int((230 - x) * factor) + x, (r, g, b))
    else:
        return (r, g, b)
