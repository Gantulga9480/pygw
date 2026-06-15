"""XP gems dropped by dead enemies."""
import random
import pygame as pg
from survivors import config as C


class XPGem:
    def __init__(self, x, y):
        r = random.random()
        if r < 0.1:
            self.tier = 2
            self.value = C.GEM_VALUES[2]
            self.color = C.GEM_COLORS[2]
            self.size = C.GEM_SIZE + 2
        elif r < 0.4:
            self.tier = 1
            self.value = C.GEM_VALUES[1]
            self.color = C.GEM_COLORS[1]
            self.size = C.GEM_SIZE
        else:
            self.tier = 0
            self.value = C.GEM_VALUES[0]
            self.color = C.GEM_COLORS[0]
            self.size = C.GEM_SIZE - 2
        self.x = x
        self.y = y
        self.alive = True
        self.pulse = 0.0

    def update(self, dt):
        self.pulse += dt * 3

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        pulse_size = int(self.size + 1 * abs(math.sin(self.pulse)))
        pg.draw.circle(surface, self.color, (sx, sy), pulse_size)
        pg.draw.circle(surface, C.C_BLACK, (sx, sy), pulse_size, 1)

    def kill(self):
        self.alive = False


import math