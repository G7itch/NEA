from lexer import *
from ast import AbstractSyntaxTree



class Interpreter(object):
    
    def __init__(self,graphqbit):
        self.lex = Lexer(rules, case_sensitive=True)
        self.command_list = []
    
    def interpret(self,line:str):
        for token in self.lex.scan(line):
            self.command_list.append(token)
        #print(self.command_list)
        #next step is to filter suppliments and split objects
        for element in self.command_list:
            match element:
                case "SUPPLIMENT"|"END_STMNT":
                    self.command_list.remove(element)
                case "OBJECT":
                    pass
                    #split up objects into dictionarys
                case _:
                    pass
        print(self.command_list)
        self.ast = AbstractSyntaxTree(self.command_list)
                    
                    
