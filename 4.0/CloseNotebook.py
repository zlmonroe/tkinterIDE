'''
An Expanded CloseNotebook based on the version from:
http://svn.python.org/projects/python/trunk/Demo/tkinter/ttk/notebook_closebtn.py
that includes both close and move functionality to the tkk.Notebook class
'''

import os
import tkinter
from tkinter import ttk
import images
from TabGhost import TabGhost

class CloseNotebook(ttk.Notebook):
    tabLoc=None
    #The integer 90 should be the width of the tabs due to the fact that the width
    #was predetermined from the class. In the future it would be nice to implemet
    #a way to detect how many tabs have been passed over when the tabs have variable
    #widths
    #this width may also be dependent on the screen width, which is not accounted for
    tabWidth=90
    def __init__(self, parent, *args, **kwargs):
        self.i1 = tkinter.PhotoImage("img_close", data=images.close)
        self.i2 = tkinter.PhotoImage("img_closeactive", data=images.close_selected)
        self.i3 = tkinter.PhotoImage("img_closepressed",data=images.close_active)

        self.style = ttk.Style()
        if "close" not in self.style.element_names():
            self.style.theme_create( "Visable", parent="alt", settings={
                "ButtonNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
                "ButtonNotebook.Tab": {
                    "configure": {"padding": [5, 1],"background": "light gray","width":10 },
                    "map":       {"background": [("selected", 'azure')], "weight": [("selected",20)],
                                  "expand": [("selected", [1, 1, 1, 0])] } } } )
            self.style.theme_use("Visable")
            self.style.element_create("close", "image", "img_close",
                ("active", "pressed", "!disabled", "img_closepressed"),
                ("active", "!disabled", "img_closeactive"), border=8, sticky='')
            self.style.layout("ButtonNotebook", [("ButtonNotebook.client", {"sticky": "nswe"})])
            self.style.layout("ButtonNotebook.Tab", [
                ("ButtonNotebook.tab", {"sticky": "nswe", "children":
                    [("ButtonNotebook.padding", {"side": "top", "sticky": "nswe",
                                                 "children":
                        [("ButtonNotebook.focus", {"side": "top", "sticky": "nswe",
                                                   "children":
                            [("ButtonNotebook.label", {"side": "left", "sticky": ''}),
                             ("ButtonNotebook.close", {"side": "right", "sticky": ''})]
                        })]
                    })]
                })]
            )

        ttk.Notebook.__init__(self, parent, style="ButtonNotebook", *args, **kwargs)
        self.maxTabs=int(parent.winfo_screenwidth()/self.tabWidth)
        parent.bind_class("TNotebook", "<ButtonPress-1>", self.__btn_press, True)
        parent.bind_class("TNotebook", "<ButtonRelease-1>", self.__btn_release)

    def __btn_press(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify(x, y)
        if elem:
            index = widget.index("@%d,%d" % (x, y))
            if "close" in elem:
                widget.state(['pressed'])
                widget.pressed_index = index
            if "label" in elem:
                self.tabLoc=(x,y)
                whichTab = self.index("@%s,%s"%self.tabLoc)
                ghostText = self.tab(whichTab)["text"]
                self.moveTab = TabGhost(event.x_root,event.y_root,ghostText,
                                    xWindow=x,tabWidth=self.tabWidth)

    def __btn_release(self, event):
        x, y, widget = event.x, event.y, event.widget
        if self.tabLoc:
            pos = self.index("@%d,%d" % self.tabLoc)
            newPos = int(pos)+int((x-self.tabLoc[0])/self.tabWidth)
            if newPos>=int(self.index("end")):
                newPos=int(self.index("end"))-1
            elif newPos<0:
                newPos=0
            if newPos<self.index("end"):
                self.insert(newPos,pos)
                self.event_generate("<<NotebookMovedTab>>")
            self.tabLoc=None
        if not widget.instate(['pressed']):
            return 0
        elem =  widget.identify(x, y)
        if elem:
            index = widget.index("@%s,%s" % (x, y))

        if "close" in elem and widget.pressed_index == index:
            if int(self.index("end"))>1:
                widget.forget(index)
                widget.event_generate("<<NotebookClosedTab>>")

        widget.state(["!pressed"])
        widget.pressed_index = None

    def manualClose(self,tab):
        result=False
        if int(self.index("end"))>1:
            self.forget(tab)
            self.event_generate("<<NotebookClosedTab>>")
            result=True
        return result
    
    def add(self, tab, text="", *args, **kwargs):
        result=False
        if int(self.index("end"))<self.maxTabs:
            ttk.Notebook.add(self, tab, text=text, *args, **kwargs)
            result=True
        return result
            


if __name__ == "__main__":
    import tkinter
    root = tkinter.Tk()
    notebook = CloseNotebook(root)
    def createTab(event=None):
        frame = tkinter.Frame(notebook)
        text = tkinter.Text(frame)
        text.pack(expand=True, fill="both")
        end=notebook.index("end")
        notebook.add(frame, text="Page %s"%end)
    for i in range(5):
        createTab()
    notebook.bind_all("<Control-n>", createTab)
    notebook.pack(expand=True,fill="both")
    root.mainloop()
    
