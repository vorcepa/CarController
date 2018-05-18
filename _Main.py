import pygame as pg
import utils
from BackgroundMap import GameMap
from GenericCar import CarActive, DirectionOfMotion, DirectionReticle
from Controller import Controller
from Sensors import Sensor


class PIDCar():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        pg.display.set_caption("Self-driving car")
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.map = GameMap()
        self.car = CarActive()
        self.direction = DirectionOfMotion(self.car.image,
                                           (self.car.rect.centerx,
                                            self.car.rect.centery))
        self.dirReticle = DirectionReticle(self.car.image,
                                           (self.car.rect.centerx,
                                            self.car.rect.centery))
        self.controller = Controller()
        self.sensor0 = Sensor(self.gameWindow, False, .1875, 200, 1)   # Starts at top right
        self.sensor1 = Sensor(self.gameWindow, False, 1.75, 180, 1)  # Starts at bottom right
        # self.sensor3 = Sensor(self.gameWindow, True,
        #                       .9, 115, 1)              # Starts behind center
        # self.sensor4 = Sensor(self.gameWindow, True,
        #                       1.1, 115, 1)
        self.sensorList = [self.sensor0, self.sensor1]
        self.sensorOffsets = [i.rOffset for i in self.sensorList]
        self.sensorTest = [None] * len(self.sensorList)

        self.testCD = 9
        self.testCDMax = 9

    def quitGame(self):
        pg.quit()
        raise SystemExit(0)

    def gotoMenu(self):
        rect = self.gameWindow.get_rect()

        def startPlay():
            self.menu = False

        self.menu = True
        while self.menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quitGame()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        return
                    if event.key == pg.K_ESCAPE:
                        self.quitGame()

            self.gameWindow.fill(utils.WHITE)
            text = utils.getFont(size=64, style='bold').render("Self-driving Car", False, utils.BLACK)
            textRect = text.get_rect()
            textRect.center = self.gameWindow.get_rect().center
            textRect.y -= 250
            self.gameWindow.blit(text, textRect)

            pg.display.update()
            self.clock.tick(self.FPS)

    def playGame(self):  # maybe rename later?
        self.gotoMenu()
        cos_theta, sin_theta, radian = (0, 0, 0)

        gameActive = True
        rOffsets = []

        for i in self.sensorList:
            rOffsets.append(i.rOffset)
        while gameActive:
            sensorRead = []
            colorPos = []

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameActive = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quitGame()

            move = self.car.move(radian)

            self.gameWindow.fill(utils.WHITE)
            self.map.resetMap()
            self.car.update(self.map.activeMap)

            """
            bgOffset updates the background *and* also returns a tuple
            of the offset (x,y) coordinates between player location
            on the background and the screen pixel location. This tuple
            is used to draw the direction circle to the correct location.
            """

            bgOffset = self.map.update(self.gameWindow, self.car.rect, move)
            directionLoc = (self.car.rect.centerx + bgOffset[0],
                            self.car.rect.centery + bgOffset[1])
            self.direction.update(self.gameWindow, (directionLoc[0],
                                                    directionLoc[1]))

            retLocX = directionLoc[0] + int(round(125*cos_theta, 0))
            retLocY = directionLoc[1] + int(round(125*sin_theta, 0))
            self.dirReticle.update(self.gameWindow, (retLocX, retLocY))

            """
            Sensors move, then the sensors are read.
            The information from the read sensors is then
            passed to the PID controller
            """
            for i in self.sensorList:
                sensorRead.append(i.move(directionLoc, radian))
                colorPos.append((i.rect.centerx, i.rect.centery))

            errorCorrection = self.controller.PID(sensorRead, rOffsets, radian)

            if errorCorrection is not None:
                cos_theta, sin_theta, radian = errorCorrection

            pg.display.update()
            self.clock.tick(self.FPS)

        self.quitGame()


if __name__ == "__main__":
    pg.init()
    gameWindow = pg.display.set_mode((800, 600))
    game = PIDCar(gameWindow)
    game.playGame()
