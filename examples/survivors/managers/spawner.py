"""Enemy spawner: schedules spawns, difficulty scaling, boss intervals."""
import random
import math
from survivors import config as C


class Spawner:
    def __init__(self):
        self.elapsed = 0.0
        self.spawn_timer = 0.0
        self.boss_timer = C.BOSS_INTERVAL
        self.pending = []  # list of (enemy_type, x, y) to spawn this frame

    def update(self, dt, hero_x, hero_y, camera):
        self.elapsed += dt
        self.pending.clear()

        # Determine spawn interval (ramps down over time)
        t = min(self.elapsed / C.SPAWN_INTERVAL_RAMP_TIME, 1.0)
        self._interval = C.SPAWN_BASE_INTERVAL - (C.SPAWN_BASE_INTERVAL - C.SPAWN_MIN_INTERVAL) * t

        # Regular spawn
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = self._interval
            etype = self._pick_enemy_type()
            sx, sy = self._spawn_position(hero_x, hero_y, camera)
            self.pending.append((etype, sx, sy))

        # Boss spawn
        self.boss_timer -= dt
        if self.boss_timer <= 0:
            self.boss_timer = C.BOSS_INTERVAL
            sx, sy = self._spawn_position(hero_x, hero_y, camera)
            self.pending.append(("boss", sx, sy))

        return self.pending

    def _pick_enemy_type(self):
        r = random.random()
        minutes = self.elapsed / 60.0

        if self.elapsed > C.ENEMY_UNLOCK_BRUTE and r < 0.15:
            return "brute"
        if self.elapsed > C.ENEMY_UNLOCK_RUNNER and r < 0.45:
            return "runner"
        return "zombie"

    def _spawn_position(self, hero_x, hero_y, camera):
        """Spawn outside camera viewport, in a random direction."""
        angle = random.uniform(0, 2 * math.pi)
        margin = 60
        dist = max(camera.screen_w, camera.screen_h) / 2 + margin
        cx = camera.offset_x + camera.screen_w / 2
        cy = camera.offset_y + camera.screen_h / 2
        return (cx + math.cos(angle) * dist, cy + math.sin(angle) * dist)

    def scale(self):
        """Difficulty multiplier based on elapsed minutes."""
        minutes = self.elapsed / 60.0
        hp_mult = 1.0 + C.HP_SCALE_PER_MIN * minutes
        dmg_mult = 1.0 + C.DMG_SCALE_PER_MIN * minutes
        return hp_mult, dmg_mult