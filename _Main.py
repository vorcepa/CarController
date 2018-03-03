import pygame as pg
import utils
from BackgroundMap import GameMap
from GenericCar import CarActive, DirectionOfMotion, DirectionReticle


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
            text = utils.getFont(size=64,
                                 style='bold').render("Self-driving Car",
                                                      False, utils.BLACK)
            textRect = text.get_rect()
            textRect.center = self.gameWindow.get_rect().center
            textRect.y -= 250
            self.gameWindow.blit(text, textRect)

            pg.display.update()
            self.clock.tick(self.FPS)

    def playGame(self):  # maybe rename later?
        self.gotoMenu()
        rotation = (125, 0)
        radian = 0
        move = (0, 0)

        gameActive = True
        while gameActive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameActive = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quitGame()

            move = self.car.move(radian)

            activeKey = pg.key.get_pressed()
            if activeKey[pg.K_RIGHT] and not activeKey[pg.K_LEFT]:
#                move = self.car.move(radian)
                rotation = self.dirReticle.move(activeKey)
                radian = rotation[2]
            if activeKey[pg.K_LEFT] and not activeKey[pg.K_RIGHT]:
#                move = self.car.move(radian)
                rotation = self.dirReticle.move(activeKey)
                radian = rotation[2]
#            if activeKey[pg.K_UP]:
#                self.car.move(radian)
#            if activeKey[pg.K_DOWN]:
#                self.car.move(radian)

            self.gameWindow.fill(utils.WHITE)
            self.map.resetMap()

            self.car.update(self.map.activeMap)

            """
            offset updates the background *and* also returns a tuple
            of the offset (x,y) coordinates between player location
            on the background and the screen pixel location. This tuple
            is used to draw the direction circle to the correct location.
            """

            offset = self.map.update(self.gameWindow, self.car.rect, move)
            directionLoc = (self.car.rect.centerx + offset[0],
                            self.car.rect.centery + offset[1])
            self.direction.update(self.gameWindow, (directionLoc[0],
                                                    directionLoc[1]))

            """testing dirRecticle GIVE IT SOME SPACE"""
            self.dirReticle.update(self.gameWindow,
                                   (directionLoc[0] + rotation[0],
                                    directionLoc[1] + rotation[1]))
            pg.display.update()
            self.clock.tick(self.FPS)

        self.quitGame()


if __name__ == "__main__":
    pg.init()
    gameWindow = pg.display.set_mode((800, 600))
    game = PIDCar(gameWindow)
    game.playGame()
