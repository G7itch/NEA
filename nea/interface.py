import idlelib.colorizer as ic
import idlelib.percolator as ip
import os
import re
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.filedialog import *

from interpreter import Interpreter


class CodeEditor(tk.Tk):

    # noinspection PyPep8Naming
    def __init__(self, interpreter: Interpreter, file_open=None) -> None:
        """Creates the editor interface that the user interacts with throughout the entire program
        @param interpreter: The interpreter object being used
        @param file_open: Shortcut to open a file if this is not our first time setting up
        @return: None
        """
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
        # Initialise syntax highlighting

        KEYWORD = (r"\b(?P<KEYWORD>False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else"
                   r"|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try"
                   r"|while|with|yield)\b")
        # noinspection PyShadowingNames
        EXCEPTION = (r"([^.'\"\\#]\b|^)(?P<EXCEPTION>ArithmeticError|AssertionError|AttributeError|BaseException"
                     r"|BlockingIOError|BrokenPipeError|BufferError|BytesWarning|ChildProcessError"
                     r"|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError"
                     r"|DeprecationWarning|EOFError|Ellipsis|EnvironmentError|Exception|FileExistsError"
                     r"|FileNotFoundError|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError"
                     r"|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError"
                     r"|KeyboardInterrupt|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError"
                     r"|NotImplemented|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning"
                     r"|PermissionError|ProcessLookupError|RecursionError|ReferenceError|ResourceWarning|RuntimeError"
                     r"|RuntimeWarning|StopAsyncIteration|StopIteration|SyntaxError|SyntaxWarning|SystemError"
                     r"|SystemExit|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError"
                     r"|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError"
                     r"|Warning|WindowsError|ZeroDivisionError)\b")
        BUILTIN = (r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|all|any|ascii|bin|breakpoint|callable|chr|classmethod|compile"
                   r"|complex|copyright|credits|delattr|dir|divmod|enumerate|eval|exec|exit|filter|format|frozenset"
                   r"|getattr|globals|hasattr|hash|help|hex|id|input|isinstance|issubclass|iter|len|license|locals"
                   r"|map|max|memoryview|min|next|oct|open|ord|pow|print|quit|range|repr|reversed|round|set|setattr"
                   r"|slice|sorted|staticmethod|sum|type|vars|zip)\b")
        DOCSTRING = (r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|("
                     r"?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)")
        STRING = (r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"["
                  r"^\"\\\n]*(\\.[^\"\\\n]*)*\"?)")
        TYPES = (r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object|qbit|QBIT|cbit|CBIT|vector"
                 r"|VECTOR|gate|GATE|H|Z|X|Y|hadamard|HADAMARD)\b")  # Slightly modified to include new keywords
        NUMBER = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
        CLASSDEF = r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]"  # recolor of DEFINITION for class definitions
        DECORATOR = r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"
        INSTANCE = r"\b(?P<INSTANCE>super|self|cls)\b"
        COMMENT = r"(?P<COMMENT>#[^\n]*)"
        SYNC = r"(?P<SYNC>\n)"
        PROG = (rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|"
                rf"{DECORATOR}|{NUMBER}|{CLASSDEF}")
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

        if file_open is not None and type(file_open) is str:
            self.__openFile(file_name=file_open)

    ################################################################################
    # Note: syntax highlighting is based on the tkinter module used for idle itself

    # noinspection PyUnusedLocal
    def handle_enter(self, event) -> None:
        """
        Inserts Entry widget content into Text widget and clears Entry.
        @param event: Binding for tkinter, not used in function
        @return: None
        """
        code_line = self.entry.get()
        code_line = str(code_line)
        self.text_widget.insert("end", code_line + "\n")
        self.entry.delete(0, "end")
        self.__interpreter.interpret(code_line)

    def __newFile(self) -> None:
        """
        Creates a new file in the code editor, resetting title, file reference, and clearing text.
        @return: None
        """
        self.title("Untitled - Code editor")
        self.__file = None
        self.text_widget.delete(1.0, END)

    def darkstyle(self) -> ttk.Style:
        """
        Return a dark style to the window
        @return: style
        """
        style = ttk.Style(self)
        self.tk.call('source', r"C:\Users\OSINT\OneDrive\Documents\GitHub\NEA\azuredark\azuredark.tcl")
        style.theme_use('azure')
        return style

    def __openFile(self, file_name: str = None) -> None | bool:
        """
        Opens a file dialog to load a file into the code editor, updating title and content.
        @param file_name: name of the file to open
        @return: None if successful, otherwise False
        """
        if file_name is None:
            self.__file = askopenfilename(defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        else:
            self.__file = file_name

        if self.__file == "":
            self.__file = None
        else:
            try:
                self.title(os.path.basename(self.__file) + " - Code editor")
            except FileNotFoundError:
                return False
            self.text_widget.delete(1.0, END)
            file = open(self.__file, "r")
            self.text_widget.insert(1.0, file.read())
            file.close()

        recents = open(self.recents, "a")
        recents.write(str(os.path))
        recents.close()

    def __cut(self) -> None:
        """
        Links the clipboard's cutting function to the tkinter window
        @return: None
        """
        self.text_widget.event_generate("<<Cut>>")

    def __copy(self) -> None:
        """
        Links the clipboard's copy function to the tkinter window
        @return: None
        """
        self.text_widget.event_generate("<<Copy>>")

    def __paste(self) -> None:
        """
        Links the clipboard's pasting function to the tkinter window
        @return: None
        """
        self.text_widget.event_generate("<<Paste>>")

    def __saveFile(self) -> None:
        """
        Saves the content of the code editor to an existing or new file.
        @return: None
        """
        if self.__file is None:
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
        recents.write(str(os.path))
        recents.close()

    def __quitApplication(self) -> None:
        """
        Quits the application
        @return: None
        """
        self.destroy()


def filemenu() -> str:
    """
    Creates the menu for the file system. Second main menu for the user to interact with.
    @return: Any file that the user chooses to load from recents
    """
    # other systems may need to use 'clear' instead
    os.system("cls")
    file_open = None
    # The following logo needs to be displayed using raw strings otherwise pycharm gets snotty
    print(r"  ___  ____  _")
    print(r" / _ \/ ___|(_)_ __ ___")
    print(r"| | | \___ \| | '_ ` _ \ ")
    print(r"| |_| |___) | | | | | | |")
    print(r" \__\_\____/|_|_| |_| |_|")
    print("\n\n")
    print("[1] New file")
    print("[2] Open file")
    print("\n")
    recent_file = open(r"C:\Users\OSINT\OneDrive\Documents\GitHub\NEA\recents.txt", "r")
    recent_list = []
    for line in (recent_file.readlines()[-3:]):  # we only want the 3 most recent, which are at the end of the file
        recent_list.append(line.strip("\n"))
    recent_list = set(recent_list)
    recent_list = list(recent_list)
    recent_list.reverse()
    for i in range(96, 99):
        print(f"[{i}]", recent_list[i % 96])
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
            file_open = recent_list[0]
        case 97:
            file_open = recent_list[1]
        case 98:
            file_open = recent_list[2]
        case 99:
            exit(0)
        case _:
            exit(0)

    os.system("cls")
    return file_open

