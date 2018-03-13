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
        self.omegaMin = -1000
        self.omegaMax = 1000

        self.errorCurrent = 0
    """
    testing the logic for control.  To add:
        kp (proportional)
        ki (integral)
        kd (derivative)
    Not sure if these should be individual methods.
    """
    def changeDir(self, gain):
        if gain is not 0:
            print(gain)
            self.omega += gain
            self.radian += self.omega
            if self.radian > 2:
                self.radian = 0
            elif self.radian < 0:
                self.radian = 2
        else:
            self.omega = 0
        if self.omega > self.omegaMax:
            self.omega = self.omegaMax
        elif self.omega < self.omegaMin:
            self.omega = self.omegaMin
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

    def readSensors(self, sensorList, sensorOffsets, sensorTest):
        """
        Still building.  Eventually the process needs to be:
        readSensor -> PID control modifies gain based on readSensor ->
        gain is passed to changeDir
        """
        if sensorTest is not None:
            feedback = [None] * len(sensorTest)
            for i in range(len(sensorTest)):
                if sensorTest[i] is not None:
                    if sensorTest[i][0] == (utils.GREY):
                        feedback[i] = 0
                    elif sensorTest[i][0] == (utils.GOLD):
                        feedback[i] = 1
                    else:
                        feedback[i] = 2
        else:
            feedback = [2]

        output = self.PID(sensorList, sensorOffsets, feedback)
        return output

    def PID(self, sensorList, sensorOffsets, feedback):
        error = 0
        for i in range(len(feedback)):
            if sensorOffsets[i] < 1:
                if feedback[i] is None:
                    error += -3
                else:
                    feedback[i] = -feedback[i]
                    error += feedback[i]
            else:
                if feedback[i] is None:
                    error += 3
                else:
                    error += feedback[i]
        kp = .008*error
        if -.005 < kp < .005:
            kp = 0
#        print(kp)
        output = self.changeDir(kp)
        return output
