from HighlightTextBox import HighlightTextBox
from CloseNotebook import CloseNotebook
import tkinter

class Morpheus(CloseNotebook):
    def __init__(self, root, *args, **kwargs):
        self.root = root
        CloseNotebook.__init__(self, root, *args, **kwargs)

        self.createNewTab()
        self.bind_all("<Control-n>", self.createNewTab)

    def createNewTab(self, *args, **kwargs):
        end=self.index("end")
        if end<16:
            f = tkinter.Frame(self)
            HighlightTextBox(f).pack(fill="both", expand=1)
            self.add(f, text="Page %s"%end, padding=3)

if __name__=="__main__":
    root = tkinter.Tk()
    
    Morpheus(root).pack(fill="both", expand=True)

    root.mainloop()
