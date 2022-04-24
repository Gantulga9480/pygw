from math import cos, sin, atan2, dist
import random
import pygame as pg
from Game.utils import *
from Game.color import BLACK


class scalar:

    RESOLUTION = 8

    """
    #TODO
    """

    def __init__(self, value=0, limits: tuple = None) -> None:
        if limits:
            self.has_limit = True
            self.min = round(limits[0], self.RESOLUTION)
            self.max = round(limits[1], self.RESOLUTION)
            if value < self.min:
                self.__num = self.min
            elif value > self.max:
                self.__num = self.max
            else:
                self.__num = round(value, self.RESOLUTION)
        else:
            self.has_limit = False
            self.__num = value

    @property
    def value(self):
        return self.__num

    @value.setter
    def value(self, o):
        if self.has_limit:
            if self.min <= o <= self.max:
                self.__num = round(o, self.RESOLUTION)
            else:
                self.__num = self.min if o < self.min else self.max
        else:
            self.__num = o

    def __add__(self, o: object):
        self.value += o
        return self

    def __sub__(self, o: object):
        self.value -= o
        return self

    def __mul__(self, o: object):
        self.value *= o
        return self

    def __truediv__(self, o: object):
        self.value /= o
        return self

    def __repr__(self) -> str:
        return str(self.__num)


class point2d:

    def __init__(self, x=0, y=0,
                 x_lim: tuple = None,
                 y_lim: tuple = None) -> None:
        self.x = scalar(x, x_lim)
        self.y = scalar(y, y_lim)

    @property
    def xy(self) -> tuple:
        return (self.x.value, self.y.value)

    @xy.setter
    def xy(self, o):
        if isinstance(o, (tuple, list)):
            self.x.value = o[0]
            self.y.value = o[1]
        elif isinstance(o, point2d):
            self.x.value = o.x.value
            self.y.value = o.y.value
        else:
            raise TypeError(f"Type  {type(o)} not supported")


