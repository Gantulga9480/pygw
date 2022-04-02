from Game.graphic.cartesian import scalar, plane, vector
from Game import BLACK, RED, BLUE
from utils import *
import pygame as pg
import random
import math


class MainPlane(plane):

    def __init__(self, size, unit_length=1) -> None:
        super().__init__(size, unit_length)


class ObjectPlane(plane):

    def __init__(self, size, unit_length=1) -> None:
        super().__init__(size, unit_length)


class AgentPlane(plane):

    def __init__(self,
                 size: tuple,
                 unit_length=1) -> None:
        super().__init__(size, unit_length)

    def move(self, agent_vec: vector, parent_vec: vector):
        d = agent_vec.length / FPS * self.unit_length
        vx = math.cos(agent_vec.direction) * d
        vy = math.sin(agent_vec.direction) * d
        parent_vec._x += vx
        parent_vec._y += vy
        self.XY = parent_vec.XY
        if round(self.X) == 0 or round(self.X) == self._size[0] or \
                round(self.Y) == 0 or round(self.Y) == self._size[1]:
            return True
        return False

    def set_limit(self):
        self.x_lim = [(self._x_dif - self._size[0]) // self.unit_length,
                      (self._size[0] - self._x_dif) // self.unit_length]
        self.y_lim = [(self._x_dif - self._size[0]) // self.unit_length,
                      (self._size[0] - self._x_dif) // self.unit_length]


class agent:

    def __init__(self, x, y, parent: plane) -> None:
        self.parent = parent
        self.position = parent.vector(x, y)
        self.plane = AgentPlane((WIDTH, HEIGHT), WIDTH//(MAX_SPEED//1.4142*2))
        self.plane.XY = self.position.XY
        self.head = self.plane.vector(1, 0)

    def move(self, positions):
        _rect = self.rect
        is_collide = _rect.collidelistall(positions)
        if is_collide:
            self.head.rotate(math.pi)
        is_hit = self.plane.move(self.head, self.position)
        if is_hit:
            self.head.rotate(math.pi)

    @property
    def rect(self):
        return pg.Rect(self.plane.X,
                       self.plane.Y, 0, 0).inflate(AGENT_SIZE, AGENT_SIZE)


class environment:

    def __init__(self, num_agents=1) -> None:
        self.plane = MainPlane((WIDTH, HEIGHT))
        self.agents: list[agent] = []
        self.speeds = [1/1.3, 1/1.25, 1/1.2, 1/1.15, 1/1.1, 1,
                       1.1, 1.15, 1.2, 1.25, 1.3]
        self.ro_speeds = [-math.pi/8, -math.pi/16, -math.pi/32, -math.pi/64, 0,
                          math.pi/64, math.pi/32, math.pi/16, math.pi/8]
        # for _ in range(num_agents):
        self.agents.append(agent(0, 0, self.plane))
        self.agents.append(agent(100, 0, self.plane))
        self.agents.append(agent(100, 100, self.plane))
        self.agents.append(agent(100, 200, self.plane))

    def step(self):
        for i, agent in enumerate(self.agents):
            pos = self.__get_agents_pos()
            # agent.head *= random.choice(self.speeds)
            # agent.head.rotate(random.choice(self.ro_speeds))
            pos.pop(i)
            agent.move(pos)

    def _step(self):
        ...

    def draw(self, parent):
        for agent in self.agents:
            # pg.draw.line(parent, BLACK, self.plane.XY, agent.plane.XY)
            pg.draw.circle(parent, BLUE, agent.rect.center, AGENT_SIZE)
            pg.draw.circle(parent, BLACK, agent.rect.center, VISION, 1)
            pg.draw.line(parent, RED, agent.rect.center,
                         agent.head.XY, 2)

    def __get_agents_pos(self):
        _rects = []
        for agent in self.agents:
            _rects.append(agent.rect)
        return _rects
