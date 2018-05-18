import pygame as pg
import utils
import math
pg.init()


class Sensor(pg.sprite.Sprite):
    """
    Pass in variables display, rOffset, dOffset, and weight.

    display is used for physically looking at the sensor's location.
    When instantiating the sensor class, set fillToggle to False to hide
    the sensor (normal functionality).  Set fillToggle to True to show
    the sensor.  The sensor will behave as normal, it will just be
    visible to the user

    rOffset is the radial (angular) offset from the direction of motion
    of the car.  If you want a sensor that is in-line with the direction of
    motion, set this variable to 0. If you want the sensor to be opposite
    the direction of motion (ie, behind the car), set this number to 1.  Use
    This number represents some fraction of pi (ie, 1 is π, .5 is π/2, 1.75
    is 7π/4, etc.)

    dOffset is the linear distance from the center of the car, in
    pixels. It is recommended that this number be greater than 0, with a range
    of ~25 pixels to the edge of the screen (<300 pixels by default).

    weight is how much the sensor affects the gain.  It is recommended that
    sensors close to the origin of the car be given a higher weight.

    production example:
        self.sensorFrontCenter = Sensor(False, 0, 125, [SOMETHING])

        - Sensor will be invisible and looking at pixels directly
        in-line with the direction of motion, and in front of the
        car

    testing example:
        self.sensorRightSide = Sensor(True, .5, 100, [SOMETHING])

        - Sensor will be visible, and
        will be located at an angle of 90 ° clockwise from
        the direction of motion.

        3/12/18
        TO DO: Determine weights to describe what a number does
        (example: weight = 5 is large weight, .01 is small weight,
        or 2 is small weight, 20 is large weight, etc.)
    """
    def __init__(self, gameWindow, display, rOffset, dOffset, weight):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([24, 24], pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.getColor = gameWindow.get_at((self.rect.centerx, self.rect.centery))

        self.gameWindow = gameWindow
        self.color = utils.WHITE
        self.weight = weight

        self.heading = headingSensor(gameWindow, display, rOffset*.8, 1000)

        self.display = display
        if not isinstance(self.display, bool):
            pg.quit()
            raise TypeError(f"Expected variable of type boolean, got type {type(self.display)}")

        self.rOffset = rOffset
        if type(self.rOffset) not in (int, float):
            pg.quit()
            raise TypeError(f"Expected variable of type int or float, got type {type(self.rOffset)}")
        self.dOffset = dOffset
        if type(self.dOffset) not in (int, float):
            pg.quit()
            raise TypeError(f"Expected variable of type int or float, got type {type(self.dOffset)}")

        self.testCD = 30
        self.testCDMax = 30

    def __findNotRoad(self, directionLoc, target, radian):
        self.update()
        car_edge_toggle = True
        heading = None
        car_edge = (self.rect.x, self.rect.y)

        xdiff_init = target[0] - directionLoc[0]
        ydiff_init = target[1] - directionLoc[1]

        x_float = directionLoc[0]
        y_float = directionLoc[1]

        dx = xdiff_init / 400
        dy = ydiff_init / 300

        while self.getColor != utils.GOLD:
            x_float += dx
            y_float += dy

            if not self.rect.x == target[0]:
                self.rect.x = int(round(x_float))
            if not self.rect.y == target[1]:
                self.rect.y = int(round(y_float))

            if self.rect.x == target[0] and self.rect.y == target[1]:
                if self.display:
                    self.gameWindow.blit(self.image, (self.rect.x, self.rect.y))
                    pg.draw.rect(self.image, utils.WHITE, (0, 0, 24, 24), 1)

                return [self.getColor[:3], car_edge, (self.rect.x, self.rect.y), heading]

            # try-except for when it throws an error for reaching the edge of the screen
            try:
                self.getColor = self.gameWindow.get_at((self.rect.centerx, self.rect.centery))
            except IndexError:
                self.getColor = utils.GOLD

            if self.getColor[2] < 215 and car_edge_toggle:
                car_edge = (self.rect.x, self.rect.y)
                car_edge_toggle = False

            if self.getColor == utils.GOLD:
                heading = self.heading.findNotRoad(directionLoc, radian)

        if self.display:
            self.gameWindow.blit(self.image, (self.rect.x, self.rect.y))
            pg.draw.rect(self.image, utils.WHITE, (0, 0, 24, 24), 1)

        return [self.getColor[:3], car_edge, (self.rect.x, self.rect.y), heading]

    def move(self, directionLoc, radian):
        heading_radian = radian
        radian += self.rOffset

        x = int(round(self.dOffset*math.cos(radian*math.pi), 0))
        y = -int(round(self.dOffset*math.sin(radian*math.pi), 0))
        self.rect.x = directionLoc[0]
        self.rect.y = directionLoc[1]

        target = (directionLoc[0] + x, directionLoc[1] + y)
        notRoadDistance = self.__findNotRoad(directionLoc, target, heading_radian)
        return notRoadDistance

    def update(self):
        try:
            self.getColor = self.gameWindow.get_at((self.rect.centerx, self.rect.centery))
            return self.getColor[:3]
        except IndexError:
            self.getColor = utils.GOLD
            return self.getColor


class headingSensor(pg.sprite.Sprite):
    def __init__(self, gameWindow, display, rOffset, dOffset):
        pg.sprite.Sprite.__init__(self)

        self.gameWindow = gameWindow
        self.display = display

        self.image = pg.Surface([24, 24], pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.getColor = gameWindow.get_at((self.rect.centerx, self.rect.centery))

        self.gameWindow = gameWindow
        self.color = utils.WHITE
        self.rOffset = rOffset
        self.dOffset = dOffset

    def findNotRoad(self, directionLoc, radian):
        self.rect.x = directionLoc[0]
        self.rect.y = directionLoc[1]
        self.update()

        if 0 <= self.rOffset <= 1:
            radian += .5
        else:
            radian += 1.5
        x = int(round(self.dOffset*math.cos(radian*math.pi), 0))
        y = -int(round(self.dOffset*math.sin(radian*math.pi), 0))

        target = (directionLoc[0] + x, directionLoc[1] + y)

        xdiff_init = target[0] - directionLoc[0]
        ydiff_init = target[1] - directionLoc[1]

        x_float = directionLoc[0]
        y_float = directionLoc[1]

        dx = xdiff_init / 400
        dy = ydiff_init / 300

        while self.getColor != utils.GOLD:
            x_float += dx
            y_float += dy

            if not self.rect.x == target[0]:
                self.rect.x = int(round(x_float))
            if not self.rect.y == target[1]:
                self.rect.y = int(round(y_float))

            if self.rect.x == target[0] and self.rect.y == target[1]:
                if self.display:
                    self.gameWindow.blit(self.image, (self.rect.x, self.rect.y))
                    pg.draw.rect(self.image, utils.WHITE, (0, 0, 24, 24), 1)

                return (self.rect.x, self.rect.y)

            # try-except for when it throws an error for reaching the edge of the screen
            try:
                self.getColor = self.gameWindow.get_at((self.rect.centerx, self.rect.centery))
            except IndexError:
                self.getColor = utils.GOLD

        if self.display:
            self.gameWindow.blit(self.image, (self.rect.x, self.rect.y))
            pg.draw.rect(self.image, utils.WHITE, (0, 0, 24, 24), 1)

        return (self.rect.x, self.rect.y)

    def update(self):
        try:
            self.getColor = self.gameWindow.get_at((self.rect.centerx, self.rect.centery))
            return self.getColor[:3]
        except IndexError:
            self.getColor = utils.GOLD
            return self.getColor