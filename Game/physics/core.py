from math import cos, sin, dist, atan2
from Game.utils import *


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


class vector2d:

    def __init__(self, x, y,
                 x_lim=None, y_lim=None,
                 max_length=None, min_length=1) -> None:
        self._head: point2d = point2d(x, y, x_lim, y_lim)
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.__limted = True if max_length else False
        self.max_length = max_length
        self.min_length = min_length
        self.update()

    def add(self, o):
        if o > 0:
            if self.__limted and (self.length() + o <= self.max_length):
                a = self.direction()
                self._head.x.value += o * cos(a)
                self._head.y.value += o * sin(a)
            elif not self.__limted:
                a = self.direction()
                self._head.x.value += o * cos(a)
                self._head.y.value += o * sin(a)
            self.update()
        elif o < 0:
            self.sub(abs(o))

    def sub(self, o):
        if o > 0:
            if o < self.length() - 1:
                a = self.direction()
                self._head.x.value -= o * cos(a)
                self._head.y.value -= o * sin(a)
            else:
                self._head.x.value, self._head.y.value = self.unit().head
            self.update()
        elif o < 0:
            self.add(abs(o))

    def scale(self, factor):
        if self.length() * factor > self.min_length:
            if self.__limted:
                if self.length() * factor < self.max_length:
                    self._head.x.value *= factor
                    self._head.y.value *= factor
                else:
                    self._head.x.value, self._head.y.value = \
                        self.unit(self.max_length)
            else:
                self._head.x.value *= factor
                self._head.y.value *= factor
        else:
            self._head.x.value, self._head.y.value = self.unit()._head.xy
        self.update()

    @property
    def x(self):
        """x coordinate in cartesian system"""
        return self._head.x.value

    @x.setter
    def x(self, x):
        """Set x in cartesian coordinate system"""
        if isinstance(x, (int, float)):
            self._head.x.value = x
        elif isinstance(x, scalar):
            self._head.x = x
        else:
            raise TypeError(f"Type  {type(x)} not supported")
        self.update()

    @property
    def y(self):
        """y coordinate in cartesian system"""
        return self._head.y.value

    @y.setter
    def y(self, y):
        """Set y coordinate in cartesian system"""
        if isinstance(y, (int, float)):
            self._head.y.value = y
        elif isinstance(y, scalar):
            self._head.y = y
        else:
            raise TypeError(f"Type  {type(y)} not supported")
        self.update()

    @property
    def head(self):
        """(x, y) values in cartesian coordinate system"""
        return (self._head.x.value, self._head.y.value)

    @head.setter
    def head(self, xy: tuple):
        """Set (x, y) for cartesian system using cartesian (x, y)"""
        if isinstance(xy, tuple):
            self._head.x.value = xy[0]
            self._head.y.value = xy[1]
        elif isinstance(xy, point2d):
            self._head = xy
        else:
            raise TypeError(f"Type  {type(xy)} not supported")
        self.update()

    @property
    def tail(self):
        return (0, 0)

    def rotate(self, rad):
        """
        Possitive values for counter-clock-wise,
        Negative values for clock-wise rotation
        """
        _x = self._head.x.value
        _y = self._head.y.value
        self._head.x.value = _x * cos(rad) - _y * sin(rad)
        self._head.y.value = _x * sin(rad) + _y * cos(rad)
        self.update()

    def update(self):
        ...

    def length(self):
        """Return length in cartesian coordinate system"""
        return dist((0, 0), (self._head.x.value, self._head.y.value))

    def direction(self):
        """Return angle from x axis in radians"""
        return atan2(self._head.y.value, self._head.x.value)

    def distance_to(self, xy) -> float:
        """Return distance of given vector from current vector in cartesian"""
        if isinstance(xy, tuple):
            return dist((0, 0),
                        ((self._head.x.value - xy[0]),
                         (self._head.y.value - xy[1])))
        elif isinstance(xy, vector2d):
            return dist((0, 0),
                        ((self._head.x.value - xy._head.x.value),
                         (self._head.y.value - xy._head.y.value)))
        elif isinstance(xy, point2d):
            return dist((0, 0),
                        ((self._head.x.value - xy.x.value),
                         (self._head.y.value - xy.y.value)))
        else:
            raise TypeError(f"Type  {type(xy)} not supported")

    def angle_between(self, xy):
        """
        Return the angle between given vector/coordinate
        and current vector in cartesian
        """
        if isinstance(xy, tuple):
            return atan2(xy[1], xy[0]) - self.direction()
        elif isinstance(xy, vector2d):
            return atan2(xy._head.y.value, xy._head.x.value) - self.direction()
        elif isinstance(xy, point2d):
            return atan2(xy.y.value, xy.x.value) - self.direction()
        else:
            raise TypeError(f"Type  {type(xy)} not supported")

    def unit(self, scale=1, toVector=True):
        """Return unit length vector scaled by 'scale' in cartesian"""
        a = self.direction()
        x = cos(a)*scale
        y = sin(a)*scale
        if toVector:
            return vector2d(x, y)
        return (x, y)

    def normal(self):
        """TODO"""
        return vector2d(-self._head.y.value, self._head.x.value)

    def dot(self, xy):
        """
        Return 'DOT/SCALAR' product of given vector/coordinate
        and currrent vector in cartesian
        """
        if isinstance(xy, vector2d):
            return self._head.x.value * xy._head.x.value + \
                self._head.y.value * xy._head.y.value
        elif isinstance(xy, tuple):
            return self._head.x.value * xy[0] + self._head.y.value * xy[1]
        elif isinstance(xy, point2d):
            return self._head.x.value * xy.x.value + \
                self._head.y.value * xy.y.value
        else:
            raise TypeError(f"Type  {type(xy)} not supported")


class Engine:

    def __init__(self) -> None:
        pass
