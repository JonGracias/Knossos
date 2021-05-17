import pygame 
import cfg
import random
import time


# Create grid that fits inside of gameboard with variable number of cells---------------------------------------------
def createGrid():                                                               # creates the grid
    for i in range(cfg.cellNum):                                                # one x row
        x = ((cfg.cellSize * i) + (cfg.WALLSIZE * i))+ cfg.GRIDLOC              # cellNum of y rows
        for j in range(cfg.cellNum):                                    
            y = ((cfg.cellSize * j) + (cfg.WALLSIZE * j))+ cfg.GRIDLOC
            cfg.grid.append((x, y))                                             # appends it to grid dict


# Draw the grid-------------------------------------------------------------------------------------------------------
def renderGrid(DISPLAYSURF):                                                    # draws the grid
    x = [a[1] for a in cfg.grid]
    y = [a[1] for a in cfg.grid]
    
    for j in range(cfg.cellNum):
        for h in range(cfg.cellNum):
            color = random.choice(cfg.COLOR_LIST)
            pygame.draw.rect(DISPLAYSURF, color,
            pygame.Rect(x[j], y[h], cfg.cellSize, cfg.cellSize))


# Carves the maze-----------------------------------------------------------------------------------------------------
def daedalus(DISPLAYSURF):                                                          # makes the maze
        x, y = cfg.xs, cfg.ys                                                       # runs until it is grid size
        if len(cfg.visited) != len(cfg.grid):                                       
            cfg.stack.append((x, y))                                                # records moves and cells visited
            cfg.visited.append((x, y))
            while len(cfg.stack) > 0:                                               # only runs when stack is not empty if all moves not possible stak will pop() until it reaches 0
                time.sleep(0)
                cell = []                                                           # empties cells list
                if (x + cfg.cellSize + cfg.WALLSIZE, y
                    ) not in cfg.visited and (                                      # fills cells list with string directions
                x + cfg.cellSize + cfg.WALLSIZE, y) in cfg.grid:                    
                    cell.append("right")
                if (x - cfg.cellSize - cfg.WALLSIZE, y) \
                    not in cfg.visited and \
                (x - cfg.cellSize - cfg.WALLSIZE, y) in cfg.grid:
                    cell.append("left")
                if (x , y + cfg.cellSize + cfg.WALLSIZE) \
                    not in cfg.visited and \
                (x, y + cfg.cellSize + cfg.WALLSIZE) in cfg.grid:
                    cell.append("down")
                if (x, y - cfg.cellSize - cfg.WALLSIZE) \
                    not in cfg.visited and \
                (x, y - cfg.cellSize - cfg.WALLSIZE) in cfg.grid:
                    cell.append("up")

                if len(cell) > 0:                                                       # runs only if cells is not empty 
                    cell_chosen = (random.choice(cell))                                 # if there was no moves will available will not run
                    if cell_chosen == "right":                                          # picks random direction
                        push_right(DISPLAYSURF, x, y)
                        cfg.solution[(x + cfg.cellSize + cfg.WALLSIZE, y)] = x, y       # add chosen direction to solution dict
                        x = x + cfg.cellSize + cfg.WALLSIZE
                        cfg.visited.append((x, y))
                        cfg.stack.append((x, y))                                        # appends stack and visited

                    elif cell_chosen == "left":
                        push_left(DISPLAYSURF, x, y)
                        cfg.solution[(x - cfg.cellSize - cfg.WALLSIZE, y)] = x, y
                        x = x - cfg.cellSize - cfg.WALLSIZE
                        cfg.visited.append((x, y))
                        cfg.stack.append((x, y))


                    elif cell_chosen == "down":
                        push_down(DISPLAYSURF, x, y)
                        cfg.solution[(x, y + cfg.cellSize + cfg.WALLSIZE)] = x, y
                        y = y + cfg.cellSize + cfg.WALLSIZE
                        cfg.visited.append((x, y))
                        cfg.stack.append((x, y))

                    elif cell_chosen == "up":
                        push_up(DISPLAYSURF, x, y)
                        cfg.solution[(x, y - cfg.cellSize - cfg.WALLSIZE)] = x, y
                        y = y - cfg.cellSize - cfg.WALLSIZE
                        cfg.visited.append((x, y))
                        cfg.stack.append((x, y))
                else:
                    x, y = cfg.stack.pop()                                               # pop() stack until there 
                    backtracking_cell(DISPLAYSURF, x, y)                                 # until there is a possible move
                    time.sleep(0)                                                        # x, y are passed to backtracking_cell
                                                                                         # that draws the black background on maze
        cfg.FPSCLOCK.tick(cfg.FPS)                                                       # FPS CLOCK so that we can control speed


