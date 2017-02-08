import tkinter

from CloseNotebook import CloseNotebook
from CodePack import CodePack
from ColorDelegator2 import ColorDelegator
##from javacompile import RunJava
from StdIO import StdIO


class MorpheusToplevel(tkinter.Toplevel):
    tabs = []
    def __init__(self, language, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.title("Morpheus")
        self.language = language

        self.closeNotebook = CloseNotebook(self)
        self.closeNotebook.pack(expand=True, fill="both")
        
        self._createConsole()
        self.createTab()

        self.closeNotebook.bind_all("<Control-t>", self.createTab)

        self.menu = tkinter.Menu(self)
        self.menu.fileMenu = tkinter.Menu(self, tearoff=False)
        self.menu.editMenu = tkinter.Menu(self, tearoff=False)
        self.menu.runMenu = tkinter.Menu(self, tearoff=False)
        self.menu.windowMenu = tkinter.Menu(self, tearoff=False)
        
        self.menu.add_cascade(label="File", menu=self.menu.fileMenu)
        self.menu.add_cascade(label="Edit", menu=self.menu.editMenu)
        self.menu.add_cascade(label="Run", menu=self.menu.runMenu)
        self.menu.add_cascade(label="Window", menu=self.menu.windowMenu)
        
        for menu, sep, label, command, shortcutText, binding in [
            (self.menu.fileMenu,0,"New File", self.newFile, "Crtl+N", "<Control-n>"),
            (self.menu.fileMenu,0,"Open", self.openFile, "Crtl+O", "<Control-o>"),
            (self.menu.fileMenu,0,"Save", self.saveFile, "Crtl+S", "<Control-s>"),
            (self.menu.fileMenu,0,"Save As", self.saveAsFile, "Crtl+Shift+S", "<Control-S>"),
            (self.menu.fileMenu,0,"New File", self.newFile, "Crtl+N", "<Control-n>"),
            (self.menu.fileMenu,1,"Exit", self.destroy, "Alt+F4", None),

            (self.menu.editMenu,0,"Comment Out Selection", self.commentOut, "Alt+3", "3"),
            (self.menu.editMenu,0,"UnComment Selection", self.unComment, "Alt+4", "4"),
            
            (self.menu.runMenu,0,"Run Current Tab", self.runTab, "F5", "<F5>"),

            (self.menu.windowMenu,0,"Open Tab in New Window", self.popTab, "Ctrl+Shift+T", "<Control-T>")
            ]:
            if sep:
                menu.add_separator()
            menu.add_command(label=label, command=command, accelerator=shortcutText)
            if binding:
                self.bind(binding, command)     

        self.languageStringVar= tkinter.StringVar()
        self.languageStringVar.set(self.language)
        def setLanguage(*args):
            self.language=self.languageStringVar.get()
            for child in self.tabs:
                child.changeLanguage(self.language)
            print("self.language set to %s"%self.language)
        self.languageStringVar.trace("w", setLanguage)
        
        self.menu.runMenu.radioLanguageMenu=tkinter.Menu(self.menu.runMenu, tearoff=False)
        radioMenu=self.menu.runMenu.radioLanguageMenu
        radioMenu.add_radiobutton(label="Python", variable=self.languageStringVar)
        radioMenu.add_radiobutton(label="Java", variable=self.languageStringVar)
        self.menu.runMenu.add_cascade(label="Choose language", menu=radioMenu)

        self.config(menu=self.menu)

        self.closeNotebook.select(1)

    def _createConsole(self, event=None):
        self.consoleFrame = tkinter.Frame(self.closeNotebook)
        self.console = StdIO(self, self.consoleFrame)
        self.consoleFrame.text=self.console
        self.console.pack(expand=True, fill="both")
        
        self.consoleScrollbar = tkinter.Scrollbar(self.console)
        self.consoleScrollbar.pack(side = tkinter.RIGHT, fill="y")
        self.console.config(yscrollcommand=self.consoleScrollbar.set)
        self.consoleScrollbar.config(command=self.console.yview)
        
        self.closeNotebook.add(self.consoleFrame, text="Console")
        self.closeNotebook.insert(0,self.consoleFrame)

    def createTab(self, event=None):
        codePack = CodePack(self.closeNotebook, language=self.language)
        self.closeNotebook.add(codePack, text="Page %s"%len(self.tabs))
        self.tabs.append(codePack)
        return "break"

    def openFile(self, event=None):
        print("openFile ran")

    def saveFile(self, event=None):
        print("saveFile ran")
        return "break"

    def saveAsFile(self, event=None):
        print("SaveAsFile ran")
        return "break"

    def newFile(self, event=None):
        print("newFile ran")
        return "break"

    def runTab(self, event=None):
        #make sure there is a console
        removed=False
        if not("%s"%self.consoleFrame in self.closeNotebook.tabs()):
            self._createConsole()
        self.closeNotebook.select(self.closeNotebook.index(self.consoleFrame))

        print("runTab ran (%s code)"%self.language)
        return "break"

    def commentOut(self, event=None):
        if event:
            if event.state==131072:
                print("commentOut ran")
        else:
            print("commentOut ran")
        return "break"

    def unComment(self, event=None):
        if event:
            if event.state==131072:
                print("unComment ran")
        else:
            print("unComment ran")
        return "break"

    def popTab(self, event=None):
        
        codePack = None
        for tab in self.closeNotebook.winfo_children():
            if tab.winfo_ismapped():
                codePack = tab
                
        top = MorpheusToplevel(self.language)
        top.update()
        
        codePackCopy = None
        for tab in top.closeNotebook.winfo_children():
            if tab.winfo_ismapped():
                codePackCopy = tab
                
        codePackCopy.text.insert("1.0",codePack.text.get("1.0","end"))
        self.closeNotebook.hide(codePack)
        



    
if __name__ == "__main__":
    root = tkinter.Tk()
    top = MorpheusToplevel("Java", root)
    root.withdraw()
    def close():
        root.destroy()
    top.protocol("WM_DELETE_WINDOW")
    root.mainloop()
