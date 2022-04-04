import math
import random
from Game.utils import *


class scalar:

    def __init__(self, value=0, limits: tuple = None) -> None:
        if limits:
            self.has_limit = True
            self.min = limits[0]
            self.max = limits[1]
            if value < self.min:
                self.__num = self.min
            elif value > self.max:
                self.__num = self.max
            else:
                self.__num = value
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
                self.__num = o
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

    def __init__(self,
                 size,
                 unit_length,
                 parent=None) -> None:
        """
        params:
        size - (x ,y)
        unit_length - pixel count for 1 unit length in cartesian system
        """
        self.parent = parent
        self._size = size
        self.unit_length = unit_length
        self._x_dif = self._size[0] // 2
        self._y_dif = self._size[1] // 2
        self.set_limit()

    def __add__(self, o):
        if self.unit_length + o <= self._size[0] or \
                self.unit_length + o <= self._size[1]:
            self.unit_length += o
        return self

    def __sub__(self, o):
        self._x_dif -= o
        self._y_dif -= o
        return self

    def __mul__(self, o):
        if self.unit_length * o <= self._size[0] or \
                self.unit_length * o <= self._size[1]:
            self.unit_length *= o
        return self

    def __truediv__(self, o):
        if self.unit_length // o >= 1:
            self.unit_length //= o
        return self

    @property
    def X(self):
        return self._x_dif

    @X.setter
    def X(self, o):
        if 0 <= o <= self._size[0]:
            self._x_dif = o
        else:
            if o > 0:
                self._x_dif = self._size[0]
            else:
                self._x_dif = 0

    @property
    def Y(self):
        return self._y_dif

    @Y.setter
    def Y(self, o):
        if 0 <= o <= self._size[1]:
            self._y_dif = o
        else:
            if o > 0:
                self._y_dif = self._size[1]
            else:
                self._y_dif = 0

    @property
    def XY(self):
        """(x, y) in pygame coordinate system"""
        return (self.X, self.Y)

    @XY.setter
    def XY(self, pos):
        self.X = pos[0]
        self.Y = pos[1]

    def set_limit(self):
        self.x_lim = [(self._x_dif - self._size[0]) // self.unit_length,
                      (self._size[0] - self._x_dif) // self.unit_length]
        self.y_lim = [(self._y_dif - self._size[1]) // self.unit_length,
                      (self._size[1] - self._y_dif) // self.unit_length]

    def getXY(self, xy):
        """Retrun cartesian (x, y) in pygame coordinate system"""
        return (self.getX(xy[0]), self.getX(xy[1]))

    def getX(self, x):
        """Retrun cartesian x in pygame coordinate system"""
        return self._x_dif + x * self.unit_length

    def getY(self, y):
        """Return cartesian y in pygame coordinate system"""
        return self._y_dif - y * self.unit_length

    def toXY(self, center: tuple):
        """Return pygame (x, y) in cartesian coordinate system"""
        return (self.toX(center[0]), self.toY(center[1]))

    def toX(self, x):
        """Return pygame x in cartesian coordinate system"""
        return (x - self._x_dif) / self.unit_length

    def toY(self, y):
        """Return pygame y in cartesian coordinate system"""
        return (self._y_dif - y) / self.unit_length

    def vector(self, x, y):
        """Return a vector object parented by current plane instance"""
        return vector(self, x, y)

    def rand_vector(self):
        """Return a random vector object parented by current plane instance"""
        return vector(self).random()


class vector:

    """
    Arithmetic operations with vector are limited by (length_min, length_max).
    Directly setting vector position using individual properties (x, y),
    (X, Y) or (xy, XY) has a limit of parent plane size max(x_lim, y_lim) in
    both axis, including negative sides.
    """

    def __init__(self, space: plane, x=0, y=0) -> None:
        if x == y == 0:
            LOG('Created NULL vector!', WARNING, log=True)
        self.space = space
        self.length_max = max(self.space.x_lim[1], self.space.y_lim[1])
        self.length_min = 0
        self.__x = scalar(x, (-self.length_max, self.length_max))
        self.__y = scalar(y, (-self.length_max, self.length_max))
        self.__last_dir = 0

    def __add__(self, o):
        self.x += o * math.cos(self.direction)
        self.y += o * math.sin(self.direction)
        return self

    def __sub__(self, num):
        if abs(num) < self.length:
            self.x -= num * math.cos(self.direction)
            self.y -= num * math.sin(self.direction)
        else:
            self.x = 0
            self.y = 0
        return self

    def __mul__(self, factor):
        """
        Since multiplying by 1 has no effect, ommited factor of 1,
        Ommited negative values. For rotating use rotate method.
        """
        if factor > 1 and self.length < self.length_max:
            if self.length == 0:
                self.x = 1 * math.cos(self.__last_dir)
                self.y = 1 * math.sin(self.__last_dir)
            else:
                self.x *= factor
                self.y *= factor
        elif 0 <= factor < 1 and self.length > self.length_min:
            self.x *= factor
            self.y *= factor
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

    @property
    def direction(self):
        """Return angle from OX in radians"""
        d = math.atan2(self.y, self.x)
        if d != 0:
            self.__last_dir = d
        return d

    def rotate(self, rad):
        """
        Possitive values for counter-clock-wise,
        negative values for clock-wise rotation
        """
        _x = self.x
        _y = self.y
        self.x = _x * math.cos(rad) - _y * math.sin(rad)
        self.y = _x * math.sin(rad) + _y * math.cos(rad)

    def random(self):
        """Set vector at random location"""
        self.x = (random.random() * 2 - 1) * self.length_max
        self.y = (random.random() * 2 - 1) * self.length_max
        return self

    def distance(self, xy) -> float:
        """Return distance of given vector from current vector"""
        if isinstance(xy, tuple):
            return math.sqrt((self.x - xy[0])**2 + (self.y - xy[1])**2)
        return math.sqrt((self.x - xy.x)**2 + (self.y - xy.y)**2)

    def angle(self, xy):
        if isinstance(xy, tuple):
            return math.atan2(xy[1], xy[0]) - self.direction
        return math.atan2(xy.y, xy.x) - self.direction

    def dot(self, vec):
        if isinstance(vec, tuple):
            return self.x * vec[0] + self.y * vec[1]
        return self.x * vec.x + self.y * vec.y
