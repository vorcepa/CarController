import pygame as pg
import numpy as np
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

    def __get_slope(self, sensorInfo):
        slope = []

        for i in range(len(sensorInfo)):
            if sensorInfo[i][3] is not None:
                dx = sensorInfo[i][2][0] - sensorInfo[i][3][0]
                dy = sensorInfo[i][3][1] - sensorInfo[i][2][1]
            else:
                dx = dy = None

            if dx is not None:
                get_arctan = np.arctan2(dy, dx)
                if get_arctan < 0:
                    get_arctan = 2*math.pi + get_arctan
                slope.append(get_arctan/math.pi)

        return slope

    def __get_error(self, slope, radian):
        errors = []

        for i in slope:
            sp_1 = i - radian

            if i > radian:
                sp_2 = radian + (2 - i)
            else:
                sp_2 = i + (2 - radian)

            get_min = min([sp_1, sp_2], key=abs)
            errors.append(get_min)

        return max(errors, key=abs)

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
        error = 0

        slope = self.__get_slope(sensorInfo)
        if slope != []:
            error = self.__get_error(slope, radian)

        k_p = -abs(.05*error)
        gain = k_p
        print(gain)

        output = self.changeDir(gain)
        return output
