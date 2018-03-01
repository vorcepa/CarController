import pygame as pg
import utils


class GameMap():
    def __init__(self):
        self.mapImage = None
        self.activeMap = None
        self.createMap()

        self.offsetX = 0
        self.offsetY = 0
        self.scrollSpeed = 5

    def createMap(self):
        """
        TO DO: NO HARD-CODED VALUES
        """
        self.mapImage = pg.Surface((2100, 2100))

        lightTile = pg.Surface((100, 100))
        lightTile.fill(utils.GREY)
        darkTile = pg.Surface((100, 100))
        darkTile.fill(utils.BLACK)
        toggle = True

        for y in range(0, 21):
            for x in range(0, 21):
                if toggle:
                    self.mapImage.blit(lightTile, (x*100, y*100))
                    toggle = not toggle
                else:
                    self.mapImage.blit(darkTile, (x*100, y*100))
                    toggle = not toggle

    def resetMap(self):
        self.activeMap = self.mapImage.copy()

    """
Car scroll is limited to a small box within the game window.
The car will move independently from the screen within a small,
pre-defined box.  Once the car hits the edge of this smaller box,
the background will start to scroll (giving the impression of a moving camera
that follows the player).
    """

    def update(self, gameWindow, playerRect):
        rect = gameWindow.get_rect()

        # car scroll
        if playerRect.centerx > rect.centerx - self.offsetX + 25:
            self.offsetX -= self.scrollSpeed
        elif playerRect.centerx < rect.centerx - self.offsetX - 25:
            self.offsetX += self.scrollSpeed

        if playerRect.centery > rect.centery - self.offsetY + 25:
            self.offsetY -= self.scrollSpeed
        elif playerRect.centery < rect.centery - self.offsetY - 25:
            self.offsetY += self.scrollSpeed

        # stop scrolling at edge of map
        if playerRect.left < 0:
            playerRect.left = 0
        elif playerRect.right > 2100:
            playerRect.right = 2100

        if playerRect.top < 0:
            playerRect.top = 0
        elif playerRect.bottom > 2100:
            playerRect.bottom = 2100

        # background scroll
        if self.offsetX > 0:
            self.offsetX = 0
        elif self.offsetX < rect.width - 2100:
            self.offsetX = rect.width - 2100

        if self.offsetY > 0:
            self.offsetY = 0
        elif self.offsetY < rect.height - 2100:
            self.offsetY = rect.height - 2100

        gameWindow.blit(self.activeMap, (self.offsetX, self.offsetY))
