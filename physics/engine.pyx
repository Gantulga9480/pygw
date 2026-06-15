import cython
from ..graphic.cartesian cimport CartesianPlane
from .body cimport Body, STATIC, FREE
from .collision cimport collision

@cython.optimize.unpack_method_calls(False)
cdef class EnginePolygon:

    cdef list bodies
    cdef collision collider

    def __init__(self, CartesianPlane plane, list bodies):
        self.bodies = bodies
        self.collider = collision(plane)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    def step(self):
        cdef int n = len(self.bodies)
        cdef int i, j
        cdef Body b
        cdef Body o
        for i in range(n):
            b = self.bodies[i]
            b.step()
            if self.bodies[i].type == STATIC:
                continue
            for j in range(n):
                if i == j or self.bodies[j].type == FREE or self.bodies[i].ID == self.bodies[j].ID:
                    continue
                o = self.bodies[j]
                if (self.bodies[i].radius + self.bodies[j].radius) >= (b.shape.plane.parent_vector.dist(o.shape.plane.parent_vector)):
                    self.collider.check(b, o)
