# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

import sys
sys.path.append('../basic')
from tools import print_list

# grid format:
#   0: navigable space
#   1: occupied space
# grid = [[0, 0, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 1, 0]]
grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
delta = [[-1, 0], # go up
         [0, -1], # go left
         [1, 0], # go down
         [0, 1]] # go right
delta_name = ['↑', '←', '↓', '→']
cost = 1.0
success_prob = 1.0
fail_prob = (1 - success_prob) / 2.0
collision_cost = 100.0
UNREACHABLE = 1000.0
DEBUG = True


def stochastic_walk(goal):
    value = [[UNREACHABLE for _ in range(len(grid[0]))] for _ in range(len(grid))]
    policy = [['■' for _ in range(len(grid[0]))] for _ in range(len(grid))]

    change = True

    while(change):
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if(goal[0] == x and goal[1] == y): # if it's the goal
                    if(value[x][y] > 0):
                        value[x][y] = 0.0
                        policy[x][y] = '＊'
                        change = True

                elif(grid[x][y] == 0): # if it's reachable (not a wall)
                    for orient in range(len(delta)):
                        # x += delta[orient][0]
                        # y += delta[orient][1]
                        v2 = cost

                        for i in range(-1, 2):
                            orient2 = (orient + i) % len(delta)
                            x2 = x + delta[orient2][0]
                            y2 = y + delta[orient2][1]

                            if(i == 0): # up
                                p2 = success_prob
                            else:
                                p2 = fail_prob

                            # check whether (x2,y2) is valid or not
                            if((0 <= x2 < len(grid)) and (0 <= y2 < len(grid[0])) and
                                       grid[x2][y2] == 0): # (x2,y2) is reachable
                                v2 += (value[x2][y2] * p2)
                            else: # (x2,y2) is a wall
                                v2 += (collision_cost * p2)
                        if(v2 < value[x][y]):
                            change = True
                            value[x][y] = v2
                            policy[x][y] = delta_name[orient]

    return [value, policy]



if __name__ == '__main__':
    goal = [0, len(grid[0])-1]
    [value, policy] = stochastic_walk(goal)
    print_list(value)
    print('---------------------')
    print_list(policy)