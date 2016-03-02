# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

import sys
sys.path.append('../basic')
from tools import print_list

grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

forward =  [[-1, 0], # go up
            [0, -1], # go left
            [1, 0], # go down
            [0, 1]] # go right
forward_name = ['↑', '←', '↓', '→']
UNREACHABLE = 999

# the cost field has 3 value: right turn, no turn, left turn
cost = [2, 1, 10]

action = [-1, 0, 1]
action_name = [' R', ' #', ' L']


def dynamic_search(init, goal):
    value = [[[UNREACHABLE for _ in range(len(grid[0]))]
             for _ in range(len(grid))]
             for _ in range(len(forward))]

    policy = [[['■' for _ in range(len(grid[0]))]
              for _ in range(len(grid))]
              for _ in range(len(forward))]

    policy_2D = [['■' for _ in range(len(grid[0]))] for _ in range(len(grid))]

    change = True

    while(change):
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for orientation in range(len(forward)):

                    if(goal[0] == x and goal[1] == y):
                        if(value[orientation][x][y] > 0):
                            value[orientation][x][y] = 0
                            policy[orientation][x][y] = '＊'
                            change = True
                    elif(grid[x][y] == 0):
                        for i in range(len(action)):
                            o2 = (orientation + action[i]) % len(forward) # tricky
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]

                            if((0 <= x2 < len(grid)) and (0 <= y2 < len(grid[0])) and
                                   (grid[x2][y2] == 0)):
                                v2 = value[o2][x2][y2] + cost[i]
                                if(v2 < value[orientation][x][y]):
                                    value[orientation][x][y] = v2
                                    policy[orientation][x][y] = action_name[i]
                                    change = True

    if(value[init[2]][init[0]][init[1]] < UNREACHABLE):
        result = 'Search successfully!'
    else:
        result = 'Failed.'

    x = init[0]
    y = init[1]
    orientation = init[2]
    policy_2D[x][y] = policy[orientation][x][y]

    while(policy[orientation][x][y] != '＊'):
        for i in range(len(action)):
            if(policy[orientation][x][y] == action_name[i]):
                orientation = (orientation + i + 3) % len(forward)
                x += forward[orientation][0]
                y += forward[orientation][1]
                policy_2D[x][y] = policy[orientation][x][y]

    return [result, value, policy_2D]


if __name__ == '__main__':
    init = [4, 3, 0]
    goal = [2, 0]

    [result, value, policy] = dynamic_search(init, goal)

    print(result)
    print_list(value)
    print_list(policy)