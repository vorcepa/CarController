import pygame as pg
import utils
pg.init()


class Sensor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((25, 25))
        self.rect = pg.Surface.get_rect(self.image)

        """
        image.fill is used for testing purposes.  Go to
        the update method and use gameWindow.blit(self.image, self.rect)
        to draw the sensor.  Note that the sensor will return
        whatever color is passed in to the fill function,
        rather than what is 'beneath' it on the gameWindow surface.
        """
        self.image.fill(utils.GREEN)

    def update(self, gameWindow, sensCoords):
        self.rect.x = sensCoords[0]
        self.rect.y = sensCoords[1]
        try:
            getColor = gameWindow.get_at((self.rect.centerx,
                                          self.rect.centery))
            return getColor[:3]
        except IndexError:
            return
