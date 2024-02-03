from math import exp
from random import choices, randint
from typing import override, Self

import numpy as np

from cbit import Cbit


class Qbit(Cbit):

    def __init__(self, dirac: int, sub=None) -> None:
        """
        Qbits are the quantum extension of Cbits that can take values intermediate of 0/1
        @param dirac: Refers to the integer that would be shown in the symbol used in dirac notation (e.g. |0>)
        @param sub: Refers to the number of bits (elements) to be used in the vector form.
        It is the subscript of dirac notation, by default, it is the minimum number required
        @return: None
        """
        super().__init__(dirac, sub)  # Error checking is provided in the super function
        self.Qbit = self.Cbit

        # Visualisation grid setup
        self.probability = [[0 for _ in range(11)] for _ in range(11)]  # For graphical visualisation
        x, y = randint(0, 10), randint(0, 10)
        self.probability[x][y] = 1
        self.__changed = [[x, y]]
        # self.prettygrid = self.prettify()
        # self.probprint()

    def measure(self) -> Self | bool:
        """
        'Measures' the Qbits state using the probabilistic definition of quantum bits
        @return: Weighted random collapsed probability, else False
        """
        if len(self.Qbit.vector) != 2:
            return False
        else:
            bits = [0, 1]
            collapse = int(choices(bits, weights=(self.Cbit.vector[0] ** 2, self.Cbit.vector[1] ** 2), k=1)[0])
            # Qbit vectors are probabilities rather than deterministic values
            self.Qbit.vector[0] = collapse
            self.Qbit.vector[1] = abs(1 - collapse)
            return self.Qbit

    @staticmethod
    def _softmax(vector: list) -> list | bool:
        """
        Performs the softmax normalisation on a list of values.
        Protected function, I am not sure what classes need to refer to this so better safe than sorry
        @see:  https://en.wikipedia.org/wiki/Softmax_function
        @param vector: List of values to perform softmax on
        @return: Softmax vector, else False
        """
        try:
            assert ((type(vector) is list or isinstance(vector, object)) and
                    all((type(ele) is int or type(ele) is float) for ele in vector))
        except AssertionError:
            print("\nE: Softmax needs a numeric array as an input\n")
            return False

        e = [exp(ele) for ele in vector]
        return [item / sum(e) for item in e]  # (e)^x_i/sum(e^x)
        # Maybe only let it apply to 0 values and everything previously seen

    @staticmethod
    def _normalise(vector: list, maxprime: float) -> list | bool:
        """
        Min-max normalisation of given list
        @param vector: The list of values to normalise
        @param maxprime: Maximum value of the new list
        @return: Normalised list, else False
        """
        try:
            assert ((type(vector) is list or isinstance(vector, object)) and all(
                (type(ele) is int or type(ele) is float) for ele in vector))
        except AssertionError:
            print("\nE: Normalise needs a numeric array as an input\n")
            return False
        if not (isinstance(maxprime, float) or isinstance(maxprime, int)):
            return False

        return [((value-min(vector)) * maxprime / (max(vector)-min(vector))) for value in vector]
        # generates a new list normalised with min 0 and specified max

    # def prettify(self):
    #    prettygrid = self.probability
    #    print(prettygrid)
    #    for i in range(len(self.probability)-1):
    #        for j in range(len(self.probability)-1):
    #            prettygrid[i][j] = float(round(self.probability[i][j],3))*100
    #    return prettygrid

    @staticmethod
    def _applygauss2d(array: list[list], step: int) -> list[list[float]] | bool:
        """
        Applies gaussian noise (centred on the standard normal Z distribution) to a 2d array
        @param array: The 2d array to apply gaussian noise to
        @param step: The diffusion step we are at
        @return: The updated 2d array, else False
        """
        try:
            assert ((type(array) is list and type(step) is int) and
                    all((type(ele) is int or type(ele) is float) for innerlist in array for ele in innerlist))
        except AssertionError:
            return False

        mean = 0
        stddv = 100 / (2 ** step)
        noise = np.random.normal(loc=mean, scale=stddv, size=(len(array), len(array[0]))).tolist()

        for i in range(len(array)):
            for j in range(len(array[0])):
                array[i][j] += noise[i][j]

        return array

    def probprint(self) -> None:
        """
        Pretty prints the probability grid
        @return: None
        """
        for i in range(len(self.probability) - 1):
            for j in range(len(self.probability) - 1):
                print(round(round(self.probability[i][j], 3) * 100, 3), end=" ")
            print()

    def diffuse(self, step: int) -> None | bool:
        """
        Diffuse the probability grid over time: A representation of uncertainly in our visualisation
        @param step: The distance into the diffusion algorithm we are
        @return: None for success, False for failure
        """
        if not (isinstance(step, int)):
            return False

        newarray = []
        self.probability = self._applygauss2d(self.probability, step)

        for i in range(len(self.probability)):
            for j in range(len(self.probability[0])):
                newarray.append(self.probability[i][j])

        newarray = self._softmax(newarray)
        n = len(self.probability[0])
        self.probability = [newarray[idx:idx + n] for idx in range(0, len(newarray), n)]
        # self.probprint()

    @override
    def setElement(self, index: int, value: float) -> bool:
        """
        Sets the value at one index in the vector to the given value
        @param index: The index of the element to set
        @param value: The value of the element to set
        @return: True for success, False for failure
        """
        try:
            assert index <= len(self.Qbit.vector) and type(index) is int
        except AssertionError:
            print("Index must be an integer less than or equal to the length of the list")
            return False

        if len(self.Qbit.vector) == 2:  # If the length is 2 then it must be a standard Qbit
            try:
                assert 1 >= value >= -1
            except AssertionError:
                print("Value can only take the range [-1,1]")
                # Checks to see if the element you're trying to add is a valid format
                return False

        self.Qbit.vector[index] = value
        return True

    # def __repr__(self):
    #    for i in range(len(self.prettygrid)-1):
    #        print(*self.prettygrid[i])
    #    return ""
