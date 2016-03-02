# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

def move(p, U, pExact, pOvershoot, pUndershoot):
    assert abs(pExact + pOvershoot + pUndershoot - 1) < 1e-6
    q = []
    l = len(p)
    for i in range(l):
        s = p[(i-U) % l] * pExact
        s += p[(i-U-1) % l] * pOvershoot
        s += p[(i-U+1) % l] * pUndershoot
        q.append(s)
    return q

def sense(p, world, measurement, pHit, pMiss):
    assert len(p) == len(world)

    q = []
    for i in range(len(world)):
        hit = (world[i] == measurement)
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    q = [q_i/s for q_i in q]
    return q

if __name__ == '__main__':
    n = 5
    pHit = 0.6
    pMiss = 0.2
    pExact = 0.8
    pOvershoot = 0.1
    pUndershoot = 0.1

    world = ['green', 'red', 'red', 'green', 'green']
    measurements = ['red', 'red']
    motions = [1, 1]

    # init prob
    p = [1./n] * n
    # p = [0, 1, 0, 0, 0]

    # sense
    # for i in range(len(measurements)):
    #     p = sense(p, world, measurements[i], pHit, pMiss)
    # print(p)

    # sense and cyclic move
    for i in range(len(motions)):
        p = sense(p, world, measurements[i], pHit, pMiss)
        p = move(p, motions[i], pExact, pOvershoot, pUndershoot)
    print(p)
