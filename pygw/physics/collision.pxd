from ..graphic.cartesian cimport CartesianPlane
from .body cimport Body


cdef class collision:

    cdef CartesianPlane plane

    cpdef void check(self, Body b1, Body b2)
    cdef void diagonal_intersect(self, Body body1, Body body2)
