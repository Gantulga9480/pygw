import pygame as pg


class Entity:
    """Base entity with world position, size, rendering, and lifecycle."""

    def __init__(self, x, y, w, h, color):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.color = color
        self.outline = (0, 0, 0)
        self.alive = True
        self.flash_timer = 0.0
        self.vx = 0.0
        self.vy = 0.0

    # ---- AABB helpers ----
    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def aabb_overlap(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)

    def point_inside(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def distance_to(self, other):
        return ((self.cx - other.cx) ** 2 + (self.cy - other.cy) ** 2) ** 0.5

    # ---- Movement ----
    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    # ---- Flash (hit effect) ----
    def hit(self):
        self.flash_timer = 0.1

    # ---- Lifecycle (override in subclasses) ----
    def update(self, dt):
        if self.flash_timer > 0:
            self.flash_timer -= dt

    def render(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        rect = pg.Rect(sx, sy, self.w, self.h)
        color = C_WHITE if self.flash_timer > 0 else self.color
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, self.outline, rect, 1)

    def kill(self):
        self.alive = False