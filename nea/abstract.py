import ctypes
from typing import Any


class Tree(object):
    """Recursive generation generic tree object"""
    name: str
    children: list[Any]

    def __init__(self, name='root', children=None):
        """Generic tree node."""
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node: 'Tree') -> None:
        """
        Adds a child node to the current referenced Tree object
        @param node: Tree object
        """
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


# print(t.children)

class Node:
    """Recursive generation binary tree object"""

    def __init__(self, data):
        try:
            assert type(data) is int
        except AssertionError:
            raise AttributeError('Data must be an integer')
        self.left = None
        self.right = None
        self.data = data

    # Insert Node
    def insert(self, data: int) -> None:
        """
        Adds a new Node object to the current root instance in the appropriate place
        @param data: data to be included
        """
        try:
            assert type(data) is int
        except AssertionError:
            raise AttributeError('Data must be an integer')
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

    def preorder_traversal(self, root: 'Node') -> list:
        """
        Performs preorder traversal on the provided root Node object
        @param root: Root node object to start ordering
        @return: res
        """
        res = []
        if root:
            res.append(root.data)
            res += self.preorder_traversal(root.left)
            res += self.preorder_traversal(root.right)
        return res

    def inorder_traversal(self, root: 'Node') -> list:
        """
        Performs inorder traversal on the provided root Node
        @param root: Root node object to start ordering
        @return: res
        """
        res = []
        if root:
            res = self.inorder_traversal(root.left)
            res.append(root.data)
            res += self.inorder_traversal(root.right)
        return res

    def postorder_traversal(self, root: 'Node') -> list:
        """
        Performs postorder traversal on the provided root Node
        @param root: Root node object to start ordering
        @return: res
        """
        res = []
        if root:
            res = self.inorder_traversal(root.left)
            res += self.inorder_traversal(root.right)
            res.append(root.data)
        return res


class AbstractSyntaxTree(object):
    """Abstract syntax tree data structure constructed from linked lists"""
    __commandlist: list[Any]
    __commandtree: list[list[int | Any]]

    def __init__(self, parsed: iter, variables):
        self.__commandtree = []
        self.__parsed = parsed
        self.__commandlist = []
        self.var_lookup = variables
        operators = []

        for element in self.__parsed:
            if type(element) is tuple:
                if type(element[1]) is list:
                    self.__commandlist.append(element[1])
                    operators.append(len(self.__commandlist) - 1)
                    self.__commandlist.append(element[0])
                else:
                    self.__commandlist.append(element[1])
                    operators.append(len(self.__commandlist) - 1)
            else:
                self.__commandlist.append(element)

        #####################################################################
        # In the future, it might be worth using the dataclass function, _post_init__ to run this code
        #####################################################################

        i = 0
        for index, element in enumerate(self.__commandlist):
            if type(element) is str:
                i += 1
                left = index - 1
                data = element
                try:
                    right = operators[i]
                except IndexError:
                    right = index + 1
                self.__commandtree.append([left, data, right])
            else:
                self.__commandtree.append([-1, element, -1])

        data = []
        expression = self.in_order_traversal(operators[0], data)
        # can then use eval on this expression or exec if it is a function call

        for index, reference in enumerate(expression):
            if type(reference) is int:
                value = ctypes.cast(reference, ctypes.py_object).value
                # real_value = ctypes.cast(value, ctypes.py_object).value #This line of code breaks everything and I
                # have no idea why but if you uncomment it python installation breaks
                actual_value = self.var_lookup[value]
                expression[index] = actual_value

        expression = " ".join(map(str, expression))

        if '=' in expression:
            exec(expression)  # evaluation of string
        else:
            print(eval(expression))  # execution of string

    def in_order_traversal(self, current_index: int, datastream: list) -> list:
        """
        Returns a list representation of the tree after performing inorder traversal
        @param current_index: The algorithms starting index
        @param datastream: The current list of sorted items
        @return: datastream
        """
        if current_index != -1:
            left_index = self.__commandtree[current_index][0]
            data = self.__commandtree[current_index][1]
            right_index = self.__commandtree[current_index][2]
            # Traverse left subtree
            self.in_order_traversal(left_index, datastream)
            # Process current node
            datastream.append(data)
            # Traverse right subtree
            self.in_order_traversal(right_index, datastream)
        return datastream
