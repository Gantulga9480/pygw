"""Hero base class — movement, auto-attack, abilities."""
import math
import pygame as pg
from pygw import core
from survivors.entities.base import Entity
from survivors import config as C


class Hero(Entity):
    def __init__(self, x, y, stats):
        super().__init__(x, y, stats["size"][0], stats["size"][1], stats["colors"][0])
        self.outline = C.C_BLACK
        self._stats = stats
        self.max_hp = stats["hp"]
        self.hp_current = stats["hp"]
        self.speed = stats["speed"]
        self.facing = 1  # 1 = right, -1 = left
        self.anim_frame = 0
        self.anim_timer = 0.0
        self.invincible = 0.0
        self.upgrade_data = {}
        self.unlocked_weapons = []

        # Ability definitions
        self.auto_ability = stats["slash"] if "slash" in stats else stats.get("slam")
        self.q_ability = stats.get("dash") or stats.get("iron_skin")
        self.e_ability = stats.get("poison") or stats.get("rally")

        # Auto-attack state
        self.auto_cooldown = 0.0
        self.auto_timer = 0.0

        # Q/E cooldowns
        self.q_cooldown = 0.0
        self.e_cooldown = 0.0

        # Active effects
        self.poison_stacks = 0  # for rogue: remaining hits with poison
        self.iron_skin_timer = 0.0
        self.rally_timer = 0.0
        self.rally_total = 0.0

    def update(self, dt, input_mgr, camera):
        super().update(dt)
        # Movement
        self._handle_movement(dt, input_mgr)
        # Animation
        self.anim_timer += dt
        if self.anim_timer > 0.15:
            self.anim_timer = 0.0
            self.anim_frame = (self.anim_frame + 1) % 4
        # Invincibility
        if self.invincible > 0:
            self.invincible -= dt
        # Cooldowns
        if self.auto_cooldown > 0:
            self.auto_cooldown -= dt
        if self.q_cooldown > 0:
            self.q_cooldown -= dt
        if self.e_cooldown > 0:
            self.e_cooldown -= dt
        # Active effects
        if self.iron_skin_timer > 0:
            self.iron_skin_timer -= dt
        if self.rally_timer > 0:
            self.rally_timer -= dt
        # Dash movement
        if hasattr(self, "_dash_timer") and self._dash_timer > 0:
            self._dash_timer -= dt
            self.x += self._dash_vx * dt
            self.y += self._dash_vy * dt
            if self._dash_timer <= 0:
                self._dash_vx = 0
                self._dash_vy = 0

    def _handle_movement(self, dt, input_mgr):
        if input_mgr is None:
            return
        dx, dy = 0.0, 0.0
        if input_mgr.is_key_pressed(core.K_LEFT) or input_mgr.is_key_pressed(core.K_a):
            dx -= 1
            self.facing = -1
        if input_mgr.is_key_pressed(core.K_RIGHT) or input_mgr.is_key_pressed(core.K_d):
            dx += 1
            self.facing = 1
        if input_mgr.is_key_pressed(core.K_UP) or input_mgr.is_key_pressed(core.K_w):
            dy -= 1
        if input_mgr.is_key_pressed(core.K_DOWN) or input_mgr.is_key_pressed(core.K_s):
            dy += 1
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length
            self.vx = dx * self.effective_speed
            self.vy = dy * self.effective_speed
            self.move(dt)
        else:
            self.vx = 0
            self.vy = 0

    def try_auto_attack(self, enemies):
        """Return a projectile dict or list if auto-attack should fire, else None."""
        if self.auto_cooldown > 0:
            return None
        target = self._find_nearest_enemy(enemies)
        if target is None:
            return None
        self.auto_cooldown = self.effective_atk_speed
        return self._create_auto_attack(target)

    def try_q_ability(self):
        """Return ability effect dict if Q should fire, else None."""
        if self.q_cooldown > 0:
            return None
        self.q_cooldown = self.q_ability["cooldown"]
        return self._create_q_effect()

    def try_e_ability(self):
        """Return ability effect dict if E should fire, else None."""
        if self.e_cooldown > 0:
            return None
        self.e_cooldown = self.e_ability["cooldown"]
        return self._create_e_effect()

    def _find_nearest_enemy(self, enemies):
        best = None
        best_dist = self.auto_ability["range"] ** 2
        for e in enemies:
            d = (self.cx - e.cx) ** 2 + (self.cy - e.cy) ** 2
            if d < best_dist:
                best_dist = d
                best = e
        return best

    def _create_auto_attack(self, target):
        return None  # Override in subclasses

    def _create_q_effect(self):
        return None  # Override in subclasses

    def _create_e_effect(self):
        return None  # Override in subclasses

    def take_damage(self, dmg):
        if self.invincible > 0:
            return 0
        if self.iron_skin_timer > 0:
            dmg = int(dmg * 0.5)
        self.max_hp_current = getattr(self, "max_hp_current", self.max_hp)
        return dmg

    def apply_upgrade(self, upgrade_def):
        upgrade_def["apply"](self, None)

    @property
    def effective_speed(self):
        mult = 1.0 + self.upgrade_data.get("move_speed", 0)
        return self.speed * mult

    @property
    def effective_dmg(self):
        base = self.auto_ability.get("dmg", 15)
        mult = 1.0 + self.upgrade_data.get("damage", 0)
        return int(base * mult)

    @property
    def effective_atk_speed(self):
        base = self.auto_ability.get("cooldown", 1.0)
        mult = 1.0 + self.upgrade_data.get("attack_speed", 0)
        return base / mult if mult > 0 else base

    @property
    def effective_magnet_range(self):
        mult = 1.0 + self.upgrade_data.get("magnet_range", 0)
        return C.MAGNET_RANGE * mult

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        # Draw hero body
        color = C.C_WHITE if self.flash_timer > 0 else self.color
        if self.invincible > 0 and int(self.invincible * 10) % 2 == 0:
            color = (color[0] // 2, color[1] // 2, color[2] // 2)
        body_h = int(self.h * 0.7)
        leg_h = self.h - body_h
        # Legs
        leg_offset = 2 if self.anim_frame % 2 else 0
        pg.draw.rect(surface, self._stats["colors"][1],
                     (sx + 2 - leg_offset, sy + body_h, 4, leg_h))
        pg.draw.rect(surface, self._stats["colors"][1],
                     (sx + self.w - 6 + leg_offset, sy + body_h, 4, leg_h))
        # Body
        pg.draw.rect(surface, color, (sx, sy, self.w, body_h))
        # Eyes
        eye_x = sx + (self.w // 2 + self.facing * 3)
        pg.draw.rect(surface, C.C_BLACK, (eye_x, sy + 4, 2, 2))
        # Outline
        pg.draw.rect(surface, self.outline, (sx, sy, self.w, self.h), 1)
        # Iron skin effect
        if self.iron_skin_timer > 0:
            pg.draw.rect(surface, C.C_GOLD, (sx - 2, sy - 2, self.w + 4, self.h + 4), 2, border_radius=3)


class SpeedRogue(Hero):
    def _create_auto_attack(self, target):
        dx = target.cx - self.cx
        dy = target.cy - self.cy
        dist = math.hypot(dx, dy) or 1
        base_proj = dict(
            type="slash_proj",
            x=self.cx - 2,
            y=self.cy - 2,
            dmg=self.effective_dmg,
            size=self.auto_ability["proj_size"],
            color=self.auto_ability["color"],
            poison=self.poison_stacks > 0,
        )
        if "throwing_knives" in self.unlocked_weapons:
            knives = []
            for angle_deg in [-45, 0, 45]:
                angle = math.radians(angle_deg)
                cos_a, sin_a = math.cos(angle), math.sin(angle)
                if self.facing == -1:
                    cos_a = -cos_a
                knives.append(dict(
                    x=self.cx - 2, y=self.cy - 2,
                    vx=(dx / dist * cos_a - dy / dist * sin_a) * self.auto_ability["proj_speed"],
                    vy=(dx / dist * sin_a + dy / dist * cos_a) * self.auto_ability["proj_speed"],
                    **base_proj,
                ))
            return knives
        return [dict(
            vx=(dx / dist) * self.auto_ability["proj_speed"],
            vy=(dy / dist) * self.auto_ability["proj_speed"],
            **base_proj,
        )]

    def _create_q_effect(self):
        dx = self.vx
        dy = self.vy
        if dx == 0 and dy == 0:
            dx = self.facing
        length = math.hypot(dx, dy) or 1
        speed = self.q_ability["range"] / self.q_ability["duration"]
        self._dash_timer = self.q_ability["duration"]
        self._dash_vx = (dx / length) * speed
        self._dash_vy = (dy / length) * speed
        self.invincible = self.q_ability["duration"]
        return dict(type="dash", hero=self)

    def _create_e_effect(self):
        self.poison_stacks = self.e_ability["hits"]
        return dict(type="poison", stacks=self.poison_stacks)

    def apply_poison_hit(self):
        if self.poison_stacks > 0:
            self.poison_stacks -= 1


class TankWarrior(Hero):
    def _create_auto_attack(self, target):
        dx = target.cx - self.cx
        dy = target.cy - self.cy
        dist = math.hypot(dx, dy) or 1
        slam_range = self.auto_ability["range"]
        slam = dict(
            type="slam_aoe",
            x=self.cx - slam_range,
            y=self.cy - slam_range,
            radius=slam_range,
            dmg=self.effective_dmg,
            color=self.auto_ability["color"],
        )
        if "shield_bounce" not in self.unlocked_weapons:
            return slam
        return [slam, dict(
            type="bounce_proj",
            x=self.cx - 2, y=self.cy - 2,
            vx=(dx / dist) * self.auto_ability["proj_speed"],
            vy=(dy / dist) * self.auto_ability["proj_speed"],
            dmg=int(self.effective_dmg * 0.6),
            bounces=3,
            size=10,
            color=C.C_CYAN,
        )]

    def _create_q_effect(self):
        duration = self.q_ability["duration"] + self.upgrade_data.get("iron_skin_duration", 0)
        self.iron_skin_timer = duration
        return dict(type="iron_skin", duration=duration)

    def _create_e_effect(self):
        duration = self.e_ability["duration"] + self.upgrade_data.get("rally_duration", 0)
        self.rally_timer = duration
        self.rally_total = duration
        return dict(type="rally", heal=self.e_ability["heal"], duration=duration)