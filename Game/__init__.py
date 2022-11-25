import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from .game import Game  # noqa
from .scene import Scene, State  # noqa
from .window import Window  # noqa
import pygame as core  # noqa
