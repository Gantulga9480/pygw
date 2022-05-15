import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.math.core cimport pi
from libc.math cimport sqrt
import numpy as np
from pygame.draw import aalines, lines


cdef class shape:

    def __cinit__(self, *args, **kwargs):
        self.vertex_count = 0

    def __init__(self,
                 CartesianPlane plane,
                 bint limit_vertex=1):
        self.plane = plane
        self.limit_vertex = limit_vertex

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    cpdef void rotate(self, double angle):
        cdef int i
        for i in range(self.vertex_count):
            (<Vector2d>self.vertices[i]).rotate(angle)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    cpdef void scale(self, double factor):
        cdef int i
        cdef double v_len
        cdef double _max = 0
        cdef double _min = (<Vector2d>self.vertices[0]).length()
        cdef double max_len = self.vertices[0].max_length
        for i in range(self.vertex_count):
            v_len = (<Vector2d>self.vertices[i]).length()
            if v_len > _max:
                _max = v_len
            elif v_len < _min:
                _min = v_len
        if factor > 1:
            if not self.limit_vertex or ((_max * factor) <= max_len):
                for i in range(self.vertex_count):
                    (<Vector2d>self.vertices[i]).scale(factor)
        elif factor < 1:
            if _min * factor >= 1:
                for i in range(self.vertex_count):
                    (<Vector2d>self.vertices[i]).scale(factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    def show(self, window, color, width, show_vertex):
        cdef int i
        cdef list heads = []
            # self.position_vec.show(window)
        for i in range(self.vertex_count):
            if show_vertex:
                self.vertices[i].show(window, color, width)
            heads.append(self.vertices[i].HEAD)
        # if aa:
        aalines(window, color, True, heads, width)
        # else:
        #     pg.draw.lines(window, color, True,
        #                   [vertex.HEAD for vertex in self.vertices], width)


cdef class rectangle(shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 CartesianPlane plane,
                 (double, double) size,
                 bint limit_vertex=1):
        super().__init__(plane, limit_vertex)

        self.vertex_count = 4

        length = sqrt((size[0]//2)**2 + (size[1]//2)**2)

        cdef list vers = []
        cdef int i

        for i in range(4):
            vers.append(Vector2d(self.plane, length, 0, max_length=self.plane.x_max))
            vers[-1].rotate(pi/2 + pi/2 * i)

        self.vertices = np.array(vers, dtype=Vector2d)


cdef class triangle(shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 CartesianPlane plane,
                 (double, double) size,
                 bint limit_vertex=1):
        super().__init__(plane, limit_vertex)

        self.vertex_count = 3

        cdef list vers = []
        cdef int i

        for i in range(3):
            vers.append(Vector2d(self.plane, size[i], 0, max_length=self.plane.x_max))
            vers[-1].rotate(pi/2 + 2*pi/3 * i)

        self.vertices = np.array(vers, dtype=Vector2d)


cdef class polygon(shape):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 CartesianPlane plane,
                 int vertex_count=2,
                 double size=1,
                 bint limit_vertex=1):
        super(polygon, self).__init__(plane, limit_vertex)

        self.vertex_count = vertex_count

        if vertex_count < 2:
            raise ValueError("Wrong vertex_count, The minimum is 2")

        cdef list vers = []
        cdef int i

        for i in range(vertex_count):
            vers.append(Vector2d(self.plane, size, 0, max_length=self.plane.x_max))
            vers[-1].rotate(pi/2 + 2*pi/vertex_count * i)

        self.vertices = np.array(vers, dtype=Vector2d)
