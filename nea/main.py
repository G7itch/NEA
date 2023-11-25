from qbit import Qbit
from cbit import Cbit
from math import sqrt
from vector import Vector
from login import Login
from interface import CodeEditor
from interpreter import Interpreter
import matplotlib.pyplot as plt
from threading import Thread
import warnings
import time
import getpass
import os
#########################################################
#Lots of general vector functions are defined in the vector class and Cbit/Qbit will inherit these
#Qbits inherits all the more specialised bit functions from Cbit, but overwrites some and adds others
#The reasoning behind tis is that Qbits can do everything that Cbits do but more - so even though they are a bigger class conceptually, inheritence makes sense this way round
#########################################################
def drawgraph(qbit,i):
    probs = []
    for j in range(len(qbit.probability)-1):
        for k in range(len(qbit.probability[0])-1):
            probs.append(qbit.probability[j][k])

        
    plt.matshow(qbit.probability,0)
    plt.ion()
    plt.title("Particle Probability distribution")
    cb = plt.colorbar()
    plt.clim(0,0.1)
    plt.show(block=False)
    plt.pause(0.5)
    cb.remove()
    qbit.diffuse(i)

def mainGraphLoop(qbit,i):
    while True:
        drawgraph(qbit,i)
        i += 1


def main():
    #####################Login to system#######################
    username = input("Enter your username or press enter to sign up: ")
    if username == "":
        a = Login()
    else:
        password = getpass.getpass(prompt="Enter your password: ")
        a = Login(username,password)
    ###########################################################
    ###########################Setup###########################
    c = Qbit(1)
    inter = Interpreter(c)
    editor = CodeEditor()
    os.system("cls")
    ###########################################################
    with warnings.catch_warnings(): #Matplotlib likes to give suggestions and prints these to the terminal, so we are suppressing them
        mainGraphLoop(c,0) 
        editor.mainloop()


main()
