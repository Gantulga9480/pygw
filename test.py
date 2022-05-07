from Game.base import Game
from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import triangle, rectangle, polygon, shape
from Game.physics.body import *
from Game.physics.collision import LineIntersectCollision as LIC
from Game.color import BLACK, RED, GREEN, BLUE
import pygame as pg
import random
import math


class TestBody(base_body):

    def __init__(self,
                 body_type,
                 pos: Vector2d,
                 vertex_count: int = 2,
                 size: float = 1,
                 limit_vertex: bool = True) -> None:
        super().__init__(body_type, pos, vertex_count, size, limit_vertex)

    def step(self):
        if self.body.state == DYNAMIC:
            self.body.step(self.plane.parent_vector, 60)


class Test(Game):

    def __init__(self, title: str = 'PyGameDemo',
                 width: int = 1600, height: int = 800,
                 fps: int = 60, render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)

        self.plane = CartesianPlane((width, height), 1)
        self.collider = LIC(self.plane)

        self.bodies: list[TestBody] = []

        self.selected = 0
        self.num_shapes = 10

        self.bodies.append(
            TestBody(
                DYNAMIC, self.plane.createRandomVector(set_limit=True), 3, 30))

        # self.bodies.append(TestBody(DYNAMIC,
        #                             self.plane.createRandomVector(),
        #                             3, 50))

        for _ in range(self.num_shapes):
            self.bodies.append(
                TestBody(
                    DYNAMIC,
                    self.plane.createRandomVector(set_limit=True), 3, 50))

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
            self.bodies[self.selected].body.acceleration.add(2)
        elif self.keys[pg.K_DOWN]:
            self.bodies[self.selected].body.acceleration.scale(1/1.1)
        if self.keys[pg.K_LEFT]:
            self.bodies[self.selected].body.acceleration.rotate(0.1)
            self.bodies[self.selected].body.velocity.rotate(0.1)
            self.bodies[self.selected].rotate(0.1)
        elif self.keys[pg.K_RIGHT]:
            self.bodies[self.selected].body.acceleration.rotate(-0.1)
            self.bodies[self.selected].body.velocity.rotate(-0.1)
            self.bodies[self.selected].rotate(-0.1)
            # self.bodies[self.selected].rotate(-0.1)

    def USR_loop(self):
        for b in self.bodies:
            if random.random() > 0.5:
                b.body.acceleration.add(1)
            else:
                b.body.acceleration.scale(1/1.1)
            if random.random() > 0.5:
                b.body.acceleration.rotate(0.1)
                b.body.velocity.rotate(0.1)
                b.rotate(0.1)
            else:
                b.body.acceleration.rotate(-0.1)
                b.body.velocity.rotate(-0.1)
                b.rotate(-0.1)
            b.step()

    def USR_render(self):
        for i in self.bodies:
            for j in self.bodies:
                if i is not j:
                    if i.body.state is not STATIC or \
                            j.body.state is not STATIC:
                        if (i.body.radius + j.body.radius) >= \
                                i.vec.distance_to(j.vec):
                            self.collider.static_collision(i, j)

            i.show(self.window)
            i.body.velocity.show(self.window)
            i.body.acceleration.show(self.window, width=3)


Test().mainloop()
