from ChangeText import ChangeText
import tkinter
import sys
import os
from idlelib import IOBinding
import io
import msvcrt

class StdIO(ChangeText):
    returnFlag=False
    deleteFlag=False
    def __init__(self, root, *args, **kwargs):
        ChangeText.__init__(self, *args, **kwargs)
        
        self.originalStdin, sys.stdin = sys.stdin, self
        self.originalStdout, sys.stdout = sys.stdout, self
        
        self.root=root
        self.tag_config("immutable", foreground="gray")
        
        self.unbind_class(ChangeText, "<Control-o>")
        
        def windowDeletion():
            self.deleteFlag=True
            sys.stdin=self.originalStdin
            sys.stdout=self.originalStdout
            sys.stdout.write(self.get("1.0","end"))
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", windowDeletion)
            
        def immutable(event):
            if not(self.tag_ranges("sel")):
                if "immutable" in self.tag_names("insert -1c"):
                    return "break"
            else:
                ranges = self.tag_ranges("sel")
                if "immutable" in self.tag_names(ranges[0]):
                    return "break"
        self.bind("<BackSpace>",immutable)
        self.bind("<Delete>", immutable)
        
        def blockInsert(event):
            if "immutable" in self.tag_names("insert"):
                if event.keysym not in ["Left","Right","Up","Down"] and (event.keysym!="c" and event.state!=4):
                    return "break"
            
        self.bind("<Key>", blockInsert)
            
        self.bind("<Return>", self.returnFlag)
                  
    def write(self, string):
        immutable = self.tag_ranges("immutable")
        if immutable==():
            immutable="1.0"
        else:
            immutable=immutable[1]
        self.insert("%s +1c"%immutable, string, ("immutable"))
        self.mark_set("insert", "end")
        self.see("end")

    def returnFlag(self, event):
        self.returnFlag=True
        
    def readline(self):
        self.returnFlag=False
        self.root.update()
        while not(self.returnFlag):
            if self.deleteFlag:
                return "\n"
            else:
                self.root.update()
                flag = self.returnFlag
        start = self.tag_ranges("immutable")[1]
        read = self.get(start, "insert lineend -1c")
        print(read)
        if read=="":
            read="\n"
        self.tag_add("immutable",start, "insert lineend")
        return read
        


if __name__=="__main__":
    from javacompile import RunJava
    root = tkinter.Tk()
    text = StdIO(root)
    text.pack()
    sys.stdout = text
    sys.stdin = text
    root.update()
    StatPackage = RunJava(codeFile="StatPackage.java")
    StatPackage.javac()
    StatPackage.java()

    root.mainloop()
