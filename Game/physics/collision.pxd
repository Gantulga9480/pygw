from Game.graphic.cartesian cimport CartesianPlane
from Game.physics.body cimport object_body


cdef class collision_detector:

    cdef CartesianPlane plane

    cpdef void check(self, object_body b1, object_body b2)
    cdef void static_resolve(self, object_body b1, object_body b2, double dx, double dy)
    cdef double line_segment_intersect(self, double p0x, double p0y, double p1x, double p1y, double p2x, double p2y, double p3x, double p3y)
    cdef void diagonal_intersect(self, object_body body1, object_body body2)
