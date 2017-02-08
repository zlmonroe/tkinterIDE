from tkinter import tix as tkinter
from ChangeText import ChangeText
from idlelib.Percolator import Percolator
from ColorDelegator2 import ColorDelegator


class CodePack(tkinter.Frame):
    lineText=None
    lastChar=""
    indentNum=0
    
    def __init__(self, parent, language="Python", font=("Courier", "10"), numbersWidth=30, *args, **kwargs):
        '''Initialize CodePack instance'''
        tkinter.Frame.__init__(self, parent)

        self.text=ChangeText(self, font=("Courier",13),
                        wrap="word", spacing3="2",
                        bd=0, undo=True,
                        background="white",
                        *args, **kwargs)
        self.text.pack(side=tkinter.RIGHT, expand=True, fill="both")
        self.text.bind("<<Change>>", self._changed)
        self.text.bind("<Control-KeyRelease-a>", self._highlightLine)
        
        self.lineNumbersFrame = tkinter.Frame(self)
        self.lineNumbersFrame.pack(side=tkinter.LEFT, fill="y")

        self.lineNumbers = tkinter.Canvas(self.lineNumbersFrame, width=30)
        self.lineNumbers.pack(expand=True, fill="y")
        

        self.font=font
        self.language=language
        
        self.p = Percolator(self.text)
        self.d = ColorDelegator(language=self.language, bg="white")
        self.p.insertfilter(self.d)
        
        self.text.tag_config("Current Line", background="cornsilk")
        self._setLanguageBindings()

    def changeLanguage(self, language):
        self.language=language
        del(self.d, self.p)
        self.p = Percolator(self.text)
        self.d = ColorDelegator(language=self.language, bg="white")
        self.p.insertfilter(self.d)

    def _setLanguageBindings(self):
        '''Sets the Key Bindings based on the chosen language for text box'''
        lang=self.language

        #Overides Tabs for all languages and replaces with spaces
        def _overrideTab(event):
            if event.state==4:
                pass
            else:
                self.text.insert(tkinter.INSERT,"    ")
                return "break"
        self.text.bind("<Tab>", _overrideTab)

        # Python (default) language bindings
        if lang=="Python":
            def _pythonReturn(event):
                self.lineText=self.text.get("insert -1l linestart","insert -1l lineend")
                if self.lineText:
                    self.lastChar = self.lineText[-1]
                    self.indentNum=len(self.lineText)-len(self.lineText.lstrip(' '))
                if self.lastChar==":":
                    self.indentNum+=4
                self.text.insert("insert linestart"," "*self.indentNum)
            self.text.bind("<KeyRelease-Return>", _pythonReturn)

        # java lanaguage bindings    
        elif lang=="Java":
            def _javaReturn(event):
                self.lineText=self.text.get("insert -1l linestart","insert -1l lineend")
                if self.lineText:
                    self.lastChar = self.lineText[-1]
                    self.indentNum=len(self.lineText)-len(self.lineText.lstrip(' '))
                if self.lastChar=="{":
                    self.indentNum+=4
                elif self.lastChar=="}":
                    if self.indentNum>=4:
                        self.indentNum+=-4
                elif self.lastChar.isalnum() or self.lastChar==')':
                        self.text.insert("insert -1l lineend",';')
                self.text.insert("insert linestart"," "*self.indentNum)

            self.text.bind("<KeyRelease-Return>", _javaReturn)

        #raise KeyError Exception if the language is not supported
        else:
            raise KeyError("Currently unsupported langauge")
        
    def _changed(self, event):
        '''events to process upon change of text box'''
        self.redrawLineNumbers()
        self._highlightLine()
        self.text.edit_separator()
        
        
    def redrawLineNumbers(self):
        '''redraw line numbers'''
        self.lineNumbers.delete("all")

        i = self.text.index("@0,0")
        while True :
            dline= self.text.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.lineNumbers.create_text(2,y,anchor="nw", text=linenum)
            i = self.text.index("%s+1line" % i)

    def _highlightLine(self, event=None):
        '''highlights the cursor's line in text widget'''
        self.text.tag_remove("Current Line","1.0",tkinter.END)
        if self.text.tag_ranges("sel")==():
            self.text.tag_add("Current Line", "insert linestart", "insert lineend+1c")    
        else:
            self.text.tag_add("Current Line", "insert linestart", "insert lineend+1c")    
            ranges = self.text.tag_ranges("sel")
            self.text.tag_remove("Current Line", ranges[0], ranges[1])

if __name__ == "__main__":
    '''test'''
    root = tkinter.Tk()
    root.title("CodePack Example")
    CodePack = CodePack(root, language="Python")
    CodePack.pack()
    def output():
        print(CodePack.text.get("1.0","end -1c"))
    button = tkinter.Button(root, text="print", command=output)
    button.pack()
    root.mainloop()
