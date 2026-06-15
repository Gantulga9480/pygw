"""Main gameplay window — camera, entities, combat, HUD."""
import math
import random
import pygame as pg
from pygw import Window, core
from survivors import config as C
from survivors.camera import Camera
from survivors.entities.hero import SpeedRogue, TankWarrior
from survivors.entities.enemy import spawn_enemy
from survivors.entities.projectile import create_projectile
from survivors.entities.effect import DamageNumber, spawn_death_particles, spawn_hit_sparks
from survivors.entities.pickup import XPGem
from survivors.managers.spawner import Spawner
from survivors.managers.player_stats import PlayerStats
from survivors.assets import play as play_sfx


class GameWindow(Window):
    def __init__(self, game, on_game_over):
        super().__init__(game, "Survivors")
        self.on_game_over = on_game_over
        self.camera = Camera(game.size)
        self.hero = None
        self.stats = None
        self.spawner = Spawner()
        self.enemies = []
        self.projectiles = []
        self.gems = []
        self.effects = []  # damage numbers
        self.particles = []
        self.grid_offset_x = 0
        self.grid_offset_y = 0

    def start(self, hero_key):
        self.spawner = Spawner()
        self.enemies.clear()
        self.projectiles.clear()
        self.gems.clear()
        self.effects.clear()
        self.particles.clear()

        stats_def = C.HERO_ROGUE_STATS if hero_key == "rogue" else C.HERO_WARRIOR_STATS
        hero_cls = SpeedRogue if hero_key == "rogue" else TankWarrior
        self.hero = hero_cls(0, 0, stats_def)
        self.hero.max_hp_current = self.hero.max_hp

        self.stats = PlayerStats(
            max_hp=stats_def["hp"],
            abilities={
                "auto": 1,
                "q": 1 if "q" in hero_key else 0,
                "e": 0,
            }
        )
        self.stats._hero_name = stats_def["name"]
        self.stats._elapsed = 0.0
        self.camera = Camera(self.game.size)

    def onUpdate(self):
        dt = 1.0 / self.game.fps
        self.stats._elapsed += dt

        # Hero update
        self.hero.update(dt, self.game.input, self.camera)

        # Ability inputs
        if self.game.input.was_key_pressed(core.K_q) or self.game.input.was_key_pressed(core.K_j):
            qfx = self.hero.try_q_ability()
            if qfx:
                if qfx["type"] == "dash":
                    self.particles.extend(spawn_death_particles(
                        self.hero.cx, self.hero.cy, C.C_CYAN, 5))
                    play_sfx("dodge")
                elif qfx["type"] == "iron_skin":
                    play_sfx("shield")
        if self.game.input.was_key_pressed(core.K_e) or self.game.input.was_key_pressed(core.K_k):
            efx = self.hero.try_e_ability()
            if efx:
                if efx["type"] == "poison":
                    play_sfx("poison")
                elif efx["type"] == "rally":
                    play_sfx("heal")

        # Rally heal tick
        if self.hero.rally_timer > 0:
            heal_per_tick = self.hero.e_ability["heal"]
            self.stats.heal(heal_per_tick)
            self.hero.rally_timer -= dt

        # Camera follow
        self.camera.follow(self.hero.cx, self.hero.cy)
        self.camera.update(dt)

        # Grid offset for scrolling background
        self.grid_offset_x = int(self.camera.offset_x) % C.GRID_SPACING
        self.grid_offset_y = int(self.camera.offset_y) % C.GRID_SPACING

        # Spawn enemies
        spawns = self.spawner.update(dt, self.hero.cx, self.hero.cy, self.camera)
        hp_m, dmg_m = self.spawner.scale()
        for etype, sx, sy in spawns:
            self.enemies.append(spawn_enemy(etype, sx, sy, hp_m, dmg_m))
            if etype == "boss":
                play_sfx("boss")

        # Update enemies
        for e in self.enemies:
            e.update(dt, self.hero)

        # Update projectiles
        for p in self.projectiles:
            p.update(dt)

        # Auto-attack
        proj_data = self.hero.try_auto_attack(self.enemies)
        if proj_data:
            if proj_data["type"] == "slam_aoe":
                self._apply_aoe(proj_data)
                self.projectiles.append(create_projectile(proj_data))
                play_sfx("slam")
            else:
                self.projectiles.append(create_projectile(proj_data))
                play_sfx("attack")

        # Collision: projectile vs enemy
        for p in self.projectiles:
            if not isinstance(p, pg.sprite.Sprite) and hasattr(p, "dmg"):
                for e in self.enemies:
                    if p.aabb_overlap(e):
                        e.take_damage(p.dmg)
                        p.kill()
                        self.particles.extend(spawn_hit_sparks(e.cx, e.cy))
                        self.effects.append(DamageNumber(e.cx, e.cy, p.dmg))
                        play_sfx("hit")
                        if hasattr(p, "poison") and p.poison:
                            self.hero.apply_poison_hit()
                            extra = self.hero.e_ability["dmg"]
                            e.take_damage(extra)
                            self.effects.append(DamageNumber(e.cx - 8, e.cy - 10, extra))
                        if not e.alive:
                            self.stats.kills += 1
                            self.particles.extend(spawn_death_particles(e.cx, e.cy, e.color))
                            self.gems.append(XPGem(e.cx, e.cy))
                            play_sfx("enemy_death")
                        break

        # Collision: enemy vs hero
        for e in self.enemies:
            if e.aabb_overlap(self.hero):
                dmg = self.stats.take_damage(e.dmg)
                self.hero.hit()
                self.effects.append(DamageNumber(self.hero.cx, self.hero.cy - 20, dmg))
                if self.stats.hp <= 0:
                    self.on_game_over()
                    return

        # Gem collection
        for gem in self.gems:
            gem.update(dt)
            dist = math.hypot(self.hero.cx - gem.x, self.hero.cy - gem.y)
            if dist < C.MAGNET_RANGE:
                # Move toward hero
                if dist > 0:
                    speed = 400
                    gem.x += (self.hero.cx - gem.x) / dist * speed * dt
                    gem.y += (self.hero.cy - gem.y) / dist * speed * dt
                if dist < 15:
                    leveled = self.stats.add_xp(gem.value)
                    gem.kill()
                    play_sfx("gem")
                    if leveled:
                        self._on_level_up()

        # Update effects
        for fx in self.effects:
            fx.update(dt)
        for p in self.particles:
            p.update(dt)

        # Cleanup dead
        self.enemies = [e for e in self.enemies if e.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]
        self.gems = [g for g in self.gems if g.alive]
        self.effects = [fx for fx in self.effects if fx.alive]
        self.particles = [p for p in self.particles if p.alive]

    def _apply_aoe(self, aoe):
        r = aoe["radius"]
        hit_any = False
        for e in self.enemies:
            dist = math.hypot(e.cx - (aoe["x"] + r), e.cy - (aoe["y"] + r))
            if dist < r:
                e.take_damage(aoe["dmg"])
                self.particles.extend(spawn_hit_sparks(e.cx, e.cy))
                self.effects.append(DamageNumber(e.cx, e.cy, aoe["dmg"]))
                hit_any = True
                if not e.alive:
                    self.stats.kills += 1
                    self.particles.extend(spawn_death_particles(e.cx, e.cy, e.color))
                    self.gems.append(XPGem(e.cx, e.cy))
                    play_sfx("enemy_death")
        if hit_any:
            play_sfx("hit")

    def _on_level_up(self):
        self.effects.append(DamageNumber(self.hero.cx, self.hero.cy - 30, f"LVL {self.stats.level}"))
        self.particles.extend(spawn_death_particles(self.hero.cx, self.hero.cy, C.C_GOLD, 12))
        play_sfx("level_up")

    def onRender(self):
        self.surface.fill(C.C_BG)
        # Grid
        self._draw_grid()
        # Gems
        for gem in self.gems:
            gem.render(self.surface, self.camera)
        # Enemies
        for e in self.enemies:
            e.render(self.surface, self.camera)
        # Projectiles
        for p in self.projectiles:
            p.render(self.surface, self.camera)
        # Hero
        self.hero.render(self.surface, self.camera)
        # Particles
        for p in self.particles:
            p.render(self.surface, self.camera)
        # Damage numbers
        for fx in self.effects:
            if isinstance(fx, DamageNumber):
                fx.render(self.surface, self.camera, self.game.font_small)
        # HUD
        self._draw_hud()

    def _draw_grid(self):
        ox = self.grid_offset_x
        oy = self.grid_offset_y
        for x in range(-ox, C.SCREEN_W + C.GRID_SPACING, C.GRID_SPACING):
            pg.draw.line(self.surface, C.C_GRID, (x, 0), (x, C.SCREEN_H))
        for y in range(-oy, C.SCREEN_H + C.GRID_SPACING, C.GRID_SPACING):
            pg.draw.line(self.surface, C.C_GRID, (0, y), (C.SCREEN_W, y))

    def _draw_hud(self):
        # HP bar
        hp_w = int(C.UI_HP_MAX_W * self.stats.hp_fraction)
        pg.draw.rect(self.surface, C.C_HP_BAR_BG,
                     (C.HUD_HP_X, C.HUD_HP_Y, C.UI_HP_MAX_W, C.UI_BAR_HEIGHT), border_radius=3)
        pg.draw.rect(self.surface, C.C_RED,
                     (C.HUD_HP_X, C.HUD_HP_Y, hp_w, C.UI_BAR_HEIGHT), border_radius=3)
        hp_text = self.game.font_small.render(f"HP {self.stats.hp}/{self.stats.max_hp}", True, C.C_WHITE)
        self.surface.blit(hp_text, (C.HUD_HP_X + C.UI_HP_MAX_W + 8, C.HUD_HP_Y + 1))

        # XP bar
        xp_w = int(C.UI_XP_MAX_W * self.stats.xp_fraction)
        pg.draw.rect(self.surface, C.C_XP_BAR_BG,
                     (C.HUD_XP_X, C.HUD_XP_Y, C.UI_XP_MAX_W, C.UI_BAR_HEIGHT), border_radius=3)
        pg.draw.rect(self.surface, C.C_PURPLE,
                     (C.HUD_XP_X, C.HUD_XP_Y, xp_w, C.UI_BAR_HEIGHT), border_radius=3)

        # Stats (top right)
        stats_lines = [
            f"LVL {self.stats.level}",
            f"Kills: {self.stats.kills}",
            self._format_time(self.stats._elapsed),
        ]
        for i, line in enumerate(stats_lines):
            s = self.game.font_small.render(line, True, C.C_LIGHT_GRAY)
            self.surface.blit(s, (C.HUD_STATS_X, C.HUD_STATS_Y + i * 16))

        # Ability icons (bottom center)
        self._draw_ability_icons()

    def _draw_ability_icons(self):
        abilities = [
            ("ATK", self.hero.auto_cooldown, self.hero.auto_ability["cooldown"], C.C_CYAN),
            ("Q", self.hero.q_cooldown, self.hero.q_ability["cooldown"], C.C_GOLD),
            ("E", self.hero.e_cooldown, self.hero.e_ability["cooldown"], C.C_GREEN),
        ]
        for i, (label, cd, max_cd, color) in enumerate(abilities):
            x = C.ab_icon_x(i)
            y = C.AB_ICON_Y
            # Background
            pg.draw.rect(self.surface, C.C_DARK_GRAY, (x, y, C.AB_ICON_SIZE, C.AB_ICON_SIZE), border_radius=4)
            pg.draw.rect(self.surface, color, (x, y, C.AB_ICON_SIZE, C.AB_ICON_SIZE), 2, border_radius=4)
            # Label
            s = self.game.font_small.render(label, True, C.C_WHITE)
            self.surface.blit(s, (x + (C.AB_ICON_SIZE - s.get_width()) // 2,
                                  y + (C.AB_ICON_SIZE - s.get_height()) // 2 - 4))
            # Cooldown overlay
            if cd > 0:
                frac = cd / max_cd
                pg.draw.rect(self.surface, (0, 0, 0, 180),
                             (x, y + C.AB_ICON_SIZE * (1 - frac),
                              C.AB_ICON_SIZE, int(C.AB_ICON_SIZE * frac)), border_radius=4)
            # Key hint
            key = ["", "Q", "E"][i]
            if key:
                ks = self.game.font_small.render(key, True, C.C_GRAY)
                self.surface.blit(ks, (x + C.AB_ICON_SIZE + 2, y + 4))

    def _format_time(self, seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}:{s:02d}"

    def on_event(self, event):
        pass