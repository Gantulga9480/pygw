"""Simple AABB and circle collision helpers."""
import math


def aabb(ax, ay, aw, ah, bx, by, bw, bh):
    """Check AABB overlap between two rectangles."""
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def circle_overlap(x1, y1, r1, x2, y2, r2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2 <= (r1 + r2) ** 2


def point_in_rect(px, py, rx, ry, rw, rh):
    return rx <= px <= rx + rw and ry <= py <= ry + rh


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def lerp(a, b, t):
    return a + (b - a) * t