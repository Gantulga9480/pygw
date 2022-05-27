from Game.graphic.cartesian cimport CartesianPlane, Vector2d


cdef class Shape:

    cdef object window
    cdef readonly CartesianPlane plane
    cdef Vector2d[:] vertices
    cdef int vertex_count

    cpdef void rotate(self, double angle)
    cpdef void scale(self, double factor)

cdef class Rectangle(Shape):
    pass

cdef class Triangle(Shape):
    pass

cdef class Polygon(Shape):
    pass