# Finds the fastest route using cfg.solution{}-------------------------------------------------------------------------
def goal(DISPLAYSURF):                                              # draws path to goal
    colors = [(random.choice(cfg.COLOR_LIST)), (cfg.BLACK)]                         
    emx = cfg.xe
    emy = cfg.ye
    for i in range(2):                                              # draws it twice once green other black
        emx = cfg.xe
        emy = cfg.ye
        for j in range(1):
            solution_cell(DISPLAYSURF, emx, emy, colors[i])         # passes x, y of key to solution cell which 
            while(emx, emy) != (cfg.xs, cfg.ys):                    # draws new rect of correct color and position
                emx, emy = cfg.solution[emx, emy]
                solution_cell(DISPLAYSURF, emx, emy, colors[i])
                time.sleep(.005)


# Draw the path and create dictionary of acceptable moves--------------------------------------------------------------
def push_up(DISPLAYSURF, x, y,):                                    # draws black lines over white lines of maze
    pygame.draw.rect(DISPLAYSURF, cfg.BLACK,                        # to make it look like there is an opening
    (x, y - cfg.WALLSIZE, cfg.cellSize, cfg.WALLSIZE), 0)           # records x, y in andron so that we can check
    cfg.andron[x, y - cfg.WALLSIZE] = True                          # if sprites are making a valid move
    pygame.display.update()

def push_down(DISPLAYSURF, x, y):
    pygame.draw.rect(DISPLAYSURF, cfg.BLACK, 
    (x, y + cfg.cellSize, cfg.cellSize, cfg.WALLSIZE), 0)
    cfg.andron[(x, y + cfg.cellSize)] = True
    pygame.display.update()

def push_left(DISPLAYSURF, x, y):
    pygame.draw.rect(DISPLAYSURF, cfg.BLACK, 
    (x - cfg.WALLSIZE, y, cfg.WALLSIZE, cfg.cellSize), 0)
    cfg.andron[(x - cfg.WALLSIZE, y)] = True
    pygame.display.update()

def push_right(DISPLAYSURF, x, y):
    pygame.draw.rect(DISPLAYSURF, cfg.BLACK, 
    (x + cfg.cellSize, y, cfg.WALLSIZE, cfg.cellSize), 0)
    cfg.andron[(x + cfg.cellSize, y)] = True
    pygame.display.update()


# Draw special cells---------------------------------------------------------------------------------------------------
# Used to show where point a and b are located. Game draws its own a and b
#def single_cell(DISPLAYSURF, x, y):
    #pygame.draw.rect(DISPLAYSURF, cfg.GREEN, 
    #(x + 2, y + 2, cfg.cellSize - 2, cfg.cellSize -2), 0)
    #pygame.display.update()
    #cfg.FPSCLOCK.tick(cfg.FPS)

# Background part of maze----------------------------------------------------------------------------------------------------
def backtracking_cell(DISPLAYSURF, x, y):                           
    pygame.draw.rect(DISPLAYSURF, cfg.BLACK, 
    (x, y, cfg.cellSize, cfg.cellSize))
    pygame.display.update()

# Draws the dots that show how to get from entrance to exit-----------------------------------------------------------
def solution_cell(DISPLAYSURF, x, y, color):
    pygame.draw.rect(DISPLAYSURF, color, 
    (x + (cfg.cellSize * .25), y+ (cfg.cellSize * .25
    ), cfg.cellSize * .5, cfg.cellSize * .5))
    pygame.display.update()