class plane:

    """
    screen_size - (width ,height) = pygame window size in pixel
    unit_length - pixel count for 1 unit length in cartesian system
    parent      - (optional) parent plance instance
    """

    def __init__(self,
                 window_size: tuple,
                 unit_length,
                 parent_vector=None,
                 set_limit=True,
                 logging=True) -> None:
        self.window_size = window_size
        self.unit_length = unit_length
        self.parent_vector: vector = parent_vector
        self.logging = logging
        if self.parent_vector:
            self.__center = self.parent_vector.headXY
        else:
            if set_limit:
                self.__center = point2d(self.window_size[0] // 2,
                                        self.window_size[1] // 2,
                                        (0, self.window_size[0]),
                                        (0, self.window_size[1]))
            else:
                self.__center = point2d(self.window_size[0] // 2,
                                        self.window_size[1] // 2)
        self.set_limit()
        if self.parent_vector:
            self.window_size = self.parent_vector.space.window_size

    def __add__(self, o):
        self.x_max += o
        self.y_max += o
        self.x_min -= o
        self.y_min -= o
        return self

    def __sub__(self, o):
        self.x_max -= o
        self.y_max -= o
        self.x_min += o
        self.y_min += o
        return self

    def __mul__(self, o):
        if self.unit_length * o >= 1:
            self.unit_length *= o
        elif o < 1:
            self.unit_length = 1
        return self

    def __truediv__(self, o):
        return self.__mul__(1/o)

    @property
    def X(self):
        """center X value in pixel"""
        return self.__center.x.value

    @X.setter
    def X(self, o):
        if isinstance(o, (int, float)):
            self.__center.x.value = o
        elif isinstance(o, scalar):
            self.__center.x = o
        else:
            raise TypeError(f"Type  {type(o)} not supported")

    @property
    def Y(self):
        """center Y value in pixel"""
        return self.__center.y.value

    @Y.setter
    def Y(self, o):
        if isinstance(o, (int, float)):
            self.__center.y.value = o
        if isinstance(o, scalar):
            self.__center.y.value = o.value
        else:
            raise TypeError(f"Type  {type(o)} not supported")

    @property
    def XY(self):
        """center (X, Y) value in pixel"""
        return (self.__center.x.value, self.__center.y.value)

    @XY.setter
    def XY(self, XY):
        if isinstance(XY, tuple):
            self.__center.x.value = XY[0]
            self.__center.y.value = XY[1]
        elif isinstance(XY, point2d):
            self.__center = XY
        elif isinstance(XY, vector):
            self.__center.x.value = XY.X
            self.__center.y.value = XY.Y
        else:
            raise TypeError(f"Type  {type(XY)} not supported")

    @property
    def shape(self):
        return (self.x_min, self.x_max, self.y_min, self.y_max)

    def set_limit(self):
        self.x_min = (self.__center.x.value - self.window_size[0]) \
            // self.unit_length
        self.x_max = (self.window_size[0] - self.__center.x.value) \
            // self.unit_length
        self.y_min = (self.__center.y.value - self.window_size[1]) \
            // self.unit_length
        self.y_max = (self.window_size[1] - self.__center.y.value) \
            // self.unit_length

    def getXY(self, xy):
        """cartesian (x, y) to pygame (X, Y)"""
        return (self.getX(xy[0]), self.getX(xy[1]))

    def getX(self, x):
        """cartesian x to pygame X"""
        return self.__center.x.value + x * self.unit_length

    def getY(self, y):
        """cartesian y to pygame Y"""
        return self.__center.y.value - y * self.unit_length

    def toXY(self, center: tuple):
        """pygame (X, Y) to cartesian (x, y)"""
        return (self.toX(center[0]), self.toY(center[1]))

    def toX(self, X):
        """pygame X to cartesian x"""
        return (X - self.__center.x.value) / self.unit_length

    def toY(self, Y):
        """pygame Y to cartesian y"""
        return (self.__center.y.value - Y) / self.unit_length

    def createVector(self, x=1, y=0, set_limit=False):
        """Return a vector object parented by current plane instance"""
        return vector(self, x, y, set_limit=set_limit)

    def createRandomVector(self):
        """Return a random vector object parented by current plane instance"""
        return vector(self).random()

    def show(self, window, color=BLACK, width=1):
        pg.draw.lines(window, color, False,
                      [(self.__center.x.value, self.__center.y.value-20),
                       (self.__center.x.value, self.__center.y.value),
                       (self.__center.x.value+20, self.__center.y.value)],
                      width)


class vector:

    """
    #TODO
    """

    def __init__(self, space: plane, x=0, y=0,
                 set_limit: bool = False) -> None:
        self.space = space
        self.length_max = max(self.space.x_max, self.space.y_max)
        self.length_min = 1
        if space.logging and x == y == 0:
            LOG('Created NULL vector!', WARNING, logging=True)
        if set_limit:
            self.head = point2d(x, y,
                                (-self.length_max, self.length_max),
                                (-self.length_max, self.length_max))
        else:
            self.head = point2d(x, y)
        self.headXY = point2d(self.X, self.Y)
        self.__limit = set_limit

    def __add__(self, o):
        if o > 0:
            if self.__limit and self.length + o <= self.length_max:
                self.head.x.value += o * cos(self.direction)
                self.head.y.value += o * sin(self.direction)
            elif not self.__limit:
                self.head.x.value += o * cos(self.direction)
                self.head.y.value += o * sin(self.direction)
        elif o < 0:
            self.__sub__(abs(o))
        self.__update()
        return self

    def __sub__(self, o):
        if o > 0:
            if o < self.length - 1:
                self.head.x.value -= o * cos(self.direction)
                self.head.y.value -= o * sin(self.direction)
            else:
                self.head.x.value, self.head.y.value = self.unit()
        elif o < 0:
            self.__add__(abs(o))
        self.__update()
        return self

    def __mul__(self, factor):
        if self.length * factor > self.length_min:
            if self.__limit:
                if self.length * factor < self.length_max:
                    self.head.x.value *= factor
                    self.head.y.value *= factor
                else:
                    self.head.x.value, self.head.y.value = \
                        self.unit(self.length_max)
            else:
                self.head.x.value *= factor
                self.head.y.value *= factor
        else:
            self.head.x.value, self.head.y.value = self.unit()
        self.__update()
        return self

    def __truediv__(self, factor):
        return self.__mul__(1/factor)

    @property
    def x(self):
        """x coordinate in cartesian system"""
        return self.head.x.value

    @x.setter
    def x(self, x):
        """Set x in cartesian coordinate system"""
        if isinstance(x, (int, float)):
            self.head.x.value = x
        elif isinstance(x, scalar):
            self.head.x = x
        else:
            raise TypeError(f"Type  {type(x)} not supported")
        self.__update()

    @property
    def y(self):
        """y coordinate in cartesian system"""
        return self.head.y.value

    @y.setter
    def y(self, y):
        """Set y coordinate in cartesian system"""
        if isinstance(y, (int, float)):
            self.head.y.value = y
        elif isinstance(y, scalar):
            self.head.y = y
        else:
            raise TypeError(f"Type  {type(y)} not supported")
        self.__update()

    @property
    def xy(self):
        """(x, y) values in cartesian coordinate system"""
        return (self.head.x.value, self.head.y.value)

    @xy.setter
    def xy(self, xy: tuple):
        """Set (x, y) for cartesian system using cartesian (x, y)"""
        if isinstance(xy, tuple):
            self.head.x.value = xy[0]
            self.head.y.value = xy[1]
        elif isinstance(xy, point2d):
            self.head = xy
        else:
            raise TypeError(f"Type  {type(xy)} not supported")
        self.__update()

    @property
    def X(self):
        """X coordinate in pygame system"""
        return self.space.getX(self.head.x.value)

    @property
    def Y(self):
        """Y coordinate in pygame system"""
        return self.space.getY(self.head.y.value)

    @property
    def XY(self):
        """(x, y) values in pygame coordinate system"""
        return (self.X, self.Y)

    @XY.setter
    def XY(self, XY):
        """Set (x, y) for cartesian system using pygame (X, Y)"""
        if isinstance(XY, tuple):
            self.head.x.value = self.space.toX(XY[0])
            self.head.y.value = self.space.toY(XY[1])
        elif isinstance(XY, point2d):
            self.head.x.value = self.space.toX(XY.x.value)
            self.head.y.value = self.space.toY(XY.y.value)
        elif isinstance(XY, vector):
            self.head.x.value = self.space.toX(XY.X)
            self.head.y.value = self.space.toY(XY.Y)
        else:
            raise TypeError(f"Type  {type(XY)} not supported")
        self.__update()

    @property
    def length(self):
        """Return length in cartesian coordinate system"""
        return dist((0, 0), (self.head.x.value, self.head.y.value))

    @length.setter
    def length(self, o):
        if isinstance(o, (float, int)):
            a = self.direction
            if self.__limit:
                if self.length_min <= o <= self.length_max:
                    self.head.x.value = cos(a) * o
                    self.head.y.value = sin(a) * o
            else:
                if self.length_min <= o:
                    self.head.x.value = cos(a) * o
                    self.head.y.value = sin(a) * o
        else:
            raise TypeError(f"Type  {type(o)} not supported")
        self.__update()

    @property
    def LENGTH(self):
        """Return length in pygame coordinate system"""
        return dist([0, 0], [self.X, self.Y])

    @property
    def direction(self):
        """Return angle from X axis in radians"""
        return atan2(self.head.y.value, self.head.x.value)

    @direction.setter
    def dircetion(self, o):
        if isinstance(o, (float, int)):
            lng = self.length
            self.head.x.value = cos(o) * lng
            self.head.y.value = sin(o) * lng
        else:
            raise TypeError(f"Type  {type(o)} not supported")
        self.__update()

    def rotate(self, rad):
        """
        Possitive values for counter-clock-wise,
        Negative values for clock-wise rotation
        """
        _x = self.head.x.value
        _y = self.head.y.value
        self.head.x.value = _x * cos(rad) - _y * sin(rad)
        self.head.y.value = _x * sin(rad) + _y * cos(rad)
        self.__update()

    def random(self):
        """Set vector head at random location"""
        self.head.x.value = (random.random() * 2 - 1) * self.space.x_max
        self.head.y.value = (random.random() * 2 - 1) * self.space.y_max
        self.__update()
        return self

    def distance(self, xy) -> float:
        """Return distance of given vector from current vector in cartesian"""
        if isinstance(xy, tuple):
            return dist((0, 0),
                        ((self.head.x.value - xy[0]),
                         (self.head.y.value - xy[1])))
        elif isinstance(xy, vector):
            return dist((0, 0),
                        ((self.head.x.value - xy.head.x.value),
                         (self.head.y.value - xy.head.y.value)))
        elif isinstance(xy, point2d):
            return dist((0, 0),
                        ((self.head.x.value - xy.x.value),
                         (self.head.y.value - xy.y.value)))
        else:
            raise TypeError(f"Type  {type(xy)} not supported")

    def angle(self, xy):
        """
        Return the angle between given vector/coordinate
        and current vector in cartesian
        """
        if isinstance(xy, tuple):
            return atan2(xy[1], xy[0]) - self.direction
        elif isinstance(xy, vector):
            return atan2(xy.head.y.value, xy.head.x.value) - self.direction
        elif isinstance(xy, point2d):
            return atan2(xy.y.value, xy.x.value) - self.direction
        else:
            raise TypeError(f"Type  {type(xy)} not supported")

    def dot(self, xy):
        """
        Return 'DOT/SCALAR' product of given vector/coordinate
        and currrent vector in cartesian
        """
        if isinstance(xy, tuple):
            return self.head.x.value * xy[0] + self.head.y.value * xy[1]
        elif isinstance(xy, vector):
            return self.head.x.value * xy.head.x.value + \
                self.head.y.value * xy.head.y.value
        elif isinstance(xy, point2d):
            return self.head.x.value * xy.x.value + \
                self.head.y.value * xy.y.value
        else:
            raise TypeError(f"Type  {type(xy)} not supported")

    def unit(self, scale=1):
        """Return unit length vector scaled by 'scale' in cartesian"""
        a = self.direction
        return vector(self.space, cos(a)*scale, sin(a)*scale, self.__limit)

    def normal(self):
        """TODO"""
        return vector(self.space, -self.head.y.value,
                      self.head.x.value, self.__limit)

    def show(self, window, color=BLACK, width=1, aa=False):
        if aa:
            pg.draw.aaline(window, color, self.space.XY,
                           self.XY, width)
        else:
            pg.draw.line(window, color, self.space.XY, self.XY, width)

    def __update(self):
        self.headXY.xy = (self.space.getX(self.head.x.value),
                          self.space.getY(self.head.y.value))
