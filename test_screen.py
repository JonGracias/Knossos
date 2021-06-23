import pygame
import sys
from pygame.locals import *
import knossos.screen
from knossos.daedalus import daeda
from knossos.maze import Maze
from knossos.color import colors as c
import time


def main():
    # INIT -------------------------------------------------------------------------------------------------------
    pygame.init()
    clock = pygame.time.Clock()
    clock_tick = 200
    screen = pygame.display.set_mode((605, 605))
    maze = daeda(15)
    mazemap = maze.mazemap
    xl = []
    widthl = []
    for value in mazemap:
        x, y, width, height = value 
        xl.append((x, y))
        widthl.append((width, height))

    mazegrid = maze.grid
    mazeandron = maze.andron
    maze_screen = pygame.Surface((605, 605), pygame.SRCALPHA)
    maze_screen.fill(c.MDBLUE)


    # RUNGAME-----------------------------------------------------------------------------------------------------
    RUNNING = True
    while RUNNING:
        checkForQuit()
        for value in mazemap:
            x, y, width, height = value 
            screen.blit(maze_screen, (0, 0))
            CELL_SURF = pygame.Surface((width, height), pygame.SRCALPHA)
            CELL_SURF.fill(c.WHITE)
            maze_screen.blit(CELL_SURF, [x, y])
            pygame.display.update()
            time.sleep(.05)





# QUITGAME--------------------------------------------------------------------------------------------------------


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


if __name__ == '__main__':
    main()