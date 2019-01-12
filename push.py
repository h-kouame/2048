''' Kouame Kouassi
this module contains the core functions to play the 2048 game
It basically removes spaces and add the values vertically and horizontally
the algorithm consists in doing just for left and make use of symmetry
to do others'''


def push_up (grid):
    """merge grid values upwards by using the same concept as for push down(see push_down comments)"""
    grid_sym = []
    for i in range(4):
            x= [0]*4
            grid_sym.append(x)   
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid_sym[i][j]=grid[j][i]
    #use push_left instead of push_right
    grid_sym, score = push_left (grid_sym)
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[j][i]=grid_sym[i][j]     
     
    return grid, score
    
def push_down (grid):
    """merge grid values downwards by making use of the push_right function"""
    #create a new grid to store the reflected grid across y=x axis
    grid_sym = []
    for i in range(4):
        x= [0]*4
        grid_sym.append(x)
    #make a reflection of the grid across y=x axis to create the conditions of using push_right function
    for i in range(len(grid)):
        for j in range(len(grid)):
            #x of grid becomes y in grid_sym and vis-versa 
            grid_sym[i][j]=grid[j][i]
    #call push_right to merge
    grid_sym, score = push_right (grid_sym)
    #restore the downward_pushed grid
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[j][i]=grid_sym[i][j]     
         
    return grid, score   
        
        
    
    
def remove_space(grid):
    '''remove the spaces within the numbers to pack them up'''
    #iterate over each row of the grid
    for i in range(len(grid)):
        #search for space in the row
        for j in range(len(grid)-1,0,-1):
            if grid[i][j-1] == 0:
                #space is found, so shift to the left
                for k in range(-4+j,0):
                    #shift the values after the space by one unit to the left
                    grid[i][k-1] = grid[i][k]
                    #empty the value shifted
                    grid[i][k] = 0

                    
def merge_left(grid):
    '''add two consecutive same values only once starting from the left'''
    score = 0
    #iterate over each row
    for i in range(len(grid)):
        #search for two consecutive same values from the left
        for j in range(len(grid)-1):
            #exclud the case where values are 0
            if grid[i][j] == grid[i][j+1] and grid[i][j] != 0:
                #search positive so add up the values in the first column
                new_value = grid[i][j]*2
                grid[i][j] = new_value
                score += new_value
                
                #empty the value of the second column
                grid[i][j+1]= 0
    return score
                
    
def push_left (grid):
    """merge grid values left"""
    #remove spaces to pack the values up
    remove_space(grid)
    #add the values where required
    score = merge_left(grid)
    #remove spaces left due to the additions
    remove_space(grid)
                
    return grid, score 
    
    
def push_right (grid):
    """merge grid values right by making use of the push_left function"""
    #reverse each list to put the array in the condition of the push_left function
    for i in range(len(grid)):
        grid[i][:] = grid[i][::-1]
    #use push_left to pack and merge
    grid_sym, score = push_left (grid)
    #restore the array in the pushed right position
    for i in range(len(grid)):
        grid[i][:] = grid_sym[i][::-1]    
    
    return grid, score
               
    
    
