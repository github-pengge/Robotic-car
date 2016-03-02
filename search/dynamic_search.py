# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

import sys
sys.path.append('../basic')
from tools import print_list

# grid format:
#   0: navigable space
#   1: occupied space
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
delta = [[-1, 0], # go up
         [0, -1], # go left
         [1, 0], # go down
         [0, 1]] # go right
delta_name = ['↑', '←', '↓', '→']
step_cost = 1
UNREACHABLE = 99


def dynamic_search(init, goal):
    value = [[UNREACHABLE for _ in range(len(grid[0]))]
             for _ in range(len(grid))]

    policy = [['■' for _ in range(len(grid[0]))]
              for _ in range(len(grid))]

    change = True

    while(change):
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):

                if(goal[0] == x and goal[1] == y):
                    if(value[x][y] > 0):
                        value[x][y] = 0
                        policy[x][y] = '＊'
                        change = True
                elif(grid[x][y] == 0):
                    for i in range(len(delta)):
                        x2 = x + delta[i][0]
                        y2 = y + delta[i][1]

                        if((0 <= x2 < len(grid)) and (0 <= y2 < len(grid[0])) and
                               (grid[x2][y2] == 0)):
                            v2 = value[x2][y2] + step_cost
                            if(v2 < value[x][y]):
                                value[x][y] = v2
                                policy[x][y] = delta_name[i]
                                change = True

    if(value[init[0]][init[1]] < UNREACHABLE):
        result = 'Search successfully!'
    else:
        result = 'Failed.'

    return [result, value, policy]


if __name__ == '__main__':
    init = [0, 0]
    goal = [len(grid)-1, len(grid[0])-1]

    [result, value, policy] = dynamic_search(init, goal)

    print(result)
    print_list(value)
    print_list(policy)