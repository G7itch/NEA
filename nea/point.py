from dataclasses import dataclass


# class Point(object):
#    def __init__(self, x, y, size, tens):
#        self.x    :float = x          # Position x_pos (m)
#        self.y    :float = y          # Position y_pos (m)
#        self.size :float = size    # Ray      (m)
#        self.tens :float = tens    # Tension    (V)
#        self.__string = str(self.x) + ", " + str(self.y) + ", " + str(self.size) + ", " + str(self.tens)

#    def __repr__(self) -> str:
#        return self.__string

@dataclass
class Point:
    x: float
    y: float
    size: float
    tens: float
