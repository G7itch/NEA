from enum import Enum
from math import sqrt, e, pi

from qbit import Qbit


##################################################################################
class Gates(Enum):
    """Creates a read only class of constant gates that can be used in function calls"""
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

    def __setattr__(cls, key, value):
        raise AttributeError("Cannot modify immutable constants")


class ImmutableConstants(metaclass=ImmutableConstantsMeta):
    """Example of using a metaclass to control child behavior"""
    CONSTANT_1 = None
    CONSTANT_2 = None
    CONSTANT_3 = None


##################################################################################
###########################     Standard gates     ###############################

def H(qbit: Qbit) -> None:
    """
    creates an equal superposition state if given a computational basis state
    @param qbit: Qbit object being acted on
    @return: None
    """
    gate = Gates["HADAMARD"].value


def X(qbit: Qbit) -> None:
    """
    The Pauli-X gate is the quantum equivalent of the NOT gate for classical computers with respect to the standard
    basis
    @param qbit: The Qbit object being acted on
    @return: None
    """
    gate = Gates["PAULI_X"].value


def Y(qbit: Qbit) -> None:
    """
    Uses the builtin complex type
    @param qbit: Qbit object being acted on
    @return: None
    """
    gate = Gates["PAULI_Y"].value


def Z(qbit: Qbit) -> None:
    """
    Pauli Z is sometimes called phase-flip.
    @param qbit: Qbit object being acted on
    @return: None
    """
    gate = Gates["PAULI_Z"].value


def P(qbit: Qbit) -> None:
    """
    This is equivalent to tracing a horizontal circle (a line of constant latitude), or a rotation about the z-axis
    on the Bloch sphere
    @param qbit: Qbit object being acted on
    @return: None
    """
    gate = Gates["PHASE"].value


######################################################################################
#################################     Algorithms  ####################################

def Entangle(qbit: Qbit, qbit2: Qbit) -> None:
    """
    A complex combination of single gates that entangles two qbits, such that the measurement of one determines the
    measurement of the other.
    @param qbit: The Qbit object being acted on
    @param qbit2: The Qbit object being acted on
    @return: None
    """
    pass


def Teleport(qbit: Qbit, qbit2: Qbit) -> None:
    """
    A complex combination of unary gates that transforms the state of one qbit to another,
    @param qbit: The first Qbit object being acted on
    @param qbit2: The second Qbit object being acted on
    @return: None
    """
    pass


#####################################################################################
###############################     Procedures    ###################################

def Measurement(qbit: Qbit):
    """A function that measures the state of the qbit.
    This function is used over each instance measure function
    because it can be parsed straight into the diagram tool"""
    pass


def Initialise(name, values):
    """This function is used over the __init__ dunder method because it allows for more control over different
    instances.
    It can also be parsed into the diagram tool"""
    pass


#####################################################################################
############################        General     #####################################

def applyGate(gate, bit, *args):
    """
    Performs matrix multiplication on gates and qbits
    @param gate: The gate being used
    @param bit: The Qbit object being applied to
    @param args: Extra qbit objects for gates needing multiple inputs
    """
    qbits = [bit] + list(args)
    if len(qbits) == 1:
        qbit = qbits[0]
    else:
        pass
