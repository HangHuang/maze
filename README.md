# 人工智能走迷宫

## 简介
本项目使用python3开发，包含三个功能  
- 用深度优先搜索算法走迷宫  
- 用强化学习走迷宫  
- 用遗传算法走迷宫

maze.py 文件用于迷宫的生成及可视化  
search.py 文件是 深度优先搜索算法 的入口文件  
RL.py 是强化学习的入口文件  
GA.py 是遗传算法的入口文件  



## 使用说明

1 .安装依赖，主要包括 pygame, scipy和numpy(若缺少其它库，根据报错提示自行安装):


    pip3 install pygame
    pip3 install scipy
    pip3 install numpy
    
    
2 .开始走迷宫


    # 用深度优先搜索算法走迷宫
    python3 search.py
    # 用强化学习走迷宫
    python3 RL.py
    # 用遗传算法走迷宫
    python3 GA.py
    
    # 上面的代码中，maze_size设置迷宫的大小，其值不应该小于4. 
    # wall_num 用于设置墙的数量，其值应小于 maze_size×maze_size×0.6
    # random_init 是随机数种子，修改该值能够生产不同的迷宫
    
    