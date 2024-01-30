from qbit import Qbit
from enum import Enum
from math import sqrt

##################################################################################
class Gates(Enum):
    HADAMARD = [[1/sqrt(2),1/sqrt(2)],
                [1/sqrt(2),-1/sqrt(2)]]

    PAULI_X = [[0,1],
               [1,0]]

    PAULI_Y = 

    


##################################################################################
###########################     Standard gates     ###############################

def H(index):
    """creates an equal superposition state if given a computational basis state"""
    

def X(index):
    """The Pauli-X gate is the quantum equivalent of the NOT gate for classical computers with respect to the standard basis"""
    pass

def Y(index):
    pass

def Z(index):
    """Pauli Z is sometimes called phase-flip."""
    pass

def P(index):
    """This is equivalent to tracing a horizontal circle (a line of constant latitude), or a rotation about the z-axis on the Bloch sphere"""
    pass

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
    qbits = [bit] + list(*args)

    
    
