import pygame as pg
import utils
pg.init()


class CarActive(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('CarV1.png')
        self.rect = self.image.get_rect()

        self.speed = 5

    def move(self, xdir, ydir):
        self.rect.x += xdir*self.speed
        self.rect.y += ydir*self.speed

    def update(self, gameWindow):
        gameWindow.blit(self.image, self.rect)


class DirectionOfMotion(pg.sprite.Sprite):
    def __init__(self, surface, pos):
        pg.sprite.Sprite.__init__(self)

        self.surface = surface
        self.color = utils.WHITE
        self.pos = pos
        self.radius = 60
        self.image = pg.draw.circle(self.surface, self.color,
                                    self.pos, self.radius, 5)

    def update(self, gameWindow):
        gameWindow.blit(self.image, self.pos)
