import getpass
import os
import warnings

from Point import Point
from Renderer import *
from interface import CodeEditor, filemenu
from interpreter import Interpreter
from login import Login
from qbit import Qbit


# Lots of general vector functions are defined in the vector
# class and Cbit/Qbit will inherit these Qbits inherits all the more specialised bit functions from Cbit,
# but overwrites some and adds others The reasoning behind this is that Qbits can do everything that Cbits do but more
# So even though they are a bigger class conceptually, inheritance makes sense this way round
def drawgraph(qbit: Qbit, step: int) -> None:
    """
    Draws the particle probability graph
    @param qbit: The Qbit object being referenced for the graph
    @param step: The step in the diffusion process we are at
    @return: None
    """
    probs = []
    for j in range(len(qbit.probability) - 1):
        for k in range(len(qbit.probability[0]) - 1):
            probs.append(qbit.probability[j][k])

    plt.matshow(qbit.probability, 0)
    plt.ion()
    plt.title("Particle Probability distribution")
    cb = plt.colorbar()
    plt.clim(0, 0.1)
    plt.show(block=False)
    plt.pause(0.5)
    cb.remove()
    qbit.diffuse(step)


def mainGraphLoop(qbit: Qbit, step: int) -> None:
    """
    Enables the functionality of the drawgraph function
    @param qbit: The Qbit object being referenced for the graph
    @param step: The step in the diffusion process we are at
    @return: None
    """
    while True:
        drawgraph(qbit, step)
        step += 1


def main() -> None:
    """
    The Main function of the program, enables all other code to run
    @return: None
    """
    # Login to the system
    print(r"  ___  ____  _")
    print(r" / _ \/ ___|(_)_ __ ___")
    print(r"| | | \___ \| | '_ ` _ \ ")
    print(r"| |_| |___) | | | | | | |")
    print(r" \__\_\____/|_|_| |_| |_|")
    print("\n\n")
    username = input("Enter your username or press enter to sign up: ")
    if username == "":
        _ = Login()
    else:
        password = getpass.getpass(prompt="Enter your password: ")
        _ = Login(username, password)
    file_open = filemenu()

    # Setup
    c = Qbit(1)
    inter = Interpreter()
    editor = CodeEditor(inter, file_open)
    system = System(8.85418782e-12, 0.04)
    renderer = Renderer(system, 0.6, 0.6, 1.6, 40, 40)
    renderer.system.addPoint(Point(-0.3, -0.3, 0.2, 5))
    renderer.system.addPoint(Point(-0.3, -0.3, 0.2, -5))
    os.system("cls")

    with warnings.catch_warnings():
        # traceback.print_stack()
        # Matplotlib likes to give suggestions and prints these to the terminal, so we are suppressing them
        mainGraphLoop(c, 0)
        # renderer.launch() #not sure if this will loop without threading
        editor.mainloop()


if __name__ == "__main__":
    main()
