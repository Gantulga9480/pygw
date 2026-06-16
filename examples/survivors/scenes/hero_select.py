"""Hero selection — four hero cards, arrow key + Enter or click to pick."""
import pygame as pg
from pygw import Window, core
from survivors import config as C


class HeroSelectWindow(Window):
    def __init__(self, game, on_pick):
        super().__init__(game, "Select Hero")
        self.on_pick = on_pick
        self.selected = 0
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
                desc="Slow, durable\nAOE crowd control\nQ: Iron Skin\nE: Rally Heal",
                color=C.C_ORANGE,
                outline=C.C_BLACK,
                stats=("HP: 200", "SPD: 2.5", "DMG: 20"),
            ),
            dict(
                key="witch",
                name="Frost Witch",
                desc="Ranged magic\nAoE slow + freeze\nQ: Blizzard\nE: Ice Nova",
                color=(160, 100, 240),
                outline=C.C_BLACK,
                stats=("HP: 120", "SPD: 2.6", "DMG: 12"),
            ),
            dict(
                key="assassin",
                name="Shadow Assassin",
                desc="High mobility\nTeleport burst\nQ: Shadow Step\nE: Shadow Clone",
                color=C.C_PURPLE,
                outline=C.C_BLACK,
                stats=("HP: 90", "SPD: 4.0", "DMG: 18"),
            ),
        ]
        self.card_w = 180
        self.card_h = 260
        total_w = 4 * self.card_w + 3 * 16
        start_x = (C.SCREEN_W - total_w) // 2
        self._positions = []
        for i in range(4):
            x = start_x + i * (self.card_w + 16)
            self._positions.append((x, 80))

    def onUpdate(self):
        if self.game.input.was_key_pressed(core.K_LEFT):
            self.selected = max(0, self.selected - 1)
        if self.game.input.was_key_pressed(core.K_RIGHT):
            self.selected = min(len(self.heroes) - 1, self.selected + 1)
        if self.game.input.was_key_pressed(core.K_RETURN):
            self.on_pick(self.heroes[self.selected]["key"])

    def onRender(self):
        self.surface.fill(C.C_BG)
        title = self.game.font_big.render("CHOOSE HERO", True, C.C_WHITE)
        tx = (C.SCREEN_W - title.get_width()) // 2
        self.surface.blit(title, (tx, 20))
        for i, hero in enumerate(self.heroes):
            bx, by = self._positions[i]
            sel = i == self.selected
            pg.draw.rect(self.surface, C.C_DARK_GRAY, (bx, by, self.card_w, self.card_h), border_radius=6)
            border_c = hero["color"] if sel else C.C_GRAY
            pg.draw.rect(self.surface, border_c, (bx, by, self.card_w, self.card_h), 2 if sel else 1, border_radius=6)
            ix = bx + (self.card_w - 50) // 2
            iy = by + 16
            pg.draw.rect(self.surface, hero["color"], (ix, iy, 50, 60), border_radius=4)
            pg.draw.rect(self.surface, hero["outline"], (ix, iy, 50, 60), 2, border_radius=4)
            name_surf = self.game.font_medium.render(hero["name"], True, hero["color"])
            nx = bx + (self.card_w - name_surf.get_width()) // 2
            self.surface.blit(name_surf, (nx, iy + 70))
            lines = hero["desc"].split("\n")
            for j, line in enumerate(lines):
                ls = self.game.font_small.render(line, True, C.C_LIGHT_GRAY)
                lx = bx + (self.card_w - ls.get_width()) // 2
                ly = iy + 95 + j * 14
                self.surface.blit(ls, (lx, ly))
            sy = iy + 150
            for stat in hero["stats"]:
                ss = self.game.font_small.render(stat, True, C.C_GRAY)
                sx = bx + (self.card_w - ss.get_width()) // 2
                self.surface.blit(ss, (sx, sy))
                sy += 14
        hint = self.game.font_small.render("Arrow keys to select, Enter to confirm", True, C.C_GRAY)
        hx = (C.SCREEN_W - hint.get_width()) // 2
        self.surface.blit(hint, (hx, self.card_h + 90))

    def on_event(self, event):
        if event.type == core.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = self.game.input.mouse_pos
            for i, (bx, by) in enumerate(self._positions):
                if bx <= mx <= bx + self.card_w and by <= my <= by + self.card_h:
                    self.selected = i
                    self.on_pick(self.heroes[i]["key"])
