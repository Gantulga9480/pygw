import cython
from pygame.draw import lines, line, aaline
from Game.math.core cimport scalar, point2d, vector2d
from libc.math cimport floor
from random import random


cdef class CartesianPlane:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 window,
                 (double, double) window_size,
                 Vector2d parent_vector=None,
                 double unit_length=1):
        if unit_length <= 0:
            raise ValueError("Wrong unit length")
        self.window = window
        self.window_size = window_size
        self.parent_vector = parent_vector
        self.unit_length = (unit_length if self.parent_vector is None
                            else self.parent_vector.plane.unit_length)
        self._center = (self.parent_vector.headXY if self.parent_vector
                        else point2d(floor(self.window_size[0] / 2), floor(self.window_size[1] / 2)))
        # if self.parent_vector is not None:
        #     self._center = self.parent_vector.headXY
        # else:
        #     self._center = point2d(floor(self.window_size[0] / 2), floor(self.window_size[1] / 2))
        self.set_limit()

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
                     double min_length=1):
        return Vector2d(self, x, y, max_length, min_length)

    def createRandomVector(self,
                           double max_length=0,
                           double min_length=1):
        vec = Vector2d(self, 1, 0, max_length, min_length)
        vec.random()
        return vec

    def show(self):
        # draw x axis
        line(self.window, (255, 0, 0), (self._center._x._num, self._center._y._num),
             (self._center._x._num, self._center._y._num-20), 2)
        # draw y axis
        line(self.window, (0, 255, 0), (self._center._x._num, self._center._y._num),
             (self._center._x._num+20, self._center._y._num), 2)

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
                 double min_length=1):
        self.window = plane.window
        self.plane = plane
        self.headXY = point2d(0, 0)
        super().__init__(x, y, max_length, min_length)

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
    def show(self, color):
        aaline(self.window, color,
               (self.plane._center._x._num, self.plane._center._y._num),
               (self.plane.get_X(self._head._x._num), self.plane.get_Y(self._head._y._num)))

    def unit(self, scale=1, vector=True):
        xy = super().unit(scale, False)
        if vector:
            return Vector2d(self.plane,
                            xy[0], xy[1], self.max_length, self.min_length)
        return xy

    def normal(self, scale=1, vector=True):
        xy = super().normal(scale, False)
        if vector:
            return Vector2d(self.plane,
                            xy[0], xy[1], self.max_length, self.min_length)
        return xy

    cpdef void random(self):
        # TODO Fix null vector creation
        if self.max_length:
            self._head._x._num = (random() * 2 - 1) * self.max_length
            self._head._y._num = (random() * 2 - 1) * self.max_length
        else:
            self._head._x._num = (random() * 2 - 1) * self.plane.x_max
            self._head._y._num = (random() * 2 - 1) * self.plane.y_max
        self.update()

    cdef (double, double) get_HEAD(self):
        return (self.plane.get_X(self._head._x._num), self.plane.get_Y(self._head._y._num))

    cdef void update(self):
        self.headXY._x._num = self.plane.get_X(self._head._x._num)
        self.headXY._y._num = self.plane.get_Y(self._head._y._num)
