from math import sqrt

import numpy as np


class System(object):
    """
    The system class is responsible for all the electromagnetic calculations being performed.
    It calculates the correct values to be displayed by the renderer.
    It is the core of the matplotlib particle configuration view.
    """

    def __init__(self, epsilon: float, gamma: float) -> None:
        """
        Initialises the system class
        @param epsilon: Stores the permittivity information
        @param gamma: Stores the conductivity information
        @return: None
        """
        self.points = []  # Array of Points
        self.walls = []  # Array of Walls
        self.epsilon = epsilon  # Permittivity
        self.gamma = gamma  # Conductivity

    def addPoint(self, point: object) -> None:
        """
        Links a point object reference to the system class
        @param point: Point object
        @return: None
        """
        self.points.append(point)

    def addWall(self, wall: object) -> None:
        """
        Links a wall object reference to the system class
        @param wall: Wall object
        @return: None
        """
        self.walls.append(wall)

    def compute(self, i: int, x_pos: list, y_pos: list, size: float, tension: float) -> float | complex:
        """
        Computes the correct EM equations for the system
        @param i: index
        @param x_pos: X position of the system point
        @param y_pos: Y position of the system point
        @param size: Size of the system point
        @param tension: Tension of the system points
        @return: EM force value
        """
        current = (tension * self.gamma * 2 * np.pi)
        sigma = (current * self.epsilon) / (self.gamma * 4 * np.pi * pow(size, 2))

        dist = sqrt(pow(y_pos[i], 2) + pow(x_pos[i], 2))  # Euclidean distance

        if dist < size:
            return ((sigma * pow(size, 2)) / self.epsilon) * (1 / size)  # Constant when we are inside the point
        else:
            return ((sigma * pow(size, 2)) / self.epsilon) * (1 / dist)

    def field(self, X: np.array, Y: np.array) -> iter:
        """
        Calculates the effects of the EM field
        @param X: X positions of the point objects
        @param Y: Y positions of the point objects
        @return: Vector
        """
        u, v = X.shape
        size = np.size(X)
        X.shape = size
        Y.shape = size
        vector = np.zeros((u, v))

        for point in self.points:
            t_x = [X[i] - point.x for i in range(np.size(X))]
            t_y = [Y[i] - point.y for i in range(np.size(Y))]
            energy = np.array([self.compute(i, t_x, t_y, point.size, point.tens) for i in range(size)], dtype=float)
            energy.shape = (u, v)
            vector = vector + energy

        return vector
