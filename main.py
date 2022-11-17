from Game import Game


class Main(Game):

    def __init__(self, title: str = 'PyGameWindow', width: int = 640, height: int = 480, fps: int = 60, flags: int = 0, render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)