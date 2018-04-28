import pygame as pg
import math
import utils
pg.init()


class Controller():
    """
    TO DO: self.omega needs to be variable.  A gain variable will
    change omega.  omega will have an absolute magnitude (ie ±.015)
    that it cannot exceed.
    """
    def __init__(self):
        self.radian = 0
        self.omega = 0
        self.omegaMin = -.1
        self.omegaMax = .1
        self.SET_POINT = 45

        self.testCD = 30
        self.testCDMax = 30

    def changeDir(self, gain):
        self.omega += gain
        if self.omega > self.omegaMax:
            self.omega = self.omegaMax
        elif self.omega < self.omegaMin:
            self.omega = self.omegaMin

        self.radian += self.omega
        if self.radian > 2:
            self.radian = 0
        elif self.radian < 0:
            self.radian = 2

        # activeKey is only here because keypresses can still control the car
        activeKey = pg.key.get_pressed()
        if activeKey[pg.K_RIGHT] and not activeKey[pg.K_LEFT]:
            self.omega = -.015
            self.radian += self.omega
            if self.radian > 2:
                self.radian = 0
        elif activeKey[pg.K_LEFT] and not activeKey[pg.K_RIGHT]:
            self.omega = .015
            self.radian += self.omega
            if self.radian > 2:
                self.radian = 0
        else:
            self.omega = 0
            self.radian += self.omega

        cos_theta = math.cos(self.radian*math.pi)
        sin_theta = math.sin(self.radian*math.pi)
        return (cos_theta, sin_theta, self.radian)

    def PID(self, sensorInfo, rOffsets, radian):
        gain = 0
        slope = []

        for i in range(len(sensorInfo)):
            if sensorInfo[i][3] is None:
                continue

            if 0.0 < rOffsets[i] < 1.0:
                dy = sensorInfo[i][3][1] - sensorInfo[i][2][1]
                dx = sensorInfo[i][3][0] - sensorInfo[i][2][0]
            else:
                dy = sensorInfo[i][3][1] - sensorInfo[i][2][1]
                dx = -(sensorInfo[i][3][0] - sensorInfo[i][2][0])

            try:
                slope.append(math.atan(dy/dx))
            except ZeroDivisionError:
                slope.append(math.copysign(math.atan(1000), dy))

        output = self.changeDir(gain)
        return output
