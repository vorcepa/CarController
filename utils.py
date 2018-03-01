import pygame as pg


"""
getFont can be called by any file that imports utils.
Shortens the amount of typing required to put a string
that is to be blitted to the game window.
Takes the arguments font name, font size, and
font style (bold, italicized, etc.)
"""


def getFont(name="Courier New", size=20, style=''):
    return pg.font.SysFont(name, size, style)


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
GOLD = (255, 210, 0)
