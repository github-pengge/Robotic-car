# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

from math import *
import random
import sys
sys.path.append('../basic')
from tools import sample, gaussian

# global params
world_size = 100.0 # size of cyclic world
landmarks = [[20.0, 20.0],
             [80.0, 80.0],
             [20.0, 80.0],
             [80.0, 20.0]]

class robot(object):
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        self.check(new_x, new_y, new_orientation)
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_forward_noise, new_turn_noise, new_sense_noise):
        self.forward_noise = new_forward_noise
        self.turn_noise = new_turn_noise
        self.sense_noise = new_sense_noise

    def check(self, x, y, orientation):
        if(x < 0 or x >= world_size):
            raise ValueError('X coordinate out of bound.')
        if(y < 0 or y >= world_size):
            raise ValueError('Y coordinate out of bound.')
        if(orientation < 0 or orientation >= 2 * pi):
            raise ValueError('Orientation must be in [0, 2*pi).')

    def __str__(self):
        return 'Robot @[x = %.6f, y = %.6f, heading = %.4f°]' % \
               (self.x, self.y, self.orientation * 180. / pi)

    def __repr__(self):
        return '[x = %.6f, y = %.6f, heading = %.4f°]' % \
               (self.x, self.y, self.orientation * 180. / pi)

    def move(self, turn, dist):
        orientation = self.orientation + random.gauss(turn, self.turn_noise)
        orientation %= 2 * pi
        noise = random.gauss(0.0, self.forward_noise)
        x = self.x + (dist + noise) * cos(orientation)
        y = self.y + (dist + noise) * sin(orientation)
        x %= world_size
        y %= world_size
        new_robot = robot()
        new_robot.set(x, y, orientation)
        new_robot.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return new_robot


    def sense(self):
        dist = []
        for landmark in landmarks:
            d = sqrt((self.x - landmark[0]) ** 2 +
                     (self.y - landmark[1]) ** 2)
            d += random.gauss(0.0, self.sense_noise)
            dist.append(d)
        return dist

    def measurement_prob(self, measurement):
        prob = 1.0
        for i in range(len(landmarks)):
            dist = sqrt(
                            (self.x - landmarks[i][0]) ** 2 +
                            (self.y - landmarks[i][1]) ** 2
                        )
            prob *= gaussian(dist, self.sense_noise, measurement[i])

        return prob

def eval(r, p):
    sum = 0.0
    for i in range(len(p)):
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx ** 2 + dy ** 2)
        sum += err
    return sum / float(len(p))

if __name__ == '__main__':
    # # programing 1
    # my_robot = robot()
    # my_robot.set_noise(5.0, 0.1, 5.0)
    # my_robot.set(30.0, 50.0, pi/2)
    # print(my_robot)
    # my_robot = my_robot.move(-pi/2, 15.0)
    # print(my_robot.sense())
    # print(my_robot)
    # my_robot.move(-pi/2, 10.0)
    # print(my_robot.sense())
    # print(my_robot)

    # programing 2
    N = 1000
    times = 10

    my_robot = robot()

    particles = []
    for i in range(N):
        x = robot()
        x.set_noise(0.05, 0.05, 5.0)
        particles.append(x)
    # print(particles)

    print(eval(my_robot, particles))
    for t in range(times):
        my_robot = my_robot.move(0.1, 5.0)
        Z = my_robot.sense()
        for i in range(N):
            particles[i] = particles[i].move(0.1, 5.0)
        # print(particles)

        w = []
        for i in range(N):
            w.append(particles[i].measurement_prob(Z))
        # print(w)

        particles = sample(particles, w, N)
        print(eval(my_robot, particles))