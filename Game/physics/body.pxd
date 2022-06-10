import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport Shape


cdef int STATIC, DYNAMIC


cdef class object_body:
    cdef readonly int body_type, body_id
    cdef readonly double radius
    cdef Shape shape
    cdef Vector2d velocity

    cpdef void step(self)
    cpdef void rotate(self, double angle)
    cpdef void scale(self, double factor)
    cpdef (double, double) position(self)
    cpdef double speed(self)

cdef class StaticBody(object_body):
    pass

cdef class DynamicBody(object_body):
    cdef double max_speed
    cpdef void Accelerate(self, double factor)

cdef class DynamicPolygonBody(DynamicBody):
    pass

cdef class DynamicRectangleBody(DynamicBody):
    pass

cdef class DynamicTriangleBody(DynamicBody):
    pass

cdef class StaticPolygonBody(StaticBody):
    pass

cdef class StaticRectangleBody(StaticBody):
    pass

cdef class StaticTriangleBody(StaticBody):
    pass
