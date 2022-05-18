from typing import Union
from Game.math.core import vector2d
from pygame.color import Color
from pygame import Surface


_Vector2d_or_tuple = Union[Vector2d, tuple]


class CartesianPlane:

    """
    screen_size - (width ,height) = pygame window size in pixel
    unit_length - pixel count for 1 unit length in cartesian system
    parent      - (optional) parent plance instance
    """

    def __init__(self,
                 window_size: tuple,
                 unit_length: float,
                 parent_vector: Vector2d = None,
                 set_limit: bool = False) -> None: ...

    @property
    def X(self) -> float: ...
    @X.setter
    def X(self, o: float) -> None: ...
    @property
    def Y(self) -> float: ...
    @Y.setter
    def Y(self, o: float) -> None: ...
    @property
    def CENTER(self) -> tuple: ...
    @CENTER.setter
    def CENTER(self, XY: tuple) -> None: ...
    @property
    def shape(self) -> tuple: ...
    def get_XY(self, xy: tuple) -> tuple: ...
    def get_X(self, x: float) -> float: ...
    def get_Y(self, y: float) -> float: ...
    def to_xy(self, XY: tuple) -> tuple: ...
    def to_x(self, X: float) -> float: ...
    def to_y(self, Y: float) -> float: ...

    def createVector(self,
                     x: float = 1,
                     y: float = 0,
                     max_length: float = 0,
                     min_length: float = 1,
                     set_limit: bool = False) -> Vector2d: ...

    def createRandomVector(self,
                           max_length: float = 0,
                           min_length: float = 1,
                           set_limit: bool = False) -> Vector2d: ...

    def show(self, window: Surface, color: Color) -> None: ...


class Vector2d(vector2d):

    """
    #TODO
    """

    def __init__(self,
                 space: CartesianPlane,
                 x: float = 1,
                 y: float = 0,
                 max_length: float = 0,
                 min_length: float = 1,
                 set_limit: bool = False) -> None: ...

    @property
    def X(self) -> float: ...
    @property
    def Y(self) -> float: ...
    @property
    def HEAD(self) -> float: ...
    @property
    def TAIL(self) -> float: ...
    def random(self) -> None: ...

    def unit(self,
             scale: float = 1,
             vector: bool = True) -> _Vector2d_or_tuple: ...

    def normal(self, scale: float, vector: bool) -> _Vector2d_or_tuple: ...
    def show(self, window: Surface, color: Color) -> None: ...
