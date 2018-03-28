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

    *** NOTE THAT POSITIVE ROTATION IS CURRENTLY CLOCKWISE.  THIS WAS A DUMB
    MISTAKE ON MY PART. ***

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

        self.gameWindow = gameWindow
        self.color = utils.WHITE

        self.distSensor = DistanceSensor(gameWindow, True, rOffset, dOffset, weight)

        self.display = display
        if not isinstance(self.display, bool):
            pg.quit()
            raise TypeError("Expected variable of type boolean, got type {}".format(type(self.display)))

        self.rOffset = rOffset
        if type(self.rOffset) not in (int, float):
            pg.quit()
            raise TypeError("Expected variable of type int or float, got type {}".format(type(self.rOffset)))
        self.dOffset = dOffset
        if type(self.dOffset) not in (int, float):
            pg.quit()
            raise TypeError("Expected variable of type int or float, got type {}".format(type(self.dOffset)))

        self.testCD = 30
        self.testCDMax = 30

    def move(self, directionLoc, radian):
        distSensorUpdate = self.distSensor.update(self.gameWindow)
        self.distSensor.move(directionLoc, radian, distSensorUpdate)

        radian += self.rOffset
        x = int(round(self.dOffset*math.cos(radian*math.pi), 0))
        y = int(round(self.dOffset*math.sin(radian*math.pi), 0))
        self.rect.x = directionLoc[0] + x
        self.rect.y = directionLoc[1] + y

    def update(self, gameWindow):
        if self.display:
            gameWindow.blit(self.image, (self.rect.x, self.rect.y))
            pg.draw.rect(self.image, utils.WHITE, (0, 0, 24, 24), 1)

        try:
            getColor = gameWindow.get_at((self.rect.centerx,
                                          self.rect.centery))
            return [getColor[:3]]
        except IndexError:
            return


class DistanceSensor(pg.sprite.Sprite):
    def __init__(self, gameWindow, display, rOffset, dOffset, weight):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([24, 24], pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

        self.gameWindow = gameWindow
        self.color = utils.BLACK

        self.display = display
        self.rOffset = rOffset
        self.dXOffset = dOffset
        self.dYOffset = dOffset
        self.dOGlobalMax = dOffset  # should never change
        self.dOXLocalMax = dOffset  # should change, but never larger than global
        self.dOYLocalMax = dOffset  # should change, but never larger than global
        self.weight = weight

        self.leftToggle = True
        self.rightToggle = True
        self.upToggle = True
        self.downToggle = True
        self.locStore = (self.rect.x, self.rect.y)

        self.allYellow = False

        self.testCD = 30
        self.testCDMax = 30

    def move(self, directionLoc, radian, test):
        try:
            if test[0] == utils.GOLD and test[1] == utils.GOLD and test[2] == utils.GOLD and test[4] == utils.GOLD:
                self.upToggle = False
            else:
                self.upToggle = True
            if test[2] == utils.GOLD and test[5] == utils.GOLD and test[8] == utils.GOLD and test[4] == utils.GOLD:
                self.rightToggle = False
            else:
                self.rightToggle = True
            if test[6] == utils.GOLD and test[7] == utils.GOLD and test[8] == utils.GOLD and test[4] == utils.GOLD:
                self.downToggle = False
            else:
                self.downToggle = True
            if test[0] == utils.GOLD and test[3] == utils.GOLD and test[6] == utils.GOLD and test[4] == utils.GOLD:
                self.leftToggle = False
            else:
                self.leftToggle = True
            if test[0] == utils.GOLD and test[1] == utils.GOLD and test[2] == utils.GOLD and test[3] == utils.GOLD and test[4] == utils.GOLD and test[5] == utils.GOLD and test[6] == utils.GOLD and test[7] == utils.GOLD and test[8] == utils.GOLD:
                self.dXOffset -= 40
                self.dYOffset -= 40
                self.allYellow = True
            else:
                self.allYellow = False
        except TypeError:
            self.dXOffset = self.dYOffset = 0

        self.rotate_val = -radian * 180
        radian += self.rOffset

        if not self.upToggle or not self.downToggle:
            xmin = abs(directionLoc[0] - self.rect.centerx)
            self.dOXLocalMax -= 10
            if self.dOXLocalMax <= xmin:
                self.dOXLocalMax = xmin
        else:
            self.dOXLocalMax = self.dOGlobalMax
        if not self.leftToggle or not self.rightToggle:
            ymin = abs(directionLoc[1] - self.rect.centery)
            self.dOYLocalMax -= 10
            if self.dOYLocalMax <= ymin:
                self.dOYLocalMax = ymin
        else:
            self.dOYLocalMax = self.dOGlobalMax

        self.dXOffset += 10
        if self.dXOffset >= self.dOXLocalMax:
            self.dXOffset = self.dOXLocalMax
        self.dYOffset += 10
        if self.dYOffset >= self.dOYLocalMax:
            self.dYOffset = self.dOYLocalMax

        x = int(round(self.dXOffset*math.cos(radian*math.pi), 0))
        y = int(round(self.dYOffset*math.sin(radian*math.pi), 0))

        self.rect.x = directionLoc[0] + x
        self.rect.y = directionLoc[1] + y

        self.testCD -= 1

        diff = (self.rect.x - self.locStore[0],
                self.rect.y - self.locStore[1])

        if self.allYellow:
            self.locStore = (self.rect.x, self.rect.y)
            return
        if diff[0] < 0 and not self.leftToggle:
            self.rect.x = self.locStore[0]
        elif diff[0] > 0 and not self.rightToggle:
            self.rect.x = self.locStore[0]
        if diff[1] < 0 and not self.upToggle:
            self.rect.y = self.locStore[1]
        elif diff[1] > 0 and not self.downToggle:
            self.rect.y = self.locStore[1]
        self.locStore = (self.rect.x, self.rect.y)

    def update(self, gameWindow):
        gameWindow.blit(self.image, (self.rect.x, self.rect.y))
        pg.draw.rect(self.image, utils.BLACK, (0, 0, 24, 24), 1)

        try:
            topLeft = gameWindow.get_at((self.rect.x + 1, self.rect.top + 1))
            topMid = gameWindow.get_at((self.rect.centerx, self.rect.top + 1))
            topRight = gameWindow.get_at((self.rect.right, self.rect.top))
            centerLeft = gameWindow.get_at((self.rect.x + 1, self.rect.centery))
            center = gameWindow.get_at((self.rect.centerx, self.rect.centery))
            centerRight = gameWindow.get_at((self.rect.right, self.rect.centery))
            botLeft = gameWindow.get_at((self.rect.x, self.rect.bottom))
            botMid = gameWindow.get_at((self.rect.centerx, self.rect.bottom))
            botRight = gameWindow.get_at((self.rect.right, self.rect.bottom))

            colorList = [topLeft, topMid, topRight, centerLeft, center,
                         centerRight, botLeft, botMid, botRight]
            return colorList

        except IndexError:
            return
