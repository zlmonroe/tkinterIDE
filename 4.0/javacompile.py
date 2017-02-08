import os
import subprocess
from subprocess import STDOUT, PIPE
import tkinter.filedialog as dialog
import shutil
import time


class RunJava():
    
    def __init__(self, codeFile=None, code=None):
        if codeFile:
            self.codeFile=codeFile
            self.classFile = os.path.basename(self.codeFile).split('.')[0]
        elif code:
            codeFile = code[1]
            with open(codeFile, 'w+') as tmp:
                tmp.write(code[0])
            self.codeFile=codeFile
            self.classFile = os.path.splitext(self.codeFile)[0]

    def javac(self):
        try:
            subprocess.check_call(["C:/Program Files/Java/jdk1.8.0_65/bin/javac.exe", self.codeFile])
        except Exception as e:
            return e
        else:
            return "compiled"

    def java(self):
        cmd=["java.exe", self.classFile]
        proc=subprocess.Popen(cmd, stdout = PIPE, stderr = STDOUT)
        input = subprocess.Popen(cmd, stdin = PIPE)
        print(proc.stdout.read().decode("utf-8"))

if __name__ == "__main__":

    java = RunJava(codeFile="./StatPackage.java")
    java.javac()
    java.java()
    input()



