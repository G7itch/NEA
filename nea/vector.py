from math import sqrt


class Vector(object):

    def __init__(self,size:int):
        """Initialises the vector as a zero array of given size"""
        try:
            assert type(size) == int #Check if size is an integer, if not prints error message and quits. The user should never encounter this error
        except AssertionError:
            print("E: Size parameter should be an integer")
            exit(1)
        self.vector = [0] * size

    def setElement(self, index:int, value:float) -> bool:
        """Sets the value at one index in the vector to a given value"""
        try: assert index <= len(self.vector) and type(index) ==int
        except AssertionError:
            print("Index must be an integer less than or equal to the length of the list")
            return False #Indicate failed execution
        self.vector[index] = value
        return True #Indicate succesful execution
    
    def getElement(self,index:int) -> float:
        """Returns the value stored in the given index of the vector"""
        try: assert index <= len(self.vector) and type(index) == int
        except AssertionError:
            print("Index must be an integer less than or equal to the length of the list")
            return False
        return self.vector[index]
    
    def scalarMul(self,num:float) -> "Vector":
        """Performs scalar multiplication on a vector"""
        mulvec = Vector(len(self.vector)) #Creates a new vector object so can be used without overwriting underlying vector
        for count,element in enumerate(self.vector):
            mulvec.setElement(count,num*element)
        return mulvec

    def __mul__(self,num:float) -> "Vector":
        """Scalar multiplication shorthand"""
        return self.scalarMul(num)
    
    def setElements(self) -> bool:
        """Provides console interface to set all of the elements of the vector"""
        print("\n")
        for i in range(len(self.vector)):
            number = float(input(f"Enter value for index {i}: "))
            self.setElement(i,number)
        print("\n")
        return True
    
    def setN(self,n:float) -> bool:
        """Shorthand, sets every element of the vector to the same number"""
        size = len(self.vector)
        self.vector = [n] * size
        return True

    def allZeros(self) -> bool:
        """Returns true if every element of the vector is 0"""
        return not(all(self.vector))
    
    def magnitude(self) -> float:
        """Returns the size of the vector using standard analytic geometry formula sqrt(a^2 + b^2...)"""
        total = 0
        for i in range(len(self.vector)):
            total += (self.vector[i])**2
        return sqrt(total)
    
    def isUnit(self) -> bool:
        """Returns true if the current vector instance is an example of a unit vector"""
        return self.magnitude() == 1
    
    def unit(self) -> "Vector":
        size = len(self.vector)
        unitvec = Vector(size) #create a new instance to not overwrite existing case
        mag = self.magnitude()
        for count,ele in enumerate(self.vector):
            unitvec.setElement(count,ele/mag)
        return unitvec
    
    def tensor(self,other: "Vector") -> "Vector":
        """Returns tensor product of two vectors"""
        newsize = len(self.vector) * len(other.vector)
        tensorproduct = Vector(newsize)
        i = -1
        for count,element in enumerate(self.vector):
            for count2, element2 in enumerate(other.vector):
                i +=1
                tensorproduct.setElement(i,element*element2)
            return tensorproduct

    def __repr__(self) -> str:
        """Returns human friendly version of object using more traditional curved brackets"""
        return "(" + str(self.vector)[1:-1] + ")"
    
