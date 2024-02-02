from math import sqrt
from typing import Self


class Vector(object):

    def __init__(self, size: int) -> None:
        """
        Initialises the vector as a zero array of given size
        @param size: The size of the vector
        @return: None
        @raise: AssertionError
        """
        try:
            assert type(size) is int
            # Check if size is an integer, if not prints an error message and quits.
            # The user should never encounter this error
        except AssertionError:
            print("E: Size parameter should be an integer")
            exit(1)
        self.vector: list = [0] * size

    def getElement(self, index: int) -> float | bool:
        """
        Returns the value stored in the given index of the vector
        @param index: The index of the element being retrieved
        @return: Element if successful, else False
        """
        try:
            assert index < len(self.vector) and type(index) is int
        except AssertionError:
            print("Index must be an integer less than or equal to the length of the list")
            return False

        return self.vector[index]

    def setElement(self, index: int, value: float) -> bool:
        """
        Sets the value at one index in the vector to a given value
        @param index: The index of the element being set
        @param value: The value to be set
        @return: True if successful, else False
        """
        try:
            assert index < len(self.vector) and type(index) is int
        except AssertionError:
            print("Index must be an integer less than or equal to the length of the list")
            return False  # Indicate failed execution
        try:
            assert type(value) is float or type(value) is int
        except AssertionError:
            print("Value must be numeric")
            return False

        self.vector[index] = value
        return True  # Indicate successful execution

    def scalarMul(self, num: float) -> Self | bool:
        """
        Performs scalar multiplication on a vector
        @param num: The scalar to multiply by
        @return: multiplied vector if successful, else False
        """
        try:
            assert (type(num) is float or type(num) is int)
        except AssertionError:
            return False
        mul_vec = Vector(len(self.vector))
        # Creates a new vector object so can be used without overwriting the underlying vector
        for count, element in enumerate(self.vector):
            mul_vec.setElement(int(count), num * element)

        return mul_vec

    def __mul__(self, num: float) -> 'Vector':
        """
        Scalar multiplication shorthand
        @param num: The scalar to multiply by
        @return: multiplied vector if successful, else False
        """
        return self.scalarMul(num)

    def setElements(self) -> bool:
        """
        Provides console interface to set all the elements of the vector
        @return: True
        """
        print("\n")
        for i in range(0, len(self.vector)):
            number = float(input(f"Enter value for index {i}: "))
            self.setElement(int(i), number)
        print("\n")
        return True

    def setN(self, n: float) -> bool:
        """
        Shorthand, sets every element of the vector to the same number
        @param n: The number to set
        @return: True if successful, else False
        """
        size = len(self.vector)
        try:
            assert type(n) is int or type(n) is float
        except AssertionError:
            print("'n' must be numeric")
            return False
        self.vector = [n] * size
        return True

    def allZeros(self) -> bool:
        """
        Returns true if every element of the vector is 0
        @return: True if all elements are 0, else False
        """
        return not (all(self.vector))

    def magnitude(self) -> float:
        """
        Returns the size of the vector using standard analytic geometry formula sqrt(a^2 + b^2...)
        @return: The magnitude of the vector
        """
        total = 0
        for i in range(0, len(self.vector)):
            total += (self.vector[i]) ** 2
            # print(total)
        return sqrt(total)

    def isUnit(self) -> bool:
        """
        Returns true if the current vector instance is an example of a unit vector
        @return: True if it is an example of a unit vector, else False
        """
        return self.magnitude() == 1

    def unit(self) -> 'Vector':
        """
        Returns a new vector instance set to be the unit vector of the existing instance
        @return: The new vector instance
        """
        size = len(self.vector)
        unit_vec = Vector(size)  # create a new instance to not overwrite the existing case
        mag = self.magnitude()
        for count, ele in enumerate(self.vector):
            unit_vec.setElement(int(count), ele / mag)
        return unit_vec

    def tensor(self, other: 'Vector') -> Self | bool:
        """
        Returns tensor product of two vectors
        @return: The tensor product of two vectors, else False
        """
        if not (isinstance(other, object)):
            return False
        new_size = len(self.vector) * len(other.vector)
        tensor_product = Vector(new_size)
        i = -1
        for count, element in enumerate(self.vector):
            for count2, element2 in enumerate(other.vector):
                i += 1
                tensor_product.setElement(int(i), element * element2)
        return tensor_product

    def __repr__(self) -> str:
        """
        Returns a human friendly version of the object using more traditional curved brackets
        @return: The representation of the vector
        """
        return "(" + str(self.vector)[1:-1] + ")"
