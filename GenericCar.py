import pygame as pg
import utils
import math
pg.init()


class CarActive(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.folder = 'ArtAssets/'

        self.imageList = [pg.image.load(self.folder + '2pi-3.png'),
                          pg.image.load(self.folder + '3pi-2.png'),
                          pg.image.load(self.folder + '3pi-4.png'),
                          pg.image.load(self.folder + '4pi-3.png'),
                          pg.image.load(self.folder + '5pi-3.png'),
                          pg.image.load(self.folder + '5pi-4.png'),
                          pg.image.load(self.folder + '5pi-6.png'),
                          pg.image.load(self.folder + '7pi-6.png'),
                          pg.image.load(self.folder + '11pi-6.png'),
                          pg.image.load(self.folder + 'pi.png'),
                          pg.image.load(self.folder + 'pi-0.png'),
                          pg.image.load(self.folder + 'pi-2.png'),
                          pg.image.load(self.folder + 'pi-3.png'),
                          pg.image.load(self.folder + 'pi-4.png'),
                          pg.image.load(self.folder + 'pi-6.png'),
                          pg.image.load(self.folder + '7pi-4.png')]

        self.images = {'0': self.imageList[10],         # 0, 360
                       'pi/6': self.imageList[14],      # 30
                       'pi/4': self.imageList[13],      # 45
                       'pi/3': self.imageList[12],      # 60
                       'pi/2': self.imageList[11],      # 90
                       '2pi/3': self.imageList[0],      # 120
                       '3pi/4': self.imageList[2],      # 135
                       '5pi/6': self.imageList[6],      # 150
                       'pi': self.imageList[9],         # 180
                       '7pi/6': self.imageList[7],      # 210
                       '5pi/4': self.imageList[5],      # 225
                       '4pi/3': self.imageList[3],      # 240
                       '3pi/2': self.imageList[1],      # 270
                       '5pi/3': self.imageList[4],      # 300
                       '7pi/4': self.imageList[15],     # 315
                       '11pi/6': self.imageList[8]}     # 330

        self.image = self.images['0']
        self.rect = self.image.get_rect()

        self.maxSpeed = 5

    def move(self, radian):
        moveX = int(round(self.maxSpeed*math.cos(radian*math.pi), 0))
        moveY = int(round(self.maxSpeed*math.sin(radian*math.pi), 0))

        self.rect.x += moveX
        self.rect.y += moveY

        if 0 <= radian <= .0833:
            self.image = self.images['0']
        elif .0833 < radian <= .2055:
            self.image = self.images['11pi/6']
        elif .2055 < radian <= .2944:
            self.image = self.images['7pi/4']
        elif .2944 < radian <= .4166:
            self.image = self.images['5pi/3']
        elif .4166 < radian <= .5833:
            self.image = self.images['3pi/2']
        elif .5833 < radian <= .7056:
            self.image = self.images['4pi/3']
        elif .7056 < radian <= .7889:
            self.image = self.images['5pi/4']
        elif .7889 < radian <= .9167:
            self.image = self.images['7pi/6']
        elif .9167 < radian <= 1.0833:
            self.image = self.images['pi']
        elif 1.0833 < radian <= 1.2111:
            self.image = self.images['5pi/6']
        elif 1.2111 < radian <= 1.2889:
            self.image = self.images['3pi/4']
        elif 1.2889 < radian <= 1.4167:
            self.image = self.images['2pi/3']
        elif 1.4167 < radian <= 1.5833:
            self.image = self.images['pi/2']
        elif 1.5833 < radian <= 1.7056:
            self.image = self.images['pi/3']
        elif 1.7056 < radian <= 1.7944:
            self.image = self.images['pi/4']
        elif 1.7944 < radian <= 1.9167:
            self.image = self.images['pi/6']
        elif radian > 1.9167:
            self.image = self.images['0']

        return (int(math.fabs(moveX)), int(math.fabs(moveY)))

    def update(self, gameWindow):
        gameWindow.blit(self.image, self.rect)


class DirectionOfMotion(pg.sprite.Sprite):
    def __init__(self, gameWindow, pos):
        pg.sprite.Sprite.__init__(self)

        self.gameWindow = gameWindow
        self.color = utils.WHITE
        self.radius = 125

    def update(self, gameWindow, pos):
        # self.image = pg.draw.circle(gameWindow, self.color, pos, self.radius, 5)
        pass


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

    def update(self, gameWindow, pos):
        # colors = [utils.LIGHTBLUE3, utils.TAN1]
        # retColor = colors[0]
        #
        # self.colorSwitchTimer -= 1
        # if self.colorSwitchTimer <= 0:
        #     self.Toggle = not self.Toggle
        #     self.colorSwitchTimer = self.TimerMax
        # if self.Toggle:
        #     retColor = colors[0]
        # elif not self.Toggle:
        #     retColor = colors[1]
        #
        # self.image = pg.draw.circle(gameWindow, retColor, pos, self.radius, 0)
        pass
