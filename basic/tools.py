# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

from math import *
import random

def sample(pop, wrt, k):
    '''
    Resampling population with respect to wrt--the weight of each individual
    in population
    :param pop: the population to be resampled
    :param wrt: weight of each individual in pop, it doesn't require to be
                a distribution.
    :param k: size of population after resampling
    :return: population after resampling
    '''
    assert len(pop) == len(wrt)
    sampled_pop = []
    index = int(random.random() * len(wrt))
    beta = 0.0
    mw = max(wrt)
    for i in range(k):
        # here we use 2*mw to ensure that it can travel around the whole
        # circle, as well as not to large to avoid too much of searching
        # in the following while-loop
        beta += random.random() * 2.0 * mw
        while(beta > wrt[index]):
            beta -= wrt[index]
            index = (index + 1) % len(wrt)
        sampled_pop.append(pop[index])

    return sampled_pop


def gaussian(mu, sigma, x):
    return 1.0 / sqrt(2 * pi * sigma ** 2) * \
               exp(-0.5 * ((x - mu) / sigma) ** 2)


def print_list(a_list, indent=0):
    # try:
    #     len(a_list[0][0])
    # except:
    #     p = 1
    # else:
    #     if(isinstance(a_list[0][0], str)):
    #         p = 1
    #     else:
    #         p = 0
    # if(p == 0):
    #     print(a_list)
    # else:
    #     s = ''
    #     for i in range(len(a_list)):
    #         s += ' ' * indent
    #         s += str(a_list[i])
    #         if(i < len(a_list) - 1):
    #             s += str('\n')
    #     print(s)
    for i in range(len(a_list)):
        print(' '*indent + '%s' % a_list[i])


def print_list_change(origin, new, num=0):
    assert len(origin) == len(new)
    for i in range(len(origin)):
        print('['+','.join('%.3s' % x for x in origin[i]))


def twiddle(n_param, run, increase=1.1, decrease=0.9, tol=0.001):
    '''
    Do parameters optimization using coordinate-descend algorithm.
    :param n_param: number of parameters
    :param run: function run, run() must receive params and perform it to the model,
                and it returns the performance (usually average error) of params.
    :param increase: multiple of parameters' increase step
    :param decrease: multiple of parameters' decrease step
    :param tol: tolerance of max parameters' decrease step
    :return: best params optimized.
    '''
    params = [0.0 for _ in range(n_param)]
    d_params = [1.0 for _ in range(n_param)]

    best_err = run(params)
    iter = 0
    while(sum(d_params) >= tol):
        for i in range(n_param):
            params[i] += d_params[i]

            err = run(params)
            if(err < best_err):
                best_err = err
                d_params[i] *= 1.1
            else:
                params[i] -= 2 * d_params[i]
                err = run(params) # do it another time to see if it makes performance better
                if(err < best_err):
                    best_err = err
                    d_params[i] *= 1.1
                else:
                    params[i] += d_params[i]
                    d_params[i] *= 0.9

        iter += 1
        print('Twiddle: #%s %s  -->  %s' % (iter, params, best_err))

    print('Final params: %s, with min error of %s' % (params, best_err))
    return params