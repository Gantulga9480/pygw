"""Main menu — Start Game, Quit buttons with hover/click interaction."""
import pygame as pg
from pygw import Window, core
from survivors import config as C


class MenuWindow(Window):
    def __init__(self, game, on_action):
        super().__init__(game, "Survivors")
        self.on_action = on_action
        self.hovered = -1  # -1 = none, 0 = start, 1 = quit
        self.buttons = [
            ("START GAME", 0),
            ("QUIT", 1),
        ]
        self.btn_w = 220
        self.btn_h = 44
        self.btn_gap = 16
        self._pre_render_buttons()

    def _pre_render_buttons(self):
        self.btn_surfs = []
        for label, _ in self.buttons:
            s = self.game.font_medium.render(label, True, C.C_BLACK)
            self.btn_surfs.append(s)

    @property
    def _btn_positions(self):
        positions = []
        total_h = len(self.buttons) * self.btn_h + (len(self.buttons) - 1) * self.btn_gap
        y_start = (C.SCREEN_H - total_h) // 2
        for i in range(len(self.buttons)):
            x = (C.SCREEN_W - self.btn_w) // 2
            y = y_start + i * (self.btn_h + self.btn_gap)
            positions.append((x, y))
        return positions

    def onUpdate(self):
        mx, my = self.game.input.mouse_pos
        self.hovered = -1
        for i, (bx, by) in enumerate(self._btn_positions):
            if bx <= mx <= bx + self.btn_w and by <= my <= by + self.btn_h:
                self.hovered = i

    def onRender(self):
        self.surface.fill(C.C_BG)
        # Title
        title = self.game.font_big.render("SURVIVORS", True, C.C_WHITE)
        tx = (C.SCREEN_W - title.get_width()) // 2
        self.surface.blit(title, (tx, 40))
        # Buttons
        for i, ((bx, by), surf) in enumerate(zip(self._btn_positions, self.btn_surfs)):
            hover = i == self.hovered
            # Button bg
            color = C.C_YELLOW if hover else C.C_DARK_GRAY
            pg.draw.rect(self.surface, color, (bx, by, self.btn_w, self.btn_h), border_radius=4)
            pg.draw.rect(self.surface, C.C_WHITE if hover else C.C_GRAY,
                         (bx, by, self.btn_w, self.btn_h), 2, border_radius=4)
            # Label
            lx = bx + (self.btn_w - surf.get_width()) // 2
            ly = by + (self.btn_h - surf.get_height()) // 2
            if not hover:
                label_surf = self.game.font_medium.render(self.buttons[i][0], True, C.C_LIGHT_GRAY)
                ly = by + (self.btn_h - label_surf.get_height()) // 2
                self.surface.blit(label_surf, (lx, ly))
            else:
                self.surface.blit(surf, (lx, ly))

    def on_event(self, event):
        if event.type == core.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered >= 0:
                action = self.buttons[self.hovered][1]
                self.on_action("start" if action == 0 else "quit")