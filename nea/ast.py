class Tree(object):

    def __init__(self):
        pass


class Node(object):

    def __init__(self,left,data,right):
        pass


class AbstractSyntaxTree(object):

    def __init__(self,parsed:iter):
        self.__commands = parsed
        self.syntaxtree = Tree()
        
        

    
