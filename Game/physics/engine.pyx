import cython
from Game.graphic.cartesian cimport CartesianPlane
from Game.physics.body cimport object_body, STATIC
from Game.physics.collision cimport collision
import numpy as np
from pygame.draw import aalines
from random import random


cdef class Engine:

    cdef object_body[:] bodies
    cdef CartesianPlane plane
    cdef collision collider

    def __init__(self, CartesianPlane plane, object_body[:] bodies):
        self.plane = plane
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
        for i in range(n):
            (<object_body>self.bodies[i]).step()
            for j in range(n):
                if i != j:
                    if self.bodies[i].type != STATIC:
                        if self.bodies[i].id != self.bodies[j].id:
                            if (self.bodies[i].radius + self.bodies[j].radius) >= ((<object_body>self.bodies[i]).shape.plane.parent_vector.distance_to((<object_body>self.bodies[j]).shape.plane.parent_vector)):
                                self.collider.check(<object_body>self.bodies[i], <object_body>self.bodies[j])
            (<object_body>self.bodies[i]).show((0, 0, 0))
