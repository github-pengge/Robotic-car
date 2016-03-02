# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

from math import *
import random
import sys
sys.path.append('../basic')
from tools import twiddle

delta_t = 1.0 # time flow speed

class robot(object):
    def __init__(self, length=20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.distance_noise = 0.0
        self.steering_noise = 0.0
        self.steering_drift = 0.0
        self.max_steering_angle = pi / 4.0

    def __repr__(self):
        return '[x=%.5f, y=%.5f, orient=%.5f, drift=%.5f]' % \
               (self.x, self.y, self.orientation, self.steering_drift)

    def __str__(self):
        return '[x=%.5f, y=%.5f, orient=%.5f, drift=%.5f]' % \
               (self.x, self.y, self.orientation, self.steering_drift)

    def set(self, new_x, new_y, new_orientation, new_max_steering_angle=None):
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)
        if(new_max_steering_angle != None):
            self.max_steering_angle = float(new_max_steering_angle) % (2.0 * pi)

    def set_noise(self, distance_noise, steering_noise):
        self.distance_noise = distance_noise
        self.steering_noise = steering_noise

    def set_drift(self, drift):
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001):
        if(steering > self.max_steering_angle):
            steering = self.max_steering_angle
        if(steering < -self.max_steering_angle):
            steering = -self.max_steering_angle
        if(distance < 0.0):
            distance = 0.0

        dist = random.gauss(distance, self.distance_noise)
        steering2 = random.gauss(steering, self.steering_noise)
        steering2 += self.steering_drift # add systematic bias
        beta = dist / self.length * tan(steering2)
        if(abs(beta) <= tolerance):
            x = self.x + dist * cos(self.orientation)
            y = self.y + dist * sin(self.orientation)
            orientation = (self.orientation + beta) % (2.0 * pi)
        else:
            R = dist / beta
            cx = self.x - sin(self.orientation) * R
            cy = self.y + cos(self.orientation) * R
            orientation = (self.orientation + beta) % (2.0 * pi)
            x = cx + sin(orientation) * R
            y = cy - cos(orientation) * R
        new_robot = robot(self.length)
        new_robot.set(x, y, orientation, self.max_steering_angle)
        new_robot.set_noise(self.distance_noise, self.steering_noise)
        new_robot.set_drift(self.steering_drift)

        return new_robot


def run(param, print_flag=False):
    '''
    param[0]: weight of proportion, param[1]: weight of differential,
    param[2]: weight of integral
    '''
    my_robot = robot()
    my_robot.set(0.0, 1.0, 0.0)
    speed = 1.0
    my_robot.set_drift(10.0 * pi / 180.0) # 10 degree
    N = 100
    CTE_old = my_robot.y
    I = 0.0
    err = 0.0
    for i in range(N * 2):
        CTE_new = my_robot.y # we want the car to drive along x-axis, so CTE = y-coordinate
        P = -param[0] * CTE_new
        D = -param[1] * ((CTE_new - CTE_old) / delta_t)
        I += -param[2] * CTE_new * delta_t
        steering = P + I + D
        my_robot = my_robot.move(steering, speed * delta_t)
        CTE_old = CTE_new
        if(i >= N):
            err += (CTE_new ** 2)
        if(print_flag):
            print(my_robot, steering)

    return err / float(N)


if __name__ == '__main__':
    n_param = 3
    params = twiddle(n_param, run)
    # err = run(params, True)
    # print(err)