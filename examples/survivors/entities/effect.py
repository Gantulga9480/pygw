"""Visual effects: damage numbers, death particles, hit sparks."""
import random
import pygame as pg
from survivors.entities.base import Entity
from survivors import config as C


class DamageNumber:
    def __init__(self, x, y, dmg, critical=False):
        self.x = x
        self.y = y
        self.dmg = dmg
        self.life = C.DAMAGE_NUMBER_LIFETIME
        self.max_life = C.DAMAGE_NUMBER_LIFETIME
        self.critical = critical

    def update(self, dt):
        self.life -= dt
        self.y -= C.DAMAGE_NUMBER_RISE_SPEED * dt

    @property
    def alive(self):
        return self.life > 0

    def render(self, surface, camera, font):
        sx, sy = camera.world_to_screen(self.x, self.y)
        if isinstance(self.dmg, str):
            color = C.C_GOLD
            s = font.render(self.dmg, True, color)
        elif self.critical:
            s = font.render(f"![{self.dmg}]", True, C.C_RED)
        else:
            s = font.render(str(self.dmg), True, C.C_YELLOW if self.critical else C.C_WHITE)
        surface.blit(s, (sx - s.get_width() // 2, sy - s.get_height()))


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 6.28)
        speed = random.uniform(30, 120)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = C.PARTICLE_LIFETIME
        self.max_life = C.PARTICLE_LIFETIME
        self.size = random.randint(2, 4)

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.95
        self.vy *= 0.95

    @property
    def alive(self):
        return self.life > 0

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        alpha = self.life / self.max_life
        pg.draw.rect(surface, self.color, (sx, sy, int(self.size * alpha), int(self.size * alpha)))


import math


def spawn_death_particles(x, y, color, count=C.PARTICLE_COUNT_DEATH):
    return [Particle(x + random.randint(-4, 4), y + random.randint(-4, 4), color) for _ in range(count)]


def spawn_hit_sparks(x, y, count=C.PARTICLE_COUNT_HIT):
    return [Particle(x + random.randint(-2, 2), y + random.randint(-2, 2), C.C_YELLOW) for _ in range(count)]