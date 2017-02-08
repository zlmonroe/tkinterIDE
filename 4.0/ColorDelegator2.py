import time
import re
import keyword
import builtins
from idlelib.Delegator import Delegator
from idlelib.configHandler import idleConf

DEBUG = False

class ColorDelegator(Delegator):

    def __init__(self, language="Python", bg="white"):
        Delegator.__init__(self)
        self.language=language
        self.bg=bg
        self.prog = re.compile(self.make_pat(self.language), re.S)
        self.idprog = re.compile(r"\s+(\w+)", re.S)
        self.LoadTagDefs()
        
    def make_pat(self, language):
        def namedAny(name, alternates):
            "Return a named group pattern matching list of alternates."
            return "(?P<%s>" % name + "|".join(alternates) + ")"
        if language=="Python":
            kw = r"\b" + namedAny("KEYWORD", keyword.kwlist) + r"\b"
            builtinlist = [str(name) for name in dir(builtins)
                                                if not name.startswith('_') and \
                                                name not in keyword.kwlist]
            # self.file = open("file") :
            # 1st 'file' colorized normal, 2nd as builtin, 3rd as string
            builtin = r"([^.'\"\\#]\b|^)" + namedAny("BUILTIN", builtinlist) + r"\b"
            comment = namedAny("COMMENT", [r"#[^\n]*"])
            stringprefix = r"(\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR|rb|rB|Rb|RB)?"
            sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
            dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
            sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
            dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
            string = namedAny("STRING", [sq3string, dq3string, sqstring, dqstring])
            return kw + "|" + builtin + "|" + comment + "|" + string +\
                   "|" + namedAny("SYNC", [r"\n"])
        elif language=="Java":
            keywordlist=['abstract', 'continue', 'for', 'new', 'switch',
                         'assert', 'default', 'goto', 'package', 'synchronized',
                         'do', 'if', 'private', 'this', 'break',
                         'implements', 'protected', 'throw',
                         'else', 'import', 'public', 'throws', 'case', 'enum',
                         'instanceof', 'return', 'transient', 'catch',
                         'extends', 'short', 'try', 'final',
                         'interface', 'static', 'void', 'class', 'finally',
                         'strictfp', 'volatile', 'const', 
                         'native', 'super', 'while',
                         #not technically keywords
                         'true', 'false', 'null']
            kw=r"\b"+namedAny("KEYWORD",keywordlist)+r"\b" 
            builtinlist=['boolean','double', 'byte', 'int','char','long','float',]
            builtin=r"([^.'\"\\#]\b|^)" + namedAny("BUILTIN", builtinlist) + r"\b"

            #Error list:
            #   1. Ends on / without */
            comment=namedAny("COMMENT",[r'//.*?\n']+[r'/\*[^\*]*((\\.|\*(?!\/))[^/\*]*)*(\*/)?'])
            
            stringprefix = r"(\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR|rb|rB|Rb|RB)?"
            sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
            dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
            string = namedAny("STRING", [sqstring, dqstring])

        return kw + "|" + builtin + "|" + comment + "|" + string +\
               "|" + namedAny("SYNC", [r"\n"])

    def setdelegate(self, delegate):
        if self.delegate is not None:
            self.unbind("<<toggle-auto-coloring>>")
        Delegator.setdelegate(self, delegate)
        if delegate is not None:
            self.config_colors()
            self.bind("<<toggle-auto-coloring>>", self.toggle_colorize_event)
            self.notify_range("1.0", "end")
        else:
            # No delegate - stop any colorizing
            self.stop_colorizing = True
            self.allow_colorizing = False

    def config_colors(self):
        for tag, cnf in self.tagdefs.items():
            if cnf:
                self.tag_configure(tag, **cnf)
        self.tag_raise('sel')

    def LoadTagDefs(self):
        theme = idleConf.GetOption('main','Theme','name')
        self.tagdefs = {
            "COMMENT": {'background': self.bg, 'foreground': '#dd0000'},
            "MODULE": {'background': self.bg, 'foreground': "turquoise3"},
            "KEYWORD": {'background': self.bg, 'foreground': 'orange'},
            "BUILTIN": {'background': self.bg, 'foreground': 'purple2'},
            "STRING": {'background': self.bg, 'foreground': '#00aa00'},
            "DEFINITION": {'background': self.bg, 'foreground': '#0000ff'},
            "SYNC": {'background':None,'foreground':None},
            "TODO": {'background': None, 'foreground': None},
            "ERROR": {'background': '#ff7777', 'foreground': '#000000'},
            "hit": {'background': '#000000', 'foreground': '#ffffff'},
            }
        if DEBUG: print('tagdefs',self.tagdefs)

    def insert(self, index, chars, tags=None):
        index = self.index(index)
        self.delegate.insert(index, chars, tags)
        self.notify_range(index, index + "+%dc" % len(chars))

    def delete(self, index1, index2=None):
        index1 = self.index(index1)
        self.delegate.delete(index1, index2)
        self.notify_range(index1)

    after_id = None
    allow_colorizing = True
    colorizing = False

    def notify_range(self, index1, index2=None):
        self.tag_add("TODO", index1, index2)
        if self.after_id:
            if DEBUG: print("colorizing already scheduled")
            return
        if self.colorizing:
            self.stop_colorizing = True
            if DEBUG: print("stop colorizing")
        if self.allow_colorizing:
            if DEBUG: print("schedule colorizing")
            self.after_id = self.after(1, self.recolorize)

    close_when_done = None # Window to be closed when done colorizing

    def close(self, close_when_done=None):
        if self.after_id:
            after_id = self.after_id
            self.after_id = None
            if DEBUG: print("cancel scheduled recolorizer")
            self.after_cancel(after_id)
        self.allow_colorizing = False
        self.stop_colorizing = True
        if close_when_done:
            if not self.colorizing:
                close_when_done.destroy()
            else:
                self.close_when_done = close_when_done

    def toggle_colorize_event(self, event):
        if self.after_id:
            after_id = self.after_id
            self.after_id = None
            if DEBUG: print("cancel scheduled recolorizer")
            self.after_cancel(after_id)
        if self.allow_colorizing and self.colorizing:
            if DEBUG: print("stop colorizing")
            self.stop_colorizing = True
        self.allow_colorizing = not self.allow_colorizing
        if self.allow_colorizing and not self.colorizing:
            self.after_id = self.after(1, self.recolorize)
        if DEBUG:
            print("auto colorizing turned",\
                  self.allow_colorizing and "on" or "off")
        return "break"

    def recolorize(self):
        self.after_id = None
        if not self.delegate:
            if DEBUG: print("no delegate")
            return
        if not self.allow_colorizing:
            if DEBUG: print("auto colorizing is off")
            return
        if self.colorizing:
            if DEBUG: print("already colorizing")
            return
        try:
            self.stop_colorizing = False
            self.colorizing = True
            if DEBUG: print("colorizing...")
            t0 = time.perf_counter()
            self.recolorize_main()
            t1 = time.perf_counter()
            if DEBUG: print("%.3f seconds" % (t1-t0))
        finally:
            self.colorizing = False
        if self.allow_colorizing and self.tag_nextrange("TODO", "1.0"):
            if DEBUG: print("reschedule colorizing")
            self.after_id = self.after(1, self.recolorize)
        if self.close_when_done:
            top = self.close_when_done
            self.close_when_done = None
            top.destroy()

    def recolorize_main(self):
        next = "1.0"
        while True:
            item = self.tag_nextrange("TODO", next)
            if not item:
                break
            head, tail = item
            self.tag_remove("SYNC", head, tail)
            item = self.tag_prevrange("SYNC", head)
            if item:
                head = item[1]
            else:
                head = "1.0"

            chars = ""
            next = head
            lines_to_get = 1
            ok = False
            while not ok:
                mark = next
                next = self.index(mark + "+%d lines linestart" %
                                         lines_to_get)
                lines_to_get = min(lines_to_get * 2, 100)
                ok = "SYNC" in self.tag_names(next + "-1c")
                line = self.get(mark, next)
                ##print head, "get", mark, next, "->", repr(line)
                if not line:
                    return
                for tag in self.tagdefs:
                    self.tag_remove(tag, mark, next)
                chars = chars + line
                m = self.prog.search(chars)
                while m:
                    for key, value in m.groupdict().items():
                        if value:
                            a, b = m.span(key)
                            self.tag_add(key,
                                         head + "+%dc" % a,
                                         head + "+%dc" % b)
                            if value in ("def", "class"):
                                m1 = self.idprog.match(chars, b)
                                if m1:
                                    a, b = m1.span(1)
                                    self.tag_add("DEFINITION",
                                                 head + "+%dc" % a,
                                                 head + "+%dc" % b)
                    m = self.prog.search(chars, m.end())
                if "SYNC" in self.tag_names(next + "-1c"):
                    head = next
                    chars = ""
                else:
                    ok = False
                if not ok:
                    # We're in an inconsistent state, and the call to
                    # update may tell us to stop.  It may also change
                    # the correct value for "next" (since this is a
                    # line.col string, not a true mark).  So leave a
                    # crumb telling the next invocation to resume here
                    # in case update tells us to leave.
                    self.tag_add("TODO", next)
                self.update()
                if self.stop_colorizing:
                    if DEBUG: print("colorizing stopped")
                    return

    def removecolors(self):
        for tag in self.tagdefs:
            self.tag_remove(tag, "1.0", "end")

def _color_delegator(parent, language):
    from tkinter import Toplevel, Text
    from idlelib.Percolator import Percolator

    top = Toplevel(parent)
    top.title("Test ColorDelegator- %s"%language)
    top.geometry("600x400+%d+%d" % (parent.winfo_rootx() + 200,
                  parent.winfo_rooty() + 150))
    source = "#Python\nif somename:\n x = 'abc'\nprint(\"Test\")\n\n/*\nJava\n*/\n\nboolean num=true;\n"
    text = Text(top, background="white")
    text.pack(expand=1, fill="both")
    text.insert("insert", source)
    text.focus_set()

    p = Percolator(text)
    d = ColorDelegator(language=language)
    p.insertfilter(d)

if __name__ == "__main__":
    from tkinter import Tk, TOP, BOTTOM, Label, Button
    root= Tk()
    root.title("Info")
    Label(text="Example for ColorDelegator for each language").pack(side=TOP)
    for language in ["Java", "Python"]:
        def runText(language):
            _color_delegator(root, language)
        Button(text=language, command=lambda lang=language: runText(lang)).pack(side=BOTTOM)
    root.mainloop()
