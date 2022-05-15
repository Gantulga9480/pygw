from Game.graphic.cartesian cimport CartesianPlane, Vector2d


cdef class shape:

    cdef readonly CartesianPlane plane
    cdef bint limit_vertex
    cdef Vector2d[:] vertices
    cdef int vertex_count

    cpdef void rotate(self, double angle)
    cpdef void scale(self, double factor)

cdef class rectangle(shape):
    pass

cdef class triangle(shape):
    pass

cdef class polygon(shape):
    pass
