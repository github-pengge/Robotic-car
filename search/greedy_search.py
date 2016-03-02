# -*- coding: utf-8 -*-
__author__ = 'Jiapeng Hong'

from copy import deepcopy
import sys
sys.path.append('../basic')
from tools import print_list

# grid format:
#   0: navigable space
#   1: occupied space
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
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
    min_path_len = open_list[0][0]
    min_path_len_index = 0
    for i in range(1, len(open_list)):
        if(open_list[i][0] <= min_path_len):
            min_path_len = open_list[i][0]
            min_path_len_index = i
    return min_path_len_index


def search_around(p, open_list, check_list, action):
    '''
    Searching around p to find all the grids that are reachable.
    :param p: place to search around, format as [g_val, x_index, y_index]
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
        x = p[1] + delta[i][0]
        y = p[2] + delta[i][1]
        if(0 <= x < rows and 0<= y < cols):
            if(check_list[x][y] == 0):
                reachable_grid.append([g_val + cost, x, y])
                check_list[x][y] = 1
                action[x][y] = i
    return reachable_grid


def greedy_search(init, goal):
    open_list = [[0, init[0], init[1]]]
    check_list = deepcopy(grid)
    check_list[init[0]][init[1]] = 1
    index = take_one(open_list)
    # step = -1
    # expand = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    action = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    while(index is not None):
        p = open_list.pop(index)
        # step += 1
        # expand[p[1]][p[2]] = step
        if(p[1] == goal[0] and p[2] == goal[1]): # reach goal
            print('Search successfully.')
            # return [p, expand]
            return [p, action]
        reachable_grid = search_around(p, open_list, check_list, action)
        open_list.extend(reachable_grid)

        if(DEBUG):
            print('---------------')
            print('take list item: %s' % p)
            print('new open list:')
            print_list(open_list, indent=4)

        index = take_one(open_list)
    # return ['Failed.', expand]
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



if __name__ == '__main__':
    init = [0,0]
    goal = [len(grid)-1, len(grid[0])-1]
    [result, action] = greedy_search(init, goal)
    print('Final open list: %s' % result)
    # print_list(expand)
    print('action: ')
    print_list(action)
    print('The path is as follow:')
    print_list(find_path(init, goal, action), indent=4)