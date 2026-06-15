import cython
from pygame.draw import aalines, aaline, polygon, line
from libc.math cimport sqrt, atan2
from ..math.core cimport pi
from .cartesian cimport CartesianPlane, Vector2d

@cython.optimize.unpack_method_calls(False)
cdef class Shape:

    def __cinit__(self, *args, **kwargs):
        self.vertex_count = 0
        self.color = (0, 0, 0)

    def __init__(self, CartesianPlane plane):
        self.plane = plane
        self.vertices = []

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cpdef void rotate(self, double angle):
        cdef int i
        cdef Vector2d v
        for i in range(self.vertex_count):
            v = self.vertices[i]
            v.rotate(angle)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cpdef void scale(self, double factor):
        cdef int i
        cdef double v_len
        cdef Vector2d v0, v
        v0 = self.vertices[0]
        cdef double _min = v0.mag()
        for i in range(self.vertex_count):
            v = self.vertices[i]
            v_len = v.mag()
            if v_len < _min:
                _min = v_len
        if factor > 1:
            for i in range(self.vertex_count):
                v = self.vertices[i]
                v.scale(factor)
        elif factor < 1:
            v0 = self.vertices[0]
            if _min * factor >= v0.min:
                for i in range(self.vertex_count):
                    v = self.vertices[i]
                    v.scale(factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    def show(self, show_vertex=False, width=1):
        cdef int i
        cdef list heads = []
        cdef Vector2d v
        if show_vertex:
            for i in range(self.vertex_count):
                v = self.vertices[i]
                v.show(self.color)
                heads.append(v._head.get_xy())
        else:
            for i in range(self.vertex_count):
                v = self.vertices[i]
                heads.append(v._head.get_xy())
        if width == 1:
            aalines(self.plane.window, self.color, True, heads)
        elif width > 1:
            polygon(self.plane.window, self.color, heads, width)
        else:
            polygon(self.plane.window, self.color, heads)

    def sync(self):
        self.sync_shape()

    cdef void sync_shape(self):
        cdef int i
        cdef Vector2d v
        for i in range(self.vertex_count):
            v = self.vertices[i]
            v.update()

@cython.optimize.unpack_method_calls(False)
cdef class Line(Shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane, double length):
        super().__init__(plane)

        self.vertex_count = 1
        self.vertices = [Vector2d(self.plane, length, 0, 0, 1)]

        self.sync_shape()

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cpdef void rotate(self, double angle):
        self.vertices[0].rotate(angle)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cpdef void scale(self, double factor):
        self.vertices[0].scale(factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    def show(self, show_vertex=False, width=1):
        if width == 1:
            aaline(self.plane.window, self.color, self.plane.origin.get_xy(), self.vertices[0]._head.get_xy())
        else:
            line(self.plane.window, self.color, self.plane.origin.get_xy(), self.vertices[0]._head.get_xy(), width)

@cython.optimize.unpack_method_calls(False)
cdef class Rectangle(Shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane, (double, double) shape):
        super().__init__(plane)

        self.vertex_count = 4

        cdef double length = sqrt((shape[0]/2.0)**2 + (shape[1]/2.0)**2)

        cdef list vers = []
        cdef int i
        cdef double angle[4]
        cdef double a1 = atan2(shape[1], shape[0])
        cdef double a2 = pi - a1
        angle[:] = [a1, a2, -a2, -a1]

        for i in range(self.vertex_count):
            vers.append(Vector2d(self.plane, length, 0, 0, 1))
            vers[-1].rotate(angle[i])

        self.vertices = vers

        self.sync_shape()

@cython.optimize.unpack_method_calls(False)
cdef class Triangle(Shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane, (double, double, double) shape):
        super().__init__(plane)

        self.vertex_count = 3

        cdef list vers = []
        cdef int i

        for i in range(self.vertex_count):
            vers.append(Vector2d(self.plane, shape[i], 0, 0, 1))
            vers[-1].rotate(pi/2 + 2*pi/3 * i)

        self.vertices = vers

        self.sync_shape()

@cython.optimize.unpack_method_calls(False)
cdef class Polygon(Shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane, tuple shape):
        super(Polygon, self).__init__(plane)

        self.vertex_count = len(shape)

        cdef list vers = []
        cdef int i

        for i in range(self.vertex_count):
            vers.append(Vector2d(self.plane, shape[i], 0, 0, 1))
            vers[-1].rotate(pi/2 + 2*pi/self.vertex_count * i)

        self.vertices = vers

        self.sync_shape()
