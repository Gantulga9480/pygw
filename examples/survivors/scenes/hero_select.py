"""Hero selection — two hero cards, arrow key + Enter or click to pick."""
import pygame as pg
from pygw import Window, core
from survivors import config as C


class HeroSelectWindow(Window):
    def __init__(self, game, on_pick):
        super().__init__(game, "Select Hero")
        self.on_pick = on_pick
        self.selected = 0  # 0 = rogue, 1 = warrior
        self.heroes = [
            dict(
                key="rogue",
                name="Speed Rogue",
                desc="Fast, glass cannon\nSingle-target focus\nQ: Shadow Dash\nE: Poison Blade",
                color=C.C_CYAN,
                outline=C.C_BLACK,
                stats=("HP: 100", "SPD: 4.0", "DMG: 15"),
            ),
            dict(
                key="warrior",
                name="Tank Warrior",
                desc="Slow, durable\nAOE crowd control\nQ: Iron Skin\nE: Rally",
                color=C.C_ORANGE,
                outline=C.C_BLACK,
                stats=("HP: 200", "SPD: 2.5", "DMG: 20"),
            ),
        ]
        self.card_w = 260
        self.card_h = 280
        self._positions = [
            ((C.SCREEN_W - 2 * self.card_w - 30) // 2, 80),
            ((C.SCREEN_W - 2 * self.card_w - 30) // 2 + self.card_w + 30, 80),
        ]

    def onUpdate(self):
        if self.game.input.was_key_pressed(core.K_LEFT):
            self.selected = max(0, self.selected - 1)
        if self.game.input.was_key_pressed(core.K_RIGHT):
            self.selected = min(len(self.heroes) - 1, self.selected + 1)
        if self.game.input.was_key_pressed(core.K_RETURN):
            self.on_pick(self.heroes[self.selected]["key"])

    def onRender(self):
        self.surface.fill(C.C_BG)
        # Title
        title = self.game.font_big.render("CHOOSE HERO", True, C.C_WHITE)
        tx = (C.SCREEN_W - title.get_width()) // 2
        self.surface.blit(title, (tx, 20))
        # Cards
        for i, hero in enumerate(self.heroes):
            bx, by = self._positions[i]
            sel = i == self.selected
            # Card bg
            pg.draw.rect(self.surface, C.C_DARK_GRAY, (bx, by, self.card_w, self.card_h), border_radius=6)
            border_c = hero["color"] if sel else C.C_GRAY
            pg.draw.rect(self.surface, border_c, (bx, by, self.card_w, self.card_h), 2 if sel else 1, border_radius=6)
            # Hero icon (simple colored rectangle as placeholder)
            ix = bx + (self.card_w - 60) // 2
            iy = by + 16
            pg.draw.rect(self.surface, hero["color"], (ix, iy, 60, 70), border_radius=4)
            pg.draw.rect(self.surface, hero["outline"], (ix, iy, 60, 70), 2, border_radius=4)
            # Name
            name_surf = self.game.font_medium.render(hero["name"], True, hero["color"])
            nx = bx + (self.card_w - name_surf.get_width()) // 2
            self.surface.blit(name_surf, (nx, iy + 80))
            # Description
            lines = hero["desc"].split("\n")
            for j, line in enumerate(lines):
                ls = self.game.font_small.render(line, True, C.C_LIGHT_GRAY)
                lx = bx + (self.card_w - ls.get_width()) // 2
                ly = iy + 110 + j * 14
                self.surface.blit(ls, (lx, ly))
            # Stats
            sy = iy + 170
            for stat in hero["stats"]:
                ss = self.game.font_small.render(stat, True, C.C_GRAY)
                sx = bx + (self.card_w - ss.get_width()) // 2
                self.surface.blit(ss, (sx, sy))
                sy += 14
        # Hint
        hint = self.game.font_small.render("Arrow keys to select, Enter to confirm", True, C.C_GRAY)
        hx = (C.SCREEN_W - hint.get_width()) // 2
        self.surface.blit(hint, (hx, self.card_h + 110))

    def on_event(self, event):
        if event.type == core.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = self.game.input.mouse_pos
            for i, (bx, by) in enumerate(self._positions):
                if bx <= mx <= bx + self.card_w and by <= my <= by + self.card_h:
                    self.selected = i
                    self.on_pick(self.heroes[i]["key"])