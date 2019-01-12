"""2048 game
hussein suleman
25 april 2014"""

#for command line argument
import sys
# random number generator
import random
# grid utility routines
import util
# grid value merging routines
import push
# AI agents to play the game
import agents
#to slow down the game when agents is not human
import time
import numpy as np

HUMAN = 'human'
RANDOM = 'random'
RANDOM_WITH_PRIOR = 'prior'
SVM = 'svm'
NN = 'nn'

def add_block (grid):
    """add a random number to a random location on the grid"""
    # set distributon of number possibilities
    options = [2, 4]
    options_distr = [0.93, 0.7]
    # get random number
    chosen = random.choices(options, options_distr)[0]
    found = False
    while (not found):
        # get random location
        x = random.randint (0, 3)
        y = random.randint (0, 3)
        # check and insert number
        if (grid[x][y] == 0):
            grid[x][y] = chosen
            found = True

def play (agent='human', record=True, filename='human_games.dat', delay=1):
    """generate grid and play game interactively"""
    # create grid
    grid = []
    util.create_grid (grid)
    # add 2 starting random numbers
    add_block (grid)
    add_block (grid)
    won_message = False
    score = 0
    trajectory = []
    saved_grid = [[]]
    try:
        while (True):
            util.print_grid (grid)
            if agent == HUMAN:
                key = input ("Enter a direction:\n")
                if (key == 'x'):
                    # quit the game
                    break
                try:
                    key = util.action_num_to_letter(int(key))
                except:
                    continue
            elif agent == SVM or agent == NN:   
                if util.grid_equal(saved_grid, grid): #previous action not allowed
                    #use pior agent since model is deterministic given the same input
                    key = agents.random_agent_with_prior()
                    print("Prior")
                else:
                    print("Model")
                    model_agent = agents.Model()
                    model_agent.load_model(filename="models/" + agent + ".joblib")
                    key = model_agent.predict([np.array(grid).flatten()])
                    key = util.action_num_to_letter(int(key[0]))
                print(key)
            elif agent == RANDOM:
                key = agents.random_agent()
            elif agent == RANDOM_WITH_PRIOR:
                key = agents.random_agent_with_prior()
            if (key in ['u', 'd', 'l', 'r']):
               # make a copy of the grid
                saved_grid = util.copy_grid (grid)
                # manipulate the grid depending on input
                if (key == 'u'):
                    _, add_score = push.push_up (grid)
                elif (key == 'd'):
                    _, add_score = push.push_down (grid)
                elif (key == 'r'):
                    _, add_score = push.push_right (grid)
                elif (key == 'l'):
                    _, add_score = push.push_left (grid)
                score += add_score
                print("Score: ", score)
                if record and key in 'ludr':
                    data_instance = np.array(saved_grid).flatten()
                    data_instance = np.append(data_instance, [util.action_letter_to_num(key), add_score, score])
                    data_instance = np.append(data_instance, np.array(grid).flatten())
                    trajectory.append(data_instance)
                # check for a grid with no more gaps or legal moves
                if util.check_lost (grid):
                    print ("Game Over!")
                    break
                # check for a grid with the final number
                elif util.check_won (grid) and not won_message:
                    print ("Won!")
                    won_message = True
                # finally add a random block if the grid has changed    
                if not util.grid_equal (saved_grid, grid):
                    add_block (grid)
            if agent != HUMAN:
                time.sleep(delay) #in seconds
    finally:
        if record:
            util.save_game(trajectory, filename="games/" + agent.lower() + "/" + agent.lower())

if __name__=="__main__":
    # initialize the random number generator to a fixed sequence
    random.seed (1)
    # play the game
    delay = 1
    if len(sys.argv) > 1:
        agent = sys.argv[1]
        if len(sys.argv) > 2:
           seed = sys.argv[2]
           random.seed (seed)
           if len(sys.argv) > 3:
               delay = sys.argv[3]
    else:
        agent = 'human'
    play(agent, delay=int(delay), record=True)
