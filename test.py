from Game.base import Game
from Game.graphic.cartesian import plane, vector2d, scalar
from Game.graphic.shapes import triangle, rectangle, circle, polygon, shape
from Game.physics.body import *
from Game.color import BLACK, RED, GREEN, BLUE
from Game.physics.collision import SeparatingAxisTheorem as SAT
from Game.physics.collision import LineIntersectCollision as LIC
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

        self.bodies: list[rigidbody] = []

        self.selected = 0
        self.num_shapes = 10

        for _ in range(self.num_shapes):
            n = random.randint(3, 6)
            posx = random.randint(self.plane.x_min, self.plane.x_max)
            posy = random.randint(self.plane.y_min, self.plane.y_max)
            self.bodies.append(
                rigidbody(self.plane, (posx, posy), n, 50, STATIC))
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

    def USR_loop(self):
        for i in range(self.bodies.__len__()):
            # self.bodies[i].step()
            # check collisions of ith body with other bodies
            collisions = self.check_collision(i)

            # current body
            b1 = self.bodies[i]
            if collisions:
                # handle collision

                # displace sizes for body 1 and body 2
                b1d = [0, 0]
                b2d = [0, 0]
                for collision_info in collisions:
                    # collided body with b1
                    # collision_info[0] -> index of collided body
                    b2 = self.bodies[collision_info[0]]
                    # body b1 collision information with b2
                    b1_collisions = collision_info[1]

                    if b1.state == DYNAMIC and b2.state == STATIC:
                        for collision in b1_collisions:
                            # collision[0] -> collided vertex id of b1
                            # collision[1] -> collision point info
                            # collision[1][0] -> collision point
                            # collision[1][1] -> collision size (0:1)
                            vertex_i = collision[0]
                            size = collision[1][1]

                            # push back sizes of x and y axes
                            b1d[0] -= b1.vertices[vertex_i].x * size
                            b1d[1] -= b1.vertices[vertex_i].y * size
                        b1.inertia = b1.inertia.unit(scale=2)
                        # b1.rotate(math.pi)
                    elif b1.state == STATIC and b2.state == DYNAMIC:
                        for collision in b1_collisions:
                            vertex_i = collision[0]
                            size = collision[1][1]
                            b2d[0] += b1.vertices[vertex_i].x * size
                            b2d[1] += b1.vertices[vertex_i].y * size
                        b2.inertia = b2.inertia.unit(scale=2)
                        # b2.rotate(math.pi)
                b1.step(*b1d)
                b2.step(*b2d)

    def USR_render(self):
        for i in range(self.bodies.__len__()):
            if self.bodies[i].state == DYNAMIC:
                self.bodies[i].show(self.window, width=5, color=GREEN)
            elif i == self.num_shapes:
                self.bodies[i].show(self.window, width=5, color=RED)
            else:
                self.bodies[i].show(self.window)
            self.bodies[i].inertia.show(self.window)

    def check_collision(self, c):
        obj1 = []
        for i in range(self.bodies.__len__()):
            if self.bodies[c].position_vec.distance(
                self.bodies[i].position_vec) <= (self.bodies[c].radius +
                                                 self.bodies[i].radius) and \
                    self.bodies[i] is not self.bodies[c]:
                if self.bodies[c].state == STATIC and \
                        self.bodies[i].state == STATIC:
                    continue
                collision = self.collider.collide(self.bodies[c],
                                                  self.bodies[i])
                if collision:
                    # current object collided with bodies[i] by some vertex
                    obj1.append([i, collision])
        return obj1


Test().mainloop()
