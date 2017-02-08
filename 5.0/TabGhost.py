import tkinter
import images

class TabGhost(tkinter.Toplevel):
    def __init__(self, x, y, text, xWindow=0, tabWidth=80, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.attributes("-alpha", 0.5)
        self.y=y
        self.offset=xWindow%tabWidth
        self.overrideredirect(True)
        self.geometry("80x20+%s+%s"%(x-self.offset,y))
        self.i1 = tkinter.PhotoImage("img_close", data=images.close)
        
        self.label = tkinter.Label(self, text=text)
        self.photo = tkinter.Label(self, image = "img_close")
        self.label.pack(side="left")
        self.photo.pack(side="right")
        
        self.bind_all("<Motion>", self.Move)
        self.bind_all("<ButtonRelease-1>", self.End)

    def End(self,event):
        self.unbind_all("<Motion>")
        self.unbind_all("<ButtonRelease-1>")
        self.destroy()

    def Move(self,event):
        x = event.x_root
        self.geometry("+%s+%s" % (x-self.offset, self.y))

if __name__ == "__main__":
    root = tkinter.Tk()
    def createGhost():
        ghost = TabGhost(50,50,"Page 1")
    button = tkinter.Button(root, text="Ghost Tab", command=createGhost)
    button.pack()
    root.mainloop()
