"""Intro screen — animated title with tagline, auto-advances after delay."""
import pygame as pg
from pygw import Window, core
from survivors import config as C


class IntroWindow(Window):
    def __init__(self, game, on_done):
        super().__init__(game, "Survivors")
        self.on_done = on_done
        self.elapsed = 0.0
        self.duration = 2.5
        self.ready = False
        self.title_surf = self.game.font_big.render("SURVIVORS", True, C.C_WHITE)
        self.sub_surf = self.game.font_medium.render("How long can you last?", True, C.C_LIGHT_GRAY)

    def onUpdate(self):
        self.elapsed += 1.0 / self.game.fps
        if self.elapsed >= self.duration and not self.ready:
            self.ready = True
            self.sub_surf = self.game.font_medium.render("Press ENTER to continue", True, C.C_YELLOW)

        if self.ready and self.game.input.was_key_pressed(core.K_RETURN):
            self.on_done()

    def onRender(self):
        self.surface.fill(C.C_BG)
        # Center title
        tx = (C.SCREEN_W - self.title_surf.get_width()) // 2
        ty = (C.SCREEN_H - self.title_surf.get_height()) // 2 - 30
        self.surface.blit(self.title_surf, (tx, ty))
        # Subtitle
        sx = (C.SCREEN_W - self.sub_surf.get_width()) // 2
        sy = ty + self.title_surf.get_height() + 20
        self.surface.blit(self.sub_surf, (sx, sy))

    def on_event(self, event):
        pass