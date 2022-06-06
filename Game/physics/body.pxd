import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport Shape


cdef int STATIC, DYNAMIC


cdef class object_dynamics:

    cdef double radius, factor
    cdef Vector2d v

    cdef void react(self, Vector2d pos)

cdef class object_body:

    cdef readonly int type, id
    cdef object_dynamics body
    cdef Shape shape
    cdef double radius

    cpdef void step(self)
    cpdef void accelerate(self, double factor)
    cpdef void stop(self, double factor)
    cpdef void rotate(self, double angle)
    cpdef void scale(self, double factor)

cdef class PolygonBody(object_body):
    pass

cdef class RectBody(object_body):
    pass

cdef class TriangleBody(object_body):
    pass
