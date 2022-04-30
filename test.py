from Game.base import Game
from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import triangle, rectangle, polygon, shape
from Game.physics.body import *
from Game.physics.collision import LineIntersectCollision as LIC
from Game.color import BLACK, RED, GREEN, BLUE
import pygame as pg
import random
import math


class TestBody(static_body):

    def __init__(self,
                 parent_space: CartesianPlane,
                 vertex_count: int = 2,
                 size: float = 1.0,
                 limit_vertex: bool = True) -> None:
        self.shape = polygon(parent_space, vertex_count, size, limit_vertex)
        super().__init__()
        self.radius = size + 1

    def collision_resolver(self, body1, body2, displacement):
        ...


class Test(Game):

    def __init__(self, title: str = 'PyGameDemo',
                 width: int = 800, height: int = 800,
                 fps: int = 60, render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)

        self.plane = CartesianPlane((width, height), 1)
        self.collider = LIC(self.plane)

        self.bodies: list[TestBody] = []

        self.selected = 0
        self.num_shapes = 10

        for _ in range(self.num_shapes):
            n = random.randint(3, 6)
            vec = self.plane.createRandomVector()
            plane = CartesianPlane((50, 50), 1, vec)
            self.bodies.append(TestBody(plane, n, 50))

    def USR_eventHandler(self):
        for event in self.events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_q:
                    if self.selected > 0:
                        self.selected -= 1
                elif event.key == pg.K_e:
                    if self.selected < self.num_shapes - 1:
                        self.selected += 1
        if self.keys[pg.K_UP]:
            self.bodies[self.selected].plane.parent_vector.y += 2
        elif self.keys[pg.K_DOWN]:
            self.bodies[self.selected].plane.parent_vector.y -= 2
        if self.keys[pg.K_LEFT]:
            self.bodies[self.selected].plane.parent_vector.x -= 2
        elif self.keys[pg.K_RIGHT]:
            self.bodies[self.selected].plane.parent_vector.x += 2
        if self.keys[pg.K_a]:
            self.bodies[self.selected].rotate(0.1)
        elif self.keys[pg.K_d]:
            self.bodies[self.selected].rotate(-0.1)

    def USR_render(self):
        for i in self.bodies:
            for j in self.bodies:
                if i is not j:
                    if (i.radius + j.radius) >= i.vec.distance_to(j.vec):
                        self.collider.static_collision(i, j)

            i.show(self.window)


Test().mainloop()
