from lexer import *
from abstract import AbstractSyntaxTree
import random, string



class Interpreter(object):
    
    def __init__(self,graphqbit):
        self.lex = Lexer(rules)
        self.command_list = []
        self.user_vars = {}
        self.__temp_vars = {}

    
    def interpret(self,line:str):
        for token in self.lex.scan(line):
            self.command_list.append(token)
        #print(self.command_list)
        #next step is to filter suppliments and split objects
        for element in self.command_list:
            match element[0]:
                case "SUPPLIMENT"|"END_STMNT": #These just make writing easier, they don't impact code at all
                    self.command_list.remove(element)
                case "OBJECT":
                    pass
                    #split up objects into dictionarys
                case _:
                    pass
        print(self.command_list)
        self.__setvars()
        self.ast = AbstractSyntaxTree(self.command_list)
                    
    def __giveaward(self):
        """This function controls the logic of awarding achievments to the user."""
        pass    

    def __setvars(self) -> list:
        """Sets the command list to include vaariable identifiers and locations - this helps for syntax parsing when put into the AST"""
        letters = string.ascii_letters
        for element in range(len(self.command_list)):
            if self.command_list[element][0] == "LITERAL" or self.command_list[element][0] == "DIGIT":
                identifier = ''.join(random.choice(letters) for i in range(20))
                while identifier in self.__temp_vars:
                    identifier = ''.join(random.choice(letters) for i in range(20))
                self.__temp_vars[identifier] = id(identifier)
                self.command_list[element] = id(identifier)
        print(self.command_list)
                    




c = Interpreter("stromg")
c.interpret(":gate: 1+1=2;")