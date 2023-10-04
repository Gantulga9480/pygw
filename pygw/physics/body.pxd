import cython
from ..graphic.cartesian cimport CartesianPlane, Vector2d
from ..graphic.shapes cimport Shape
from ..math.core cimport point2d


cdef int STATIC, DYNAMIC, FREE


cdef class Body:
    cdef readonly int type, ID
    cdef readonly double radius
    cdef readonly double friction_coef
    cdef readonly double drag_coef
    cdef readonly Shape shape
    cdef readonly Vector2d velocity
    cdef readonly bint is_attached
    cdef readonly bint is_following_dir
    cdef Body parent_body

    cpdef void step(self)
    cpdef void rotate(self, double angle)
    cpdef void scale(self, double factor)
    cpdef (double, double) position(self)
    cpdef double direction(self)
    cpdef double speed(self)
    cpdef void attach(self, Body o, bint follow_dir)
    cpdef void detach(self, Body o)
    cdef void onStep(self)
    cdef void onCollision(self, Body o, (double, double) dxy)
    cdef void onCollisionPoint(self, double dx, double dy)

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
