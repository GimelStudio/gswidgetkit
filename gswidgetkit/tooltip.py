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
# This file includes modified code from wx.lib.agw.supertooltip
#
# ----------------------------------------------------------------------------

import wx
import wx.lib.agw.supertooltip as STT


def MakeBold(font):
    """
    Makes a font bold. Utility method.

    :param `font`: the font to be made bold.
    """

    newFont = wx.Font(font.GetPointSize(), font.GetFamily(), font.GetStyle(),
                      wx.FONTWEIGHT_BOLD, font.GetUnderlined(), font.GetFaceName())

    return newFont


def ExtractLink(line):
    """
    Extract the link from an hyperlink line.

    :param `line`: the line of text to be processed.
    """

    line = line[4:]
    indxStart = line.find("{")
    indxEnd = line.find("}")
    hl = line[indxStart+1:indxEnd].strip()
    line = line[0:indxStart].strip()

    return line, hl


class ToolTipWindowBase(object):
    """ Base class for the different Windows and Mac implementation. """

    def __init__(self, parent, classParent):
        """
        Default class constructor.

        :param `parent`: the :class:`SuperToolTip` parent widget;
        :param `classParent`: the :class:`SuperToolTip` class object.
        """

        self._spacing = 18
        self._wasOnLink = False
        self._hyperlinkRect, self._hyperlinkWeb = [], []

        self._classParent = classParent

        # Bind the events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        parent.Bind(wx.EVT_KILL_FOCUS, self.OnDestroy)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnDestroy)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDestroy)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`SuperToolTip`.

        If the `event` parameter is ``None``, calculates best size and returns it.

        :param `event`: a :class:`PaintEvent` event to be processed or ``None``.
        """

        maxWidth = 0
        if event is None:
            dc = wx.ClientDC(self)
        else:
            # Go with double buffering...
            dc = wx.BufferedPaintDC(self)

        frameRect = self.GetClientRect()
        x, y, width, _height = frameRect
        # Store the rects for the hyperlink lines
        self._hyperlinkRect, self._hyperlinkWeb = [], []
        classParent = self._classParent

        # Retrieve the colours for the blended triple-gradient background
        topColour, middleColour, bottomColour = classParent.GetTopGradientColour(), \
                                                classParent.GetMiddleGradientColour(), \
                                                classParent.GetBottomGradientColour()

        # Get the user options for header, bitmaps etc...
        drawHeader, drawFooter = classParent.GetDrawHeaderLine(), classParent.GetDrawFooterLine()
        topRect = wx.Rect(frameRect.x, frameRect.y, frameRect.width, frameRect.height/2)
        bottomRect = wx.Rect(frameRect.x, frameRect.y+frameRect.height/2, frameRect.width, frameRect.height/2+1)
        # Fill the triple-gradient
        dc.GradientFillLinear(topRect, topColour, middleColour, wx.SOUTH)
        dc.GradientFillLinear(bottomRect, middleColour, bottomColour, wx.SOUTH)

        header, headerBmp = classParent.GetHeader(), classParent.GetHeaderBitmap()
        headerFont, messageFont, footerFont, hyperlinkFont = classParent.GetHeaderFont(), classParent.GetMessageFont(), \
                                                             classParent.GetFooterFont(), classParent.GetHyperlinkFont()

        yPos = 0
        bmpXPos = 0
        bmpHeight = textHeight = bmpWidth = 0

        if headerBmp and headerBmp.IsOk():
            # We got the header bitmap
            bmpHeight, bmpWidth = headerBmp.GetHeight(), headerBmp.GetWidth()
            bmpXPos = self._spacing

        if header:
            # We got the header text
            dc.SetFont(headerFont)
            textWidth, textHeight = dc.GetTextExtent(header)
            maxWidth = max(bmpWidth+(textWidth+self._spacing*2), maxWidth)
        # Calculate the header height
        height = max(textHeight, bmpHeight)
        normalText = classParent.GetTextColour()
        if header:
            dc.SetTextForeground(normalText)
            dc.DrawText(header, bmpXPos+bmpWidth+self._spacing, (height-textHeight+self._spacing)/2)
        if headerBmp and headerBmp.IsOk():
            dc.DrawBitmap(headerBmp, bmpXPos, (height-bmpHeight+self._spacing)/2, True)

        if header or (headerBmp and headerBmp.IsOk()):
            yPos += height
            if drawHeader:
                # Draw the separator line after the header
                dc.SetPen(wx.GREY_PEN)
                dc.DrawLine(self._spacing, yPos+self._spacing, width-self._spacing, yPos+self._spacing)
                yPos += self._spacing

        maxWidth = max(bmpXPos + bmpWidth + self._spacing, maxWidth)
        # Get the big body image (if any)
        embeddedImage = classParent.GetBodyImage()
        bmpWidth = bmpHeight = -1
        if embeddedImage and embeddedImage.IsOk():
            bmpWidth, bmpHeight = embeddedImage.GetWidth(), embeddedImage.GetHeight()

        # A bunch of calculations to draw the main body message
        messageHeight = 0
        lines = classParent.GetMessage().split("\n")
        yText = yPos
        embImgPos = yPos
        hyperLinkText = wx.BLUE
        messagePos = self._getTextExtent(dc, lines[0] if lines else "")[1] // 2 + self._spacing
        for line in lines:
            # Loop over all the lines in the message
            if line.startswith("<hr>"):     # draw a line
                yText += self._spacing * 2
                dc.DrawLine(self._spacing, yText+self._spacing, width-self._spacing, yText+self._spacing)
            else:
                isLink = False
                dc.SetTextForeground(normalText)
                if line.startswith("</b>"):      # is a bold line
                    line = line[4:]
                    font = MakeBold(messageFont)
                    dc.SetFont(font)
                elif line.startswith("</l>"):    # is a link
                    dc.SetFont(hyperlinkFont)
                    isLink = True
                    line, hl = ExtractLink(line)
                    dc.SetTextForeground(hyperLinkText)
                else:
                    # Is a normal line
                    dc.SetFont(messageFont)

                textWidth, textHeight = self._getTextExtent(dc, line)

                messageHeight += textHeight

                xText = (bmpWidth + 2 * (self._spacing/2)) if bmpWidth > 0 else self._spacing
                yText += textHeight/2+(self._spacing/2)
                maxWidth = max(xText + textWidth + self._spacing, maxWidth)
                dc.DrawText(line, xText, yText)
                if isLink:
                    self._storeHyperLinkInfo(xText, yText, textWidth, textHeight, hl)

        toAdd = 0
        if bmpHeight > messageHeight:
            yPos += 2*self._spacing + bmpHeight
            toAdd = self._spacing
        else:
            yPos += messageHeight + 2*self._spacing

        yText = max(messageHeight, bmpHeight+2*self._spacing)
        if embeddedImage and embeddedImage.IsOk():
            # Draw the main body image
            dc.DrawBitmap(embeddedImage, self._spacing, embImgPos + (self._spacing * 2), True)

        footer, footerBmp = classParent.GetFooter(), classParent.GetFooterBitmap()
        bmpHeight = bmpWidth = textHeight = textWidth = 0
        bmpXPos = 0

        if footerBmp and footerBmp.IsOk():
            # Got the footer bitmap
            bmpHeight, bmpWidth = footerBmp.GetHeight(), footerBmp.GetWidth()
            bmpXPos = self._spacing

        if footer:
            # Got the footer text
            footerFont.SetWeight(wx.FONTWEIGHT_NORMAL)
            dc.SetFont(footerFont.Italic())
            textWidth, textHeight = dc.GetTextExtent(footer)

        if textHeight or bmpHeight:
            if drawFooter:
                # Draw the separator line before the footer
                dc.SetPen(wx.GREY_PEN)
                dc.DrawLine(self._spacing, yPos-self._spacing/2+toAdd,
                            width-self._spacing, yPos-self._spacing/2+toAdd)
        # Draw the footer and footer bitmap (if any)
        dc.SetTextForeground(wx.Colour("#96B0DA"))
        height = max(textHeight, bmpHeight)
        yPos += toAdd
        if footer:
            toAdd = (height - textHeight + (self._spacing/2)) // 2
            dc.DrawText(footer, bmpXPos + bmpWidth + self._spacing, yPos + toAdd)
            maxWidth = max(bmpXPos + bmpWidth + (self._spacing/2) + textWidth, maxWidth)
        if footerBmp and footerBmp.IsOk():
            toAdd = (height - bmpHeight + (self._spacing/2)) / 2
            dc.DrawBitmap(footerBmp, bmpXPos, yPos + toAdd, True)
            maxWidth = max(footerBmp.GetSize().GetWidth() + bmpXPos, maxWidth)

        maxHeight = yPos + height + toAdd + 8
        if event is None:
            return maxWidth, maxHeight


    @staticmethod
    def _getTextExtent(dc, line):
        textWidth, textHeight = dc.GetTextExtent(line)
        if textHeight == 0:
            _, textHeight = dc.GetTextExtent("a")
        return textWidth, textHeight

    def _storeHyperLinkInfo(self, hTextPos, vTextPos, textWidth, textHeight, linkTarget):
        # Store the hyperlink rectangle and link
        self._hyperlinkRect.append(wx.Rect(hTextPos, vTextPos, textWidth, textHeight))
        self._hyperlinkWeb.append(linkTarget)


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`SuperToolTip`.

        :param `event`: a :class:`EraseEvent` event to be processed.

        :note: This method is intentionally empty to reduce flicker.
        """

        # This is intentionally empty to reduce flicker
        pass


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`SuperToolTip`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        self.Refresh()
        event.Skip()


    def OnMouseMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`SuperToolTip`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        x, y = event.GetPosition()
        for rect in self._hyperlinkRect:
            if rect.Contains((x, y)):
                # We are over one hyperlink...
                self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
                self._wasOnLink = True
                return

        if self._wasOnLink:
            # Restore the normal cursor
            self._wasOnLink = False
            self.SetCursor(wx.NullCursor)


    def OnDestroy(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN``, ``wx.EVT_LEFT_DCLICK`` and ``wx.EVT_KILL_FOCUS``
        events for :class:`SuperToolTip`. All these events destroy the :class:`SuperToolTip`,
        unless the user clicked on one hyperlink.

        :param `event`: a :class:`MouseEvent` or a :class:`FocusEvent` event to be processed.
        """

        if not isinstance(event, wx.MouseEvent):
            # We haven't clicked a link
            if self:  # Check if window still exists, Destroy might have been called manually (more than once)
                self.Destroy()
            return

        x, y = event.GetPosition()
        for indx, rect in enumerate(self._hyperlinkRect):
            if rect.Contains((x, y)):
                # Run the webbrowser with the clicked link
                webbrowser.open_new_tab(self._hyperlinkWeb[indx])
                return

        self.Destroy()


    def SetFont(self, font):
        """
        Sets the :class:`SuperToolTip` font globally.

        :param `font`: the font to set.
        """

        wx.PopupWindow.SetFont(self, font)
        self._classParent.InitFont()
        self.Invalidate()


    def Invalidate(self):
        """ Invalidate :class:`SuperToolTip` size and repaint it. """

        if not self._classParent.GetMessage():
            # No message yet...
            return

        self.CalculateBestSize()
        self.Refresh()

    def CalculateBestSize(self):
        """ Calculates the :class:`SuperToolTip` window best size. """

        maxWidth, maxHeight = self.OnPaint(None)
        self.SetSize((maxWidth, maxHeight))

    def CalculateBestPosition(self, widget):
        x, y = wx.GetMousePosition()
        screen = wx.ClientDisplayRect()[2:]
        left, top = widget.ClientToScreen((0, 0))
        right, bottom = widget.ClientToScreen(widget.GetClientRect()[2:])
        size = self.GetSize()

        if x+size[0]>screen[0]:
            xpos = x-size[0]
        else:
            xpos = x

        if bottom+size[1]>screen[1]:
            ypos = top-size[1] + 6
        else:
            ypos = bottom + 6

        self.SetPosition((xpos,ypos))


# Handle Mac and Windows/GTK differences...

if wx.Platform == "__WXMAC__":

    class ToolTipWindow(wx.Frame, ToolTipWindowBase):
        """ Popup window that works on wxMac. """

        def __init__(self, parent, classParent):
            """
            Default class constructor.

            :param `parent`: the :class:`SuperToolTip` parent widget;
            :param `classParent`: the :class:`SuperToolTip` class object.
            """

            wx.Frame.__init__(self, parent, style=wx.NO_BORDER|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR|wx.POPUP_WINDOW)
            # Call the base class
            ToolTipWindowBase.__init__(self, parent, classParent)

else:

    class ToolTipWindow(ToolTipWindowBase, wx.PopupWindow):
        """
        A simple :class:`PopupWindow` that holds fancy tooltips.
        Not available on Mac as :class:`PopupWindow` is not implemented there.
        """

        def __init__(self, parent, classParent):
            """
            Default class constructor.

            :param `parent`: the :class:`SuperToolTip` parent widget;
            :param `classParent`: the :class:`SuperToolTip` class object.
            """

            wx.PopupWindow.__init__(self, parent)
            # Call the base class
            ToolTipWindowBase.__init__(self, parent, classParent)



class ToolTip(STT.SuperToolTip):
    def __init__(self, header, message, target, bodyImage=wx.NullBitmap, headerBmp=wx.NullBitmap, footer="", footerBmp=wx.NullBitmap):
        STT.SuperToolTip.__init__(self, message, bodyImage, header, headerBmp, footer, footerBmp)

        self.SetHeader(header)
        self.SetTarget(target)
        self.SetStartDelay(.5)
        self.SetTopGradientColour(wx.Colour("#272727"))
        self.SetMiddleGradientColour(wx.Colour("#272727"))
        self.SetBottomGradientColour(wx.Colour("#272727"))
        self.SetTextColour(wx.Colour("#ccc"))

    def OnStartTimer(self):
        """ The creation time has expired, create the :class:`SuperToolTip`. """

        # target widget might already be destroyed
        if not self._widget:
            self._startTimer.Stop()
            return

        tip = ToolTipWindow(self._widget, self)
        self._superToolTip = tip
        self._superToolTip.CalculateBestSize()
        self._superToolTip.CalculateBestPosition(self._widget)

        self._superToolTip.Show()

        self._startTimer.Stop()
        self._endTimer.Start(self._endDelayTime*1000)


    def OnEndTimer(self):
        """ The show time for :class:`SuperToolTip` has expired, destroy the :class:`SuperToolTip`. """

        if self._superToolTip:
            self._superToolTip.Destroy()

        self._endTimer.Stop()


    def DoShowNow(self):
        """ Create the :class:`SuperToolTip` immediately. """

        if self._superToolTip:
            # need to destroy it if already exists,
            # otherwise we might end up with many of them
            self._superToolTip.Destroy()

        tip = ToolTipWindow(self._widget, self)
        self._superToolTip = tip
        self._superToolTip.CalculateBestSize()
        self._superToolTip.CalculateBestPosition(self._widget)

        # need to stop this, otherwise we get into trouble when leaving the window
        self._startTimer.Stop()

        self._superToolTip.Show()

        self._endTimer.Start(self._endDelayTime*1000)

