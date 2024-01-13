from lexer import *
from abstract import AbstractSyntaxTree



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
        self.ast = AbstractSyntaxTree(self.command_list)
                    
    def __giveaward(self):
        """This function controls the logic of awarding achievments to the user."""
        pass    

c = Interpreter("stromg")
c.interpret(":gate: 1+1=2;")