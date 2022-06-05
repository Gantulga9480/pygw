import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.physics.body cimport DYNAMIC, STATIC, object_body


cdef class collision_detector:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane plane) -> None:
        self.plane = plane

    cpdef void check(self, object_body b1, object_body b2):
        self.diagonal_intersect(b1, b2)

    cdef void static_resolve(self, object_body b1, object_body b2, double dx, double dy):
        cdef double factor = 0
        if b1.type == DYNAMIC and b2.type == DYNAMIC:
            b1.body.v.scale(factor)
            b2.body.v.scale(factor)
            b1.shape.plane.parent_vector.add_xy((-dx/2, -dy/2))
            b2.shape.plane.parent_vector.add_xy((dx/2, dy/2))
        elif b1.type == DYNAMIC and b2.type == STATIC:
            b1.body.v.scale(factor)
            b1.shape.plane.parent_vector.add_xy((-dx, -dy))
        elif b1.type == STATIC and b2.type == DYNAMIC:
            b2.body.v.scale(factor)
            b2.shape.plane.parent_vector.add_xy((dx, dy))

    @cython.cdivision(True)
    cdef double line_segment_intersect(self, double p0x, double p0y, double p1x, double p1y, double p2x, double p2y, double p3x, double p3y):
        cdef double s10_x = p1x - p0x
        cdef double s10_y = p1y - p0y
        cdef double s32_x = p3x - p2x
        cdef double s32_y = p3y - p2y
        cdef double denom = s10_x * s32_y - s32_x * s10_y
        if denom == 0:
            return 0  # collinear
        cdef double denom_is_positive = denom > 0
        cdef double s02_x = p0x - p2x
        cdef double s02_y = p0y - p2y
        cdef double s_numer = s10_x * s02_y - s10_y * s02_x
        if (s_numer < 0) == denom_is_positive:
            return 0  # no collision
        cdef double t_numer = s32_x * s02_y - s32_y * s02_x
        if (t_numer < 0) == denom_is_positive:
            return 0  # no collision
        if (s_numer > denom) == denom_is_positive or \
                (t_numer > denom) == denom_is_positive:
            return 0  # no collision
        # collision detected
        cdef double t = t_numer / denom
        # intersection_point = [p0[0] + (t * s10_x), p0[1] + (t * s10_y)]
        return 1-t

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.cdivision(True)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    cdef void diagonal_intersect(self, object_body body1, object_body body2):
        cdef object_body b1 = body1
        cdef object_body b2 = body2
        cdef int i, j
        cdef double dx, dy, val
        cdef (double, double) l1s
        cdef (double, double) l1e
        cdef (double, double) l2s
        cdef (double, double) l2e
        for i in range(2):
            if i == 1:
                b1 = body2
                b2 = body1
            dx = 0
            dy = 0
            for i in range(b1.shape.vertex_count):
                # check for every vertex of first shape against ...
                l1s = self.plane.to_xy(b1.shape.plane.get_CENTER())
                l1e = self.plane.to_xy((<Vector2d>b1.shape.vertices[i]).get_HEAD())
                for j in range(b2.shape.vertex_count):
                    # ... every edge of second shape
                    l2s = self.plane.to_xy((<Vector2d>b2.shape.vertices[j]).get_HEAD())
                    l2e = self.plane.to_xy((<Vector2d>b2.shape.vertices[(j+1)%b2.shape.vertex_count]).get_HEAD())
                    # check these two line segments are intersecting or not
                    val = self.line_segment_intersect(l1s[0], l1s[1], l1e[0], l1e[1], l2s[0], l2s[1], l2e[0], l2e[1])
                    if val > 0:
                        # points.append(self.plane.getXY(val[0]))
                        dx += (l1e[0] - l1s[0]) * val
                        dy += (l1e[1] - l1s[1]) * val
            if dx != 0 or dy != 0:
                self.static_resolve(b1, b2, dx, dy)
        # return points
