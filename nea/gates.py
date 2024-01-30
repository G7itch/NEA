from qbit import Qbit
from enum import Enum
from math import sqrt, e, pi

##################################################################################
class Gates(Enum):
    """Creates a read only class of constant gates that can be used in function calls"""
    HADAMARD = [[1/sqrt(2),1/sqrt(2)],
                [1/sqrt(2),-1/sqrt(2)]]

    PAULI_X = [[0,1],
               [1,0]]

    PAULI_Y = [[0,-1j],
               [1j,0]]

    PAULI_Z = [[1,0],
               [0,-1]]

    PHASE = [[1,0],
             [0,1j]]

    T = [[1,0],
         [0,e**(1j*pi/4)]]

    CNOT = [[1,0,0,0],
            [0,1,0,0],
            [0,0,0,1],
            [0,0,1,0]]

    CZ = [[1,0,0,0],
          [0,1,0,0],
          [0,0,1,0],
          [0,0,0,-1]]
    
    SWAP = [[1,0,0,0],
            [0,0,1,0],
            [0,1,0,0],
            [0,0,0,1]]

    TOFFOLI = [[1,0,0,0,0,0,0,0],
               [0,1,0,0,0,0,0,0],
               [0,0,1,0,0,0,0,0],
               [0,0,0,1,0,0,0,0],
               [0,0,0,0,1,0,0,0],
               [0,0,0,0,0,1,0,0],
               [0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,1,0]]

    


##################################################################################
###########################     Standard gates     ###############################

def H(index):
    """creates an equal superposition state if given a computational basis state"""
    gate = Gates["HADAMARD"].value

def X(index):
    """The Pauli-X gate is the quantum equivalent of the NOT gate for classical computers with respect to the standard basis"""
    gate = Gates["PAULI_X"].value

def Y(index):
    """Uses the builtin complex type"""
    gate = Gates["PAULI_Y"].value

def Z(index):
    """Pauli Z is sometimes called phase-flip."""
    gate = Gates["PAULI_Z"].value

def P(index):
    """This is equivalent to tracing a horizontal circle (a line of constant latitude), or a rotation about the z-axis on the Bloch sphere"""
    gate = Gates["PHASE"].value

######################################################################################
#################################     Algorithms  ####################################

def Entangle(qbit,qbit2):
    """A complex combination of single gates that entangles two qbits, such that the measurment of one determines the cmesaurement of the other."""

def Teleport(qbit1,qbit2):
    pass

#####################################################################################
###############################     Procedures    ###################################

def Measurement(index):
    """A function that measures the state of the qbit. This function is used over each instances measure function because it can be parsed straight into the diagram tool"""
    pass

def Initialise(name,values):
    """This function is used over the __init__ dunder method because it allows for more control over different instances. It can also be parsed into the diagram tool"""
    pass

#####################################################################################
############################    General #############################################

def applyGate(gate,bit,*args):
    """Performs matrix multiplication on gates and qbits"""
    qbits = [bit] + list(args)
    if len(qbits) == 1:
        qbit = qbits[0]
    else:
        pass
    
    
