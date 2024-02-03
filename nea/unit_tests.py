import io
import unittest
from unittest import mock
import os
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import abstract
import cbit
import databasesetup
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


class TestTree(unittest.TestCase):

    def setUp(self):
        self.root = abstract.Tree('root')
        self.child1 = abstract.Tree('child1')
        self.child2 = abstract.Tree('child2')
        self.child3 = abstract.Tree('child3')
        self.child4 = abstract.Tree('child4')

    def test_init_name_and_children(self):
        self.assertEqual(self.root.name, 'root')
        self.assertEqual(self.root.children, [])

    def test_init_with_children(self):
        tree_with_children = abstract.Tree('parent', [self.child1, self.child2])
        self.assertEqual(tree_with_children.name, 'parent')
        self.assertEqual(tree_with_children.children, [self.child1, self.child2])

    def test_add_child_single(self):
        self.root.add_child(self.child1)
        self.assertEqual(self.root.children, [self.child1])

    def test_add_child_multiple(self):
        self.root.add_child(self.child1)
        self.root.add_child(self.child2)
        self.assertEqual(self.root.children, [self.child1, self.child2])

    def test_add_child_nested(self):
        self.child1.add_child(self.child3)
        self.assertEqual(self.child1.children, [self.child3])

    def test_add_child_non_tree(self):
        with self.assertRaises(AssertionError):
            # Adding a non-Tree object should raise an AssertionError
            self.root.add_child('not_a_tree')

    def test_repr(self):
        self.assertEqual(repr(self.root), 'root')
        self.assertEqual(repr(self.child1), 'child1')


class TestNode(unittest.TestCase):

    def setUp(self):
        self.root = abstract.Node(10)
        self.root.insert(5)
        self.root.insert(15)
        self.root.insert(3)
        self.root.insert(7)

    def test_insert(self):
        # Test the structure after inserting elements
        expected_preorder = [10, 5, 3, 7, 15]
        self.assertEqual(self.root.preorder_traversal(self.root), expected_preorder)

        # Test inserting duplicate data
        self.root.insert(5)
        self.assertEqual(self.root.preorder_traversal(self.root), expected_preorder)

    def test_preorder_traversal(self):
        expected_preorder = [10, 5, 3, 7, 15]
        self.assertEqual(self.root.preorder_traversal(self.root), expected_preorder)

    def test_inorder_traversal(self):
        expected_inorder = [3, 5, 7, 10, 15]
        self.assertEqual(self.root.inorder_traversal(self.root), expected_inorder)

    def test_postorder_traversal(self):
        expected_postorder = [3, 7, 5, 15, 10]
        self.assertEqual(self.root.postorder_traversal(self.root), expected_postorder)

    def test_invalid_insert_parameters(self):
        with self.assertRaises(AttributeError):
            # Attempting to insert a non-integer value
            self.root.insert('invalid_data')

        with self.assertRaises(AttributeError):
            # Attempting to insert a Node object instead of an integer
            invalid_node = abstract.Node(20)
            self.root.insert(invalid_node)


# AbstractSyntaxTree here

class TestCbit(unittest.TestCase):
    def setUp(self):
        self.single_bit_cbit = cbit.Cbit(int(1))
        self.tensor_product_cbit = cbit.Cbit(3, 2)

    def test_init_single_bit_cbit(self):
        self.assertEqual(self.single_bit_cbit.Cbit.vector, [0, 1])

    def test_init_tensor_product_cbit(self):
        expected_tensor_product_vector = [0, 0, 0, 1]
        self.assertEqual(self.tensor_product_cbit.Cbit.vector, expected_tensor_product_vector)

    def test_setElement_single_bit_cbit(self):
        self.assertTrue(self.single_bit_cbit.setElement(0, 1))
        self.assertEqual(self.single_bit_cbit.Cbit.vector, [1, 1])

        # Test invalid index
        self.assertFalse(self.single_bit_cbit.setElement(2, 1))
        self.assertEqual(self.single_bit_cbit.Cbit.vector, [1, 1])

        # Test invalid value
        self.assertFalse(self.single_bit_cbit.setElement(0, 2))
        self.assertEqual(self.single_bit_cbit.Cbit.vector, [1, 1])

    def test_setElement_tensor_product_cbit(self):
        self.assertTrue(self.tensor_product_cbit.setElement(2, 1))
        expected_tensor_product_vector = [0, 0, 1, 1]
        self.assertEqual(self.tensor_product_cbit.Cbit.vector, expected_tensor_product_vector)

        # Test invalid index
        self.assertFalse(self.tensor_product_cbit.setElement(4, 1))
        self.assertEqual(self.tensor_product_cbit.Cbit.vector, expected_tensor_product_vector)

        # Test invalid value
        self.assertFalse(self.tensor_product_cbit.setElement(2, 2))
        self.assertEqual(self.tensor_product_cbit.Cbit.vector, expected_tensor_product_vector)

    def test_measure_single_bit_cbit(self):
        # Since it's a single bit, measure should return the second element of the vector
        self.assertEqual(self.single_bit_cbit.measure(), 1)

    def test_measure_tensor_product_cbit(self):
        # Since it's a tensor product, measure should return False
        self.assertFalse(self.tensor_product_cbit.measure())

    def test_probcollapse_single_bit_cbit(self):
        # In a single bit, the probability of |0> is 0 and |1> is 1
        expected_output = "Probability of collapse: \n|0>, 0%\n|1>, 100%\n"
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.single_bit_cbit.probcollapse()
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_probcollapse_tensor_product_cbit(self):
        # In a tensor product, the probability of each state is 25%
        expected_output = "Probability of collapse: \n|00>, 0%\n|01>, 0%\n|10>, 0%\n|11>, 100%\n"
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.tensor_product_cbit.probcollapse()
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_repr_single_bit_cbit(self):
        expected_representation = "(0, 1)"
        self.assertEqual(repr(self.single_bit_cbit), expected_representation)

    def test_repr_tensor_product_cbit(self):
        expected_representation = "(0, 0, 0, 1)"
        self.assertEqual(repr(self.tensor_product_cbit), expected_representation)


