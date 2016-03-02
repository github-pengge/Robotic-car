# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

from math import *
import sys
sys.path.append('../basic')
from Matrix import matrix

def f(x, mu, sigma2):
    return 1./(sqrt(2. * pi * sigma2)) * exp(-1./2 * (x-mu)**2 / sigma2)

def update(mu1, var1, mu2, var2):
    new_mu = (mu1 * var2 + mu2 * var1) / (var1 + var2)
    new_var = 1. / (1. / var1 + 1. / var2)
    return [new_mu, new_var]

def predict(mu1, var1, mu2, var2):
    new_mu = mu1 + mu2
    new_var = var1 + var2
    return [new_mu, new_var]

def Kalman_filter(x, P, measurements):
    for i in range(len(measurements)):
        # measurement update
        y = - H * x + measurements[i]
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + K * y
        P = (I - K * H) * P

        # motion update
        x = F * x + u
        P = F * P * F.transpose()

    return [x, P]

u = matrix([[0.], [0.]])
F = matrix([[1., 1.], [0., 1.]])
H = matrix([[1., 0.]])
R = matrix([[1.]])
I = matrix([[1., 0.], [0., 1.]])

if __name__ == '__main__':
    # measurements = [5, 6, 7, 9, 10]
    # motions = [1, 1, 2, 1, 1]
    # measurement_sig = 4
    # motion_sig = 2
    # mu = 0
    # sig = 0.00000001
    #
    # for i in range(len(motions)):
    #     [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    #     print('update: [%s, %s]' % (mu, sig))
    #     [mu, sig] = predict(mu, sig, motions[i], motion_sig)
    #     print('predict: [%s, %s]' % (mu, sig))

    # Kalman filter
    measurements = [1,2,3]
    x = matrix([[0.], [0.]])
    P = matrix([[1000., 0], [0., 1000.]])
    [x, P] = Kalman_filter(x, P, measurements)
    print('x = ')
    print(x)
    print('P = ')
    print(P)