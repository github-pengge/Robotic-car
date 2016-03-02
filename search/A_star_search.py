# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

from copy import deepcopy
import sys
sys.path.append('../basic')
from tools import print_list

# grid format:
#   0: navigable space
#   1: occupied space
grid = [[0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0]]
delta = [[-1, 0], # go up
         [0, -1], # go left
         [1, 0], # go down
         [0, 1]] # go right
delta_name = ['↑', '←', '↓', '→']
cost = 1
DEBUG = False


def take_one(open_list):
    if(len(open_list) == 0):
        return None
    min_path_len = open_list[0][1]
    min_path_len_index = 0
    for i in range(1, len(open_list)):
        if(open_list[i][1] <= min_path_len):
            min_path_len = open_list[i][1]
            min_path_len_index = i
    return min_path_len_index


def search_around(p, heuristic, open_list, check_list, action):
    '''
    Searching around p to find all the grids that are reachable.
    :param p: place to search around, format as [g_val, x_index, y_index]
    :param heuristic: min distance to goal of each grid without considering blocks.
    :param open_list: records the grids that had been under consideration
    :param check_list: identifies whether a grid is check or not
    :param action: records action of the previous step
    :return: all the around grids that are reachable.
            Warning: check_list may also changed.
    '''
    reachable_grid = []
    g_val = p[0]
    rows = len(grid)
    cols = len(grid[0])
    for i in range(len(delta)):
        x = p[2] + delta[i][0]
        y = p[3] + delta[i][1]
        g2_val = g_val + cost
        if(0 <= x < rows and 0<= y < cols):
            if(check_list[x][y] == 0):
                reachable_grid.append([g2_val, g2_val + heuristic[x][y], x, y])
                check_list[x][y] = 1
                action[x][y] = i
    return reachable_grid


def A_star_search(init, goal, heuristic):
    open_list = [[0, heuristic[init[0]][init[1]], init[0], init[1]]]
    check_list = deepcopy(grid)
    check_list[init[0]][init[1]] = 1
    index = take_one(open_list)
    step = -1
    expand = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    action = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    while(index is not None):
        p = open_list.pop(index)
        step += 1
        expand[p[2]][p[3]] = step
        if(p[2] == goal[0] and p[3] == goal[1]): # reach goal
            print('Search successfully.')
            # return [p, expand]
            print_list(expand)
            return [p, action]
        reachable_grid = search_around(p, heuristic, open_list, check_list, action)
        open_list.extend(reachable_grid)

        if(DEBUG):
            print('---------------')
            print('take list item: %s' % p)
            print('new open list:')
            print_list(open_list, indent=4)

        index = take_one(open_list)
    # return ['Failed.', expand]
    print_list(expand)
    return ['Failed.', action]


def find_path(init, goal, action):
    path = [['  ' if u == 0 else '■' for u in grid[i]]
            for i in range(len(grid))]
    path[goal[0]][goal[1]] = '＊'
    x = goal[0]
    y = goal[1]
    while(action[x][y] != -1):
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        path[x2][y2] = delta_name[action[x][y]]
        x = x2
        y = y2
    return path


def get_heuristic(goal):
    heuristic = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    M = max(goal[0], len(grid)-goal[0])
    N = max(goal[1], len(grid[0])-goal[1])
    for i in range(M + 1):
        for j in range(N + 1):
            x = goal[0] - i
            y = goal[1] - j
            if(x >= 0 and y >= 0):
                heuristic[x][y] = i + j
            x2 = goal[0] + i
            y2 = goal[1] - j
            if(goal[0] < x2 < len(grid) and 0 <= y2 <= goal[1]):
                heuristic[x2][y2] = i + j
            x3 = goal[0] + i
            y3 = goal[1] + j
            if(goal[0] <= x3 < len(grid) and goal[1] < y3 < len(grid[0])):
                heuristic[x3][y3] = i + j
            x4 = goal[0] - i
            y4 = goal[1] + j
            if(0 <= x4 < goal[0] and goal[1] < y4 < len(grid[0])):
                heuristic[x4][y4] = i + j
    return heuristic



if __name__ == '__main__':
    init = [0,0]
    goal = [len(grid)-1, len(grid[0])-1]
    heuristic = get_heuristic(goal)
    [result, action] = A_star_search(init, goal, heuristic)
    print('Final open list: %s' % result)
    # print_list(expand)
    print('action: ')
    print_list(action, indent=4)
    print('The path is as follow:')
    print_list(find_path(init, goal, action), indent=4)