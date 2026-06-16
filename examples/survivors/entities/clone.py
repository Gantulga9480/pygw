"""Shadow Clone entity for Shadow Assassin."""
import math
import random
import pygame as pg
from survivors.entities.base import Entity
from survivors import config as C


class ShadowClone(Entity):
    def __init__(self, x, y, duration, dmg_ratio, original_hero):
        size = original_hero.w
        super().__init__(x, y, size, size, original_hero.color)
        self.outline = C.C_BLACK
        self.duration = duration
        self.life = duration
        self.dmg_ratio = dmg_ratio
        self.auto_dmg = int(original_hero.effective_dmg * dmg_ratio)
        self.auto_cd = 1.0
        self.attack_on_cooldown = 1.0
        self.original_hero = original_hero
        self._auto_ability = {"dmg": self.auto_dmg, "proj_speed": 350, "proj_size": 6, "range": 250}

    def update(self, dt):
        super().update(dt)
        self.life -= dt
        if self.life <= 0:
            self.kill()

    def _find_nearest_enemy(self, enemies):
        best = None
        best_dist = self._auto_ability["range"] ** 2
        for e in enemies:
            d = (self.cx - e.cx) ** 2 + (self.cy - e.cy) ** 2
            if d < best_dist:
                best_dist = d
                best = e
        return best

    def _create_auto_attack(self, target):
        dx = target.cx - self.cx
        dy = target.cy - self.cy
        dist = math.hypot(dx, dy) or 1
        is_crit = self.original_hero.effective_crit_chance > 0 and (random.random() < self.original_hero.effective_crit_chance)
        color = C.C_GOLD if is_crit else C.C_PURPLE
        return dict(
            type="shadow_bolt",
            x=self.cx - 2,
            y=self.cy - 2,
            target=target,
            homing_speed=350,
            dmg=self.auto_dmg,
            size=6,
            color=color,
            poison=False,
            crit=is_crit,
        )

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        alpha = int(255 * (self.life / self.duration))
        body_h = int(self.h * 0.7)
        leg_h = self.h - body_h
        leg_offset = 2 if int(self.anim_frame) % 2 else 0
        pg.draw.rect(surface, (*self.color[0], alpha), (sx + 2 - leg_offset, sy + body_h, 4, leg_h))
        pg.draw.rect(surface, (*self.color[0], alpha), (sx + self.w - 6 + leg_offset, sy + body_h, 4, leg_h))
        pg.draw.rect(surface, (*self.color[1], alpha), (sx, sy, self.w, body_h))
        pg.draw.rect(surface, C.C_BLACK, (sx, sy, self.w, self.h), 1)
