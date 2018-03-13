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

        self.gameWindow = gameWindow
        self.color = utils.WHITE
        self.x = 24
        self.y = 24
        self.centerx = self.x // 2
        self.centery = self.y // 2
        self.area = (self.x, self.y)
#        self.image = pg.Surface((25, 25))
#        self.rect = pg.Surface.get_rect(self.image)
#        self.rectDraw = pg.draw.rect(self.image, utils.WHITE, self.rect, 2)
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
        self.testCD -= 1
        radian += self.rOffset
        x = int(round(self.dOffset*math.cos(radian*math.pi), 0))
        y = int(round(self.dOffset*math.sin(radian*math.pi), 0))
        self.x = directionLoc[0] + x
        self.y = directionLoc[1] + y
        self.centerx = self.x + 12
        self.centery = self.y + 12
#        if self.testCD <= 0:
#            self.testCD = self.testCDMax
#            print(x, self.rect.x)

    def update(self, gameWindow):
        if self.display:
            self.image = pg.draw.rect(gameWindow, utils.WHITE, (self.x, self.y, 24, 24), 1)

        try:
            getColor = gameWindow.get_at((self.centerx,
                                          self.centery))
            return [getColor[:3]]
        except IndexError:
            return
