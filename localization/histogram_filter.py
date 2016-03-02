# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

'''
Actually, this is the homework assignment of Unit 1 of cs373.
Here, we implement a 2-D histogram filter, which is much similar
to the real world.
'''

def move(p, motion, p_move):
    '''
    Update probabilities of each place after one movement (for cyclic movement)
    :param p: probabilities of each place
    :param motion: direction of movement, [0,0] for not move, [0,1] for move right,
                    [0,-1] for move left, [1,0] for move down, not up! [-1,0] for move up.
    :param p_move: probability of move
    :return p: probabilities of each place after this move
    '''
    assert len(motion) == 2
    q = []
    rows = len(p)
    cols = len(p[0])
    for i in range(rows):
        q.append([])
        for j in range(cols):
            prob = p[i][j] * (1-p_move)
            prob += p[(i-motion[0]) % rows][(j-motion[1]) % cols] * p_move
            q[i].append(prob)
    return q

def sense(p, colors, measurement, sensor_right):
    '''
    Update probabilities of each place after receiving information from sensor
    for one time (for cyclic movement)
    :param p: probabilities of each place
    :param colors: color of each place
    :param measurement: information receive from sensor
    :param sensor_right: the probability of sensor that sensor correctly
    :return p: probabilities of each place after receiving information from sensor
                for one time
    '''
    assert len(p) == len(colors) and len(p[0]) == len(colors[0])
    # in fact, assertion should be more than this

    q = []
    for i in range(len(colors)):
        q.append([])
        for j in range(len(colors[0])):
            hit = (colors[i][j].lower() == measurement.lower())
            q[i].append(p[i][j] * (hit * sensor_right + (1-hit) * (1-sensor_right)))

    # normalize it
    s = 0.0
    for i in range(len(q)):
        s += sum(q[i])
    q = [[q[i][j]/s for j in range(len(q[0]))] for i in range(len(q))]
    return q

def test():
    colors = [['red', 'green', 'green', 'red', 'red'],
              ['red', 'red', 'green', 'red', 'red'],
              ['red', 'red', 'green', 'green', 'red'],
              ['red', 'red', 'red', 'red', 'red']]
    measurements = ['green', 'green', 'green', 'green', 'green']
    motions = [[0,0], [0,1], [1,0], [1,0], [0,1]]
    sensor_right = 0.7
    p_move = 0.8

    # init p
    p = []
    s = len(colors) * len(colors[0])
    for row in range(len(colors)):
        one_row = [1./s for _ in range(len(colors[0]))]
        p.append(one_row)

    for i in range(len(motions)):
        p = move(p, motions[i], p_move)
        p = sense(p, colors, measurements[i], sensor_right)
    # print(p)

    import sys
    sys.path.append('../basic')
    from Matrix import matrix
    p_mat = matrix(p)
    print(p_mat)

if __name__ == '__main__':
    colors = [['green', 'green', 'green'],
              ['green', 'red', 'red'],
              ['green', 'green', 'green']]

    measurements = ['red', 'red']
    motions = [[0, 0],[0, 1]]

    sensor_right = 0.8
    p_move = 1.0

    # init p
    p = []
    s = len(colors) * len(colors[0])
    for row in range(len(colors)):
        one_row = [1./s for _ in range(len(colors[0]))]
        p.append(one_row)

    for i in range(len(motions)):
        p = sense(p, colors, measurements[i], sensor_right)
        p = move(p, motions[i], p_move)
    print(p)

    # test
    test()