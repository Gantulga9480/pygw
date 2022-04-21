import math
import random
from Game.utils import *


class scalar:

    RESOLUTION = 4

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


class plane:

    """
    screen_size - (width ,height) = pygame window size in pixel
    unit_length - pixel count for 1 unit length in cartesian system
    parent      - (optional) parent plance instance
    """

    def __init__(self,
                 screen_size: tuple(int, int),
                 unit_length,
                 parent=None) -> None:
        self._size = screen_size
        self.unit_length = unit_length
        self.parent = parent
        self._x_center = self._size[0] // 2
        self._y_center = self._size[1] // 2
        self.set_limit()

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
        if self.unit_length / o >= 1:
            self.unit_length /= o
        elif o > 1:
            self.unit_length = 1
        return self

    @property
    def centerX(self):
        """center X value in pixel"""
        return self._x_center

    @centerX.setter
    def centerX(self, o):
        if 0 <= o <= self._size[0]:
            self._x_center = o
        else:
            if o > 0:
                self._x_center = self._size[0]
            else:
                self._x_center = 0

    @property
    def centerY(self):
        """center Y value in pixel"""
        return self._y_center

    @centerY.setter
    def centerY(self, o):
        if 0 <= o <= self._size[1]:
            self._y_center = o
        else:
            if o > 0:
                self._y_center = self._size[1]
            else:
                self._y_center = 0

    @property
    def center(self):
        """center (X, Y) value in pixel"""
        return (self.centerX, self.centerY)

    @center.setter
    def center(self, pos):
        if isinstance(pos, tuple):
            self.centerX = pos[0]
            self.centerY = pos[1]
        elif isinstance(pos, vector):
            self.centerX = pos.X
            self.centerY = pos.Y

    def set_limit(self):
        self.x_min = (self._x_center - self._size[0]) // self.unit_length
        self.x_max = (self._size[0] - self._x_center) // self.unit_length
        self.y_min = (self._y_center - self._size[1]) // self.unit_length
        self.y_max = (self._size[1] - self._y_center) // self.unit_length

    def getXY(self, xy):
        """cartesian (x, y) to pygame (x, y)"""
        return (self.getX(xy[0]), self.getX(xy[1]))

    def getX(self, x):
        """cartesian x to pygame x"""
        return self._x_center + x * self.unit_length

    def getY(self, y):
        """cartesian y to pygame y"""
        return self._y_center - y * self.unit_length

    def toXY(self, center: tuple):
        """pygame (x, y) to cartesian (x, y)"""
        return (self.toX(center[0]), self.toY(center[1]))

    def toX(self, x):
        """pygame x to cartesian x"""
        return (x - self._x_center) / self.unit_length

    def toY(self, y):
        """pygame y to cartesian y"""
        return (self._y_center - y) / self.unit_length

    def createVector(self, x, y):
        """Return a vector object parented by current plane instance"""
        return vector(self, x, y)

    def createRandomVector(self):
        """Return a random vector object parented by current plane instance"""
        return vector(self).random()


class vector:

    """
    #TODO
    """

    def __init__(self, space: plane, x=1, y=0,
                 limit_axes: bool = True) -> None:
        if x == y == 0:
            LOG('Created NULL vector!', WARNING, log=True)
        self.space = space
        self.length_max = max(self.space.x_max, self.space.y_max)
        self.length_min = 1
        self.__limit = limit_axes
        if self.__limit:
            self.__x = scalar(x, (-self.length_max, self.length_max))
            self.__y = scalar(y, (-self.length_max, self.length_max))
        else:
            self.__x = scalar(x)
            self.__y = scalar(y)

    def __add__(self, o):
        if o > 0:
            if self.__limit and self.length + o <= self.length_max:
                self.x += o * math.cos(self.direction)
                self.y += o * math.sin(self.direction)
            elif not self.__limit:
                self.x += o * math.cos(self.direction)
                self.y += o * math.sin(self.direction)
        elif o < 0:
            self.__sub__(abs(o))
        return self

    def __sub__(self, o):
        if o > 0:
            if o < self.length - 1:
                self.x -= o * math.cos(self.direction)
                self.y -= o * math.sin(self.direction)
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

    def __truediv__(self, _):
        raise Exception("Use multiplication instead :)")

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
            self.x = math.cos(self.direction) * xy
            self.y = math.sin(self.direction) * xy

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
        return math.sqrt(self.x**2 + self.y**2)

    @length.setter
    def length(self, o):
        if isinstance(o, (float, int)):
            a = self.direction
            if self.__limit:
                if self.length_min <= o <= self.length_max:
                    self.x = math.cos(a) * o
                    self.y = math.sin(a) * o
            else:
                if self.length_min <= o:
                    self.x = math.cos(a) * o
                    self.y = math.sin(a) * o
        raise TypeError(f"int, float required. Got {type(o)}")

    @property
    def LENGTH(self):
        """Return length in pygame coordinate system"""
        return math.sqrt(self.X**2 + self.Y**2)

    @property
    def direction(self):
        """Return angle from X axis in radians"""
        return math.atan2(self.y, self.x)

    @direction.setter
    def dircetion(self, o):
        if isinstance(o, (float, int)):
            lng = self.length
            self.x = math.cos(o) * lng
            self.y = math.sin(o) * lng
        raise TypeError(f"int, float required. Got {type(o)}")

    def rotate(self, rad):
        """
        Possitive values for counter-clock-wise,
        Negative values for clock-wise rotation
        """
        _x = self.x
        _y = self.y
        self.x = _x * math.cos(rad) - _y * math.sin(rad)
        self.y = _x * math.sin(rad) + _y * math.cos(rad)

    def random(self):
        """Set vector head at random location"""
        self.x = (random.random() * 2 - 1) * self.space.x_max
        self.y = (random.random() * 2 - 1) * self.space.y_max
        return self

    def distance(self, xy) -> float:
        """Return distance of given vector from current vector"""
        if isinstance(xy, tuple):
            return math.sqrt((self.x - xy[0])**2 + (self.y - xy[1])**2)
        return math.sqrt((self.x - xy.x)**2 + (self.y - xy.y)**2)

    def angle(self, xy):
        """
        Return the angle between given vector/coordinate
        and current vector
        """
        if isinstance(xy, tuple):
            return math.atan2(xy[1], xy[0]) - self.direction
        return math.atan2(xy.y, xy.x) - self.direction

    def dot(self, vec):
        """
        Return 'DOT/SCALAR' product of given vector/coordinate
        and currrent vector
        """
        if isinstance(vec, tuple):
            return self.x * vec[0] + self.y * vec[1]
        return self.x * vec.x + self.y * vec.y

    def unit(self, scale=1) -> tuple:
        """Return unit length vector scaled by 'scale' in cartesian"""
        a = self.direction
        return (math.cos(a)*scale, math.sin(a)*scale)
