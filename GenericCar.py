import pygame as pg
import utils
import math
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
        self.radius = 125

    def update(self, gameWindow, pos):
        self.image = pg.draw.circle(gameWindow, self.color,
                                    pos, self.radius, 5)


class DirectionReticle(pg.sprite.Sprite):
    def __init__(self, surface, pos):
        pg.sprite.Sprite.__init__(self)

        self.surface = surface
        self.pos = pos
        self.radius = 15

        self.colorSwitchTimer = 25
        self.TimerMax = 25
        self.Toggle = True

        self.radian = 0
        self.omega = .015

    def move(self, activeKey):
        """TESTING.  BE SURE TO CLEAN UP"""
        if activeKey[pg.K_RIGHT]:
            self.radian += self.omega
            if self.radian > 2:
                self.radian = 0
        elif activeKey[pg.K_LEFT]:
            self.radian -= self.omega
            if self.radian < 0:
                self.radian = 2

        outputX = 125*math.cos(self.radian*math.pi)
        outputY = 125*math.sin(self.radian*math.pi)
        return (int(round(outputX, 0)), int(round(outputY, 0)))

    def update(self, gameWindow, pos):
        colors = [utils.LIGHTBLUE3, utils.TAN1]
        retColor = colors[0]

        self.colorSwitchTimer -= 1
        if self.colorSwitchTimer <= 0:
            self.Toggle = not self.Toggle
            self.colorSwitchTimer = self.TimerMax
        if self.Toggle:
            retColor = colors[0]
        elif not self.Toggle:
            retColor = colors[1]

        self.image = pg.draw.circle(gameWindow, retColor,
                                    pos, self.radius, 0)
