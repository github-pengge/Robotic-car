# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

DEBUG = False


def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=1e-6):
    smooth_path = [[u for u in v] for v in path] # deep copy path for initialization
    N = len(path)
    change = True

    while(change):
        change = False

        for i in range(1, N-1): # excludes the first and last points
            x = smooth_path[i][0]
            y = smooth_path[i][1]
            smooth_path[i][0] += weight_data * (path[i][0] - smooth_path[i][0])
            smooth_path[i][0] += weight_smooth * (smooth_path[i+1][0]
                                                  + smooth_path[i-1][0]
                                                  - 2.0 * smooth_path[i][0])
            smooth_path[i][1] += weight_data * (path[i][1] - smooth_path[i][1])
            smooth_path[i][1] += weight_smooth * (smooth_path[i+1][1]
                                                  + smooth_path[i-1][1]
                                                  - 2.0 * smooth_path[i][1])

            if(DEBUG):
                print(path[i], smooth_path[i])

            if(abs(x - smooth_path[i][0]) > tolerance or
                       abs(y - smooth_path[i][1]) > tolerance):
                change = True

    return smooth_path


if __name__ == '__main__':
    path = [[0,0],
            [0,1],
            [0,2],
            [1,2],
            [2,2],
            [3,2],
            [4,2],
            [4,3],
            [4,4]]
    smooth_path = smooth(path, weight_data=0.5, weight_smooth=0.0)
    for i in range(len(path)):
        print('[' + ','.join('%.3f' % x for x in path[i]) + '] --> [' +
              ','.join('%.3f' % x for x in smooth_path[i]) + ']')