from Game.graphic.cartesian cimport CartesianPlane
from Game.physics.body cimport object_body


cdef class collision:

    cdef CartesianPlane plane
    cdef double friction_factor

    cpdef void check(self, object_body b1, object_body b2)
    cdef void resolve(self, object_body b1, object_body b2, double dx, double dy)
    cdef void diagonal_intersect(self, object_body body1, object_body body2)
