from qbit import Qbit
from login import Login
from interface import CodeEditor, filemenu
from interpreter import Interpreter
from Renderer import *
import matplotlib.pyplot as plt
import warnings
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
    print("  ___  ____  _")       
    print(" / _ \/ ___|(_)_ __ ___") 
    print("| | | \___ \| | '_ ` _ \ ")  
    print("| |_| |___) | | | | | | |")  
    print(" \__\_\____/|_|_| |_| |_|") 
    print("\n\n")
    username = input("Enter your username or press enter to sign up: ")
    if username == "":
        a = Login()
    else:
        password = getpass.getpass(prompt="Enter your password: ")
        a = Login(username,password)
    file_open = filemenu()
    ###########################################################
    ###########################Setup###########################
    c = Qbit(1)
    inter = Interpreter(c)
    editor = CodeEditor(inter,file_open)
    system = System(8.85418782e-12, 0.04)
    renderer = Renderer(system, 0.6, 0.6, 1.6, 40, 40)
    renderer.system.addPoint(Point(-0.3, -0.3, 0.2, 5))
    renderer.system.addPoint(Point(-0.3, -0.3, 0.2, -5))
    os.system("cls")
    ###########################################################
    with warnings.catch_warnings():
        #traceback.print_stack() #Matplotlib likes to give suggestions and prints these to the terminal, so we are suppressing them
        mainGraphLoop(c,0)
        #renderer.launch() #not sure if this will loop without threading
        editor.mainloop()


if __name__ == "__main__":
    main()
