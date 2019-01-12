'''This program contains some core functions for the games 2048: it basically 
consists in manipulating 2-D arrays
By Kouame KOUASSI
On 27 april 2014'''
import datetime
import os
import numpy as np

def create_grid(grid):
    """create a 4x4 grid"""
    for i in range(4):
        x= [0]*4
        grid.append(x)
    return grid

def print_grid (grid):
    """print out a 4x4 grid in 5-width columns within a box"""    
    #print the upper part of the frame
    print('+--------------------+')
    #print the array and the borders of the frame
    x = "{0:<5}"
    for i in range(4):
        for j in range(4):
            if j == 0:
                print('|',end='')
            if grid[i][j] == 0:
                print(x.format(' '),end = '')
            else:
                print(x.format(grid[i][j]),end='')
            if j == 3:
                print('|')
       
    #print the lower part of the frame
    print('+--------------------+') 
    
    
def check_lost (grid):
    """return True if there are no 0 values and no adjacent values that are equal; otherwise False"""
    #separate these conditions into tzo differents conditions
    condition_1 = True
    condition_2 = True
    #check if there are 0 values
    for i in grid:
        #i is assigned each sub_string and check if 0 is a value of i
        if 0 in i:
            condition_1 = False
            break
        else:
            continue
    #check if no adjacent values that are equal except the horizontally in row 4
    for i in range(3):
        for j in range(3):
            if grid[i][j] == grid[i][j+1] or grid[i][j] == grid[i+1][j]:
                condition_2 = False
                break
            else :
                continue
    #check horizontally for row 3 
    else:
        for i in range(3):
            if grid[3][i] == grid[3][i+1]:
                condition_2 = False
                break
            else:
                continue
    #return True if condition_1 stays True(0 not found) and as well as condition_2(not adjacent found)
    if condition_1 and condition_2:
        return True
    else:
        return False
    
    
def check_won (grid):
    """return True if a value>=32 is found in the grid; otherwise False""" 
    #i gets assigned each array in the grid
    for i in grid:
        #j gets assigned eah value in i
        for j in i:
            #check if a value in j in bigger than or equal to 32 and if so return True
            if j >= 2048:
                return True
    #return False if value bigger than or equal to 32 not found
    return False

def copy_grid (grid):
    """return a copy of the grid"""
    #create an empty grid
    grid_copy = create_grid([])
    for i in range(4):
        for j in range(4):
            grid_copy[i][j] = grid[i][j]
    return grid_copy

def grid_equal (grid1, grid2):
    """check if 2 grids are equal - return boolean value"""
    if grid1 == grid2:
        return True
    return False

def action_letter_to_num(letter):
    if letter == 'l':
        return 1
    elif letter == 'r':
        return 3
    elif letter == 'u':
        return 5
    elif letter == 'd':
        return 2
    return

def action_num_to_letter(num):
    if num == 1:
        return 'l'
    elif num == 3:
        return 'r'
    elif num == 5:
        return 'u'
    elif num == 2:
        return 'd'
    return

def load_game(filename="games/human/human_09-01-19-16-55.csv"):
    trajectory = np.loadtxt(filename, delimiter=',')
    current_states = trajectory[:, 0:16]
    actions = trajectory[:, 16]
    rewards = trajectory[:, 17]
    cumulated_rewards = trajectory[:, 18]
    next_states = trajectory[:, 19:]
    #exclude the last actions
    return current_states[:-1], actions[:-1], rewards[:-1], cumulated_rewards[:-1], next_states[:-1]


def load_games(directory="games/human/"):
    if os.path.isdir(directory):
        current_states = np.ndarray(shape=(0,16))
        actions = np.array([])
        rewards = np.array([])
        cumulated_rewards = np.array([])
        next_states = np.ndarray(shape=(0, 16))
        for filename in os.listdir(directory):
            temp_current_states, temp_actions, temp_rewards, temp_cumulated_rewards, temp_next_states = load_game(filename=directory + filename)
            current_states = np.concatenate((current_states, temp_current_states))
            actions = np.concatenate((actions, temp_actions))
            rewards = np.concatenate((rewards, temp_rewards))
            cumulated_rewards = np.concatenate((cumulated_rewards, temp_cumulated_rewards))
            next_states = np.concatenate((next_states, temp_next_states))
        return current_states, actions, rewards, cumulated_rewards, next_states
    else:
        print("Folder does not exist!")
        exit(0)

    
def save_game(trajectory, filename='games/game'):
    current_time = datetime.datetime.now()
    current_time = current_time.strftime("_%d/%m/%y/%H:%M").replace('/', '-').replace(':', '-')
    filename = filename + current_time + ".csv"
    np.savetxt(filename, trajectory, delimiter=',')


if __name__=="__main__":
    current_states, actions, rewards, cumulated_rewards, next_states = load_games(directory="games/human/")
    #print("current_states: ", current_states[-5:])
    unique_actions, action_counts = np.unique(actions[:-1].astype(int), return_counts=True)
    print(unique_actions, action_counts)
    print(np.asarray(([action_num_to_letter(i) for i in unique_actions], action_counts/(len(actions)-1))))
    #print("rewards: ", rewards[:200])
    #print("actions: ", actions[:100])
    
