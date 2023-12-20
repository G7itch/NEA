from cbit import Cbit
from random import choices, randint
from math import exp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import time

class Qbit(Cbit):

    def __init__(self,dirac:int,sub=None):
        """Qbits are the quantum extension of Cbits that can take values intermediate of 0/1"""
        super().__init__(dirac,sub) #Error checking is provided in the super function
        self.Qbit = self.Cbit
        ########################## Visualisation grid setup #################################
        self.probability = [[0 for i in range(11)] for j in range(11)] #For graphical visualisation
        x, y =randint(0,10), randint(0,10)
        self.probability[x][y] = 1
        self.__changed = [[x,y]]
        #self.prettygrid = self.prettify()
        #self.probprint()
        #######################################################################################

    def measure(self) -> int:
        """'Measures' the Qbits state using the probabilistic definition of quantum bits"""
        if len(self.Qbit.vector) != 2:
            return False
        else:
            bits = [0,1]
            collapse = int(choices(bits, weights=(self.Qbit.vector[0]**2,self.Qbit.vector[1]**2),k=1)[0])#Qbit vectors are probabilities rather than deterministic values
            return collapse

    def _softmax(self,vector:list) -> list: #Protected function, I am not sure what classes need to refer to this so better safe than sorry
        """Performs the softmax normalisation on a list of values. https://en.wikipedia.org/wiki/Softmax_function"""
        e = [exp(ele) for ele in vector]
        return [item/sum(e) for item in e] #(e)^x_i/sum(e^x)
        #Maybe only let it apply to 0 values and everything previously seen
    
    def _normalise(self,vector:list,maxprime:float) -> list:
        """Min-max normalisation of given list"""
        min, max = 0, 1 #predefined because we know we are using probabilities
        return [(maxprime*(value-max)+maxprime) for value in vector] #generates new list normalised with min 0 and specified max

    #def prettify(self):
    #    prettygrid = self.probability
    #    print(prettygrid)
    #    for i in range(len(self.probability)-1):
    #        for j in range(len(self.probability)-1):
    #            prettygrid[i][j] = float(round(self.probability[i][j],3))*100
    #    return prettygrid

    def _applygauss2d(self,array:list,n:int) -> bool:
        """Applies gaussian noise (centred on the standard normal Z distribution) to a 2d array"""
        mean = 0
        stddv = 100/(2**n)
        noise = np.random.normal(loc=mean,scale=stddv,size=(len(array),len(array[0]))).tolist()
        for i in range(len(array)):
            for j in range(len(array[0])):
                array[i][j] += noise[i][j]
        #print(array)
        return array
                
        
    def probprint(self) -> None:
        for i in range(len(self.probability)-1):
            for j in range(len(self.probability)-1):
                print(round(round(self.probability[i][j],3)*100,3),end=" ")
            print()

    def diffuse(self,step:int) -> list:
        """Diffuse the probability grid over time. A representation of uncertaincy in our visualisation"""
        newarray = []
        self.probability = self._applygauss2d(self.probability,step)
        for i in range(len(self.probability)):
            for j in range(len(self.probability[0])):
                newarray.append(self.probability[i][j])
        newarray = self._softmax(newarray)
        n = len(self.probability[0])
        self.probability = [newarray[idx:idx+n] for idx in range(0,len(newarray),n)]
        #self.probprint()
    
    def setElement(self,index:int,value:float) -> bool:
        """Sets the value at one index in the vector to the given value"""
        try: assert index <= len(self.Qbit.vector) and type(index) == int
        except AssertionError:
            print("Index must be an integer less than or equal to the length of the list") 
            return False
        if len(self.Qbit.vector) == 2: #If the lenght is 2 then it must be a standard Qbit
            try: assert value <= 1 and value >= -1
            except:
                print("Value can only take the range [-1,1]") #Checks to see if the element youre trying to add is a valid format
                return False
        self.Qbit.vector[index] = value
        return True

    #def __repr__(self):
    #    for i in range(len(self.prettygrid)-1):
    #        print(*self.prettygrid[i])
    #    return ""


