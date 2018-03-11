import pygame as pg
import utils
import math
pg.init()
"""
Pass in variables fillToggle, radianOffset, distance.

fillToggle is used for physically looking at the sensor's location.
When instantiating the sensor class, set fillToggle to False to hide
the sensor (normal functionality).  Set fillToggle to True to show
the sensor.  Not that the sensor will read the image.fill color rather
than what is 'underneath' it on the game window surface.  This breaks
the functionality of the sensor, but is useful for testing.

radianOffset is the radial (angular) offset from the direction of motion
of the car.  If you want a sensor that is in-line with the direction of motion,
set this variable to 0. If you want the sensor to be opposite the direction
of motion (ie, behind the car), set this number to [SOMETHING]

distanceOffset is the linear distance from the center of the car, in pixels.
It is recommended that this number be greater than 0, with a range of
~25 pixels to the edge of the screen (<300 pixels by default).

working example:
    self.sensorFrontCenter = Sensor(False, 0, 125)

testing location example:
    self.sensorRightSide = Sensor(True, [SOMETHING], 100)
"""


class Sensor(pg.sprite.Sprite):
    def __init__(self, fillToggle, radianOffset, distanceOffset):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((25, 25))
        self.rect = pg.Surface.get_rect(self.image)
        self.fillToggle = fillToggle
        if not isinstance(self.fillToggle, bool):
            raise TypeError("Expected variable of type boolean, got type {}".format(type(self.fillToggle)))
        self.image.fill(utils.GREEN)

        self.radianOffset = radianOffset
        if type(self.radianOffset) not in (int, float):
            raise TypeError("Expected variable of type int or float, got type {}".format(type(self.radianOffset)))
        self.distanceOffset = distanceOffset
        if type(self.distanceOffset) not in (int, float):
            raise TypeError("Expected variable of type int or float, got type {}".format(type(self.radianOffset)))            

        self.testCD = 30
        self.testCDMax = 30

    def move(self, directionLoc, radian):
        self.testCD -= 1
        radian += self.radianOffset
        x = int(round(self.distanceOffset*math.cos(radian*math.pi), 0))
        y = int(round(self.distanceOffset*math.sin(radian*math.pi), 0))
        self.rect.x = directionLoc[0] + x
        self.rect.y = directionLoc[1] + y
#        if self.testCD <= 0:
#            self.testCD = self.testCDMax
#            print(x, self.rect.x)

    def update(self, gameWindow):
        if self.fillToggle:
            gameWindow.blit(self.image, (self.rect.x, self.rect.y))

        try:
            getColor = gameWindow.get_at((self.rect.centerx,
                                          self.rect.centery))
            return getColor[:3]
        except IndexError:
            return
