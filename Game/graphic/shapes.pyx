import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.math.core cimport pi
from libc.math cimport sqrt, atan2
import numpy as np
from pygame.draw import aalines, lines, polygon as poly


cdef class Shape:

    def __cinit__(self, *args, **kwargs):
        self.vertex_count = 0

    def __init__(self, CartesianPlane plane):
        self.window = plane.window
        self.plane = plane

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cpdef void rotate(self, double angle):
        cdef int i
        for i in range(self.vertex_count):
            (<Vector2d>self.vertices[i]).rotate(angle)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cpdef void scale(self, double factor):
        cdef int i
        cdef double v_len
        cdef double _min = (<Vector2d>self.vertices[0]).mag()
        cdef double _max = _min
        for i in range(self.vertex_count):
            v_len = (<Vector2d>self.vertices[i]).mag()
            if v_len > _max:
                _max = v_len
            elif v_len < _min:
                _min = v_len
        if factor > 1:
            # TODO max len check
            if ((_max * factor) <= self.vertices[0].max_length):
                for i in range(self.vertex_count):
                    (<Vector2d>self.vertices[i]).scale(factor)
        elif factor < 1:
            if _max * factor >= self.vertices[0].min_length:
                for i in range(self.vertex_count):
                    (<Vector2d>self.vertices[i]).scale(factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    def show(self, color, show_vertex=False):
        cdef int i
        cdef list heads = []
        if show_vertex:
            # self.position_vec.show()
            for i in range(self.vertex_count):
                self.vertices[i].show((0, 0, 0))
                heads.append((<Vector2d>self.vertices[i]).get_HEAD())
        else:
            for i in range(self.vertex_count):
                heads.append((<Vector2d>self.vertices[i]).get_HEAD())
        aalines(self.window, color, True, heads)
        # poly(self.window, color, heads)


cdef class Rectangle(Shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane, (double, double) size):
        super().__init__(plane)

        self.vertex_count = 4

        cdef double length = sqrt((size[0]//2)**2 + (size[1]//2)**2)

        cdef list vers = []
        cdef int i
        cdef double angle[4]
        cdef double a1 = atan2(size[1], size[0])
        cdef double a2 = pi - a1
        angle[:] = [a1, a2, -a2, -a1]

        for i in range(self.vertex_count):
            vers.append(Vector2d(self.plane, length, 0, self.plane.window_size[0]))
            vers[-1].rotate(angle[i])

        self.vertices = np.array(vers, dtype=Vector2d)


cdef class Triangle(Shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane, (double, double, double) size):
        super().__init__(plane)

        self.vertex_count = 3

        cdef list vers = []
        cdef int i

        for i in range(self.vertex_count):
            vers.append(Vector2d(self.plane, size[i], 0, self.plane.window_size[0]))
            vers[-1].rotate(pi/2 + 2*pi/3 * i)

        self.vertices = np.array(vers, dtype=Vector2d)


cdef class Polygon(Shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane, tuple size):
        super(Polygon, self).__init__(plane)

        self.vertex_count = size.__len__()

        if self.vertex_count < 2:
            raise ValueError("Wrong vertex_count, The minimum is 2")

        cdef list vers = []
        cdef int i

        for i in range(self.vertex_count):
            # TODO
            vers.append(Vector2d(self.plane, size[i], 0, self.plane.window_size[0]))
            vers[-1].rotate(pi/2 + 2*pi/self.vertex_count * i)

        self.vertices = np.array(vers, dtype=Vector2d)
