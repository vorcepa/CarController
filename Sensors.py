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

        self.distSensor = DistanceSensor(gameWindow, display, rOffset, dOffset, weight)

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
        colorLoc = (self.rect.x, self.rect.y)
        dColors = self.distSensor.update(self.gameWindow)
        self.distSensor.move(directionLoc, radian, dColors, colorLoc)

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
            return getColor[:3]
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
        self.display = display
        self.color = utils.BLACK

        self.weight = weight
        self.rOffset = rOffset  # radial offset

        # linear offsets
        self.GLOBAL_OFFSET = dOffset
        self.x_local_offset = dOffset
        self.y_local_offset = dOffset  # x and y can vary between 0 and global offset

        self.testCD = 30
        self.testCDMax = 30

    @staticmethod
    def __sensor_in_car(dColors):
        for key in dColors:
            if dColors[key][2] > 200:
                return True
        return False

    @staticmethod
    def __all_yellow(dColors):
        try:
            for key in dColors:
                if dColors[key] != utils.GOLD:
                    return False
            return True
        except TypeError:
            return True

    def move(self, directionLoc, radian, dColors, colorLoc):
        radian += self.rOffset

        if self.__sensor_in_car(dColors):
            xdiff = self.rect.x - colorLoc[0]
            ydiff = self.rect.y - colorLoc[1]
            self.rect.x -= int(xdiff/10)
            self.rect.y -= int(ydiff/10)

        while self.__all_yellow(dColors):
            self.rect.y += 24
            if self.rect.y > 600:
                self.rect.y = 0
                self.rect.x += 24
                if self.rect.x > 800:
                    self.rect.x = 0
            dColors = self.update(self.gameWindow)

        """
        4/9/18
        TO DO: Re-implement sensor behaviour.  Make it work more gooder.
        """

    def update(self, gameWindow):
        if self.display:
            gameWindow.blit(self.image, (self.rect.x, self.rect.y))
            pg.draw.rect(self.image, self.color, (0, 0, 24, 24), 1)

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

            colorList = {'top left': topLeft[:3], 'top mid': topMid[:3], 'top right': topRight[:3],
                         'center left':centerLeft[:3], 'center': center[:3], 'center right': centerRight[:3],
                         'bot left': botLeft[:3], 'bot mid': botMid[:3], 'bot right': botRight[:3]}
            return colorList

        except IndexError:
            return
