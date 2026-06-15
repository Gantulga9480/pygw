from __future__ import annotations

from pygw import Game, Scene, Window, core


class MainMenu(Scene):

    def __init__(self, parent, size, position):
        super().__init__(parent, size, position)
        self.active_window_name = "Menu"

    def onUpdate(self):
        pass

    def onRender(self):
        if self.surface is None:
            return
        self.surface.fill((30, 30, 60))

        font = core.font.SysFont("monospace", 36, bold=True)
        small_font = core.font.SysFont("monospace", 20)

        title = font.render("WINDOW MANAGER DEMO", True, (100, 200, 255))
        self.surface.blit(title, (20, 30))

        info = small_font.render(f"Active: {self.active_window_name}", True, (255, 255, 100))
        self.surface.blit(info, (20, 90))

        y = 130
        instructions = [
            ("1", "Switch to Game Window"),
            ("2", "Switch to Color Window"),
            ("3", "Switch Back to Menu"),
            ("ESC", "Exit"),
        ]
        for key, action in instructions:
            key_surf = small_font.render(key, True, (255, 200, 50))
            action_surf = small_font.render(action, True, (200, 200, 255))
            self.surface.blit(key_surf, (20, y))
            self.surface.blit(action_surf, (55, y))
            y += 28


class GameScene(Scene):

    def __init__(self, parent, size, position, game_state):
        super().__init__(parent, size, position)
        self.game_state = game_state
        self.ball_x = 150
        self.ball_y = 150
        self.dx = 3
        self.dy = 3

    def onUpdate(self):
        if self.game_state.active == 1:
            self.ball_x += self.dx
            self.ball_y += self.dy
            w, h = self.game_state.size
            if self.ball_x < 20 or self.ball_x > w - 20:
                self.dx = -self.dx
            if self.ball_y < 20 or self.ball_y > h - 20:
                self.dy = -self.dy

    def onRender(self):
        if self.surface is None:
            return
        self.surface.fill((20, 40, 20))
        core.draw.circle(self.surface, (100, 255, 100), (int(self.ball_x), int(self.ball_y)), 20)
        core.draw.circle(self.surface, (200, 255, 200), (int(self.ball_x) - 5, int(self.ball_y) - 5), 8)


class ColorScene(Scene):

    def __init__(self, parent, size, position):
        super().__init__(parent, size, position)
        self.hue = 0

    def onUpdate(self):
        if self.game_state.active == 2:
            self.hue = (self.hue + 1) % 360

    def onRender(self):
        if self.surface is None:
            return
        r = int(128 + 127 * ((self.hue / 60) % 6 - 1))
        g = int(128 + 127 * ((self.hue / 120 + 2) % 6 - 1))
        b = int(128 + 127 * ((self.hue / 60 + 4) % 6 - 1))
        self.surface.fill((max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))))
        font = core.font.SysFont("monospace", 24, bold=True)
        text = font.render(f"Hue: {self.hue}", True, (255, 255, 255))
        self.surface.blit(text, (50, 80))


class WindowDemo(Game):

    def __init__(self):
        super().__init__()
        self.title = "Window Manager Demo"
        self.size = (350, 280)
        self._game_state = type('GameState', (), {'active': 0, 'size': self.size})()
        self._menu_scene = None

    def setup(self):
        menu_win = Window(self, "Menu")
        self._menu_scene = MainMenu(menu_win, self.size, (0, 0))
        self._menu_scene.active_window_name = "Menu"
        menu_win.add_child(self._menu_scene)
        self.add_window(menu_win)

        game_win = Window(self, "Game")
        game_scene = GameScene(game_win, self.size, (0, 0), self._game_state)
        game_win.add_child(game_scene)
        self.add_window(game_win)

        color_win = Window(self, "Color")
        self._color_scene = ColorScene(color_win, self.size, (0, 0))
        self._color_scene.game_state = self._game_state
        color_win.add_child(self._color_scene)
        self.add_window(color_win)

        self.switch_window(0)

    def loop(self):
        pass

    def on_event(self, event):
        if event.type == core.KEYDOWN:
            if event.key == core.K_1:
                self._game_state.active = 1
                self.switch_window(1)
                self._menu_scene.active_window_name = "Game"
            elif event.key == core.K_2:
                self._game_state.active = 2
                self.switch_window(2)
                self._menu_scene.active_window_name = "Color"
            elif event.key == core.K_3:
                self._game_state.active = 0
                self.switch_window(0)
                self._menu_scene.active_window_name = "Menu"
            elif event.key == core.K_ESCAPE:
                self.running = False


if __name__ == "__main__":
    WindowDemo().loop_forever()
