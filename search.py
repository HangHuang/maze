#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 下午8:15
# @Author  : future
# @File    : search.py
# @summary : Find a path by searching

import maze as maze_api


def is_legal(x,y,is_go,maze):
    global maze_size
    if x < 0 or y <0 or x >= maze_size or y >= maze_size:
        return False
    if is_go[x][y] != 0 or maze[x][y] == 0:
        return False
    return True

def search_path(maze,is_go,x,y,step,path):
    size = len(maze)
    if x == size -1 and y == size -1:
        return 1
    offs = [[0,1],[1,0],[-1,0],[0,-1]]
    for off in offs:
        t_x = x + off[0]
        t_y = y + off[1]
        if is_legal(t_x,t_y,is_go,maze):
            is_go[t_x][t_y] = step
            path.append(off)
            find = search_path(maze,is_go,t_x,t_y,step + 1,path)
            if find == 1:
                return 1
            is_go[t_x][t_y] = 0
            path.pop()


if __name__ == "__main__":
    maze_size = 5  # the length of maze
    wall_num = 7  # the number of wall
    random_init = 666666  # generate different labyrinths by modifying this parameter
    maze = maze_api.init_maze(size=maze_size, wall_num=wall_num, random_init=random_init)

    path = []
    is_go = [([0] * maze_size) for i in range(maze_size)]
    is_go[0][0] = 1
    search_path(maze, is_go, 0, 0, 2, path)

    print("find path by search, as follow:")
    print(path)
    maze_api.print_path(maze, is_go)
    maze_api.draw_path(maze, path, block_size=40,algrithmn_name="search")