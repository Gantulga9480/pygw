"""Hero base class — movement, auto-attack, abilities."""
import math
import random
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
        keys = list(stats.keys())
        self.auto_ability = stats.get("slash") or stats.get("slam") or stats.get("frost_bolt") or stats.get("shadow_bolt")
        self.q_ability = stats.get("dash") or stats.get("iron_skin") or stats.get("blizzard") or stats.get("shadow_step")
        self.e_ability = stats.get("poison") or stats.get("rally") or stats.get("ice_nova") or stats.get("shadow_clone")

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

        # Passive system
        self._frenzy_stacks = 0
        self._last_enemy_hp = {}

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
        best_dist = self.effective_range ** 2
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

    def apply_upgrade(self, upgrade_def, stats=None):
        upgrade_def["apply"](self, stats)
        hp_bonus = upgrade_def["name"] in ("Vitality", "Goliath", "Fortress")
        if hp_bonus:
            old_max = self.max_hp
            bonus = 10 if upgrade_def["name"] == "Vitality" else 25 if upgrade_def["name"] == "Goliath" else 50
            self.max_hp += bonus
            if stats:
                stats.max_hp += bonus
                if stats.hp == old_max:
                    stats.hp += bonus

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
        mult = 1.0 + self.upgrade_data.get("attack_speed", 0) + self.effective_frenzy_bonus
        return base / mult if mult > 0 else base

    @property
    def effective_magnet_range(self):
        mult = 1.0 + self.upgrade_data.get("magnet_range", 0)
        return C.MAGNET_RANGE * mult

    @property
    def effective_slam_radius(self):
        base = self.auto_ability.get("range", 100)
        mult = 1.0 + self.upgrade_data.get("slam_radius", 0)
        return base * mult

    @property
    def effective_slam_cooldown(self):
        base = self.auto_ability.get("cooldown", 1.5)
        reduce = self.upgrade_data.get("slam_cooldown_reduce", 0)
        return base * (1.0 - reduce)

    @property
    def effective_dash_cooldown(self):
        base = self.q_ability.get("cooldown", 5.0)
        reduce = self.upgrade_data.get("dash_cd_reduce", 0)
        return max(1.0, base - reduce)

    @property
    def effective_poison_dmg(self):
        base = self.e_ability.get("dmg", 2)
        bonus = self.upgrade_data.get("poison_dmg", 0)
        return base + bonus

    @property
    def effective_range(self):
        base = self.auto_ability.get("range", 100)
        mult = 1.0 + self.upgrade_data.get("attack_range", 0)
        return base * mult

    @property
    def effective_q_cd(self):
        return self.q_ability["cooldown"]

    @property
    def effective_e_cd(self):
        return self.e_ability["cooldown"]

    @property
    def effective_crit_chance(self):
        return self.upgrade_data.get("crit_chance", 0)

    @property
    def effective_lifesteal(self):
        return self.upgrade_data.get("lifesteal", 0)

    @property
    def effective_thorns(self):
        return self.upgrade_data.get("thorns", 0)

    @property
    def effective_evasion(self):
        return self.upgrade_data.get("evasion", 0)

    @property
    def effective_siphon_dmg(self):
        return self.upgrade_data.get("siphon_dmg", 0)

    @property
    def effective_siphon_heal(self):
        return self.upgrade_data.get("siphon_heal", 0)

    @property
    def effective_armor(self):
        return self.upgrade_data.get("armor", 0)

    @property
    def effective_replenish(self):
        return self.upgrade_data.get("replenish", 0)

    @property
    def effective_second_wind(self):
        return self.upgrade_data.get("second_wind", 0)

    @property
    def effective_executioner_mult(self):
        return self.upgrade_data.get("executioner_mult", 1.0)

    @property
    def effective_executioner_threshold(self):
        return self.upgrade_data.get("executioner_threshold", 0)

    @property
    def effective_frenzy_bonus(self):
        return self._frenzy_stacks * self.upgrade_data.get("frenzy_per_kill", 0)

    def take_damage(self, dmg):
        if self.invincible > 0:
            return 0
        original_dmg = dmg
        if self.iron_skin_timer > 0:
            dmg = int(dmg * 0.5)
        if self.effective_armor > 0:
            dmg = max(1, dmg - self.effective_armor)
        self.max_hp_current = getattr(self, "max_hp_current", self.max_hp)
        return dmg

    def get_armor_blocked(self, dmg):
        if self.invincible > 0:
            return 0
        blocked = 0
        if self.iron_skin_timer > 0:
            blocked += dmg - int(dmg * 0.5)
        after_iron = dmg - blocked
        if self.effective_armor > 0:
            blocked += after_iron - max(1, after_iron - self.effective_armor)
        return blocked

    def check_evasion(self):
        return random.random() < self.effective_evasion

    def register_kill(self):
        self._frenzy_stacks += 1

    def get_thorns(self):
        return self.effective_thorns

    def apply_lifesteal(self, dmg):
        if self.effective_lifesteal > 0:
            heal = int(self.effective_lifesteal)
            self.hp_current = min(self.max_hp, self.hp_current + heal)
            return heal
        return 0

    def apply_siphon(self, dmg):
        if self.effective_siphon_dmg > 0:
            bonus = int(dmg * self.effective_siphon_dmg)
            if bonus > 0:
                self.hp_current = min(self.max_hp, self.hp_current + bonus)
        return int(dmg * self.effective_siphon_dmg) if self.effective_siphon_dmg > 0 else 0

    def apply_second_wind(self):
        if self.effective_second_wind > 0:
            heal = int(self.effective_second_wind)
            self.hp_current = min(self.max_hp, self.hp_current + heal)

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
    @property
    def effective_q_cd(self):
        return self.effective_dash_cooldown

    @property
    def effective_e_cd(self):
        return self.e_ability["cooldown"]

    def _create_auto_attack(self, target):
        dx = target.cx - self.cx
        dy = target.cy - self.cy
        dist = math.hypot(dx, dy) or 1
        is_crit = random.random() < self.effective_crit_chance
        base_proj = dict(
            type="slash_proj",
            x=self.cx - 2,
            y=self.cy - 2,
            dmg=self.effective_dmg,
            size=self.auto_ability["proj_size"],
            color=C.C_GOLD if is_crit else self.auto_ability["color"],
            poison=self.poison_stacks > 0,
            crit=is_crit,
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
        self.q_cooldown = self.effective_dash_cooldown
        return dict(type="dash", hero=self)

    def _create_e_effect(self):
        base_hits = self.e_ability["hits"]
        bonus_stacks = self.upgrade_data.get("poison_stacks", 0)
        self.poison_stacks = base_hits + bonus_stacks
        return dict(type="poison", stacks=self.poison_stacks)

    def apply_poison_hit(self):
        if self.poison_stacks > 0:
            self.poison_stacks -= 1


class TankWarrior(Hero):
    @property
    def effective_atk_speed(self):
        base = self.auto_ability.get("cooldown", 1.5)
        reduce = self.upgrade_data.get("slam_cooldown_reduce", 0)
        speed_mult = 1.0 + self.upgrade_data.get("attack_speed", 0) + self.effective_frenzy_bonus
        return base * (1.0 - reduce) / speed_mult if speed_mult > 0 else base * (1.0 - reduce)

    @property
    def effective_q_cd(self):
        base = self.q_ability["cooldown"]
        bonus = self.upgrade_data.get("iron_skin_duration", 0)
        return base  # Iron Resolve doesn't change the cooldown, only duration

    @property
    def effective_e_cd(self):
        return self.e_ability["cooldown"]

    def _create_auto_attack(self, target):
        slam_range = self.effective_slam_radius
        is_crit = random.random() < self.effective_crit_chance
        return dict(
            type="slam_aoe",
            cx=self.cx,
            cy=self.cy,
            hit_radius=slam_range,
            visual_radius=slam_range,
            dmg=self.effective_dmg,
            color=C.C_GOLD if is_crit else self.auto_ability["color"],
            crit=is_crit,
        )

    def _create_q_effect(self):
        duration = self.q_ability["duration"] + self.upgrade_data.get("iron_skin_duration", 0)
        self.iron_skin_timer = duration
        return dict(type="iron_skin", duration=duration)

    def _create_e_effect(self):
        duration = self.e_ability["duration"] + self.upgrade_data.get("rally_duration", 0)
        self.rally_timer = duration
        self.rally_total = duration
        return dict(type="rally", heal=self.e_ability["heal"], duration=duration)


class FrostWitch(Hero):
    @property
    def effective_q_cd(self):
        base = self.q_ability["cooldown"]
        reduce = self.upgrade_data.get("blizzard_cd_reduce", 0)
        return base * (1 - reduce)

    @property
    def effective_e_cd(self):
        base = self.e_ability["cooldown"]
        return base * (1 - self.upgrade_data.get("ice_nova_cd_reduce", 0))

    @property
    def effective_frost_bolt_range(self):
        base = self.auto_ability.get("range", 200)
        mult = 1.0 + self.upgrade_data.get("frost_range", 0)
        return base * mult

    def _create_auto_attack(self, target):
        dx = target.cx - self.cx
        dy = target.cy - self.cy
        dist = math.hypot(dx, dy) or 1
        is_crit = random.random() < self.effective_crit_chance
        is_slow = random.random() < 0.5
        base_proj = dict(
            type="frost_bolt",
            x=self.cx - 2,
            y=self.cy - 2,
            vx=(dx / dist) * self.auto_ability["proj_speed"],
            vy=(dy / dist) * self.auto_ability["proj_speed"],
            dmg=self.effective_dmg,
            size=self.auto_ability["proj_size"],
            color=C.C_GOLD if is_crit else self.auto_ability["color"],
            poison=False,
            slow=is_slow,
            slow_stacks=1 + self.upgrade_data.get("frost_slow_stacks", 0),
            crit=is_crit,
        )
        return [base_proj]

    def _create_q_effect(self):
        duration = self.q_ability["duration"] + self.upgrade_data.get("blizzard_duration", 0)
        radius = self.q_ability.get("radius", 120)
        self.blizzard_timer = duration
        self.blizzard_radius = radius
        self.blizzard_total = duration
        return dict(type="blizzard", duration=duration, radius=radius)

    def _create_e_effect(self):
        range_val = self.e_ability.get("range", 100)
        dmg = self.effective_dmg
        is_crit = random.random() < self.effective_crit_chance
        if is_crit:
            dmg *= 2
        return dict(
            type="ice_nova",
            cx=self.cx,
            cy=self.cy,
            hit_radius=range_val,
            visual_radius=range_val,
            dmg=dmg,
            color=C.C_GOLD if is_crit else self.e_ability["color"],
            crit=is_crit,
            chain=self.upgrade_data.get("chain_freeze", 0) > 0,
        )


class ShadowAssassin(Hero):
    @property
    def effective_q_cd(self):
        base = self.q_ability["cooldown"]
        reduce = self.upgrade_data.get("shadow_step_cd_reduce", 0)
        return base * (1 - reduce)

    @property
    def effective_e_cd(self):
        base = self.e_ability["cooldown"]
        return base * (1 - self.upgrade_data.get("shadow_clone_cd_reduce", 0))

    @property
    def effective_shadow_bolt_homing(self):
        return self.auto_ability["proj_speed"] * (1 + self.upgrade_data.get("shadow_homing", 0))

    def _create_auto_attack(self, target):
        is_crit = random.random() < self.effective_crit_chance
        return dict(
            type="shadow_bolt",
            x=self.cx - 2,
            y=self.cy - 2,
            target=target,
            homing_speed=self.effective_shadow_bolt_homing,
            dmg=self.effective_dmg,
            size=self.auto_ability["proj_size"],
            color=C.C_GOLD if is_crit else self.auto_ability["color"],
            poison=False,
            crit=is_crit,
        )

    def _create_q_effect(self):
        range_val = self.q_ability.get("range", 180)
        dmg = self.effective_dmg * (1 + self.upgrade_data.get("shadow_step_dmg", 0))
        is_crit = random.random() < self.effective_crit_chance
        if is_crit:
            dmg *= 2
        return dict(
            type="shadow_step",
            target_range=range_val,
            dmg=dmg,
            color=C.C_GOLD if is_crit else self.q_ability["color"],
            crit=is_crit,
        )

    def _create_e_effect(self):
        duration = self.e_ability["duration"] + self.upgrade_data.get("shadow_clone_duration", 0)
        clones = self.upgrade_data.get("shadow_clones", 0) + 1
        return dict(
            type="shadow_clone",
            duration=duration,
            clone_count=clones,
            clone_dmg_ratio=self.e_ability.get("clone_dmg", 0.7),
        )