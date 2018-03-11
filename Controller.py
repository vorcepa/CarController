import pygame as pg
import math
pg.init()


class Controller():
    """
    TO DO: self.omega needs to be variable.  A gain variable will
    change omega.  omega will have an absolute magnitude (ie ±.015)
    that it cannot exceed.
    """
    def __init__(self):
        self.radian = 0
        self.omega = .015  # FOR PROPER PID THIS NEEDS TO BE CHANGED TO GAIN

    """
    testing the logic for control.  To add:
        kp (proportional)
        ki (integral)
        kd (derivative)
    Not sure if these should be individual methods.
    """
    def changeDir(self, activeKey, feedback):
        if activeKey[pg.K_RIGHT] and not activeKey[pg.K_LEFT]:
            self.radian += self.omega
            if self.radian > 2:
                self.radian = 0
        elif activeKey[pg.K_LEFT] and not activeKey[pg.K_RIGHT]:
            self.radian -= self.omega
            if self.radian < 0:
                self.radian = 2
        if feedback == 0:
            self.radian += self.omega
            if self.radian > 2:
                self.radian = 0
        elif feedback == 1:
            self.radian -= self.omega
            if self.radian < 0:
                self.radian = 2

        cos_theta = math.cos(self.radian*math.pi)
        sin_theta = math.sin(self.radian*math.pi)
        return (cos_theta, sin_theta, self.radian)

    def readSensors(self, sensorTest):
        """
        Still building.  Eventually the process needs to be:
        readSensor -> PID control modifies gain based on readSensor ->
        gain is passed to changeDir
        """
        if sensorTest is not None:
            feedback = [None] * len(sensorTest)
            for i in range(len(sensorTest)):
                if sensorTest[i] == (0, 0, 0):
                    feedback[i] = 0
                elif sensorTest[i] == (128, 128, 128):
                    feedback[i] = 1
                else:
                    feedback[i] = 2
        else:
            feedback = [2]
        # activeKey is only here because keypresses can still control the car
        activeKey = pg.key.get_pressed()

        output = self.changeDir(activeKey, feedback)
        return output

    def PID(self):
        pass
