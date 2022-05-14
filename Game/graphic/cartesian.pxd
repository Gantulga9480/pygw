from Game.math.core cimport point2d, vector2d


cdef class CartesianPlane:
    cdef (double, double) window_size
    cdef double unit_length
    cdef public Vector2d parent_vector
    cdef bint logging
    cdef point2d _center


cdef class Vector2d(vector2d):

    cdef CartesianPlane space
    cdef point2d headXY
    cdef bint is_limited
