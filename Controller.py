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

        self.testCD = 30
        self.testCDMax = 30
    """
    testing the logic for control.  To add:
        kp (proportional)
        ki (integral)
        kd (derivative)
    Not sure if these should be individual methods.
    """
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
            self.omega = .015
            self.radian += self.omega
            if self.radian > 2:
                self.radian = 0
        elif activeKey[pg.K_LEFT] and not activeKey[pg.K_RIGHT]:
            self.omega = -.015
            self.radian += self.omega
            if self.radian < 0:
                self.radian = 2
        else:
            self.omega = 0
            self.radian += self.omega
        

        cos_theta = math.cos(self.radian*math.pi)
        sin_theta = math.sin(self.radian*math.pi)
        return (cos_theta, sin_theta, self.radian)

    def PID(self, sensorInfo, rOffsets):
        gain = 0
        if abs(sensorInfo[2][0]) >= abs(sensorInfo[2][1]):
            error = abs(sensorInfo[2][0])
        else:
            error = abs(sensorInfo[2][1])

        if sensorInfo[0] != utils.GREY:
            gain += error/10000

        output = self.changeDir(gain)
        return output
