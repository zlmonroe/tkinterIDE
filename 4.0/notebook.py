from tkinter import tix as tkinter
from tkinter import ttk

root = tkinter.Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", side=tkinter.LEFT)

for info in [
    "Title 1",
    "Title 2",
    "Title 3"]:
    tab = tkinter.Frame()
    notebook.add(tab, text=info)
    tkinter.Text(tab).pack()

#buttons
buttonFrame = tkinter.Frame()
buttonFrame.pack(side=tkinter.RIGHT, fill="y")
for text in [
    "thing 1",
    "thing 2",
    "thing 3"]:
    b = tkinter.Button(buttonFrame, text=text)
    b.pack()
    
