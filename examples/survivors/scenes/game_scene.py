"""Main gameplay window — camera, entities, combat, HUD."""
import math
import random
import pygame as pg
from pygw import Window, core
from survivors import config as C
from survivors.camera import Camera
from survivors.entities.hero import SpeedRogue, TankWarrior, FrostWitch, ShadowAssassin
from survivors.entities.clone import ShadowClone
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
        self.upgrade_overlay_active = False
        self.selected_upgrade = []
        self.selected_card = -1
        self.hovered_card = -1
        self.overlay_timer = 0.0

    def start(self, hero_key):
        self.spawner = Spawner()
        self.enemies.clear()
        self.projectiles.clear()
        self.gems.clear()
        self.effects.clear()
        self.particles.clear()
        self.clones = []
        self.blizzard_timer = 0.0
        self.blizzard_total = 0.0
        self.blizzard_radius = 0
        self.upgrade_overlay_active = False
        self.selected_upgrade = []
        self.selected_card = -1
        self.hovered_card = -1
        self.overlay_timer = 0.0

        stats_def = {"rogue": C.HERO_ROGUE_STATS, "warrior": C.HERO_WARRIOR_STATS, "witch": C.HERO_WITCH_STATS, "assassin": C.HERO_ASSASSIN_STATS}[hero_key]
        hero_cls = {"rogue": SpeedRogue, "warrior": TankWarrior, "witch": FrostWitch, "assassin": ShadowAssassin}[hero_key]
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

        if self.upgrade_overlay_active:
            self.overlay_timer += dt
            return

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
                    self.stats.active_effects["iron_skin"] = qfx["duration"]
                    play_sfx("shield")
                elif qfx["type"] == "blizzard":
                    self.blizzard_timer = qfx["duration"]
                    self.blizzard_total = qfx["duration"]
                    self.blizzard_radius = qfx.get("radius", 120)
                    play_sfx("slam")
                elif qfx["type"] == "shadow_step":
                    target = self.hero._find_nearest_enemy(self.enemies)
                    if target:
                        dx = target.cx - self.hero.cx
                        dy = target.cy - self.hero.cy
                        dist = math.hypot(dx, dy) or 1
                        range_val = qfx["target_range"]
                        self.hero.x += (dx / dist) * range_val
                        self.hero.y += (dy / dist) * range_val
                        self.hero.invincible = 0.2
                        self.hero.x = max(0, self.hero.x)
                        self.hero.y = max(0, self.hero.y)
                        # Apply burst damage
                        step_dmg = qfx.get("dmg", 30)
                        target.take_damage(step_dmg)
                        self.effects.append(DamageNumber(target.cx, target.cy, step_dmg))
                        if qfx.get("crit"):
                            self.effects.append(DamageNumber(target.cx, target.cy - 6, "!", color=C.C_GOLD))
                        if not target.alive:
                            self._on_enemy_kill(target)
                        self.particles.extend(spawn_death_particles(
                            self.hero.cx, self.hero.cy, C.C_PURPLE, 8))
                        play_sfx("dodge")
        if self.game.input.was_key_pressed(core.K_e) or self.game.input.was_key_pressed(core.K_k):
            efx = self.hero.try_e_ability()
            if efx:
                if efx["type"] == "poison":
                    play_sfx("poison")
                elif efx["type"] == "rally":
                    play_sfx("heal")
                elif efx["type"] == "ice_nova":
                    self._apply_aoe(efx)
                    # Slow enemies in range
                    nova_radius = efx.get("hit_radius", 100)
                    for e in self.enemies:
                        if e.alive and math.hypot(e.cx - self.hero.cx, e.cy - self.hero.cy) < nova_radius:
                            e.apply_slow(2.0, 0.6)
                    self.projectiles.append(create_projectile(efx))
                    play_sfx("slam")
                elif efx["type"] == "shadow_clone":
                    for i in range(efx["clone_count"]):
                        clone_x = self.hero.x + (i - (efx["clone_count"] - 1) / 2) * 40
                        clone_y = self.hero.y
                        clone = ShadowClone(clone_x, clone_y, efx["duration"],
                                           efx["clone_dmg_ratio"], self.hero)
                        self.clones.append(clone)
                    play_sfx("shield")

 # Rally heal tick (per second, scaled by dt)
        if self.hero.rally_timer > 0:
            heal_per_tick = self.hero.e_ability["heal"]
            self.stats.heal(heal_per_tick * dt)
            self.hero.rally_timer -= dt
        # Blizzard damage tick (per second, scaled by dt)
        if self.blizzard_timer > 0:
            for e in self.enemies:
                dist = math.hypot(e.cx - self.hero.cx, e.cy - self.hero.cy)
                if dist < self.blizzard_radius:
                    e.take_damage(self.hero.q_ability["dmg"])
                    if not e.alive:
                        self._on_enemy_kill(e)
            self.blizzard_timer -= dt

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
        # Update clones
        for c in self.clones:
            c.update(dt)

        # Auto-attack
        proj_data = self.hero.try_auto_attack(self.enemies)
        if proj_data:
            proj_list = proj_data if isinstance(proj_data, list) else [proj_data]
            for p in proj_list:
                if p["type"] == "slam_aoe":
                    self._apply_aoe(p)
                    self.projectiles.append(create_projectile(p))
                    play_sfx("slam")
                else:
                    self.projectiles.append(create_projectile(p))
                    play_sfx("attack")
        # Clone auto-attack
        for c in self.clones:
            if c.alive and not c.attack_on_cooldown:
                target = c._find_nearest_enemy(self.enemies)
                if target:
                    c.attack_on_cooldown = 1.0
                    proj = c._create_auto_attack(target)
                    if proj:
                        self.projectiles.append(proj)
                        play_sfx("attack")
            else:
                c.attack_on_cooldown -= dt

        # Collision: projectile vs enemy
        for p in self.projectiles:
            if not isinstance(p, pg.sprite.Sprite) and hasattr(p, "dmg"):
                for e in self.enemies:
                    if p.aabb_overlap(e):
                        dmg = p.dmg
                        is_crit = getattr(p, "crit", False)
                        if is_crit:
                            dmg *= 2
                        # Executioner
                        if e.hp > 0 and e.max_hp > 0:
                            if e.hp / e.max_hp <= self.hero.effective_executioner_threshold:
                                dmg = int(dmg * self.hero.effective_executioner_mult)
    # Siphon bonus damage
                        siphon_dmg = max(1, int(dmg * self.hero.effective_siphon_dmg)) if self.hero.effective_siphon_dmg > 0 else 0
                        if siphon_dmg > 0:
                            dmg += siphon_dmg
                        e.take_damage(dmg)
                        if is_crit:
                            self.effects.append(DamageNumber(e.cx, e.cy - 6, f"{dmg}!"))
                        else:
                            self.effects.append(DamageNumber(e.cx, e.cy, dmg))
                        self.particles.extend(spawn_hit_sparks(e.cx, e.cy))
                        play_sfx("hit")
                        if hasattr(p, "slow") and p.slow:
                            e.apply_slow(2.0, 0.6)
                            self.effects.append(DamageNumber(e.cx, e.cy + 10, "SLOW", color=(140, 200, 255)))
                            p.dmg = int(p.dmg * 0.7)
                            p.bounces -= 1
                            if p.bounces <= 0:
                                p.kill()
                        else:
                            p.kill()
                        if hasattr(p, "poison") and p.poison:
                            self.hero.apply_poison_hit()
                            extra = self.hero.effective_poison_dmg
                            e.take_damage(extra)
                            self.effects.append(DamageNumber(e.cx - 8, e.cy - 10, extra))
                        # Passive: Lifesteal + Siphon heal
                        if self.hero.effective_lifesteal > 0:
                            heal = self.hero.apply_lifesteal(dmg)
                            if heal > 0:
                                self.effects.append(DamageNumber(e.cx, e.cy + 10, f"+{heal}", color=C.C_GREEN))
                        if self.hero.effective_siphon_heal > 0:
                            siphon_heal = int(self.hero.effective_siphon_heal)
                            self.hero.hp_current = min(self.hero.max_hp, self.hero.hp_current + siphon_heal)
                            self.effects.append(DamageNumber(e.cx + 10, e.cy + 10, f"+{siphon_heal}", color=C.C_GREEN))
                        if not e.alive:
                            self._on_enemy_kill(e)
                        break

        # Collision: enemy vs hero
        for e in self.enemies:
            if e.aabb_overlap(self.hero) and e.attack_cooldown <= 0:
                # Evasion check
                if self.hero.check_evasion():
                    self.effects.append(DamageNumber(self.hero.cx, self.hero.cy - 20, "DODGE"))
                    e.attack_cooldown = e.attack_interval
                    continue
                dmg = self.stats.take_damage(e.dmg, armor=self.hero.effective_armor)
                self.hero.hit()
                self.effects.append(DamageNumber(self.hero.cx, self.hero.cy - 20, dmg))
                # Armor visual feedback
                if self.hero.effective_armor > 0:
                    self.effects.append(DamageNumber(self.hero.cx, self.hero.cy - 10, f"-{self.hero.effective_armor}", color=C.C_GRAY))
                # Thorns reflection
                thorns = self.hero.get_thorns()
                if thorns > 0:
                    e.take_damage(thorns)
                    self.effects.append(DamageNumber(e.cx, e.cy, f"THN {thorns}"))
                    if not e.alive:
                        self._on_enemy_kill(e)
                e.attack_cooldown = e.attack_interval
                if self.stats.hp <= 0:
                    self.on_game_over()
                    return

        # Gem collection
        for gem in self.gems:
            gem.update(dt)
            dist = math.hypot(self.hero.cx - gem.x, self.hero.cy - gem.y)
            if dist < self.hero.effective_magnet_range:
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

    def _on_enemy_kill(self, e):
        self.stats.kills += 1
        self.hero.register_kill()
        # Frenzy visual
        if self.hero.effective_frenzy_bonus > 0:
            self.effects.append(DamageNumber(e.cx, e.cy - 12, f"FRENZY +{self.hero._frenzy_stacks}", color=C.C_ORANGE))
        if self.hero.effective_second_wind > 0:
            self.hero.apply_second_wind()
        if self.hero.effective_replenish > 0:
            factor = self.hero.effective_replenish
            self.hero.auto_cooldown *= (1 - factor)
            self.hero.q_cooldown *= (1 - factor)
            self.hero.e_cooldown *= (1 - factor)
            self.effects.append(DamageNumber(e.cx, e.cy - 22, f"CD -{int(factor * 100)}%", color=C.C_PURPLE))
        self.particles.extend(spawn_death_particles(e.cx, e.cy, e.color))
        self.gems.append(XPGem(e.cx, e.cy))
        play_sfx("enemy_death")

    def _apply_aoe(self, aoe):
        hit_radius = aoe.get("hit_radius", aoe.get("radius"))
        hit_any = False
        for e in self.enemies:
            dist = math.hypot(e.cx - aoe["cx"], e.cy - aoe["cy"])
            if dist < hit_radius:
                dmg = aoe["dmg"]
                is_crit = aoe.get("crit", False)
                if is_crit:
                    dmg *= 2
                if e.hp > 0 and e.max_hp > 0:
                    if e.hp / e.max_hp <= self.hero.effective_executioner_threshold:
                        dmg = int(dmg * self.hero.effective_executioner_mult)
                if self.hero.effective_siphon_dmg > 0:
                    dmg += max(1, int(dmg * self.hero.effective_siphon_dmg))
                e.take_damage(dmg)
                self.hero.apply_lifesteal(dmg)
                self.particles.extend(spawn_hit_sparks(e.cx, e.cy))
                if is_crit:
                    self.effects.append(DamageNumber(e.cx, e.cy - 6, f"{dmg}!"))
                else:
                    self.effects.append(DamageNumber(e.cx, e.cy, dmg))
                hit_any = True
                if not e.alive:
                    self._on_enemy_kill(e)
        if hit_any:
            play_sfx("hit")

    def _on_level_up(self):
        self.effects.append(DamageNumber(self.hero.cx, self.hero.cy - 30, f"LVL {self.stats.level}"))
        self.particles.extend(spawn_death_particles(self.hero.cx, self.hero.cy, C.C_GOLD, 12))
        play_sfx("level_up")
        self._start_upgrade_overlay()

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
        # Upgrade overlay
        if self.upgrade_overlay_active:
            self._draw_upgrade_overlay()

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
        hp_text = self.game.font_small.render(f"HP {int(self.stats.hp)}/{self.stats.max_hp}", True, C.C_WHITE)
        self.surface.blit(hp_text, (C.HUD_HP_X + C.UI_HP_MAX_W + 8, C.HUD_HP_Y + 1))

        # XP bar
        xp_w = int(C.UI_XP_MAX_W * self.stats.xp_fraction)
        pg.draw.rect(self.surface, C.C_XP_BAR_BG,
                     (C.HUD_XP_X, C.HUD_XP_Y, C.UI_XP_MAX_W, C.UI_BAR_HEIGHT), border_radius=3)
        pg.draw.rect(self.surface, C.C_PURPLE,
                     (C.HUD_XP_X, C.HUD_XP_Y, xp_w, C.UI_BAR_HEIGHT), border_radius=3)

        # Stats (top right)
        lvl_text = f"LVL {self.stats.level}"
        if self.stats.total_upgrades > 0:
            lvl_text += f" \u2B06{self.stats.total_upgrades}"
        stats_lines = [
            lvl_text,
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
            ("ATK", self.hero.auto_cooldown, self.hero.effective_atk_speed, C.C_CYAN),
            ("Q", self.hero.q_cooldown, self.hero.effective_q_cd, C.C_GOLD),
            ("E", self.hero.e_cooldown, self.hero.effective_e_cd, C.C_GREEN),
        ]
        for i, (label, cd, max_cd, color) in enumerate(abilities):
            x = C.ab_icon_x(i)
            y = C.AB_ICON_Y
            # Background
            pg.draw.rect(self.surface, C.C_DARK_GRAY, (x, y, C.AB_ICON_SIZE, C.AB_ICON_SIZE), border_radius=4)
            # Label (always visible on top of background)
            s = self.game.font_small.render(label, True, C.C_WHITE)
            self.surface.blit(s, (x + (C.AB_ICON_SIZE - s.get_width()) // 2,
                                  y + (C.AB_ICON_SIZE - s.get_height()) // 2 - 4))
            # Cooldown overlay (semi-transparent, drawn above label)
            if cd > 0:
                frac = cd / max_cd
                overlay_h = int(C.AB_ICON_SIZE * frac)
                overlay_y = y + C.AB_ICON_SIZE - overlay_h
                if overlay_h > 0:
                    overlay_surf = pg.Surface((C.AB_ICON_SIZE, overlay_h), pg.SRCALPHA)
                    pg.draw.rect(overlay_surf, (0, 0, 0, 140),
                                 (0, 0, C.AB_ICON_SIZE, overlay_h), border_radius=0)
                    self.surface.blit(overlay_surf, (x, overlay_y))
            # Border on top of everything
            pg.draw.rect(self.surface, color, (x, y, C.AB_ICON_SIZE, C.AB_ICON_SIZE), 2, border_radius=4)

    def _format_time(self, seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}:{s:02d}"

    def _start_upgrade_overlay(self):
        self.upgrade_overlay_active = True
        self.selected_card = -1
        self.hovered_card = -1
        self.overlay_timer = 0.0
        pool = self._get_available_upgrades()
        count = min(3, len(pool))
        if count > 0:
            indices = list(range(len(pool)))
            random.shuffle(indices)
            self.selected_upgrade = [pool[i] for i in indices[:count]]
        else:
            self.selected_upgrade = []
        play_sfx("select")

    def _get_available_upgrades(self):
        cls_name = self.hero.__class__.__name__.lower()
        if "rogue" in cls_name:
            hero_short = "rogue"
        elif "warrior" in cls_name:
            hero_short = "warrior"
        elif "witch" in cls_name:
            hero_short = "witch"
        elif "assassin" in cls_name:
            hero_short = "assassin"
        else:
            hero_short = "rogue"

        # Passive stat keys: if > 0, hero already has that passive
        passive_keys = {
            "crit_chance": "crit", "lifesteal": "lifesteal", "evasion": "evasion",
            "thorns": "thorns", "siphon_dmg": "siphon", "frenzy_per_kill": "frenzy",
            "armor": "armor", "replenish": "replenish", "second_wind": "second_wind",
            "executioner_mult": "executioner",
        }

        available = []
        for u in C.UPGRADES:
            if self.stats.level < u.get("min_level", 1):
                continue
            if "hero_filter" in u and not u["hero_filter"](hero_short):
                continue
            # Exclude already-owned passives (status upgrades can reappear)
            if "passive" in u:
                for stat_key, passive_id in passive_keys.items():
                    if passive_id == u["passive"] and self.hero.upgrade_data.get(stat_key, 0) > 0:
                        break
                else:
                    available.append(u)
            else:
                for _ in range(u["weight"]):
                    available.append(u)
        return available

    def _draw_upgrade_overlay(self):
        alpha = min(self.overlay_timer * 3, 0.6)
        dim = pg.Surface((C.SCREEN_W, C.SCREEN_H), pg.SRCALPHA)
        dim.fill((0, 0, 0, int(255 * alpha)))
        self.surface.blit(dim, (0, 0))

        title = self.game.font_medium.render("LEVEL UP!", True, C.C_GOLD)
        tx = (C.SCREEN_W - title.get_width()) // 2
        self.surface.blit(title, (tx, 40))

        total_w = 3 * C.UPGRADE_CARD_W + 2 * C.UPGRADE_CARD_PAD
        start_x = (C.SCREEN_W - total_w) // 2
        card_y = 100

        for i, upgrade in enumerate(self.selected_upgrade):
            cx = start_x + i * (C.UPGRADE_CARD_W + C.UPGRADE_CARD_PAD)
            cy = card_y
            cw = C.UPGRADE_CARD_W
            ch = C.UPGRADE_CARD_H
            border_color = C.RARITY_BORDERS.get(upgrade["rarity"], C.C_GRAY)
            bg_color = (60, 60, 80) if i == self.hovered_card else C.C_DARK_GRAY
            pg.draw.rect(self.surface, bg_color, (cx, cy, cw, ch), border_radius=C.UPGRADE_CARD_RADIUS)
            border_w = 2 if i == self.selected_card else 1
            pg.draw.rect(self.surface, border_color, (cx, cy, cw, ch), border_w, border_radius=C.UPGRADE_CARD_RADIUS)

            if i == self.selected_card:
                tick = self.game.font_small.render("\u2713", True, C.C_GREEN)
                self.surface.blit(tick, (cx + cw - 24, cy + 4))

            rarity_label = upgrade["rarity"].upper()
            rtag = self.game.font_small.render(rarity_label, True, border_color)
            self.surface.blit(rtag, (cx + 8, cy + 8))

            name_surf = self.game.font_medium.render(upgrade["name"], True, C.C_WHITE)
            nx = cx + (cw - name_surf.get_width()) // 2
            self.surface.blit(name_surf, (nx, cy + 28))

            desc_surf = self.game.font_small.render(upgrade["desc"], True, C.C_LIGHT_GRAY)
            dx = cx + (cw - desc_surf.get_width()) // 2
            self.surface.blit(desc_surf, (dx, cy + 60))

            key_hint = self.game.font_small.render(f"[{i + 1}]", True, C.C_GRAY)
            self.surface.blit(key_hint, (cx + 8, cy + ch - 20))

        hint = self.game.font_small.render("Press 1/2/3 or click to select, Esc to skip", True, C.C_GRAY)
        hx = (C.SCREEN_W - hint.get_width()) // 2
        self.surface.blit(hint, (hx, C.SCREEN_H - 40))

    def _pick_upgrade(self, index):
        if index < 0 or index >= len(self.selected_upgrade):
            return
        upgrade = self.selected_upgrade[index]
        self.hero.apply_upgrade(upgrade, self.stats)
        self.stats.record_upgrade()
        play_sfx("select")
        self.upgrade_overlay_active = False

    def on_event(self, event):
        if self.upgrade_overlay_active:
            if event.type == core.MOUSEMOTION:
                mx, my = self.game.input.mouse_pos
                total_w = 3 * C.UPGRADE_CARD_W + 2 * C.UPGRADE_CARD_PAD
                start_x = (C.SCREEN_W - total_w) // 2
                self.hovered_card = -1
                for i in range(len(self.selected_upgrade)):
                    cx = start_x + i * (C.UPGRADE_CARD_W + C.UPGRADE_CARD_PAD)
                    if cx <= mx <= cx + C.UPGRADE_CARD_W and 100 <= my <= 100 + C.UPGRADE_CARD_H:
                        self.hovered_card = i

            if event.type == core.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered_card >= 0:
                    self._pick_upgrade(self.hovered_card)

            if event.type == core.KEYDOWN:
                if event.key in (core.K_1, core.K_2, core.K_3):
                    self._pick_upgrade(event.key - core.K_1)
                elif event.key == core.K_ESCAPE:
                    self.upgrade_overlay_active = False