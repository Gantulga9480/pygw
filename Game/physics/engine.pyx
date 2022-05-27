import cython
from Game.graphic.cartesian cimport CartesianPlane
from Game.physics.body cimport object_body, DYNAMIC, STATIC
from Game.physics.collision cimport collision_detector
import numpy as np
from pygame.draw import aalines
from random import random


cdef class Engine:

    cdef object_body[:] bodies
    cdef CartesianPlane plane
    cdef collision_detector collider

    def __init__(self, CartesianPlane plane, object_body[:] bodies):
        self.plane = plane
        self.bodies = bodies
        self.collider = collision_detector(plane)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    @cython.initializedcheck(False)
    def step(self):
        cdef int n = self.bodies.shape[0]
        cdef int i, j
        cdef double r

        for i in range(n):
            if self.bodies[i].type == DYNAMIC:
                r = random()
                if r > 0.5:
                    (<object_body>self.bodies[i]).accel(0.01)
                else:
                    (<object_body>self.bodies[i]).stop(1/1.1)
                if r > 0.5:
                    (<object_body>self.bodies[i]).rotate(0.1)
                else:
                    (<object_body>self.bodies[i]).rotate(-0.1)
                (<object_body>self.bodies[i]).step()
            for j in range(n):
                if i != j:
                    if self.bodies[i].type != STATIC or self.bodies[j].type != STATIC:
                        if (self.bodies[i].radius + self.bodies[j].radius) >= ((<object_body>self.bodies[i]).shape.plane.parent_vector.distance_to((<object_body>self.bodies[j]).shape.plane.parent_vector)):
                            self.collider.check(<object_body>self.bodies[i], <object_body>self.bodies[j])
            (<object_body>self.bodies[i]).show((0, 0, 0))
