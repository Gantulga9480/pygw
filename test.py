from .Game import Game, Color


class test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 640,
                 height: int = 480,
                 fps: int = 60,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)
