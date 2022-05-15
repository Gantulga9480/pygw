import cython
from Game.graphic.cartesian cimport CartesianPlane
from Game.physics.body cimport base_body, DYNAMIC, STATIC
from Game.physics.collision cimport collision_detector
import numpy as np


cdef class Engine:

    cdef base_body[:] bodies
    cdef CartesianPlane plane
    cdef collision_detector col

    def __init__(self, CartesianPlane plane, base_body[:] bodies):
        self.bodies = bodies
        self.plane = plane
        self.col = collision_detector(plane)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    def step(self):
        cdef int n = self.bodies.shape[0]
        cdef int i, j

        for i in range(n):
            if self.bodies[i].type == DYNAMIC:
                (<base_body>self.bodies[i]).step()
            for j in range(n):
                if i != j:
                    if self.bodies[i].type != STATIC or self.bodies[j].type != STATIC:
                        if (self.bodies[i].radius + self.bodies[j].radius) >= ((<base_body>self.bodies[i]).plane.parent_vector.distance_to((<base_body>self.bodies[j]).plane.parent_vector)):
                            self.col.check(<base_body>self.bodies[i], <base_body>self.bodies[j])
