import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Draggable(object):
    """
    Sets up movement for objects in a matplotlib window
    """
    lock = None  # only one can be animated at a time

    def __init__(self, point, update, object_selected: object) -> None:
        """
        Initialises the draggable object
        @param point: The point variable holds point object data
        @param update: This variable holds the reference to the renderer clear function
        @param object_selected: This variable holds the
        reference to the object that is being made into a draggable object
        @return: None
        """
        self.point = point
        self.press = None
        self.background = None
        self.update = update
        self.object = object_selected

    # noinspection PyAttributeOutsideInit
    def connect(self) -> None:
        """
        connect to all the events we need
        @return: None
        """
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event) -> None:
        """
        Sets up the selected object for being moved
        @param event: Movement event
        @return: None
        """
        if event.inaxes != self.point.axes:
            return None
        if Draggable.lock is not None:
            return None
        contains, attrd = self.point.contains(event)
        if not contains:
            return None
        self.press = self.point.center, event.xdata, event.ydata
        Draggable.lock = self
        canvas = self.point.figure.canvas  # draw everything but the selected rectangle and store the pixel buffer
        axes = self.point.axes
        self.point.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)
        axes.draw_artist(self.point)  # redraw just the rectangle
        canvas.blit(axes.bbox)  # blit just the redrawn area

    def on_motion(self, event) -> None:
        """
        Draws the motion of the selected object
        @param event: Movement event
        @return: None
        """
        if Draggable.lock is not self:
            return None
        if event.inaxes != self.point.axes:
            return None
        self.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.center = (self.point.center[0] + dx, self.point.center[1] + dy)
        canvas = self.point.figure.canvas
        axes = self.point.axes
        # restore the background region
        canvas.restore_region(self.background)
        # redraw just the current rectangle
        axes.draw_artist(self.point)
        # blit just the redrawn area
        canvas.blit(axes.bbox)
        self.object.x = self.point.center[0]
        self.object.y = self.point.center[1]

    def on_release(self) -> None:
        """
        On release, we reset the press data
        @return: None
        """
        if Draggable.lock is not self:
            return None
        self.press = None
        Draggable.lock = None

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        self.background = None

        # Update the system on release
        self.update()

        # redraw the full figure
        self.point.figure.canvas.draw()

    def disconnect(self):
        """
        Disconnect all the stored connection ids
        @return: None
        """
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)
