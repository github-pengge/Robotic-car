# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

import random
from math import *
import sys
sys.path.append('../basic')
from tools import sample, gaussian

world_size = 100.0
length = 20.0
bearing_noise = 0.1
steering_noise = 0.1
distance_noise = 5.0
tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.
landmarks  = [[100.0, 0.0],
              [0.0, 0.0],
              [0.0, 100.0],
              [100.0, 100.0]]

class robot(object):
    def __init__(self, length):
        self.length = length
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.bearing_noise = 0.0
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.max_steering_angle = pi / 4.0

    def set(self, new_x, new_y, new_orientation,
            new_max_steering_angle=None):
        # if(new_x <= -world_size or new_x >= world_size):
        #     raise ValueError('X coordinate out of bound.')
        # if(new_y <= -world_size or new_y >= world_size):
        #     raise ValueError('Y coordinate out of bound.')
        if(new_orientation < 0 or new_orientation >= 2 * pi):
            raise ValueError('Orientation must be in [0, 2*pi).')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
        if(new_max_steering_angle is not None):
            self.max_steering_angle = new_max_steering_angle

    def set_noise(self, new_bearing_noise, new_steering_noise, new_distance_noise):
        self.bearing_noise = new_bearing_noise
        self.steering_noise = new_steering_noise
        self.distance_noise = new_distance_noise

    def __str__(self):
        return 'Robot @[x = %.6f, y = %.6f, orient = %.4f°]' % \
               (self.x, self.y, self.orientation * 180.0 / pi)

    def __repr__(self):
        return '[x = %.6f, y = %.6f, orient = %.4f°]' % \
               (self.x, self.y, self.orientation * 180.0 / pi)

    def move(self, motion, tolerance=0.001):
        steering = motion[0]
        distance = motion[1]
        if(abs(steering) > self.max_steering_angle):
            raise ValueError('Exceeding max steering angle.')
        if(distance < 0.0):
            raise ValueError('Moving backwards is not valid.')

        dist = random.gauss(distance, self.distance_noise)
        steering2 = random.gauss(steering, self.steering_noise)
        beta = dist / self.length * tan(steering2)
        if(abs(beta) < tolerance):
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
        new_robot.set_noise(self.bearing_noise, self.steering_noise,
                            self.distance_noise)
        return new_robot

    def sense(self, add_noise=True):
        measurement = []
        for i in range(len(landmarks)):
            dx = landmarks[i][0] - self.x
            dy = landmarks[i][1] - self.y
            bearing = atan2(dy, dx) - self.orientation
            if(add_noise):
                bearing = random.gauss(bearing, self.bearing_noise)
            bearing %= (2.0 * pi)
            measurement.append(bearing)
        return measurement

    def measurement_prob(self, measurement):
        predicted_measurement = self.sense(False)
        error = 1.0
        for i in range(len(measurement)):
            error_bearing = abs(measurement[i] - predicted_measurement[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi
            error *= gaussian(0.0, self.bearing_noise, error_bearing)
        return error


def get_position(particles, wrt=None):
    N = len(particles)
    if(wrt is None):
        wrt = [1.0 for _ in range(N)]
    s = sum(wrt)
    w = [w_i/s for w_i in wrt]
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(N):
        x += (particles[i].x * w[i])
        y += (particles[i].y * w[i])
        orientation += ((
                           (
                                particles[i].orientation - particles[0].orientation + pi
                            ) % (2.0 * pi) + (particles[0].orientation - pi)
                       ) * w[i])

    return [x, y, orientation]

def particle_filter(motions, measurements, N=500):
    # make particles
    particles = []
    for i in range(N):
        r = robot(length)
        r.set_noise(bearing_noise, steering_noise, distance_noise)
        particles.append(r)

    # update particles
    for i in range(len(motions)):
        for j in range(N):
            particles[j] = particles[j].move(motions[i])

        # measurement update
        w = []
        for j in range(N):
            w.append(particles[j].measurement_prob(measurements[i]))

        # resampling
        particles = sample(particles, w, N)
    return get_position(particles)

def generate_ground_truth(motions):
    r = robot(length)
    r.set_noise(bearing_noise, steering_noise, distance_noise)
    measurements = []
    for i in range(len(motions)):
        r = r.move(motions[i])
        measurements.append(r.sense())
    return [r, measurements]

def check_output(real_robot, estimated_pos):
    dx = abs(real_robot.x - estimated_pos[0])
    dy = abs(real_robot.y - estimated_pos[1])
    d_orient = abs(real_robot.orientation - estimated_pos[2])
    d_orient = (d_orient + pi) / (2.0 * pi) - pi
    if(dx < tolerance_xy and dy < tolerance_xy and
        d_orient < tolerance_orientation):
        return True
    else:
        return False

if __name__ == '__main__':
    num_of_iterations = 8

    # my_robot = robot(length)
    # my_robot.set(30.0, 20.0, 0.0)
    # my_robot.set_noise(bearing_noise, steering_noise, distance_noise)
    # # motions = [[0.0, 10.0], [pi / 6.0, 10.0], [0.0, 20.0]]
    # print(my_robot.sense())

    motions = [[2.0 * pi / 10.0, 20.0] for _ in range(num_of_iterations)]
    measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
                    [3.510067, 2.916300, 2.146394, 1.598332],
                    [2.972469, 2.407489, 1.588474, 1.611094],
                    [1.906178, 1.193329, 0.619356, 0.807930],
                    [1.352825, 0.662233, 0.144927, 0.799090],
                    [0.856150, 0.214590, 5.651497, 1.062401],
                    [0.194460, 5.660382, 4.761072, 2.471682],
                    [5.717342, 4.736780, 3.909599, 2.342536]]
    print(particle_filter(motions, measurements))

    # test 2
    x = generate_ground_truth(motions)
    final_robot = x[0]
    measurements = x[1]
    estimated_position = particle_filter(motions, measurements)
    print('Ground truth: %s' % final_robot)
    print('Particle filter: %s' % estimated_position)
    print('Code check: %s' % check_output(final_robot, estimated_position))