from vector import Vector
from math import log2

class Cbit(Vector):

    def __init__(self,dirac:int,sub=None):
        """Dirac refers to the integer that would be shown in the symbol used in dirac notation (e.g. |0>)
           Sub refers to the number of bits (elements) to be used in the vector form. It is the subscript of dirac notation, by defauly it is the minimum number required
           Dirac and sub are both integers
           
           Init function creates either a Cbit vector or a tensor product if multiple bit are supplied."""
        
        self.Cbit = None
        self.__sub = sub #Preformatting to change sub before testing
        try: assert type(dirac) == int
        except AssertionError:
            print("E: 'dirac' must be a positive integer")
            exit(1)

        if sub == None:
            self.__sub = len("{0:b}".format(dirac))
        ####################### Error Checking ############################
        try: assert (type(self.__sub) == int and type(dirac) == int) and (self.__sub >= 0 and dirac >= 0)
        except AssertionError:
            print("'Sub' and 'dirac' must be positive integers")
            exit(1)
        
        try: assert self.__sub >= len("{0:b}".format(dirac))
        except AssertionError:
            print("Sub value must be at least the minimum number of bits required to represent the input, consider omitting the sub parameter in your call")
            exit()
        ###################################################################

        self.__dirac = (self.__sub - len("{0:b}".format(dirac))) * "0" + "{0:b}".format(dirac) #Settings binary dirac value with the correct number of leading 0's
 
        ###################################################################

        ############# If there are multiple bits, rather than make a cbit vector, calculate their tensor product######################
        if self.__sub == 1:
            self.Cbit = Vector(2)
            self.Cbit.setElement(abs(0 - int(self.__dirac)),1)
        else:
            self.__dirac.split()
            tensorprod = None
            for count,ele in enumerate(self.__dirac):
                ele = int(ele)
                if count == 0:
                    continue
                element = Vector(2)
                element.setElement(abs(0-ele),1) #Makes the vector (0,1) if the element is 1 and (1,0) if the element is 0
                if tensorprod == None:
                    lastelement = Vector(2)
                    lastelement.setElement(abs(0-int(self.__dirac[count-1])),1) #Adjusts the vector in the same way as the last comment
                else:
                    lastelement = tensorprod
                tensorprod = element.tensor(lastelement)
            
            self.Cbit = tensorprod

    @override
    def setElement(self, index:int, value:float) -> bool:
        """Sets the value at one index in the vector to the given value"""
        try: assert index <= len(self.Cbit.vector) and type(index) == int
        except AssertionError:
            print("E: Index must be an integer less than or equal to the length of the list")
            return False
        if len(self.Cbit.vector) == 2: #If the length is 2 then it must be a standard bit not a tensorproduct
            try: assert value == 1 or value == 0
            except:
                print("E: Value can only take 0 or 1") #Checks to see if the element youre trying to add is valid for the format of Cbits
                return False
        self.Cbit.vector[index] = value
        return True

    def measure(self) -> int:
        if len(self.Cbit.vector) != 2:
            return False
        else:
            return self.Cbit.vector[1]
        
    def probcollapse(self):
        size = log2(len(self.Cbit.vector))
        print("Probability of collapse: ")
        for count,element in enumerate(self.Cbit.vector):
            state = int(size - len("{0:b}".format(count))) * "0" + "{0:b}".format(count)
            percent = element ** 2
            print(f"|{state}>, {percent*100}%")
        return

    def __repr__(self) -> str:
        """Returns a friendly version of object using typical notation"""
        return "(" + str(self.Cbit.vector)[1:-1] + ")"
    
