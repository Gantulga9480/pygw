from Game.graphic.cartesian import scalar, plane, vector
from Game import BLACK, RED, BLUE
from utils import *
import pygame as pg
import random
import math


class MainPlane(plane):

    def __init__(self, size, unit_length=1, parent=None) -> None:
        super().__init__(size, unit_length, parent)


class ObjectPlane(plane):

    def __init__(self, size, unit_length=1, parent=None) -> None:
        super().__init__(size, unit_length, parent)


class AgentPlane(plane):

    def __init__(self,
                 size: tuple,
                 unit_length=1,
                 parent: plane = None,
                 position_vector: vector = None) -> None:
        super().__init__(size, unit_length, parent)
        self.unit_length = self.parent.unit_length
        self.position_vector = position_vector
        self.XY = self.position_vector.XY

    def move(self, head_vec: vector):
        d = head_vec.length / FPS * self.unit_length
        vx = math.cos(head_vec.direction) * d
        vy = math.sin(head_vec.direction) * d
        self.position_vector.x += vx
        self.position_vector.y += vy
        self.XY = self.position_vector.XY
        is_hit = self.wall_collision()
        if is_hit:
            if is_hit == LEFT_WALL or is_hit == RIGHT_WALL:
                if is_hit == LEFT_WALL:
                    self.re_posotion(x=AGENT_SIZE)
                else:
                    self.re_posotion(x=WIDTH-AGENT_SIZE)
                if head_vec.direction < 0:
                    head_vec.rotate((-math.pi-2*head_vec.direction))
                elif head_vec.direction >= 0:
                    head_vec.rotate((math.pi-2*head_vec.direction))
            else:
                if is_hit == TOP_WALL:
                    self.re_posotion(y=AGENT_SIZE)
                else:
                    self.re_posotion(y=HEIGHT-AGENT_SIZE)
                head_vec.rotate(-head_vec.direction*2)
            head_vec *= 0.5

    def set_limit(self):
        self.x_lim = [(self._x_dif - self._size[0]) // self.unit_length,
                      (self._size[0] - self._x_dif) // self.unit_length]
        self.y_lim = [(self._x_dif - self._size[0]) // self.unit_length,
                      (self._size[0] - self._x_dif) // self.unit_length]

    def wall_collision(self):
        if round(self.X)-AGENT_SIZE < 0:
            return LEFT_WALL
        elif round(self.X)+AGENT_SIZE > self._size[0]:
            return RIGHT_WALL
        elif round(self.Y)-AGENT_SIZE < 0:
            return TOP_WALL
        elif round(self.Y)+AGENT_SIZE > self._size[1]:
            return BOTTOM_WALL
        return False

    def re_posotion(self, x=None, y=None):
        if x:
            self.position_vector.x = self.parent.toX(x)
        if y:
            self.position_vector.y = self.parent.toY(y)
        self.XY = self.position_vector.XY


class agent:

    def __init__(self, parent: plane, id, x=None, y=None) -> None:
        self.parent = parent
        self.id = id
        self.position = \
            self.parent.vector(x, y) if x and y else self.parent.rand_vector()
        self.plane = AgentPlane(size=(WIDTH, HEIGHT),
                                unit_length=WIDTH//(MAX_SPEED//1.4142*2),
                                parent=self.parent,
                                position_vector=self.position)
        self.head = self.plane.vector(0, 0)

    def move(self, agents):
        self.plane.move(self.head)

    @property
    def rect(self):
        return pg.Rect(self.plane.X,
                       self.plane.Y, 0, 0).inflate(AGENT_SIZE, AGENT_SIZE)


class environment:

    def __init__(self) -> None:
        self.plane = MainPlane((WIDTH, HEIGHT))
        self.agents: list[agent] = []
        self.speeds = [1/1.3, 1/1.25, 1/1.2, 1/1.15, 1/1.1, 1,
                       1.1, 1.15, 1.2, 1.25, 1.3]
        self.ro_speeds = [-math.pi/8, -math.pi/16, -math.pi/32, -math.pi/64, 0,
                          math.pi/64, math.pi/32, math.pi/16, math.pi/8]
        for i in range(1):
            self.agents.append(agent(self.plane, i))

    def step(self):
        for agent in self.agents:
            if agent.id != 0:
                agent.head *= random.choice(self.speeds)
                agent.head.rotate(random.choice(self.ro_speeds)*60/FPS)
            agent.move(self.agents)
            self.collision(agent)

    def _step(self):
        ...

    def draw(self, parent):
        for agent in self.agents:
            # pg.draw.line(parent, BLACK, self.plane.XY, agent.plane.XY)
            pg.draw.circle(parent, BLUE, agent.rect.center, AGENT_SIZE)
            # pg.draw.circle(parent, BLACK, agent.rect.center, VISION, 1)
            pg.draw.line(parent, RED, agent.rect.center, agent.head.XY, 2)

    def collision(self, current: agent):
        for agent in self.agents:
            if agent.id != current.id:
                v = vector(self.plane,
                           agent.position.x - current.position.x,
                           agent.position.y - current.position.y)
                if v.length <= AGENT_SIZE*2:
                    d = (AGENT_SIZE*2 - v.length) * 0.5
                    w = v.direction
                    if current.head.length >= agent.head.length:
                        agent.position.x += d * math.cos(w)
                        agent.position.y += d * math.sin(w)
                    elif current.head.length < agent.head.length:
                        current.position.x -= d * math.cos(w)
                        current.position.y -= d * math.sin(w)
