from Point import *
from Wall import *
import numpy as np
from math import sqrt

class System():
    def __init__(self, epsilon, gamma):
        self.points = []        # Array of Points
        self.walls = []         # Array of Walls
        self.epsilon = epsilon  # Permitivity
        self.gamma = gamma      # Conductivity

    def addPoint(self, point):
        self.points.append(point)

    def addWall(self, wall):
        self.walls.append(wall)
   
    def compute(self, i, X, Y, R, U):
        I = (U * self.gamma * 2 * np.pi)
        Sigma = (I * self.epsilon) / (self.gamma * 4 * np.pi * pow(R,2))
        
        dist = sqrt(pow(Y[i], 2) + pow(X[i], 2)) # Euclidean distance
        
        if (dist < R):
            return ((Sigma * pow(R, 2))/self.epsilon)*(1/R) # Constant when we are inside the point
        else:
            return ((Sigma * pow(R, 2))/self.epsilon)*(1/dist)

    def field(self, X, Y) -> iter:
        u, v = X.shape
        size = np.size(X)
        X.shape = (size)
        Y.shape = (size)
        V = np.zeros((u, v))

        for point in self.points:
            tX = [X[i]-point.x for i in range(np.size(X))]
            tY = [Y[i]-point.y for i in range(np.size(Y))]
            E = np.array([self.compute(i, tX, tY, point.size, point.tens) for i in range(size)], dtype=float)
            E.shape = (u, v)
            V = V + E
        
        return V
