import cython
from pygame.draw import lines, line, aaline
from Game.math.core cimport scalar, point2d, vector2d
from libc.math cimport floor
from random import random


@cython.optimize.unpack_method_calls(False)
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
        self.center = (self.parent_vector.headXY if self.parent_vector
                        else point2d(floor(self.window_size[0] / 2), floor(self.window_size[1] / 2)))
        self.set_limit()

    @property
    def X(self):
        return self.center.x.num

    @X.setter
    def X(self, o):
        raise NotImplementedError

    @property
    def Y(self):
        return self.center.y.num

    @Y.setter
    def Y(self, o):
        raise NotImplementedError

    @property
    def CENTER(self):
        return (self.center.x.num, self.center.y.num)

    @CENTER.setter
    def CENTER(self, o):
        raise NotImplementedError

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

    @cython.optimize.unpack_method_calls(False)
    def show(self):
        # draw x axis
        line(self.window, (255, 0, 0), (self.center.x.num, self.center.y.num),
             (self.center.x.num, self.center.y.num-20), 2)
        # draw y axis
        line(self.window, (0, 255, 0), (self.center.x.num, self.center.y.num),
             (self.center.x.num+20, self.center.y.num), 2)

    cpdef double to_X(self, double x):
        return self.center.x.num + x * self.unit_length

    cpdef double to_Y(self, double y):
        return self.center.y.num - y * self.unit_length

    cpdef (double, double) to_XY(self, (double, double) xy):
        return (self.center.x.num + xy[0] * self.unit_length, self.center.y.num - xy[1] * self.unit_length)

    @cython.cdivision(True)
    cpdef double to_x(self, double X):
        return (X - self.center.x.num) / self.unit_length

    @cython.cdivision(True)
    cpdef double to_y(self, double Y):
        return (self.center.y.num - Y) / self.unit_length

    @cython.cdivision(True)
    cpdef (double, double) to_xy(self, (double, double) XY):
        return ((XY[0] - self.center.x.num) / self.unit_length, (self.center.y.num - XY[1]) / self.unit_length)

    @cython.cdivision(True)
    cdef void set_limit(self):
        self.x_min = floor((self.center.x.num - self.window_size[0]) / self.unit_length)
        self.x_max = floor((self.window_size[0] - self.center.x.num) / self.unit_length)
        self.y_min = floor((self.center.y.num - self.window_size[1]) / self.unit_length)
        self.y_max = floor((self.window_size[1] - self.center.y.num) / self.unit_length)

    cdef (double, double) get_CENTER(self):
        return (self.center.x.num, self.center.y.num)

    cdef double get_X(self):
        return self.center.x.num

    cdef double get_Y(self):
        return self.center.y.num


@cython.optimize.unpack_method_calls(False)
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

    def __repr__(self):
        return f'X:{self.X}, Y:{self.Y} - x:{self.head.x}, y:{self.head.y}'

    @property
    def X(self):
        return self.plane.to_X(self.head.x.num)

    @property
    def Y(self):
        return self.plane.to_Y(self.head.y.num)

    @property
    def HEAD(self):
        return (self.plane.to_X(self.head.x.num), self.plane.to_Y(self.head.y.num))

    @property
    def TAIL(self):
        return (self.plane.center.x.num, self.plane.center.y.num)

    @cython.nonecheck(False)
    @cython.optimize.unpack_method_calls(False)
    def show(self, color):
        aaline(self.window, color,
               (self.plane.center.x.num, self.plane.center.y.num),
               (self.plane.to_XY(self.head.get_xy())))

    def unit(self, double scale=1, bint vector=True):
        cdef (double, double) xy = self.unit_vector(scale)
        if vector:
            return Vector2d(self.plane, xy[0], xy[1], self.max_length, self.min_length)
        return xy

    def normal(self, double scale=1, bint vector=True):
        cdef (double, double) xy = self.normal_vector(scale)
        if vector:
            return Vector2d(self.plane, xy[0], xy[1], self.max_length, self.min_length)
        return xy

    # @cython.optimize.unpack_method_calls(False)
    cpdef void random(self):
        # TODO Fix null vector creation
        cdef double r1 = random()
        cdef double r2 = random()
        if self.max_length:
            self.head.x.num = (r1 * 2 - 1) * self.max_length
            self.head.y.num = (r2 * 2 - 1) * self.max_length
        else:
            self.head.x.num = (r1 * 2 - 1) * self.plane.x_max
            self.head.y.num = (r2 * 2 - 1) * self.plane.y_max
        self.update()

    cdef (double, double) get_HEAD(self):
        return (self.plane.to_X(self.head.x.num), self.plane.to_Y(self.head.y.num))

    cdef (double, double) get_TAIL(self):
        return (self.plane.to_X(self.tail.x.num), self.plane.to_Y(self.tail.y.num))

    cdef void update(self):
        self.headXY.set_xy(self.plane.to_XY(self.head.get_xy()))
