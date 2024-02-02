import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from draggable import *
from system import *

mpl.rcParams['toolbar'] = 'None'


# noinspection PyPep8Naming
class Renderer(object):
    """The renderer object is used to render meshes onto the matplotlib window"""
    def __init__(self, system: System, XMAX: float, YMAX: float, density: float, rx: int, ry: int) -> None:
        """
        Initialises the renderer object
        @param system: References the system to render on
        @param XMAX: Stores the maximum x value for the matplotlib window
        @param YMAX: Stores the maximum y for the matplotlib window
        @param density: Stores the density information of the system
        @param rx: Stores the x point density value
        @param ry: Stores the y point density value
        @return: None
        """
        try:
            assert (type(XMAX) is float and type(YMAX) is float and type(density) is float)
        except AssertionError:
            raise TypeError("Bad parameter type")

        self.system = system
        self.XMAX, self.YMAX = XMAX, YMAX
        self.density = density
        self.rx, self.ry = rx, ry
        self.figure = None
        self.ax = None
        self.draggables = None

    def launch(self) -> None:
        """
        Launches the renderer object
        @return: None
        """
        self.figure, self.ax = plt.subplots()
        self.update()
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y$')
        self.ax.set_xlim(-self.XMAX, self.XMAX)
        self.ax.set_ylim(-self.YMAX, self.YMAX)
        self.ax.set_aspect('equal')
        plt.show()

    def update(self) -> None:
        """
        Updates the renderer object
        @return: None
        """
        self.clear()
        self.dfield()
        self.dpoints()
        self.dwalls()

    def clear(self) -> None:
        """
        Clears the renderer object
        @return: None
        """
        # self.ax = plt.gca()
        self.ax.cla()
        # clear arrowheads streamplot

    # noinspection PyUnresolvedReferences
    def dfield(self) -> None:
        """
        Create a new field object
        @return: None
        """
        x = np.linspace(-self.XMAX, self.XMAX, self.rx)
        y = np.linspace(-self.YMAX, self.YMAX, self.ry)
        X, Y = np.meshgrid(x, y)
        V = self.system.field(X, Y)
        [Ex, Ey] = np.gradient(V, self.rx, self.ry)

        # Draw only if the field exists
        if len(Ex) and len(Ey):
            self.ax.streamplot(x, y, Ey, Ex, color=(2 * np.log(np.hypot(Ex, Ey))), linewidth=1, cmap=plt.cm.inferno,
                               density=self.density, arrowstyle='->', arrowsize=1.5)
            self.ax.matshow(V, interpolation='nearest', alpha=1, cmap=plt.cm.plasma,
                            extent=(-self.XMAX, self.XMAX, self.YMAX, -self.YMAX))

    def dpoints(self) -> None:
        """
        Create a new points object
        @return: None
        """
        self.draggables = []
        for point in self.system.points:
            # noinspection PyUnresolvedReferences
            circle = Circle((point.x, point.y), point.size,
                            color=plt.cm.RdBu(mpl.colors.Normalize(vmin=-10, vmax=10)(-point.tens)), zorder=100)
            self.ax.add_patch(circle)
            draggable = Draggable(circle, self.update, point)
            draggable.connect()
            self.draggables.append(draggable)

    def dwalls(self):
        """
        Create a new walls object
        @return: None
        """
        for wall in self.system.walls:
            self.ax.plot([wall.x1, wall.y1], [wall.x2, wall.y2], marker='o')
