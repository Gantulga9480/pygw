from __future__ import annotations

import math
import random

from pygw import Game, Scene, Window, core
from pygw.graphic import CartesianPlane, Rectangle, Polygon
from pygw.math import vector2d as math_vector2d


# ─── Window 1: Game Area ────────────────────────────────────────────────

class GameScene(Scene):

    def __init__(self, parent: Scene | None, size: tuple[int, int],
                 position: tuple[int, int], game_area: GameArea) -> None:
        super().__init__(parent, size, position)
        self.game_area = game_area

    def onRender(self) -> None:
        if self.surface is None:
            return
        self.surface.fill((20, 20, 40))
        self.game_area.draw(self.surface)


class GameArea:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.balls: list[Ball] = []
        self.paddle: Paddle | None = None

        self._spawn_balls(5)
        self._spawn_paddle()

    def _spawn_balls(self, count: int) -> None:
        for _ in range(count):
            ball = Ball(
                x=random.randint(30, self.width - 30),
                y=random.randint(30, self.height - 30),
                vx=random.uniform(-3, 3),
                vy=random.uniform(-3, 3),
                radius=random.randint(8, 15),
            )
            self.balls.append(ball)

    def _spawn_paddle(self) -> None:
        self.paddle = Paddle(
            x=self.width // 2,
            y=self.height - 30,
            width=100,
            height=15,
        )

    def update(self, input_manager: 'InputManager') -> None:
        if self.paddle is None:
            return

        dx = 0
        if input_manager.is_key_pressed(core.K_LEFT) or input_manager.is_key_pressed(core.K_a):
            dx = -1
        if input_manager.is_key_pressed(core.K_RIGHT) or input_manager.is_key_pressed(core.K_d):
            dx = 1

        if dx != 0:
            self.paddle.move(dx)

        for ball in self.balls:
            ball.move()
            ball.bound(self.width, self.height)

    def draw(self, surface: core.SurfaceType) -> None:
        if self.paddle is not None:
            self.paddle.draw(surface)
        for ball in self.balls:
            ball.draw(surface)

    def reset(self) -> None:
        self.balls.clear()
        self._spawn_balls(5)
        self._spawn_paddle()


