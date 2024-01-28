import ctypes

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

class Node:
   
   def __init__(self, data):
      self.left = None
      self.right = None
      self.data = data
# Insert Node
   def insert(self, data):
      if self.data:
         if data < self.data:
            if self.left is None:
               self.left = Node(data)
            else:
               self.left.insert(data)
         elif data > self.data:
            if self.right is None:
               self.right = Node(data)
            else:

               self.right.insert(data)
      else:
         self.data = data
   
   def PreorderTraversal(self, root):
      res = []
      if root:
         res.append(root.data)
         res = res + self.PreorderTraversal(root.left)
         res = res + self.PreorderTraversal(root.right)
      return res
   
   def inorderTraversal(self, root):
      res = []
      if root:
         res = self.inorderTraversal(root.left)
         res.append(root.data)
         res = res + self.inorderTraversal(root.right)
      return res
   
   def postorderTraversal(self,root):
      res = []
      if root:
        res = self.inorderTraversal(root.left)
        res = res + self.inorderTraversal(root.right)
        res.append(root.data)
      return res


class AbstractSyntaxTree(object):

    def __init__(self,parsed:iter,vars):
        self.__commandtree = []
        self.__parsed = parsed
        self.__commandlist = []
        self.var_lookup = vars
        operators = []
        for element in self.__parsed:
            if type(element) == tuple:
                if type(element[1]) == list:
                   self.__commandlist.append(element[1])
                   operators.append(len(self.__commandlist)-1)
                   self.__commandlist.append(element[0])
                else:
                   self.__commandlist.append(element[1])
                   operators.append(len(self.__commandlist)-1)
            else:
               self.__commandlist.append(element)
        
        i = 0
        for index,element in enumerate(self.__commandlist):
            if type(element) == str:
                i+=1
                left = index-1
                data = element
                try:
                    right = operators[i]
                except:
                    right = index+1
                self.__commandtree.append([left,data,right])
            else:
                self.__commandtree.append([-1,element,-1])
        #print(self.__commandtree)
        data = []
        expression = self.in_order_traversal(operators[0],data) # can then use eval on this expression or exec if it is a function call
        for index,reference in enumerate(expression):
            if type(reference) == int:
                value = ctypes.cast(reference, ctypes.py_object).value
                #realvalue = ctypes.cast(value, ctypes.py_object).value #This line of code breaks everything and i have no idea why but if you uncomment it python installation breaks
                actualvalue = self.var_lookup[value]
                expression[index] = actualvalue
        
        expression = " ".join(map(str,expression))
        #print(expression)
        if '=' in expression:
           exec(expression) #evaluation of string
        else:
           print(eval(expression)) #execution of string

    def in_order_traversal(self, current_index,datastream):
        if current_index != -1:
            left_index = self.__commandtree[current_index][0]
            data = self.__commandtree[current_index][1]
            right_index = self.__commandtree[current_index][2]
        # Traverse left subtree
            self.in_order_traversal(left_index,datastream)
        # Process current node
            datastream.append(data) 
        # Traverse right subtree
            self.in_order_traversal(right_index,datastream)
        return datastream


            
               
        

