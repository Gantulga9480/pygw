import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.physics.body cimport DYNAMIC, STATIC, object_body
from Game.math.util cimport LSI as line_segment_intersect


cdef class collision:

    def __cinit__(self, *args, **kwargs):
        self.friction_factor = 0.3

    def __init__(self, CartesianPlane plane) -> None:
        self.plane = plane

    cpdef void check(self, object_body b1, object_body b2):
        self.diagonal_intersect(b1, b2)

    cdef void resolve(self, object_body b1, object_body b2, double dx, double dy):
        if b1.body_type == DYNAMIC and b2.body_type == DYNAMIC:
            b1.velocity.scale(self.friction_factor)
            b2.velocity.scale(self.friction_factor)
            b1.shape.plane.parent_vector.set_head((b1.shape.plane.parent_vector.head.x.num + -dx/2, b1.shape.plane.parent_vector.head.y.num + -dy/2))
            b2.shape.plane.parent_vector.set_head((b2.shape.plane.parent_vector.head.x.num + dx/2, b2.shape.plane.parent_vector.head.y.num + dy/2))
        elif b1.body_type == DYNAMIC and b2.body_type == STATIC:
            b1.velocity.scale(self.friction_factor)
            b1.shape.plane.parent_vector.set_head((b1.shape.plane.parent_vector.head.x.num + -dx, b1.shape.plane.parent_vector.head.y.num + -dy))
        elif b1.body_type == STATIC and b2.body_type == DYNAMIC:
            b2.velocity.scale(self.friction_factor)
            b2.shape.plane.parent_vector.set_head((b2.shape.plane.parent_vector.head.x.num + dx, b2.shape.plane.parent_vector.head.y.num + dy))

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.cdivision(True)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cdef void diagonal_intersect(self, object_body body1, object_body body2):
        cdef int i, j
        cdef double dx = 0, dy = 0, val
        cdef (double, double) l1s
        cdef (double, double) l1e
        cdef (double, double) l2s
        cdef (double, double) l2e
        for i in range(body1.shape.vertex_count):
            # check for every vertex of first shape against ...
            l1s = self.plane.to_xy(body1.shape.plane.get_CENTER())
            l1e = self.plane.to_xy((<Vector2d>body1.shape.vertices[i]).get_HEAD())
            for j in range(body2.shape.vertex_count):
                # ... every edge of second shape
                l2s = self.plane.to_xy((<Vector2d>body2.shape.vertices[j]).get_HEAD())
                l2e = self.plane.to_xy((<Vector2d>body2.shape.vertices[(j+1)%body2.shape.vertex_count]).get_HEAD())
                # check these two line segments are intersecting or not
                val = 1 - line_segment_intersect(l1s[0], l1s[1], l1e[0], l1e[1], l2s[0], l2s[1], l2e[0], l2e[1])
                if val < 1:
                    dx += (l1e[0] - l1s[0]) * val
                    dy += (l1e[1] - l1s[1]) * val
        if dx != 0 or dy != 0:
            self.resolve(body1, body2, dx, dy)
