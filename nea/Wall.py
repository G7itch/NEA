class Wall(object):

    def __init__(self, x1, y1, x2, y2):
        """Setup boundary points"""
        self.x1 :int = x1
        self.y1 :int = y1
        self.x2 :int = x2
        self.y2 :int = y2
        self.__string = str(self.x1) + ", " + str(self.y1) + ", " + str(self.x2) + ", " + str(self.y2)

    def __repr__(self) -> str:
        """Returns object in machine readable form"""
        return self.__string
