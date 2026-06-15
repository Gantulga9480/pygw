import math


class Camera:
    """Smooth-follow camera. Tracks a world position and computes screen offset."""

    def __init__(self, screen_size):
        self.screen_w, self.screen_h = screen_size
        self.target_x = 0.0
        self.target_y = 0.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.smoothing = 0.12  # Lower = smoother, higher = snappier

    def follow(self, x, y):
        self.target_x = x
        self.target_y = y

    def update(self, dt):
        # Smoothly lerp offset toward centering target on screen
        desired_x = self.target_x - self.screen_w / 2
        desired_y = self.target_y - self.screen_h / 2
        t = 1.0 - (1.0 - self.smoothing) ** (dt * 60)  # Frame-rate independent lerp
        self.offset_x += (desired_x - self.offset_x) * t
        self.offset_y += (desired_y - self.offset_y) * t

    def world_to_screen(self, wx, wy):
        return (wx - self.offset_x, wy - self.offset_y)

    def screen_to_world(self, sx, sy):
        return (sx + self.offset_x, sy + self.offset_y)

    @property
    def viewport_min(self):
        return (self.offset_x, self.offset_y)

    @property
    def viewport_max(self):
        return (self.offset_x + self.screen_w, self.offset_y + self.screen_h)

    def distance_to_viewport_center(self, wx, wy):
        cx = self.offset_x + self.screen_w / 2
        cy = self.offset_y + self.screen_h / 2
        return math.hypot(wx - cx, wy - cy)