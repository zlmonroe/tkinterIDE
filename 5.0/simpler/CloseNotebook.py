import os
import tkinter
from tkinter import ttk

class CloseNotebook(ttk.Notebook):
    def __init__(self, root, *args, **kwargs):
        self.pressed_index=None
        
        self.imgdir = os.path.join(os.path.dirname(__file__), 'img')
        self.i1 = tkinter.PhotoImage("img_close", file=os.path.join(self.imgdir, 'close.gif'))
        self.i2 = tkinter.PhotoImage("img_closeactive",
            file=os.path.join(self.imgdir, 'close_active.gif'))
        self.i3 = tkinter.PhotoImage("img_closepressed",
            file=os.path.join(self.imgdir, 'close_pressed.gif'))

        self.style = ttk.Style()

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
                         ("ButtonNotebook.close", {"side": "left", "sticky": ''})]
                    })]
                })]
            })]
        )
        ttk.Notebook.__init__(self, style="ButtonNotebook")
        self.bind_class("TNotebook", "<ButtonPress-1>", self.btn_press, True)
        self.bind_class("TNotebook", "<ButtonRelease-1>", self.btn_release)

    def btn_press(self,event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify(x, y)
        index = widget.index("@%d,%d" % (x, y))

        if "close" in elem:
            widget.state(['pressed'])
            widget.pressed_index = index

    def btn_release(self,event):
        x, y, widget = event.x, event.y, event.widget

        if not widget.instate(['pressed']):
            return

        elem =  widget.identify(x, y)
        if elem!="":
            index = widget.index("@%d,%d" % (x, y))

        if "close" in elem and widget.pressed_index == index:
            widget.forget(index)
            widget.event_generate("<<NotebookClosedTab>>")

        widget.state(["!pressed"])
        widget.pressed_index = None

if __name__=="__main__":
    root = tkinter.Tk()

    nb = CloseNotebook(root)
    f1 = tkinter.Frame(nb, background="red")
    f2 = tkinter.Frame(nb, background="green")
    f3 = tkinter.Frame(nb, background="blue")
    
    nb.add(f1, text='Red', padding=3)
    nb.add(f2, text='Green', padding=3)
    nb.add(f3, text='Blue', padding=3)
    
    nb.pack(expand=1, fill='both')

    root.mainloop()
