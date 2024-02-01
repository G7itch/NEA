import tkinter as tk
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import tkinter.ttk as ttk
import re
import idlelib.colorizer as ic
import idlelib.percolator as ip
from interpreter import Interpreter


class CodeEditor(tk.Tk):

    def __init__(self, interpreter: Interpreter, file_open=None):
        """Creates the editor interface that the user interacts with throughout the entire program"""
        super().__init__()

        self.recents = r"C:\Users\OSINT\OneDrive\Documents\GitHub\NEA\recents.txt"
        self.title("Code Editor")
        self.darkstyle()  # Sets the editor to dark mode
        self.__thisMenuBar = Menu(self)
        self.__thisFileMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisEditMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__file = None
        self.__interpreter = interpreter
        # if not(isinstance(interpreter,Interpreter)):
        #    raise TypeError("Interpreter object is not valid")
        self.text_widget = tk.Text(self, wrap="word", undo=True, font=("Calibri", 16))
        self.text_widget.pack(expand=True, fill="both")
        self.__thisScrollBar = Scrollbar(self.text_widget)

        self.entry = tk.Entry(self, width=50, font=("Calibri", 16))
        self.entry.pack(side="bottom", fill="x")
        self.entry.bind("<Return>", self.handle_enter)
        ###################################################################
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)

        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)

        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)
        self.config(menu=self.__thisMenuBar)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.__thisScrollBar.set)
        #####################################################################
        ################# Initialise syntax highlighting#####################
        KEYWORD = r"\b(?P<KEYWORD>False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"
        EXCEPTION = r"([^.'\"\\#]\b|^)(?P<EXCEPTION>ArithmeticError|AssertionError|AttributeError|BaseException|BlockingIOError|BrokenPipeError|BufferError|BytesWarning|ChildProcessError|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|DeprecationWarning|EOFError|Ellipsis|EnvironmentError|Exception|FileExistsError|FileNotFoundError|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError|KeyboardInterrupt|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError|NotImplemented|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|PermissionError|ProcessLookupError|RecursionError|ReferenceError|ResourceWarning|RuntimeError|RuntimeWarning|StopAsyncIteration|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|WindowsError|ZeroDivisionError)\b"
        BUILTIN = r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|all|any|ascii|bin|breakpoint|callable|chr|classmethod|compile|complex|copyright|credits|delattr|dir|divmod|enumerate|eval|exec|exit|filter|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|isinstance|issubclass|iter|len|license|locals|map|max|memoryview|min|next|oct|open|ord|pow|print|quit|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|sum|type|vars|zip)\b"
        DOCSTRING = r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)"
        STRING = r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
        TYPES = r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object|qbit|QBIT|cbit|CBIT|vector|VECTOR|gate|GATE|H|Z|X|Y|hadamard|HADAMARD)\b"  # Slightly modified to include new keywords
        NUMBER = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
        CLASSDEF = r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]"  # recolor of DEFINITION for class definitions
        DECORATOR = r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"
        INSTANCE = r"\b(?P<INSTANCE>super|self|cls)\b"
        COMMENT = r"(?P<COMMENT>#[^\n]*)"
        SYNC = r"(?P<SYNC>\n)"
        PROG = rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|{DECORATOR}|{NUMBER}|{CLASSDEF}"
        IDPROG = r"(?<!class)\s+(\w+)"
        TAGDEFS = {'COMMENT': {'foreground': "orange", 'background': None},
                   'TYPES': {'foreground': "orange", 'background': None},
                   'NUMBER': {'foreground': "orange", 'background': None},
                   'BUILTIN': {'foreground': "orange", 'background': None},
                   'STRING': {'foreground': "orange", 'background': None},
                   'DEFINITION': {'foreground': "orange", 'background': None},
                   'INSTANCE': {'foreground': "orange", 'background': None},
                   'KEYWORD': {'foreground': "orange", 'background': None},
                   }

        cd = ic.ColorDelegator()
        cd.prog = re.compile(PROG, re.S | re.M)
        cd.idprog = re.compile(IDPROG, re.S)
        cd.tagdefs = {**cd.tagdefs, **TAGDEFS}
        ip.Percolator(self.text_widget).insertfilter(cd)

        if file_open is not None and type(file_open) == str:
            self.__openFile(file_name=file_open)

    ################################################################################
    # Note: syntax highlighting is based on the tkinter module used for idle itself

    def handle_enter(self, event):
        """Inserts Entry widget content into Text widget and clears Entry."""
        code_line = self.entry.get()
        code_line = str(code_line)
        self.text_widget.insert("end", code_line + "\n")
        self.entry.delete(0, "end")
        self.__interpreter.interpret(code_line)

    def __newFile(self):
        """Creates a new file in the code editor, resetting title, file reference, and clearing text."""
        self.title("Untitled - Code editor")
        self.__file = None
        self.text_widget.delete(1.0, END)

    def darkstyle(self):
        """Return a dark style to the window"""
        style = ttk.Style(self)
        self.tk.call('source', r"C:\Users\OSINT\OneDrive\Documents\GitHub\NEA\azuredark\azuredark.tcl")
        style.theme_use('azure')
        return style

    def __openFile(self, file_name=None):
        """Opens a file dialog to load a file into the code editor, updating title and content."""
        if file_name == None:
            self.__file = askopenfilename(defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        else:
            self.__file = file_name

        if self.__file == "":
            self.__file = None
        else:
            try:
                self.title(os.path.basename(self.__file) + " - Code editor")
            except:
                return False
            self.text_widget.delete(1.0, END)
            file = open(self.__file, "r")
            self.text_widget.insert(1.0, file.read())
            file.close()

        recents = open(self.recents, "a")
        recents.append(str(os.path(self.__file)))
        recents.close()

    def __cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def __copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def __paste(self):
        self.text_widget.event_generate("<<Paste>>")

    def __saveFile(self):
        """Saves the content of the code editor to an existing or new file."""
        if self.__file == None:
            self.__file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

            if self.__file == "":
                self.__file = None
            else:
                file = open(self.__file, "w")
                file.write(self.text_widget.get(1.0, END))
                file.close()
                self.title(os.path.basename(self.__file) + " - Code editor")

        else:
            file = open(self.__file, "w")
            file.write(self.text_widget.get(1.0, END))
            file.close()

        recents = open(self.recents, "a")
        recents.append(str(os.path(self.__file)))
        recents.close()

    def __quitApplication(self):
        self.destroy()


def filemenu():
    os.system("cls")
    file_open = None
    print("  ___  ____  _")
    print(" / _ \/ ___|(_)_ __ ___")
    print("| | | \___ \| | '_ ` _ \ ")
    print("| |_| |___) | | | | | | |")
    print(" \__\_\____/|_|_| |_| |_|")
    print("\n\n")
    print("[1] New file")
    print("[2] Open file")
    print("\n")
    recentfile = open(r"C:\Users\OSINT\OneDrive\Documents\GitHub\NEA\recents.txt", "r")
    recentlist = []
    for line in (recentfile.readlines()[-3:]):  # we only want the 3 most recent, which are at the end of the file
        recentlist.append(line.strip("\n"))
    recentlist = set(recentlist)
    recentlist = list(recentlist)
    recentlist.reverse()
    for i in range(96, 99):
        print(f"[{i}]", recentlist[i % 96])
    print("\n")
    print("[99] quit")
    print("\n")
    option = int(input("> "))

    match option:
        case 1:
            file_open = None
        case 2:
            file_open = askopenfilename(defaultextension=".txt",
                                        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        case 96:
            file_open = recentlist[0]
        case 97:
            file_open = recentlist[1]
        case 98:
            file_open = recentlist[2]
        case 99:
            exit(0)

    os.system("cls")
    return file_open
