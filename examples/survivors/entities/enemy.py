"""Enemy types: zombie, runner, brute, boss."""
import math
import pygame as pg
from survivors.entities.base import Entity
from survivors import config as C


class Enemy(Entity):
    def __init__(self, x, y, etype, hp_mult=1.0, dmg_mult=1.0):
        templates = {
            "zombie": C.ENEMY_ZOMBIE,
            "runner": C.ENEMY_RUNNER,
            "brute": C.ENEMY_BRUTE,
            "boss": C.ENEMY_BOSS,
        }
        t = templates[etype]
        super().__init__(x, y, t["size"][0], t["size"][1], t["color"])
        self.outline = t.get("outline", C.C_BLACK)
        self.etype = etype
        self.max_hp = int(t["hp"] * hp_mult)
        self.hp = self.max_hp
        self.speed = t["speed"]
        self.dmg = int(t["dmg"] * dmg_mult)
        self.anim_frame = 0
        self.anim_timer = 0.0
        self.hit_flash = 0.0
        self.attack_cooldown = 0.0
        self.attack_interval = 0.75
        self._slow_timer = 0.0
        self._slow_factor = 1.0

    def update(self, dt, hero):
        super().update(dt)
        # Chase hero
        dx = hero.cx - self.cx
        dy = hero.cy - self.cy
        dist = math.hypot(dx, dy) or 1
        speed_mult = self._slow_factor if self._slow_timer > 0 else 1.0
        self.vx = (dx / dist) * self.speed * speed_mult
        self.vy = (dy / dist) * self.speed * speed_mult
        self.move(dt)
        if self._slow_timer > 0:
            self._slow_timer -= dt
        # Animation
        self.anim_timer += dt
        if self.anim_timer > 0.2:
            self.anim_timer = 0.0
            self.anim_frame = (self.anim_frame + 1) % 2
        if self.hit_flash > 0:
            self.hit_flash -= dt
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def take_damage(self, dmg):
        self.hp -= dmg
        self.hit_flash = 0.1
        if self.hp <= 0:
            self.kill()

    def apply_slow(self, duration, factor=0.6):
        self._slow_timer = max(self._slow_timer, duration)
        self._slow_factor = min(self._slow_factor, factor)

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        # Body
        color = C.C_WHITE if self.hit_flash > 0 else self.color
        # Simple body shape with slight animation bob
        bob = 1 if self.anim_frame else 0
        pg.draw.rect(surface, color, (sx, sy - bob, self.w, self.h))
        # Eyes
        eye_color = C.C_RED if self.etype == "boss" else C.C_YELLOW
        pg.draw.rect(surface, eye_color, (sx + 3, sy + 4 - bob, 3, 3))
        pg.draw.rect(surface, eye_color, (sx + self.w - 6, sy + 4 - bob, 3, 3))
        # Outline
        pg.draw.rect(surface, self.outline, (sx, sy - bob, self.w, self.h), 1)
        # HP bar for boss
        if self.etype == "boss" and self.hp < self.max_hp:
            bar_w = self.w + 10
            bar_h = 4
            bar_x = sx - 5
            bar_y = sy - 8 - bob
            pg.draw.rect(surface, C.C_RED, (bar_x, bar_y, bar_w, bar_h))
            pg.draw.rect(surface, C.C_GREEN, (bar_x, bar_y, bar_w * (self.hp / self.max_hp), bar_h))
        # Brute indicator
        if self.etype == "brute":
            pg.draw.rect(surface, C.C_DARK_GRAY, (sx + 2, sy + self.h - 4 - bob, self.w - 4, 3))


def spawn_enemy(etype, x, y, hp_mult, dmg_mult):
    return Enemy(x, y, etype, hp_mult, dmg_mult)