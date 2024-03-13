@value
struct Vector2D:
    var __vector: SIMD[DType.float16, 2]

    fn __init__(inout self):
        """Initialises the vector as a zero array of given size."""
        self.__vector = SIMD[DType.float16, 2](0, 0)

    fn getElement(borrowed self, borrowed index: Int) raises -> Float16:
        """Returns the value stored in the given index of the vector.

        Args:
            index: The index of the element being retrieved.

        Returns:
            Element if successful, else False.
        """
        if index >= self.__vector.__len__():
            raise Error('Index needs to be less than the length of the list')
        else:
            return self.__vector.__getitem__(idx=index)

    fn setElement(inout self, borrowed index: Int, value: Float16) raises -> Bool:
        """Sets the value at one index in the vector to a given value.

        Args:
            index: The index of the element being set.
            value: [The value to be set.

        Returns:
            True if successful, else False. 
        """
        if index >= self.__vector.__len__():
            raise Error('Index needs to be less than the legnth of the list')
        else:
            self.__vector.__setitem__(idx=index,val=value)
            return True

    fn scalarMul(borrowed self, borrowed number: Float16) -> Vector2D:
        """Performs scalar multiplication on a vector.

        Args:
            number: The scalar to multiply by.

        Returns:
            Multiplied vector if successful, else False.
        """
        var mul_vec = Vector2D()
        mul_vec.__vector = self.__vector * number
        return mul_vec
    
    fn __mul__(borrowed self, borrowed number: Float16) -> Vector2D:
        """Scalar multiplication shorthand.

        Args:
            number: The scalar to multiply by.

        Returns:
            Multiplied vector if successful, else False.
        """
        return self.scalarMul(number=number)

    fn setN(inout self, borrowed number: Float16) -> Vector2D:
        """Shorthand, sets every element of the vector to the same number.

        Args:
            number: The number to set.

        Returns:
            Updated vector object.
        """
        self.__vector = self.__vector.splat(number)
        return self
    
    fn allZeros(borrowed self) raises -> Bool:
        """Returns true if every element of the vector is 0.

        Returns:
            True if all elements are 0, false otherwise.
        """
        var total: Int8 = 0
        for i in range(2):
            if self.getElement(i) == 0:
                total += 1
        return total == 2
    
    fn magnitude(borrowed self) raises -> Float16:
        """Returns the size of the vector using standard analytic geometry formula sqrt(a^2 + b^2...).

        Returns:
            The magnitude of the vector.
        """
        var total: Float16 = 0
        for i in range(0, 2):
            total += self.getElement(i) ** 2
        return total ** 0.5

    fn isUnit(borrowed self) raises -> Bool:
        """Returns true if the current vector instance is an example of a unit vector.

        Returns:
            True if it is an example of a unit vector, else False.
        """
        return self.magnitude() == 1
    
    fn unit(borrowed self) raises -> Vector2D:
        """Returns a new vector instance set to be the unit vector of the existing instance.

        Returns:
            The new vector instance.
        """
        var unit_vec = Vector2D()
        var mag = self.magnitude()
        if mag == 0:
            raise Error('No unit vector exists for zero vector')
        for i in range(2):
            _ = unit_vec.setElement(index=i,value=self.getElement(i) / mag)
        return unit_vec
    
    fn __repr__(self) -> String:
        """Returns a human friendly version of the object using more traditional curved brackets.

        Returns:
            The representation of the vector.
        """
        return "(" + str(self.__vector)[1:-1] + ")"

    
