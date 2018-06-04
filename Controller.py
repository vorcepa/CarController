import pygame as pg
import numpy as np
import math
pg.init()


class Controller():
    def __init__(self):
        self.radian = 0
        self.omega = 0
        self.omegaMin = -.2
        self.omegaMax = .2

        self.integral = 0
        self.previous_error = 0

        self.p_const = .1
        self.i_const = 1/60
        self.d_const = 1/60
        self.n = 0
        self.gain = 0

        self.testCD = 15
        self.testCDMax = 15

    def __get_slope(self, sensorInfo, rOffsets):
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
                slope.append((get_arctan/math.pi, rOffsets[i]))

        return slope

    def __get_error(self, slope, radian):
        errors = []

        for i in range(len(slope)):
            sp_1 = slope[i][0] - radian

            if slope[i][0] > radian:
                sp_2 = radian + (2 - slope[i][0])
            else:
                sp_2 = slope[i][0] + (2 - radian)

            get_min = (min([sp_1, sp_2], key=abs), slope[i][1])
            errors.append(get_min)

        get_max = 0
        for j in range(len(errors)):
            get_max = max(get_max, abs(errors[j][0]))

        for k in range(len(errors)):
            if abs(errors[k][0]) == get_max:
                return errors[k]

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
        error = (0, 0)
        self.n += 1

        slope = self.__get_slope(sensorInfo, rOffsets)
        if slope != []:
            error = self.__get_error(slope, radian)

        self.integral += error[0]*self.i_const/self.n
        derivative = (error[0] - self.previous_error)*self.d_const
        self.previous_error = error[0]

        if error[1] <= 1:
            k_p = -abs(self.p_const*error[0])
            k_i = .025 * self.integral
        else:
            k_p = abs(self.p_const*error[0])
            k_i = -.025 * self.integral

        k_d = 6 * derivative

        self.gain = k_p + k_i + k_d

        output = self.changeDir(self.gain)
        return output
