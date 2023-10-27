from qbit import Qbit
from cbit import Cbit
from math import sqrt
from vector import Vector
from login import Login
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib import cm, colors
import time
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
    plt.show(block=False)
    plt.pause(0.5) # 0.5 seconds
    qbit.diffuse(i)


def main():
    #####################Login to system#######################
    username = input("Enter your username or press enter to sign up: ")
    if username == "":
        a = Login()
    else:
        password = input("Enter your password: ")
        a = Login(username,password)
    ###########################################################
    #################Qbit Setup for graphing###################
    c = Qbit(1)
    i = 0
    ###########################################################
    while True:
        drawgraph(c,i)
        i += 1


main()