class TestSetupInit(unittest.TestCase):
    def setUp(self):
        # Remove any existing database file and achievements.json before testing
        if os.path.exists("master.db"):
            os.remove("master.db")
        if os.path.exists("achievements.json"):
            os.remove("achievements.json")

    @unittest.expectedFailure
    def test_init(self):
        databasesetup.Setup()

        # Check if the database file exists
        self.assertTrue(os.path.exists("master.db"))

        # Check if the tables are created
        conn = sqlite3.connect("file:master.db?mode=rw", uri=True)
        c = conn.cursor()

        # Check if 'highscores' table is created
        c.execute("PRAGMA table_info(highscores)")
        highscores_columns = [column[1] for column in c.fetchall()]
        self.assertIn('userid', highscores_columns)
        self.assertIn('score', highscores_columns)

        # Check if 'challenges' table is created
        c.execute("PRAGMA table_info(challenges)")
        challenges_columns = [column[1] for column in c.fetchall()]
        self.assertIn('challengeid', challenges_columns)
        self.assertIn('challengedesc', challenges_columns)
        self.assertIn('difficulty', challenges_columns)
        self.assertIn('reward', challenges_columns)
        self.assertIn('regex', challenges_columns)

        # Check if the achievements.json file is created
        self.assertTrue(os.path.exists("achievements.json"))

        conn.close()

    @unittest.expectedFailure
    def test_populate_db(self):
        databasesetup.Setup()

        # Check if the database file exists
        self.assertTrue(os.path.exists("master.db"))

        # Check if the 'challenges' table is populated
        conn = sqlite3.connect("file:master.db?mode=rw", uri=True)
        c = conn.cursor()

        c.execute("SELECT * FROM challenges")
        challenges_data = c.fetchall()
        expected_challenges_data = [
            (0, 'Entangle two particles', 1.0, 10, r"\w*(ENTANGLE|E|e|entangle|Entangle)\((\w+,\w+)\)\w*/gm"),
            (1, 'Use a hadamard gate for the first time', 0.5, 5, r"\w*(hadamard|h|H|HADAMARD)\((\w+|(\w*,\w+)+)\)\w*"),
            (2, 'Teleport a particle', 2.5, 50, None)
        ]
        self.assertEqual(challenges_data, expected_challenges_data)

        conn.close()

    def tearDown(self):
        # Remove the created database file and achievements.json after testing
        if os.path.exists("master.db"):
            os.remove("master.db")
        if os.path.exists("achievements.json"):
            os.remove("achievements.json")


class TestDraggable(unittest.TestCase):
    def setUp(self):
        self.fig, self.ax = plt.subplots()
        self.circle = Circle((1, 1), radius=0.1, color='r')
        self.ax.add_patch(self.circle)

    def test_draggable_init(self):
        draggable_test = draggable.Draggable(self.circle, self.update_callback, object_selected=None)
        self.assertIsNotNone(draggable_test)

    def test_draggable_connect_disconnect(self):
        draggable_test = draggable.Draggable(self.circle, self.update_callback, object_selected=None)
        draggable_test.connect()

        # Check if the connection IDs are assigned
        self.assertIsNotNone(draggable_test.cidpress)
        self.assertIsNotNone(draggable_test.cidrelease)
        self.assertIsNotNone(draggable_test.cidmotion)

        # Disconnect and check if IDs are None
        draggable_test.disconnect()
        self.assertIsNone(draggable_test.cidpress)
        self.assertIsNone(draggable_test.cidrelease)
        self.assertIsNone(draggable_test.cidmotion)

    def test_draggable_movement(self):
        draggable_test = draggable.Draggable(self.circle, self.update_callback, object_selected=None)
        draggable_test.connect()

        # Simulate button press event
        press_event = plt.gcf().canvas.events.key_press
        press_event(x=2, y=2, key='button_press_event')

        # Simulate motion event
        motion_event = plt.gcf().canvas.events.motion_notify
        motion_event(x=3, y=3)

        # Simulate release event
        release_event = plt.gcf().canvas.events.key_release
        release_event(x=3, y=3, key='button_release_event')

        # Check if the update callback is called
        self.assertTrue(self.update_called)

    def update_callback(self):
        self.update_called = True

    def tearDown(self):
        plt.close()




if __name__ == '__main__':
    unittest.main(verbosity=2)