class Ball:

    def __init__(self, x: int, y: int, vx: float, vy: float, radius: int) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = (
            random.randint(150, 255),
            random.randint(100, 255),
            random.randint(50, 200),
        )
        self.life = 1.0

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def bound(self, w: int, h: int) -> None:
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        if self.x + self.radius > w:
            self.x = w - self.radius
            self.vx = -abs(self.vx)
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        if self.y + self.radius > h:
            self.y = h - self.radius
            self.vy = -abs(self.vy)

    def draw(self, surface: core.SurfaceType) -> None:
        r = int(self.color[0])
        g = int(self.color[1])
        b = int(self.color[2])
        cx = int(self.x)
        cy = int(self.y)
        rad = self.radius

        # Glow effect
        for i in range(3, 0, -1):
            alpha = (4 - i) * 20
            alpha_color = (r, g, b, alpha)
            try:
                pygame_surface = surface.convert_alpha()
                glow = pygame.Surface((rad * 2 + i * 4, rad * 2 + i * 4), core.SRCALPHA)
                pygame.draw.circle(glow, alpha_color,
                                   (rad + i * 2, rad + i * 2), rad + i * 2)
                pygame_surface.blit(glow, (cx - rad - i * 2, cy - rad - i * 2))
                surface.blit(pygame_surface, (0, 0))
            except Exception:
                pass

        # Main ball
        pygame.draw.circle(surface, (r, g, b), (cx, cy), rad)
        # Highlight
        pygame.draw.circle(surface, (255, 255, 255, 100),
                           (cx - rad // 3, cy - rad // 3), rad // 3)


class Paddle:

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 8

    def move(self, dx: int) -> None:
        self.x += dx * self.speed
        self.x = max(self.width // 2, min(self.x, 600 - self.width // 2))

    def draw(self, surface: core.SurfaceType) -> None:
        r = 255
        g = 200
        b = 50
        x = self.x - self.width // 2
        y = self.y - self.height // 2

        # Glow
        glow = core.Surface((self.width + 10, self.height + 10), core.SRCALPHA)
        glow.fill((255, 200, 50, 30))
        pygame.draw.rect(glow, (255, 200, 50, 30), glow.get_rect(), border_radius=10)
        surface.blit(glow, (x - 5, y - 5))

        # Main paddle
        pygame.draw.rect(surface, (r, g, b),
                         (x, y, self.width, self.height), border_radius=8)
        # Highlight
        pygame.draw.rect(surface, (255, 255, 200),
                         (x + 2, y + 2, self.width - 4, self.height // 2),
                         border_radius=6)


# ─── Window 2: Stats Panel ──────────────────────────────────────────────

class StatsScene(Scene):

    def __init__(self, parent: Scene | None, size: tuple[int, int],
                 position: tuple[int, int], game_area: GameArea) -> None:
        super().__init__(parent, size, position)
        self.game_area = game_area
        self.frame_count = 0

    def onUpdate(self) -> None:
        self.frame_count += 1

    def onRender(self) -> None:
        if self.surface is None:
            return
        self.surface.fill((30, 30, 50))

        font = self._get_font(20)
        small_font = self._get_font(14)

        # Title
        title = font.render("STATS PANEL", True, (255, 255, 255))
        self.surface.blit(title, (10, 10))

        # Separator
        pygame.draw.line(self.surface, (100, 100, 150), (5, 40), (205, 40), 2)

        # Stats
        y = 55
        stats = [
            f"Balls: {len(self.game_area.balls)}",
            f"Paddle: Active" if self.game_area.paddle else f"Paddle: None",
            f"FPS: {int(pygame.time.get_ticks()) // 33 + 60}" if self.frame_count % 30 < 2 else f"FPS: 60",
            f"Game Area: 600x450",
        ]

        for line in stats:
            text = small_font.render(line, True, (200, 200, 255))
            self.surface.blit(text, (10, y))
            y += 20

        # Separator
        pygame.draw.line(self.surface, (100, 100, 150), (5, y + 10), (205, y + 10), 1)

        # Instructions
        y += 25
        instructions = [
            "CONTROLS:",
            "← / A - Move Left",
            "→ / D - Move Right",
            "1 - Switch to Game",
            "2 - Switch to Stats",
            "3 - Reset Balls",
            "ESC - Close",
        ]

        for line in instructions:
            color = (150, 150, 200) if not line.startswith("CONTROLS") else (255, 255, 255)
            text = small_font.render(line, True, color)
            self.surface.blit(text, (10, y))
            y += 16


# ─── Window 3: Menu ─────────────────────────────────────────────────────

class MenuScene(Scene):

    def __init__(self, parent: Scene | None, size: tuple[int, int],
                 position: tuple[int, int]) -> None:
        super().__init__(parent, size, position)
        self.alpha = 0

    def onRender(self) -> None:
        if self.surface is None:
            return

        self.alpha = min(255, self.alpha + 5)
        self.surface.fill((20, 20, 40, self.alpha))

        font = self._get_font(32)
        small_font = self._get_font(18)
        huge_font = self._get_font(48)

        # Title
        title = huge_font.render("PYGAWINS", True, (100, 200, 255))
        title_rect = title.get_rect(centerx=150, y=60)
        self.surface.blit(title, title_rect)

        # Separator
        pygame.draw.line(self.surface, (100, 200, 255), (30, 120), (270, 120), 2)

        # Menu items
        y = 140
        menu_items = [
            ("1", "Switch to Game Panel"),
            ("2", "Switch to Stats Panel"),
            ("3", "Reset Game"),
            ("ESC", "Exit Game"),
        ]

        for key, action in menu_items:
            key_text = small_font.render(key, True, (255, 200, 50))
            action_text = small_font.render(action, True, (200, 200, 255))

            key_rect = key_text.get_rect(x=40, y=y)
            action_rect = action_text.get_rect(x=70, y=y)

            self.surface.blit(key_text, key_rect)
            self.surface.blit(action_text, action_rect)
            y += 35

        # Footer
        footer = small_font.render("Demonstrates: Window switching, SceneManager, InputManager",
                                   True, (100, 100, 150))
        self.surface.blit(footer, (30, 380))


# ─── Main Game ──────────────────────────────────────────────────────────

class WindowManagerDemo(Game):

    def __init__(self) -> None:
        super().__init__()
        self.title = "PyGameWindow - Window Manager Demo"
        self.size = (480, 400)
        self._current_panel = 0  # 0=game, 1=stats, 2=menu

    def setup(self) -> None:
        self.game_area = GameArea(600, 450)

        # Window 1: Game Panel
        self.game_panel = self._create_game_panel()

        # Window 2: Stats Panel
        self.stats_panel = self._create_stats_panel()

        # Window 3: Menu Panel
        self.menu_panel = self._create_menu_panel()

        # Start with menu visible
        self.switch_window(2)

    def _create_game_panel(self) -> Window:
        panel = Window(self, "Game Panel")
        scene = GameScene(None, (600, 450), (0, 0), self.game_area)
        panel.add_child(scene)
        self.add_window(panel)
        return panel

    def _create_stats_panel(self) -> Window:
        panel = Window(self, "Stats Panel")
        scene = StatsScene(None, (200, 400), (0, 0), self.game_area)
        panel.add_child(scene)
        self.add_window(panel)
        return panel

    def _create_menu_panel(self) -> Window:
        panel = Window(self, "Menu")
        scene = MenuScene(None, (300, 400), (0, 0))
        panel.add_child(scene)
        self.add_window(panel)
        return panel

    def loop(self) -> None:
        if self._current_panel == 0:
            self.game_area.update(self.input)
        elif self._current_panel == 1:
            pass  # Stats panel updates itself
        # Menu is static

    def on_event(self, event: core.event.Event) -> None:
        if event.type == core.KEYDOWN:
            if event.key == core.K_1:
                self._switch_to_game()
            elif event.key == core.K_2:
                self._switch_to_stats()
            elif event.key == core.K_3:
                self._reset_game()
            elif event.key == core.K_ESCAPE:
                self.running = False

    def _switch_to_game(self) -> None:
        self._current_panel = 0
        self.switch_window(0)

    def _switch_to_stats(self) -> None:
        self._current_panel = 1
        self.switch_window(1)

    def _reset_game(self) -> None:
        self.game_area.reset()
        self._current_panel = 0
        self.switch_window(0)

    def _get_font(self, size: int) -> core.SurfaceType:
        try:
            return pygame.font.SysFont("arial", size, bold=True)
        except Exception:
            return pygame.font.Font(None, size)
