import cython
from pygame.draw import lines, line, aaline
from Game.math.core cimport scalar, point2d, vector2d
from libc.math cimport floor
from random import random


cdef class CartesianPlane:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 (double, double) window_size,
                 double unit_length,
                 Vector2d parent_vector=None,
                 bint set_limit=1,
                 bint logging=1):
        if unit_length <= 0:
            raise ValueError("Wrong unit length")
        self.window_size = window_size
        self.unit_length = unit_length
        self.parent_vector = parent_vector
        self.logging = logging
        if self.parent_vector is not None:
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
        if self.parent_vector is not None:
            self.window_size = self.parent_vector.plane.window_size

    @property
    def X(self):
        return self._center._x._num

    @X.setter
    def X(self, o):
        ...

    @property
    def Y(self):
        return self._center._y._num

    @Y.setter
    def Y(self, o):
        ...

    @property
    def CENTER(self):
        return (self._center._x._num, self._center._y._num)

    @CENTER.setter
    def CENTER(self, o):
        ...

    @property
    def shape(self):
        return (self.x_min, self.x_max, self.y_min, self.y_max)

    def createVector(self,
                     double x=1,
                     double y=0,
                     double max_length=0,
                     double min_length=1,
                     bint set_limit=0):
        return Vector2d(self, x, y, max_length, min_length, set_limit)

    def createRandomVector(self,
                           double max_length=0,
                           double min_length=1,
                           bint set_limit=0):
        vec = Vector2d(self, 1, 0, max_length, min_length, set_limit)
        vec.random()
        return vec

    def show(self, window, color, width):
        lines(window, color, False,
              [(self._center._x._num, self._center._y._num-20),
              (self._center._x._num, self._center._y._num),
              (self._center._x._num+20, self._center._y._num)],
              width)

    cpdef double get_X(self, double x):
        return self._center._x._num + x * self.unit_length

    cpdef double get_Y(self, double y):
        return self._center._y._num - y * self.unit_length

    cpdef (double, double) get_XY(self, (double, double) xy):
        return (self._center._x._num + xy[0] * self.unit_length, self._center._y._num - xy[1] * self.unit_length)

    @cython.cdivision(True)
    cpdef double to_x(self, double X):
        return (X - self._center._x._num) / self.unit_length

    @cython.cdivision(True)
    cpdef double to_y(self, double Y):
        return (self._center._y._num - Y) / self.unit_length

    @cython.cdivision(True)
    cpdef (double, double) to_xy(self, (double, double) XY):
        return ((XY[0] - self._center._x._num) / self.unit_length, (self._center._y._num - XY[1]) / self.unit_length)

    cdef (double, double) get_CENTER(self):
        return (self._center._x._num, self._center._y._num)

    @cython.cdivision(True)
    cdef void set_limit(self):
        self.x_min = floor((self._center._x._num - self.window_size[0]) / self.unit_length)
        self.x_max = floor((self.window_size[0] - self._center._x._num) / self.unit_length)
        self.y_min = floor((self._center._y._num - self.window_size[1]) / self.unit_length)
        self.y_max = floor((self.window_size[1] - self._center._y._num) / self.unit_length)


cdef class Vector2d(vector2d):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 CartesianPlane plane,
                 double x=1,
                 double y=0,
                 double max_length=0,
                 double min_length=1,
                 bint set_limit=0):
        self.plane = plane
        self.headXY = point2d(0, 0)
        self.is_limited = set_limit
        if set_limit:
            super().__init__(x, y,
                             (-self.plane.x_max, self.plane.x_max),
                             (-self.plane.y_max, self.plane.y_max),
                             max_length, min_length)
        else:
            super().__init__(x, y, (0, 0), (0, 0), max_length, min_length)

    @property
    def X(self):
        return self.plane.get_X(self._head._x._num)

    @property
    def Y(self):
        return self.plane.get_Y(self._head._y._num)

    @property
    def HEAD(self):
        return (self.plane.get_X(self._head._x._num), self.plane.get_Y(self._head._y._num))

    @property
    def TAIL(self):
        return (self.plane._center._x._num, self.plane._center._y._num)

    @cython.nonecheck(False)
    def show(self, window, color, width):
        aaline(window, color,
               (self.plane._center._x._num, self.plane._center._y._num),
               (self.plane.get_X(self._head._x._num), self.plane.get_Y(self._head._y._num)),
               width)

    def unit(self, scale=1, vector=True):
        xy = super().unit(scale, False)
        if vector:
            return Vector2d(self.plane,
                            xy[0], xy[1],
                            self.max_length, self.min_length, self.is_limited)
        return xy

    def normal(self, scale=1, vector=True):
        xy = super().normal(scale, False)
        if vector:
            return Vector2d(self.plane,
                            xy[0], xy[1],
                            self.max_length, self.min_length, self.is_limited)
        return xy

    @cython.cdivision(True)
    cpdef void random(self):
        self._head._x._num = (random() * 2 - 1) * self.plane.x_max
        self._head._y._num = (random() * 2 - 1) * self.plane.y_max
        self.update()

    cdef (double, double) get_HEAD(self):
        return (self.plane.get_X(self._head._x._num), self.plane.get_Y(self._head._y._num))

    cdef void update(self):
        self.headXY._x._num = self.plane.get_X(self._head._x._num)
        self.headXY._y._num = self.plane.get_Y(self._head._y._num)
