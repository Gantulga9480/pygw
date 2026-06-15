import random
from pygw import Game, Scene, Window, core


class SC(Scene):

    def __init__(self, parent, size, position):
        super().__init__(parent, size, position)

    def onUpdate(self):
        pass

    def onRender(self):
        b = random.randint(0, 100)
        if self.surface is not None:
            self.surface.fill((255, 255, b))


class SC1(Scene):

    def __init__(self, parent, size, position):
        super().__init__(parent, size, position)

    def onUpdate(self):
        pass

    def onRender(self):
        b = random.randint(0, 100)
        if self.surface is not None:
            self.surface.fill((255, 0, b))


class Win(Window):

    def __init__(self, game, title='Pygame'):
        super().__init__(game, title)
        self.add_child(SC(self, (300, 300), (100, 100)))

    def onUpdate(self):
        g = random.randint(0, 100)
        if self.surface is not None:
            self.surface.fill((0, g, 0))


class Win1(Window):

    def __init__(self, game, title='Pygame'):
        super().__init__(game, title)
        self.add_child(SC1(self, (300, 300), (500, 100)))

    def onUpdate(self):
        r = random.randint(0, 100)
        if self.surface is not None:
            self.surface.fill((r, 0, 0))


class Test(Game):

    def __init__(self):
        super().__init__()
        self.size = (1024, 720)

    def setup(self):
        main_win = Win(self, 'test-main')
        self.add_window(main_win)
        main_win.enable_bb()

        second_win = Win1(self, 'test-second')
        self.add_window(second_win)
        second_win.enable_bb()

    def on_event(self, event):
        if event.type == core.KEYDOWN:
            if event.key == core.K_1:
                self.switch_window(0)
            elif event.key == core.K_2:
                self.switch_window(1)


if __name__ == "__main__":
    Test().loop_forever()
