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

    def __init__(self, x, y, x_lim: tuple, y_lim: tuple) -> None:
        self.__x = scalar(x, x_lim)
        self.__y = scalar(y, y_lim)


class plane:

    """
    screen_size - (width ,height) = pygame window size in pixel
    unit_length - pixel count for 1 unit length in cartesian system
    parent      - (optional) parent plance instance
    """

    def __init__(self,
                 window_size: tuple,
                 unit_length,
                 parent=None,
                 set_limit=True) -> None:
        self.window_size = window_size
        self.unit_length = unit_length
        self.parent = parent
        if set_limit:
            self.__center_X = scalar(self.window_size[0] // 2,
                                     (0, self.window_size[0]))
            self.__center_Y = scalar(self.window_size[1] // 2,
                                     (0, self.window_size[1]))
        else:
            self.__center_X = scalar(self.window_size[0] // 2)
            self.__center_Y = scalar(self.window_size[1] // 2)
        self.set_limit()
        if self.parent:
            self.window_size = self.parent.window_size

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
    def centerX(self):
        """center X value in pixel"""
        return self.__center_X.value

    @centerX.setter
    def centerX(self, o):
        self.__center_X.value = o

    @property
    def centerY(self):
        """center Y value in pixel"""
        return self.__center_Y.value

    @centerY.setter
    def centerY(self, o):
        self.__center_Y.value = o

    @property
    def center(self):
        """center (X, Y) value in pixel"""
        return (self.__center_X.value, self.__center_Y.value)

    @center.setter
    def center(self, pos):
        if isinstance(pos, tuple):
            self.centerX = pos[0]
            self.centerY = pos[1]
        elif isinstance(pos, vector):
            self.centerX = pos.X
            self.centerY = pos.Y

    @property
    def shape(self):
        return (self.x_min, self.x_max, self.y_min, self.y_max)

    def set_limit(self):
        self.x_min = (self.__center_X.value - self.window_size[0]) \
            // self.unit_length
        self.x_max = (self.window_size[0] - self.__center_X.value) \
            // self.unit_length
        self.y_min = (self.__center_Y.value - self.window_size[1]) \
            // self.unit_length
        self.y_max = (self.window_size[1] - self.__center_Y.value) \
            // self.unit_length

    def getXY(self, xy):
        """cartesian (x, y) to pygame (x, y)"""
        return (self.getX(xy[0]), self.getX(xy[1]))

    def getX(self, x):
        """cartesian x to pygame x"""
        return self.__center_X.value + x * self.unit_length

    def getY(self, y):
        """cartesian y to pygame y"""
        return self.__center_Y.value - y * self.unit_length

    def toXY(self, center: tuple):
        """pygame (x, y) to cartesian (x, y)"""
        return (self.toX(center[0]), self.toY(center[1]))

    def toX(self, x):
        """pygame x to cartesian x"""
        return (x - self.__center_X.value) / self.unit_length

    def toY(self, y):
        """pygame y to cartesian y"""
        return (self.__center_Y.value - y) / self.unit_length

    def createVector(self, x=1, y=0, set_limit=False):
        """Return a vector object parented by current plane instance"""
        return vector(self, x, y, set_limit=set_limit)

    def createRandomVector(self):
        """Return a random vector object parented by current plane instance"""
        return vector(self).random()

    def show(self, window, color=BLACK, width=1):
        pg.draw.line(window, color, self.center,
                     (self.centerX, self.centerY-20), width)
        pg.draw.line(window, color, self.center,
                     (self.centerX+20, self.centerY), width)


class vector:

    """
    #TODO
    """

    def __init__(self, space: plane, x=0, y=0,
                 set_limit: bool = False) -> None:
        if x == y == 0:
            LOG('Created NULL vector!', WARNING, logging=True)
        self.space = space
        self.length_max = max(self.space.x_max, self.space.y_max)
        self.length_min = 1
        self.__limit = set_limit
        if self.__limit:
            self.__x = scalar(x, (-self.length_max, self.length_max))
            self.__y = scalar(y, (-self.length_max, self.length_max))
        else:
            self.__x = scalar(x)
            self.__y = scalar(y)

    def __add__(self, o):
        if o > 0:
            if self.__limit and self.length + o <= self.length_max:
                self.x += o * cos(self.direction)
                self.y += o * sin(self.direction)
            elif not self.__limit:
                self.x += o * cos(self.direction)
                self.y += o * sin(self.direction)
        elif o < 0:
            self.__sub__(abs(o))
        return self

    def __sub__(self, o):
        if o > 0:
            if o < self.length - 1:
                self.x -= o * cos(self.direction)
                self.y -= o * sin(self.direction)
            else:
                self.x, self.y = self.unit()
        elif o < 0:
            self.__add__(abs(o))
        return self

    def __mul__(self, factor):
        if self.length * factor > self.length_min:
            if self.__limit:
                if self.length * factor < self.length_max:
                    self.x *= factor
                    self.y *= factor
                else:
                    self.x, self.y = self.unit(self.length_max)
            else:
                self.x *= factor
                self.y *= factor
        else:
            self.x, self.y = self.unit()
        return self

    def __truediv__(self, factor):
        return self.__mul__(1/factor)

    @property
    def x(self):
        """x coordinate in cartesian system"""
        return self.__x.value

    @x.setter
    def x(self, value):
        """Set x in cartesian coordinate system"""
        self.__x.value = value

    @property
    def y(self):
        """y coordinate in cartesian system"""
        return self.__y.value

    @y.setter
    def y(self, value):
        """Set y coordinate in cartesian system"""
        self.__y.value = value

    @property
    def xy(self):
        """(x, y) values in cartesian coordinate system"""
        return (self.x, self.y)

    @xy.setter
    def xy(self, xy: tuple):
        """Set (x, y) for cartesian system using cartesian (x, y)"""
        if isinstance(xy, tuple):
            self.x = xy[0]
            self.y = xy[1]
        elif isinstance(xy, (float, int)):
            self.x = cos(self.direction) * xy
            self.y = sin(self.direction) * xy

    @property
    def X(self):
        """X coordinate in pygame system"""
        return self.space.getX(self.x)

    @property
    def Y(self):
        """Y coordinate in pygame system"""
        return self.space.getY(self.y)

    @property
    def XY(self):
        """(x, y) values in pygame coordinate system"""
        return (self.X, self.Y)

    @XY.setter
    def XY(self, xy: tuple):
        """Set (x, y) for cartesian system using pygame (x, y)"""
        self.x = self.space.toX(xy[0])
        self.y = self.space.toY(xy[1])

    @property
    def length(self):
        """Return length in cartesian coordinate system"""
        return dist((0, 0), (self.x, self.y))

    @length.setter
    def length(self, o):
        if isinstance(o, (float, int)):
            a = self.direction
            if self.__limit:
                if self.length_min <= o <= self.length_max:
                    self.x = cos(a) * o
                    self.y = sin(a) * o
            else:
                if self.length_min <= o:
                    self.x = cos(a) * o
                    self.y = sin(a) * o
        raise TypeError(f"int, float required. Got {type(o)}")

    @property
    def LENGTH(self):
        """Return length in pygame coordinate system"""
        return dist([0, 0], [self.X, self.Y])

    @property
    def direction(self):
        """Return angle from X axis in radians"""
        return atan2(self.y, self.x)

    @direction.setter
    def dircetion(self, o):
        if isinstance(o, (float, int)):
            lng = self.length
            self.x = cos(o) * lng
            self.y = sin(o) * lng
        raise TypeError(f"int, float required. Got {type(o)}")

    def rotate(self, rad):
        """
        Possitive values for counter-clock-wise,
        Negative values for clock-wise rotation
        """
        _x = self.x
        _y = self.y
        self.x = _x * cos(rad) - _y * sin(rad)
        self.y = _x * sin(rad) + _y * cos(rad)

    def random(self):
        """Set vector head at random location"""
        self.x = (random.random() * 2 - 1) * self.space.x_max
        self.y = (random.random() * 2 - 1) * self.space.y_max
        return self

    def distance(self, xy) -> float:
        """Return distance of given vector from current vector"""
        if isinstance(xy, tuple):
            return dist((0, 0), ((self.x - xy[0]), (self.y - xy[1])))
        return dist((0, 0), ((self.x - xy.x), (self.y - xy.y)))

    def angle(self, xy):
        """
        Return the angle between given vector/coordinate
        and current vector
        """
        if isinstance(xy, tuple):
            return atan2(xy[1], xy[0]) - self.direction
        return atan2(xy.y, xy.x) - self.direction

    def dot(self, vec):
        """
        Return 'DOT/SCALAR' product of given vector/coordinate
        and currrent vector
        """
        if isinstance(vec, tuple):
            return self.x * vec[0] + self.y * vec[1]
        return self.x * vec.x + self.y * vec.y

    def unit(self, scale=1):
        """Return unit length vector scaled by 'scale' in cartesian"""
        a = self.direction
        return vector(self.space, cos(a)*scale, sin(a)*scale, self.__limit)

    def normal(self):
        """TODO"""
        return vector(self.space, -self.y, self.x, self.__limit)

    def show(self, window, color=BLACK, width=1, aa=False):
        if aa:
            pg.draw.aaline(window, color, self.space.center,
                           self.XY, width)
        else:
            pg.draw.line(window, color, self.space.center, self.XY, width)
