"""Placeholder game over screen — shows stats, returns to menu or quits."""
import pygame as pg
from pygw import Window, core
from survivors import config as C


class GameOverWindow(Window):
    def __init__(self, game, on_action):
        super().__init__(game, "Game Over")
        self.on_action = on_action
        self.stats = None
        self.hovered = -1

    def show(self, stats, hero_key):
        self.stats = stats

    def onUpdate(self):
        mx, my = self.game.input.mouse_pos
        self.hovered = -1
        btns = self._get_buttons()
        for i, (bx, by, bw, bh) in enumerate(btns):
            if bx <= mx <= bx + bw and by <= my <= by + bh:
                self.hovered = i

    def _get_buttons(self):
        btn_w = 200
        btn_h = 44
        gap = 16
        total_h = 2 * btn_h + gap
        y_start = 300
        return [
            ((C.SCREEN_W - btn_w) // 2, y_start, btn_w, btn_h),
            ((C.SCREEN_W - btn_w) // 2, y_start + btn_h + gap, btn_w, btn_h),
        ]

    def onRender(self):
        self.surface.fill(C.C_BG)
        # Title
        title = self.game.font_big.render("GAME OVER", True, C.C_RED)
        tx = (C.SCREEN_W - title.get_width()) // 2
        self.surface.blit(title, (tx, 80))
        # Stats
        if self.stats:
            lines = [
                f"Hero: {self.stats._hero_name}",
                f"Level: {self.stats.level}",
                f"Kills: {self.stats.kills}",
                f"Time: {self._format_time(self.stats._elapsed)}",
            ]
            for i, line in enumerate(lines):
                ls = self.game.font_medium.render(line, True, C.C_LIGHT_GRAY)
                lx = (C.SCREEN_W - ls.get_width()) // 2
                ly = 140 + i * 28
                self.surface.blit(ls, (lx, ly))
        # Buttons
        labels = ["MAIN MENU", "QUIT"]
        for i, ((bx, by, bw, bh), label) in enumerate(zip(self._get_buttons(), labels)):
            hover = i == self.hovered
            pg.draw.rect(self.surface, C.C_YELLOW if hover else C.C_DARK_GRAY,
                         (bx, by, bw, bh), border_radius=4)
            pg.draw.rect(self.surface, C.C_WHITE if hover else C.C_GRAY,
                         (bx, by, bw, bh), 2, border_radius=4)
            ls = self.game.font_medium.render(label, True, C.C_BLACK if hover else C.C_LIGHT_GRAY)
            lx = bx + (bw - ls.get_width()) // 2
            ly = by + (bh - ls.get_height()) // 2
            self.surface.blit(ls, (lx, ly))

    def _format_time(self, seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}:{s:02d}"

    def on_event(self, event):
        if event.type == core.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered == 0:
                self.on_action("menu")
            elif self.hovered == 1:
                self.on_action("quit")
        if event.type == core.KEYDOWN:
            if event.key == core.K_RETURN:
                self.on_action("menu")