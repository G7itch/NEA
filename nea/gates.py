from enum import Enum
from math import sqrt, e, pi
from random import randint

from qbit import Qbit


##################################################################################
class Gates(Enum):
    """Creates a read-only class of constant gates that can be used in function calls"""
    HADAMARD = [[1 / sqrt(2), 1 / sqrt(2)],
                [1 / sqrt(2), -1 / sqrt(2)]]

    PAULI_X = [[0, 1],
               [1, 0]]

    PAULI_Y = [[0, -1j],
               [1j, 0]]

    PAULI_Z = [[1, 0],
               [0, -1]]

    PHASE = [[1, 0],
             [0, 1j]]

    T = [[1, 0],
         [0, e ** (1j * pi / 4)]]

    CNOT = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]]

    CZ = [[1, 0, 0, 0],
          [0, 1, 0, 0],
          [0, 0, 1, 0],
          [0, 0, 0, -1]]

    SWAP = [[1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]]

    TOFFOLI = [[1, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0, 1, 0]]


# Below is another way you can create a constant class
# It uses the metaclasses and an undermentioned to block any attempt at writing to a variable
# I chose to go with the top implementation as it produced cleaner code.
# Although this is more pythonic.
class ImmutableConstantsMeta(type):
    """Another implementation of a constant class"""

    def __setattr__(cls, key, value) -> None:
        """
        Overrides the class setter so changes cannot be made to elements in child classes
        @param key: Key of the attribute being modified
        @param value: Value the attribute is being modified to
        @return: None
        @raise AttributeError: Cannot modify immutable constants
        """
        raise AttributeError("Cannot modify immutable constants")


class ImmutableConstants(metaclass=ImmutableConstantsMeta):
    """Example of using a metaclass to control child behavior"""
    CONSTANT_1 = None
    CONSTANT_2 = None
    CONSTANT_3 = None


# Standard gates

# noinspection PyPep8Naming
def H(qbit: Qbit) -> Qbit:
    """
    creates an equal superposition state if given a computational basis state
    @param qbit: Qbit object being acted on
    @return: qbit
    """
    gate = Gates["HADAMARD"].value
    qbit = matrixMultiplication(gate, qbit)
    qbit.probability = [[0 for _ in range(11)] for _ in range(11)]
    for i in range(2):
        x = randint(0, 11)
        y = randint(0, 11)
        qbit.probability[x][y] = 0.5
    return qbit


# noinspection PyPep8Naming
def X(qbit: Qbit) -> Qbit:
    """
    The Pauli-X gate is the quantum equivalent of the NOT gate for classical computers with respect to the standard
    basis
    @param qbit: The Qbit object being acted on
    @return: qbit
    """
    gate = Gates["PAULI_X"].value
    qbit = matrixMultiplication(gate, qbit)
    return qbit


# noinspection PyPep8Naming
def Y(qbit: Qbit) -> Qbit:
    """
    Uses the builtin complex type
    @param qbit: Qbit object being acted on
    @return: qbit
    """
    gate = Gates["PAULI_Y"].value
    qbit = matrixMultiplication(gate, qbit)
    return qbit


# noinspection PyPep8Naming
def Z(qbit: Qbit) -> Qbit:
    """
    Pauli Z is sometimes called phase-flip.
    @param qbit: Qbit object being acted on
    @return: qbit
    """
    gate = Gates["PAULI_Z"].value
    qbit = matrixMultiplication(gate, qbit)
    return qbit


# noinspection PyPep8Naming
def P(qbit: Qbit) -> Qbit:
    """
    This is equivalent to tracing a horizontal circle (a line of constant latitude), or a rotation about the z-axis
    on the Bloch sphere
    @param qbit: Qbit object being acted on
    @return: qbit
    """
    gate = Gates["PHASE"].value
    qbit = matrixMultiplication(gate, qbit)
    return qbit


def CNOT(control: Qbit, target: Qbit) -> Qbit:
    """
    This is equivalent to a controlled NOT gate
    @param control: The control qbit
    @param target: The target qbit
    @return: the target qbit after any changes
    """
    if control.vector[1] == 0:
        return target
    else:
        qbit2 = X(target)
    return qbit2


def CZ(control: Qbit, target: Qbit) -> Qbit:
    """
    This is equivalent to a controlled NOT gate
    @param control: The control qbit
    @param target: The target qbit
    @return: the target qbit after any changes
    """
    if control.vector[1] == 0:
        return target
    else:
        qbit2 = Z(target)
    return qbit2


# Algorithms

# noinspection PyPep8Naming
def Entangle(qbit: Qbit, qbit2: Qbit) -> Qbit | bool:
    """
    A complex combination of single gates that entangles two qbits, such that the measurement of one determines the
    measurement of the other.
    @param qbit: The Qbit object being acted on
    @param qbit2: The Qbit object being acted on
    @return: Entangled qbits
    """
    qbit.vector = [1, 0]
    qbit2.vector = [1, 0]
    qbit = H(qbit)
    qbit2 = CNOT(qbit, qbit2)
    return qbit.tensor(qbit2)


# noinspection PyPep8Naming
def Teleport(qbit: Qbit, qbit2: Qbit) -> Qbit:
    """
    A complex combination of unary gates that transforms the state of one qbit to another,
    @param qbit: The first Qbit object being acted on
    @param qbit2: The second Qbit object being acted on
    @return: None
    """
    temp_qbit = Qbit(0)
    temp_qbit = H(temp_qbit)
    qbit2 = CNOT(temp_qbit, qbit2)
    temp_qbit = CNOT(qbit, temp_qbit)
    qbit = H(qbit)
    Measurement(temp_qbit)
    qbit = Measurement(qbit)
    qbit2 = CNOT(temp_qbit, qbit2)
    qbit2 = CZ(qbit, qbit2)
    qbit2 = Measurement(qbit2)
    return qbit2


# Procedures

# noinspection PyPep8Naming
def Measurement(qbit: Qbit) -> Qbit:
    """
    A function that measures the state of the qbit.
    This function is used over each instance measure function
    because it can be parsed straight into the diagram tool
    @param qbit: The Qbit object being measured
    @return: None
    """
    print(qbit.measure())
    return qbit.measure()


# noinspection PyPep8Naming
def Initialise(name: str, values: list) -> None:
    """
    This function is used over the __init__ dunder method because it allows for more control over different
    instances. It can also be parsed into the diagram tool
    @param name: The identifier of the qbit to be created
    @param values: The values the qbit should take
    @return: None
    """
    locals()[name] = Qbit(1)


def matrixMultiplication(gate: list[list[float]], bit: Qbit) -> Qbit:
    bit.vector = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*bit.vector)]
                  for A_row in gate]
    bit.vector = [x for y in bit.vector for x in y]
    return bit
