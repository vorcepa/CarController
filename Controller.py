import pygame as pg
import math
pg.init()


class Controller():
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

    """Still building.  Eventually the process needs to be:
        readSensor -> PID control modifies gain based on readSensor ->
        gain is passed to changeDir
    """
    def readSensors(self, sensorTest):
        # activeKey is only here because keypresses can still control the car
        activeKey = pg.key.get_pressed()
        if sensorTest == (0, 0, 0):
            feedback = 0
        elif sensorTest == (128, 128, 128):
            feedback = 1
        else:
            feedback = 2
        output = self.changeDir(activeKey, feedback)
        return output
