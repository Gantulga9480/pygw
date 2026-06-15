"""Main Survivors game — orchestrates windows, input, and game state."""
import pygame as pg

from pygw import Game, Window

from survivors import config as C
from survivors.camera import Camera


# Window indices
WIN_INTRO = 0
WIN_MENU = 1
WIN_HERO_SELECT = 2
WIN_GAME = 3
WIN_GAME_OVER = 4


class SurvivorsGame(Game):
    def __init__(self):
        super().__init__()
        self.title = "Survivors"
        self.size = (C.SCREEN_W, C.SCREEN_H)
        self.fps = C.FPS

        # Game state
        self.selected_hero = None  # "rogue" or "warrior"
        self.game_scene = None

        # Fonts (shared)
        self.font_small = None
        self.font_medium = None
        self.font_big = None

    def setup(self):
        # Init fonts
        self.font_small = pg.font.SysFont("monospace", C.UI_FONT_TINY, bold=True)
        self.font_medium = pg.font.SysFont("monospace", C.UI_FONT_SIZE, bold=True)
        self.font_big = pg.font.SysFont("monospace", C.UI_FONT_BIG, bold=True)

        # Force display surface creation (must come before mixer init)
        _ = self.display_surface

        # Sound disabled

        # Import scenes lazily (they import game assets that depend on config)
        from survivors.scenes.intro import IntroWindow
        from survivors.scenes.menu import MenuWindow
        from survivors.scenes.hero_select import HeroSelectWindow
        from survivors.scenes.game_scene import GameWindow
        from survivors.scenes.game_over import GameOverWindow

        self.intro_window = IntroWindow(self, self._on_intro_done)
        self.menu_window = MenuWindow(self, self._on_menu_action)
        self.hero_select_window = HeroSelectWindow(self, self._on_hero_picked)
        self.game_window = GameWindow(self, self._on_game_over)
        self.game_over_window = GameOverWindow(self, self._on_game_over_action)

        self.add_window(self.intro_window)
        self.add_window(self.menu_window)
        self.add_window(self.hero_select_window)
        self.add_window(self.game_window)
        self.add_window(self.game_over_window)

        # Start on intro
        self.switch_window(WIN_INTRO)

    # ---- Menu callbacks ----
    def _on_intro_done(self):
        self.switch_window(WIN_MENU)

    def _on_menu_action(self, action):
        if action == "start":
            self.switch_window(WIN_HERO_SELECT)
        elif action == "quit":
            self.running = False

    def _on_hero_picked(self, hero_key):
        self.selected_hero = hero_key
        self.game_window.start(hero_key)
        self.switch_window(WIN_GAME)

    def _on_game_over(self):
        self.game_over_window.show(self.game_window.stats, self.selected_hero)
        self.switch_window(WIN_GAME_OVER)

    def _on_game_over_action(self, action):
        if action == "menu":
            self.switch_window(WIN_MENU)
        elif action == "quit":
            self.running = False

    # ---- Global event handling ----
    def on_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                win = self.scene_manager.active_window
                if win == self.game_window:
                    self._on_game_over()
                elif win == self.game_over_window:
                    self._on_game_over_action("menu")
                elif win == self.hero_select_window:
                    self.switch_window(WIN_MENU)