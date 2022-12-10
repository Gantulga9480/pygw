import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport Shape
from Game.math.core cimport point2d


cdef int STATIC, DYNAMIC, FREE


cdef class Body:
    cdef public int type, id
    cdef public double radius
    cdef public double friction_coef
    cdef public double drag_coef
    cdef public Shape shape
    cdef public Vector2d velocity
    cdef bint is_attached
    cdef bint is_following_dir
    cdef Body parent_body

    cpdef void step(self)
    cpdef void rotate(self, double angle)
    cpdef void scale(self, double factor)
    cpdef (double, double) position(self)
    cpdef double direction(self)
    cpdef double speed(self)
    cpdef void attach(self, Body o, bint follow_dir)
    cpdef void detach(self, Body o)
    cdef void USR_step(self)
    cdef void USR_resolve_collision(self, Body o, (double, double) dxy)
    cdef void USR_resolve_collision_point(self, double dx, double dy)

cdef class FreeBody(Body):
    cpdef void accelerate(self, double speed)

cdef class StaticBody(Body):
    pass

cdef class DynamicBody(Body):
    cpdef void accelerate(self, double speed)

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

cdef class FreePolygonBody(FreeBody):
    pass

cdef class Ray(FreeBody):
    cdef readonly double x
    cdef readonly double y
    cpdef void reset(self)
