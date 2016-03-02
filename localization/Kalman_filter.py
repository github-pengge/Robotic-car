# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

import sys
sys.path.append('../basic')
from Matrix import matrix

# global params
dt = 0.1
u = matrix([[0.], [0.], [0.], [0.]])
F = matrix([[1., 0., dt, 0,],
            [0., 1., 0., dt],
            [0., 0., 1., 0.],
            [0., 0., 0., 1.]])
H = matrix([[1., 0., 0., 0.],
            [0., 1., 0., 0.]])
R = matrix([[0.1, 0.],
            [0., 0.1]])
I = matrix.eye(4)


def Kalman_filter(x, P, measurements):
    for i in range(len(measurements)):
        # motion update
        x = F * x + u
        P = F * P * F.transpose()

        # measurement update
        y = - H * x + measurements[i]
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + K * y
        P = (I - K * H) * P


    return [x, P]

if __name__ == '__main__':
    # one example
    # measurements = [[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]]
    # initial_xy = [4., 12.]

    # another example
    # measurements = [[1., 4.], [6., 0.], [11., -4.], [16., -8.]]
    # initial_xy = [-4., 8.]

    # a third example
    measurements = [[1., 17.], [1., 15.], [1., 13.], [1., 11.]]
    initial_xy = [1., 19.]

    x = matrix([[initial_xy[0]], [initial_xy[1]], [0.], [0.]])
    P = matrix([[0., 0., 0., 0.],
                [0., 0., 0., 0.],
                [0., 0., 1000., 0.],
                [0., 0., 0., 1000.]])

    [x, P] = Kalman_filter(x, P, measurements)
    print('x = ')
    print(x)
    print('P = ')
    print(P)