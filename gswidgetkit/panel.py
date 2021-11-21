

import wx


class RoundedPanel(wx.Panel):
    """
    Base class for panels with rounded corners
    """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                          size=wx.DefaultSize, style=wx.NO_BORDER | wx.TAB_TRAVERSAL)
        self.parent = parent