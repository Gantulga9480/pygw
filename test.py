from Game.base import Game
from Game.graphic.cartesian import plane, vector2d, scalar
from Game.graphic.shapes import triangle, rectangle, circle, polygon, shape
from Game.physics.body import *
from Game.physics.collision import SeparatingAxisTheorem as SAT
from Game.physics.collision import LineIntersectCollision as LIC
from Game.color import BLACK, RED, GREEN, BLUE
import pygame as pg
import random
import math


class Test(Game):

    def __init__(self, title: str = 'PyGameDemo',
                 width: int = 800, height: int = 800,
                 fps: int = 60, render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)

        self.plane = plane((width, height), 1)
        self.collider = LIC(self.plane)

        self.bodies: list[body] = []

        self.selected = 0
        self.num_shapes = 10

        for _ in range(self.num_shapes):
            n = random.randint(3, 6)
            posx = random.randint(self.plane.x_min, self.plane.x_max)
            posy = random.randint(self.plane.y_min, self.plane.y_max)
            self.bodies.append(
                body(self.plane, (posx, posy), n, 50, STATIC))
        self.bodies[0].state = DYNAMIC

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
            self.bodies[self.selected].position_vec.y += 3
        elif self.keys[pg.K_DOWN]:
            self.bodies[self.selected].position_vec.y -= 3
        if self.keys[pg.K_LEFT]:
            self.bodies[self.selected].position_vec.x -= 3
        elif self.keys[pg.K_RIGHT]:
            self.bodies[self.selected].position_vec.x += 3
        if self.keys[pg.K_a]:
            self.bodies[self.selected].rotate(0.1)
        elif self.keys[pg.K_d]:
            self.bodies[self.selected].rotate(-0.1)

    def USR_render(self):
        for i in self.bodies:
            for j in self.bodies:
                if i is not j and (i.state != STATIC or j.state != STATIC):
                    if (i.radius + j.radius) >= \
                            i.position_vec.distance(j.position_vec):
                        self.collider.collide(i, j)

            i.show(self.window)


Test().mainloop()
