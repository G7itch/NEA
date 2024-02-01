import ctypes
import gc
import json
import random
import sqlite3
import string
from datetime import datetime

from plyer import notification

from abstract import AbstractSyntaxTree
from lexer import *


class Interpreter(object):
    """The interpreter class manages the interpretation the lexer parsed input"""

    def __init__(self) -> None:
        """
        Initialise the interpreter class
        @return: None
        """
        self.ast = None
        self.lex = Lexer(rules)
        self.command_list = []
        self.user_vars = {}
        self.__temp_vars = {}
        self.__command_string = ""

    def interpret(self, line: str) -> None:
        """
        Interpret the lexical-parsed input from the user and send it for execution
        @param line: The input line
        @return: None
        """
        letters = string.ascii_letters
        objs = False
        self.__temp_vars = {}
        self.__command_string = ""  # This is used for regexing against to check for achievements

        for token in self.lex.scan(line):
            self.command_list.append(token)
            self.__command_string += token[1]

        # the next step is to filter supplements and split objects
        for count, element in enumerate(self.command_list):
            match element[0]:
                case "SUPPLIMENT" | "END_STMNT":  # These just make writing easier, they don't impact code at all
                    self.command_list.remove(element)
                case "OBJECT":
                    objs = True
                    parameters = (((element[1].split("("))[1]).strip(")")).split(
                        ",")  # creates a list of all the parameters that the object has
                    function = (element[1].split("("))[0]
                    for param in range(len(parameters)):
                        identifier = ''.join(random.choice(letters) for _ in range(20))
                        while identifier in self.__temp_vars:
                            identifier = ''.join(random.choice(letters) for _ in range(20))
                        self.__temp_vars[identifier] = parameters[param]
                        parameters[param] = id(identifier)
                    self.command_list[count] = (function, parameters)
                case _:
                    pass

        self.__setvars()
        self.__giveaward()

        if not objs:
            self.ast = AbstractSyntaxTree(self.command_list, self.__temp_vars)
        else:
            objects = [function for function in self.command_list if type(function) is tuple]
            for function in objects:
                params = [self.__temp_vars[ctypes.cast(param, ctypes.py_object).value] for param in function[1]]
                # This line makes a list of (references -> identifiers -> values) and stores it in the params variable
                function = str(function[0]) + "(" + ",".join(map(str, params)) + ")"  # String formatting for execution
                exec(function)

        # Free up memory from temporary variables that we will not use again
        # noinspection PyUnusedLocal
        for element in self.__temp_vars:
            del element  # allocate null value to memory address
        gc.collect()  # use the builtin garbage collector

    def __giveaward(self) -> None | bool:
        """
        This function controls the logic of awarding achievements to the user.
        @return: None if successful execution, otherwise False
        """
        self.__conn = sqlite3.connect("file:master.db?mode=rw", uri=True)
        self.__c = self.__conn.cursor()
        self.__c.row_factory = lambda cursor, row: row[0]  # converts results into a simple list for checking
        regex_strings = self.__c.execute('SELECT regex FROM challenges').fetchall()
        for regex in regex_strings:
            # Check if they have met the requirements for earning the achievement
            if regex is not None:
                if re.match(regex, self.__command_string) is not None:

                    # Gather relevant data
                    challengeid = int(
                        self.__c.execute(f"SELECT challengeid FROM challenges WHERE regex='{regex}'").fetchall()[0])
                    challengedesc = str(
                        self.__c.execute(f"SELECT challengedesc FROM challenges WHERE regex='{regex}'").fetchall()[0])
                    stats = {"challengeID": challengeid,
                             "date": datetime.today().strftime('%Y-%m-%d'),
                             "challengeDesc": challengedesc}
                    json_string = json.dumps(stats)

                    with open("achievements.json", "r") as achievements:  # is the achievement already got?
                        if json_string in achievements.readlines():
                            return False

                    with open("achievements.json", "a") as achievements:  # write to JSON
                        achievements.write(json_string)
                        achievements.write("\n")

                        # Give the user a desktop notification
                        title = "Achievement unlocked!"
                        message = challengedesc
                        notification.notify(title=title, message=message, app_name="QSim", ticker="Achievement!")

        self.__conn.close()

    def __setvars(self) -> None:
        """
        Sets the command list to include variable identifiers and locations
        This helps for syntax parsing when put into the AST.
        @return: None
        """
        letters = string.ascii_letters
        for element in range(len(self.command_list)):
            if self.command_list[element][0] == "LITERAL" or self.command_list[element][0] == "DIGIT":
                identifier = ''.join(random.choice(letters) for _ in range(20))
                while identifier in self.__temp_vars:
                    identifier = ''.join(random.choice(letters) for _ in range(20))
                self.__temp_vars[identifier] = self.command_list[element][1]
                self.command_list[element] = id(identifier)


def test():  # testing code for functions
    print("hello world")


def test2(hi):  # testing code for functions with parameters being parsed to interpret
    print("hi,", hi)

# Putting commands here like this can bypass the login process for quicker testing
# c = Interpreter("t")
# c.interpret("")
