from ColorDelegator2 import ColorDelegator
from idlelib.Percolator import Percolator
from tkinter import Text

class HighlightTextBox(Text):
    '''Implements a Text box with a syntax highlighter'''
    def __init__(self, root, *args, **kwargs):
        Text.__init__(self, root, *args, **kwargs)
        self.d = ColorDelegator()
        self.p = Percolator(self)
        self.p.insertfilter(self.d)

if __name__=="__main__":
    from tkinter import Tk
    try:
        from ctypes import *
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    root = Tk()
    h = HighlightTextBox(root)
    h.pack()
    root.mainloop()

