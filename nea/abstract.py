class Tree(object):

    def __init__(self, name='root', children=None):
        "Generic tree node."
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def __repr__(self):
        return self.name

#    *
#   /|\
#  1 2 +
#     / \
#    3   4
example_tree = Tree('*', [Tree('1'),
                          Tree('2'),
                          Tree('+', [Tree('3'),
                                     Tree('4')])])
#print(t.children)


class AbstractSyntaxTree(object):

    def __init__(self,parsed:iter):
        self.__commands = parsed
        self.syntaxtree = Tree()
        
        

    
