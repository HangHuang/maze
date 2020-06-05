#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 下午7:21
# @Author  : future
# @File    : maze.py
# @summary : Generate a labyrinth

import random
import copy
import pygame
import time
from pygame.locals import *


def print_maze(maze):
    size = len(maze)
    t_maze = copy.deepcopy(maze)
    print("maze initialize ok, as follow:")
    for i in range(size):
        for j in range(size):
            if maze[i][j] == 0:
                t_maze[i][j] = "-"
            else:
                t_maze[i][j] = "1"

    t_maze[0][0] = "s"
    t_maze[size-1][size-1] = "t"
    for item in t_maze:
        print(item)


# size is the length of maze, wall_num is the number of wall,
# generate different labyrinths by modifying the random_init parameter
def init_maze(size, wall_num, random_init=1):
    random.seed(random_init)
    matrix = [([1] * size) for i in range(size)]

    not_go = [([0] * size) for i in range(size)]
    not_go[0][0] = 1
    not_go[1][0] = 1
    not_go[2][0] = 1
    for i in range(size - 1):
        not_go[2][i] = 1
    for i in range(3,size,1):
        not_go[i][size - 2] = 1
    not_go[size - 1][size - 1] = 1

    wall_get = 0
    for i in range(size * size * 100):
        index_row = random.randint(0, size - 1)
        index_col = random.randint(0, size - 1)
        if not_go[index_row][index_col] == 0:
            matrix[index_row][index_col] = 0
            not_go[index_row][index_col] = 1
            wall_get +=1
            if wall_get == wall_num:
                break
    if wall_get < wall_num:
        raise ValueError("wall_num is too large!")
    print_maze(matrix)
    return matrix


def print_path(maze,path):
    size = len(maze)
    for i in range(size):
        for k in range(size):
            if maze[i][k] == 0:
                path[i][k] = "-"
            else:
                path[i][k] = str(path[i][k])
    for item in path:
        print(item)


# pos = (x, y), top left position of the rect
def set_block(screen, color, pos,block_size):
    top_side_rect   = Rect(pos[0], pos[1], block_size, 1)
    right_side_rect = Rect(pos[0] + block_size, pos[1], 1, block_size)
    bottom_side_rect= Rect(pos[0], pos[1] + block_size, block_size, 1)
    left_side_rect  = Rect(pos[0], pos[1], 1, block_size)
    center_rect     = Rect(pos[0]+1, pos[1]+1, block_size-1, block_size-1)
    pygame.draw.rect(screen, (255, 255, 255), top_side_rect)
    pygame.draw.rect(screen, (255, 255, 255), right_side_rect)
    pygame.draw.rect(screen, (255, 255, 255), bottom_side_rect)
    pygame.draw.rect(screen, (255, 255, 255), left_side_rect)
    pygame.draw.rect(screen, color, center_rect)


def draw_path(maze,path,block_size,algrithmn_name="maze"):
    pygame.init()
    pygame.display.set_caption(algrithmn_name)
    map_size = len(maze)
    screen = pygame.display.set_mode((block_size * map_size, block_size * map_size), pygame.RESIZABLE)
    screen.fill((255, 255, 255))

    for yIdx, rowItem in enumerate(maze):
        for xIdx, blockItem in enumerate(rowItem):
            if blockItem == 0:
                block_pos = (xIdx * block_size, yIdx * block_size)
                set_block(screen, (0, 0, 0), block_pos,block_size)

    posX = 0
    posY = 0
    set_block(screen, (255, 0, 0), (0, 0), block_size)  # start point
    set_block(screen, (0, 0, 255), ((map_size - 1) * block_size, (map_size - 1) * block_size), block_size)  # end point
    pygame.display.update()

    for direction in path:
        t_posX = posX + direction[0]
        t_posY = posY + direction[1]
        if t_posX >= 0 and t_posX < map_size and t_posY >= 0 and t_posY < map_size and maze[t_posX][t_posY] != 0:
            posX = t_posX
            posY = t_posY
            time.sleep(0.5)
        else:
            continue

        if posX == 0 and posY == 0:
            continue

        current_pos = (posY * block_size, posX * block_size)
        set_block(screen, (0, 255, 0), current_pos,block_size)
        pygame.display.update()

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
    pass




if __name__ == "__main__":
    maze = init_maze(size=5,wall_num=12,random_init=6666666)
    draw_path(maze,[],40)



