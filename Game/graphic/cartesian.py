from math import dist
from Game.physics.core import scalar, point2d, vector2d
import pygame as pg
import random
from Game.utils import *
from Game.color import *


class CartesianPlane:

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
        self.parent_vector: Vector2d = parent_vector
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
    def CENTER(self):
        """center (X, Y) value in pixel"""
        return (self.__center.x.value, self.__center.y.value)

    @CENTER.setter
    def CENTER(self, XY):
        if isinstance(XY, tuple):
            self.__center.x.value = XY[0]
            self.__center.y.value = XY[1]
        elif isinstance(XY, point2d):
            self.__center = XY
        elif isinstance(XY, Vector2d):
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
        if isinstance(xy, (tuple, list)):
            return (self.getX(xy[0]), self.getY(xy[1]))
        if isinstance(xy, Vector2d):
            return (self.getX(xy.x), self.getY(xy.x))
        raise TypeError(f"Type  {type(xy)} not supported")

    def getX(self, x):
        """cartesian x to pygame X"""
        return self.__center.x.value + x * self.unit_length

    def getY(self, y):
        """cartesian y to pygame Y"""
        return self.__center.y.value - y * self.unit_length

    def toXY(self, XY):
        """pygame (X, Y) to cartesian (x, y)"""
        if isinstance(XY, (tuple, list)):
            return (self.toX(XY[0]), self.toY(XY[1]))
        if isinstance(XY, Vector2d):
            return (self.toX(XY.X), self.toY(XY.X))
        raise TypeError(f"Type  {type(XY)} not supported")

    def toX(self, X):
        """pygame X to cartesian x"""
        return (X - self.__center.x.value) / self.unit_length

    def toY(self, Y):
        """pygame Y to cartesian y"""
        return (self.__center.y.value - Y) / self.unit_length

    def createVector(self,
                     x=1, y=0,
                     max_length=None,
                     min_length=1,
                     set_limit=False):
        """Return a vector object parented by current plane instance"""
        return Vector2d(self, x, y, max_length, min_length, set_limit)

    def createRandomVector(self,
                           max_length=None,
                           min_length=1,
                           set_limit=False):
        """Return a random vector object parented by current plane instance"""
        vec = Vector2d(self,
                       max_length=max_length,
                       min_length=min_length,
                       set_limit=set_limit)
        vec.random()
        return vec

    def show(self, window, color=BLACK, width=1):
        pg.draw.lines(window, color, False,
                      [(self.__center.x.value, self.__center.y.value-20),
                       (self.__center.x.value, self.__center.y.value),
                       (self.__center.x.value+20, self.__center.y.value)],
                      width)


class Vector2d(vector2d):

    """
    #TODO
    """

    def __init__(self,
                 space: CartesianPlane,
                 x=1,
                 y=0,
                 max_length=None,
                 min_length=1,
                 set_limit: bool = False) -> None:
        if space.logging and (x == y == 0):
            LOG('Created NULL vector!', WARNING, logging=True)
        self.space = space
        self.headXY = point2d(0, 0)
        self.is_limited = set_limit
        if set_limit:
            super().__init__(x, y, (-self.space.x_max, self.space.x_max),
                                   (-self.space.y_max, self.space.y_max),
                             max_length, min_length)
        else:
            super().__init__(x, y, max_length=max_length,
                             min_length=min_length)

    @property
    def X(self):
        """X coordinate in pygame system"""
        return self.space.getX(self._head.x.value)

    @property
    def Y(self):
        """Y coordinate in pygame system"""
        return self.space.getY(self._head.y.value)

    @property
    def HEAD(self):
        """(x, y) values in pygame coordinate system"""
        return (self.X, self.Y)

    @property
    def TAIL(self):
        return self.space.CENTER

    @property
    def LENGTH(self):
        """Return length in pygame coordinate system"""
        return dist([0, 0], [self.X, self.Y])

    def random(self):
        """Set vector head at random location"""
        self._head.x.value = (random.random() * 2 - 1) * self.space.x_max
        self._head.y.value = (random.random() * 2 - 1) * self.space.y_max
        self.update()

    def show(self, window, color=BLACK, width=1, aa=False):
        if aa:
            pg.draw.aaline(window, color, self.TAIL, self.HEAD, width)
        else:
            pg.draw.line(window, color, self.TAIL, self.HEAD, width)

    def update(self):
        self.headXY.xy = (self.space.getX(self._head.x.value),
                          self.space.getY(self._head.y.value))

    def unit(self, scale=1, vector=True):
        xy = super().unit(scale, False)
        if vector:
            return Vector2d(self.space,
                            xy[0], xy[1],
                            self.max_length, self.min_length, self.is_limited)
        return xy

    def normal(self, scale=1, vector=True):
        xy = super().normal(scale, False)
        if vector:
            return Vector2d(self.space,
                            xy[0], xy[1],
                            self.max_length, self.min_length, self.is_limited)
        return xy
