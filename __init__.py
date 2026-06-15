import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from .game import Game  # noqa
from .scene import Scene  # noqa
from .window import Window  # noqa
from .input_manager import InputManager  # noqa
from .scene_manager import SceneManager  # noqa
import pygame as core  # noqa
