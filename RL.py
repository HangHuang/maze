# -*- coding: utf-8 -*
# -*- coding: cp936 -*-
## Intro to Reinforcement Learning Example - by Genevieve Hayes ##
## Use Q-Learning to find the optimal policy for a simple maze environment ##

# Import libraries
import numpy as np
import mdp
import maze as maze_api


# Create transition and reward matrices
def create_matrices(maze, reward, penalty_s, penalty_l, prob):
    """Create reward and transition matrices for input into the mdp QLearning
    function
    
    Args:
    maze: array. 0-1 numpy array giving the positions of the white cells
    (denoted 1) and the gray cells (denoted 0) in the maze;
    reward: float. Reward for reaching the end of the maze;
    penalty_s: float. Penalty for entering a white cell;
    penalty_l: float. Penalty for entering a gray cell;
    prob: float. Probability of moving in the intended direction.
    
    Returns:
    R: array. Reward matrix;
    T: array. Transition matrix.
    """
    
    r, c = np.shape(maze)
    states = r*c
    p = prob
    q = (1 - prob)*0.5
    
    # Create reward matrix
    path = maze*penalty_s
    walls = (1 - maze)*penalty_l
    combined = path + walls
    
    combined[-1, -1] = reward
            
    R = np.reshape(combined, states)
    
    # Create transition matrix
    T_up = np.zeros((states, states))
    T_left = np.zeros((states, states))
    T_right = np.zeros((states, states))
    T_down = np.zeros((states, states))
    
    wall_ind = np.where(R == penalty_l)[0]

    for i in range(states):
        # Up
        if (i - c) < 0 or (i - c) in wall_ind :
            T_up[i, i] += p
        else:
            T_up[i, i - c] += p
        
        if i%c == 0 or (i - 1) in wall_ind:
            T_up[i, i] += q
        else:
            T_up[i, i-1] += q
        
        if i%c == (c - 1) or (i + 1) in wall_ind:
            T_up[i, i] += q
        else:
            T_up[i, i+1] += q
            
        # Down
        if (i + c) > (states - 1) or (i + c) in wall_ind:
            T_down[i, i] += p
        else:
            T_down[i, i + c] += p
        
        if i%c == 0 or (i - 1) in wall_ind:
            T_down[i, i] += q
        else:
            T_down[i, i-1] += q
        
        if i%c == (c - 1) or (i + 1) in wall_ind:
            T_down[i, i] += q
        else:
            T_down[i, i+1] += q
            
        # Left
        if i%c == 0 or (i - 1) in wall_ind:
            T_left[i, i] += p
        else:
            T_left[i, i-1] += p
            
        if (i - c) < 0 or (i - c) in wall_ind:
            T_left[i, i] += q
        else:
            T_left[i, i - c] += q
        
        if (i + c) > (states - 1) or (i + c) in wall_ind:
            T_left[i, i] += q
        else:
            T_left[i, i + c] += q
        
        # Right
        if i%c == (c - 1) or (i + 1) in wall_ind:
            T_right[i, i] += p
        else:
            T_right[i, i+1] += p
            
        if (i - c) < 0 or (i - c) in wall_ind:
            T_right[i, i] += q
        else:
            T_right[i, i - c] += q
        
        if (i + c) > (states - 1) or (i + c) in wall_ind:
            T_right[i, i] += q
        else:
            T_right[i, i + c] += q
    
    T = [T_up, T_left, T_right, T_down] 
    
    return T, R


def convert_path(martix,step,x,y,is_go,path_):
    size = len(martix)
    if x ==size - 1 and y == size - 1:
        return 1
    off = [[-1,0],[0,-1],[0,1],[1,0]]
    v = martix[x][y]
    t_x = x + off[v][0]
    t_y = y + off[v][1]
    if t_x < 0 or t_x >= size or t_y < 0 or t_y >=size or is_go[t_x][t_y] > 0:
        return 0
    is_go[t_x][t_y] = step
    path_.append(off[v])
    return convert_path(martix,step+1,t_x,t_y,is_go,path_)


if __name__ == "__main__":
    maze_size = 5  # the length of maze
    wall_num = 7  # the number of wall
    random_init = 666666  # generate different labyrinths by modifying this parameter

    # Set q-learning parameters
    gamma = 0.9  # Discount factor
    alpha = 0.3  # Learning rate
    eps = 0.5  # Random action prob
    decay = 1.0  # Decay rate
    iters = 50000  # Number of iterations

    # Define maze array
    maze = maze_api.init_maze(size=maze_size, wall_num=wall_num, random_init=random_init)
    maze = np.asarray(maze, dtype=np.float32)

    # Create transition and reward matrices
    T, R = create_matrices(maze, 1, -0.04, -0.75, 0.8)

    # Run Q-learning algorithm to find optimal policy
    np.random.seed(1)
    q = mdp.QLearning(T, R, gamma, alpha, eps, decay, iters)
    q.run()

    # Print optimal policy
    pol = np.reshape(np.array(list(q.policy)), np.shape(maze))

    # Convert pol to the format required by maze_api for visualization
    is_go = [([0] * maze_size) for i in range(maze_size)]
    is_go[0][0] = 1
    path_ = []
    convert_path(pol, 2, 0, 0, is_go, path_)

    print("find path by Reorcement Learning, as follow:")
    maze_api.print_path(maze, is_go)
    maze_api.draw_path(maze, path_, block_size=40,algrithmn_name="RL")


