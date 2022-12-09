import cython
from Game.graphic.cartesian cimport CartesianPlane
from Game.physics.body cimport object_body, STATIC, FREE
from Game.physics.collision cimport collision

@cython.optimize.unpack_method_calls(False)
cdef class EnginePolygon:

    cdef object_body[:] bodies
    cdef collision collider

    def __init__(self, CartesianPlane plane, object_body[:] bodies):
        self.bodies = bodies
        self.collider = collision(plane)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    def step(self):
        cdef int n = self.bodies.shape[0]
        cdef int i, j
        cdef (double, double) dxy
        # Check for every body ...
        for i in range(n):
            # Take one gentle step in environment
            (<object_body>self.bodies[i]).step()
            # ... Against every other body
            for j in range(n):
                # Will not check bodies against itself
                if i != j:
                    # Will not check STATIC body and against FREE body
                    if self.bodies[i].type != STATIC and self.bodies[j].type != FREE:
                        # Bodies that have same id will be skipped
                        if self.bodies[i].id != self.bodies[j].id:
                            # radius1 + radius2 >= distance between body2 and body1 means we have some work to do
                            if (self.bodies[i].radius + self.bodies[j].radius) >= ((<object_body>self.bodies[i]).shape.plane.parent_vector.distance_to((<object_body>self.bodies[j]).shape.plane.parent_vector)):
                                self.collider.check(<object_body>self.bodies[i], <object_body>self.bodies[j])
            # Throw body on to screen
            (<object_body>self.bodies[i]).show()
