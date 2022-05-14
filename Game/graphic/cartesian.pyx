import cython
import random
from pygame import draw
from Game.math.core cimport scalar, point2d, vector2d
from libc.math cimport floor


cdef class CartesianPlane:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 (double, double) window_size,
                 double unit_length,
                 Vector2d parent_vector=None,
                 bint set_limit=True,
                 bint logging=True):
        self.window_size = window_size
        self.unit_length = unit_length
        self.parent_vector = parent_vector
        self.logging = logging
        if self.parent_vector:
            self._center = self.parent_vector.headXY
        else:
            if set_limit:
                self._center = point2d(
                                       floor(self.window_size[0] / 2),
                                       floor(self.window_size[1] / 2),
                                       (0, self.window_size[0]),
                                       (0, self.window_size[1]))
            else:
                self._center = point2d(
                                       floor(self.window_size[0] / 2),
                                       floor(self.window_size[1] / 2))
        self.set_limit()
        if self.parent_vector:
            self.window_size = self.parent_vector.space.window_size

    @property
    def X(self):
        return self._center._x._num

    @X.setter
    def X(self, o):
        if isinstance(o, (int, float)):
            self._center.x = o
        elif isinstance(o, scalar):
            self._center.x = o
        else:
            raise TypeError(f"Type  {type(o)} not supported")

    @property
    def Y(self):
        """center Y value in pixel"""
        return self._center._y._num

    @Y.setter
    def Y(self, o):
        if isinstance(o, (int, float)):
            self._center.y = o
        if isinstance(o, scalar):
            self._center.y = o.value
        else:
            raise TypeError(f"Type  {type(o)} not supported")

    @property
    def CENTER(self):
        """center (X, Y) value in pixel"""
        return (self._center.x, self._center.y)

    @CENTER.setter
    def CENTER(self, XY):
        if isinstance(XY, tuple):
            self._center.x = XY[0]
            self._center.y = XY[1]
        elif isinstance(XY, point2d):
            self._center = XY
        elif isinstance(XY, Vector2d):
            self._center.x = XY.X
            self._center.y = XY.Y
        else:
            raise TypeError(f"Type  {type(XY)} not supported")


cdef class Vector2d(vector2d):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 CartesianPlane space,
                 double x=1,
                 double y=0,
                 double max_length=0,
                 double min_length=1,
                 bint set_limit=False):
        self.space = space
        self.headXY = point2d(0, 0)
        self.is_limited = set_limit
        if set_limit:
            super().__init__(x, y, (-10, 10), (-10, 10), max_length, min_length)
        else:
            super().__init__(x, y, None, None, max_length, min_length)
