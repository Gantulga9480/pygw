import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport polygon, polygon_test


cdef int STATIC, DYNAMIC


cdef class body_dynamics:

    cdef double radius, factor
    cdef Vector2d acceleration, velocity

    cdef void react(self, Vector2d pos)

cdef class base_body(polygon):

    cdef readonly int type, id
    cdef body_dynamics body
    cdef double radius

    cpdef void step(self)
    cpdef void accel(self, double factor)
    cpdef void stop(self, double factor)
    cpdef void rotate(self, double angle)

cdef class base_body_test(polygon_test):

    cdef readonly int type, id
    cdef body_dynamics body
    cdef double radius

    cpdef void step(self)
    cpdef void accel(self, double factor)
    cpdef void stop(self, double factor)
    cpdef void rotate(self, double angle)
