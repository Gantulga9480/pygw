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

    def __init__(self, center_x, center_y, hit_radius, visual_radius=None, color=(255, 255, 255)):
        if visual_radius is None:
            visual_radius = hit_radius
        self.color = color
        w = int(visual_radius * 2)
        super().__init__(center_x - visual_radius, center_y - visual_radius, w, w, (0, 0, 0))
        self.center_x = center_x
        self.center_y = center_y
        self.hit_radius = hit_radius
        self.visual_radius = visual_radius
        self.life = 0.3

    def update(self, dt):
        self.life -= dt
        if self.life <= 0:
            self.kill()

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.center_x, self.center_y)
        alpha = self.life / 0.3
        r = int(self.visual_radius)
        pg.draw.circle(surface, (*self.color, int(255 * alpha)), (sx, sy), r, 2)


class BounceProjectile(Entity):
    """Projectile that bounces between enemies."""

    def __init__(self, x, y, vx, vy, dmg, size=10, bounces=3, color=C.C_CYAN):
        super().__init__(x - size / 2, y - size / 2, size, size, color)
        self.vx = vx
        self.vy = vy
        self.dmg = dmg
        self.bounces = bounces
        self.max_bounces = bounces
        self.life = 3.0
        self.hit_list = []

    def update(self, dt):
        super().update(dt)
        self.move(dt)
        self.life -= dt
        if self.life <= 0:
            self.kill()

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.cx, self.cy)
        r = int(self.w / 2)
        pg.draw.circle(surface, self.color, (sx, sy), r)
        pg.draw.circle(surface, C.C_BLACK, (sx, sy), r, 1)


class HomingProjectile(Entity):
    """Projectile that tracks a target enemy."""

    def __init__(self, proj):
        size = proj.get("size", 6)
        super().__init__(proj["x"] - size / 2, proj["y"] - size / 2, size, size, proj["color"])
        self.target = proj["target"]
        self.dmg = proj["dmg"]
        self.homing_speed = proj.get("homing_speed", 350)
        self.life = 3.0
        self.poison = proj.get("poison", False)
        self.slow = proj.get("slow", False)
        self.slow_stacks = proj.get("slow_stacks", 0)

    def update(self, dt):
        super().update(dt)
        if self.target and self.target.alive:
            dx = self.target.cx - self.cx
            dy = self.target.cy - self.cy
            dist = math.hypot(dx, dy) or 1
            self.vx = (dx / dist) * self.homing_speed
            self.vy = (dy / dist) * self.homing_speed
        self.move(dt)
        self.life -= dt
        if self.life <= 0:
            self.kill()

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.cx, self.cy)
        r = int(self.w / 2)
        pg.draw.circle(surface, self.color, (sx, sy), r)
        pg.draw.circle(surface, C.C_BLACK, (sx, sy), r, 1)


def create_projectile(proj):
    if proj["type"] == "slam_aoe":
        cx = proj.get("cx") or proj["x"] + proj["radius"]
        cy = proj.get("cy") or proj["y"] + proj["radius"]
        hr = proj.get("hit_radius") or proj["radius"]
        vr = proj.get("visual_radius") or proj["radius"]
        col = proj.get("color") or (255, 255, 255)
        return AOEFlash(cx, cy, hr, vr, col)
    if proj["type"] == "ice_nova":
        return AOEFlash(proj.get("cx") or proj["x"], proj.get("cy") or proj["y"],
                        proj.get("hit_radius", 100), proj.get("visual_radius", 100),
                        proj.get("color", C.C_CYAN))
    if proj["type"] == "shadow_step":
        dmg = proj["dmg"]
        is_crit = proj.get("crit", False)
        if is_crit:
            dmg *= 2
        return dict(
            type="slam_aoe",
            cx=0,
            cy=0,
            hit_radius=60,
            visual_radius=60,
            dmg=dmg,
            color=proj.get("color", C.C_PURPLE),
            crit=is_crit,
        )
    if proj.get("target") and proj["type"] in ("shadow_bolt", "frost_bolt"):
        return HomingProjectile(proj)
    if proj["type"] == "bounce_proj":
        return BounceProjectile(proj["x"], proj["y"], proj["vx"], proj["vy"],
                                proj["dmg"], proj.get("size", 10),
                                proj.get("bounces", 3),
                                proj.get("color", C.C_CYAN))
    return Projectile(proj["x"], proj["y"], proj["vx"], proj["vy"],
                      proj["dmg"], proj["size"], proj["color"],
                      poison=proj.get("poison", False))