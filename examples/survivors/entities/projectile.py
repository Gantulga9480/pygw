"""Projectiles and AOE effects."""
import math
import pygame as pg
from survivors.entities.base import Entity
from survivors import config as C


class Projectile(Entity):
    def __init__(self, x, y, vx, vy, dmg, size, color, poison=False):
        super().__init__(x - size / 2, y - size / 2, size, size, color)
        self.vx = vx
        self.vy = vy
        self.dmg = dmg
        self.poison = poison
        self.life = 3.0  # seconds before auto-destroy

    def update(self, dt):
        super().update(dt)
        self.move(dt)
        self.life -= dt
        if self.life <= 0:
            self.kill()

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        color = C.C_WHITE if self.flash_timer > 0 else self.color
        if self.poison:
            color = C.C_GREEN
        r = int(self.w / 2)
        pg.draw.circle(surface, color, (sx + r, sy + r), r)
        pg.draw.circle(surface, C.C_BLACK, (sx + r, sy + r), r, 1)


class AOEFlash(Entity):
    """Brief visual flash for AOE attacks like Ground Slam."""

    def __init__(self, x, y, radius, color):
        w = int(radius * 2)
        super().__init__(x - radius, y - radius, w, w, color)
        self.radius = radius
        self.life = 0.3

    def update(self, dt):
        self.life -= dt
        if self.life <= 0:
            self.kill()

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        alpha = self.life / 0.3
        r = int(self.radius)
        pg.draw.circle(surface, (*self.color, int(255 * alpha)), (sx + r, sy + r), r, 2)


def create_projectile(proj):
    if proj["type"] == "slam_aoe":
        return AOEFlash(proj["x"], proj["y"], proj["radius"], proj["color"])
    return Projectile(proj["x"], proj["y"], proj["vx"], proj["vy"],
                      proj["dmg"], proj["size"], proj["color"],
                      poison=proj.get("poison", False))