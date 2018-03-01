import pygame as pg
import utils
from BackgroundMap import GameMap
from GenericCar import CarActive, DirectionOfMotion


class PIDCar():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        pg.display.set_caption("Self-driving car")
        self.clock = pg.time.Clock()
        self.FPS = 30

        self.map = GameMap()
        self.car = CarActive()
        self.direction = DirectionOfMotion(self.car.image,
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
            text = utils.getFont(size=64, style='bold').render("Self-driving Car", False, utils.BLACK)
            textRect = text.get_rect()
            textRect.center = self.gameWindow.get_rect().center
            textRect.y -= 250
            self.gameWindow.blit(text, textRect)

            pg.display.update()
            self.clock.tick(self.FPS)

    def playGame(self):  # maybe rename later?
        self.gotoMenu()

        gameActive = True
        while gameActive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameActive = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quitGame()

            activeKey = pg.key.get_pressed()
            if activeKey[pg.K_RIGHT]:
                self.car.move(1, 0)
            if activeKey[pg.K_LEFT]:
                self.car.move(-1, 0)
            if activeKey[pg.K_UP]:
                self.car.move(0, -1)
            if activeKey[pg.K_DOWN]:
                self.car.move(0, 1)

            self.gameWindow.fill(utils.WHITE)
            self.map.resetMap()

            self.car.update(self.map.activeMap)
            self.map.update(self.gameWindow, self.car.rect)
#            self.direction.update(self.image, self.car.rect)
            pg.display.update()
            self.clock.tick(self.FPS)

        self.quitGame()


if __name__ == "__main__":
    pg.init()
    gameWindow = pg.display.set_mode((800, 600))
    game = PIDCar(gameWindow)
    game.playGame()
