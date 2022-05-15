from Game.graphic.cartesian cimport CartesianPlane
from Game.physics.body cimport base_body


cdef class collision_detector:

    cdef CartesianPlane plane

    cpdef void check(self, base_body b1, base_body b2)
    cdef void static_resolve(self, base_body b1, base_body b2, double dx, double dy)
    cdef double line_segment_intersect(self, double p0x, double p0y, double p1x, double p1y, double p2x, double p2y, double p3x, double p3y)
    cdef void diagonal_intersect(self, base_body body1, base_body body2)
