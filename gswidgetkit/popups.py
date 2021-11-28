import wx
from wx.lib.newevent import NewCommandEvent


class Popup(wx.Control):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER, *args, **kwargs):
        wx.Control.__init__(self, parent, id, pos, size, style, *args, **kwargs)
        
        self.parent = parent

