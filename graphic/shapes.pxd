from .cartesian cimport CartesianPlane, Vector2d


cdef class Shape:

    cdef readonly CartesianPlane plane
    cdef readonly int vertex_count
    cdef readonly Vector2d[:] vertices
    cdef public color

    cpdef void rotate(self, double angle)
    cpdef void scale(self, double factor)
    cdef void sync_shape(self)

cdef class Line(Shape):
    pass

cdef class Rectangle(Shape):
    pass

cdef class Triangle(Shape):
    pass

cdef class Polygon(Shape):
    pass