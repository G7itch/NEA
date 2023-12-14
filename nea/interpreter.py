from lexer import *



class Interpreter(object):
    
    def __init__(self,graphqbit):
        self.lex = Lexer(rules, case_sensitive=True)
        self.command_list = []

    
    def interpret(self,line:str):
        for token in self.lex.scan(line):
            self.command_list.append(token)
        #print(self.command_list)
        #next step is to filter suppliments and split objects

