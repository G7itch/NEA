import unittest
import abstract
import cbit
import draggable
import gates
import interface
import interpreter
import lexer
import login
import main
import point
import qbit
import renderer
import system
import vector
import wall


class UnitTestsAbstractTree(unittest.TestCase):

    def setUp(self):
        pass

    def test_Tree_init_intended(self):
        pass

    def test_Tree_init_bad_param_children(self):
        pass

    def test_Tree_init_bad_param_name(self):
        pass

    def test_Tree_add_child_intended(self):
        pass

    def test_Tree_add_child_bad_param_node(self):
        pass


class UnitTestsAbstractNode(unittest.TestCase):

    def setUp(self):
        pass

    def test_Node_init_intended(self):
        pass

    def test_Node_init_bad_param_left(self):
        pass

    def test_Node_init_bad_param_right(self):
        pass

    def test_Node_init_bad_param_data(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
