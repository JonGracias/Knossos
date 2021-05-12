
import pygame
pygame.init()

# colors--------------------------------------------------------------------------------------------------------------
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (78,   0,   0)
LIGHTRED   = (178,   0,   0)
GREEN = (0, 128, 0)
BLUE  = (  0,   0, 255)
DARKBLUE  = (  0,   0, 128)
LIMEGREEN = (0, 255, 0)
SILVER = (198, 198, 198)
YELLOW = (255, 255, 0)

# DISPLAYSURF size, Background size and location, grid location--------------------------------------------------------------------------------------------
WINDOW = 800
WINDOWX = 1000
WALLSIZE = int(WINDOW / 200)
BGSIZE = int((WINDOW * .9))
LOC = int(WINDOW * .05)
GRIDLOC = int(LOC + 2)
BASICFONTSIZE = 20

# Game time------------------------------------------------------------------------------------------------------------
FPS = 60
FPSCLOCK = pygame.time.Clock()

# Grid information----------------------------------------------------------------------------------------------
cellNum = 20
cellSize = int(BGSIZE / cellNum ) - WALLSIZE
xs, ys = 0, 0
xe, ye = 0, 0
grid = []

# Grid coords--------------------------------------------------------------------------------------------------
solution = {}
stack = []
visited = []

# character variables------------------------------------------------------------------------------------------------
andron = {}
chrono = cellNum * 7
clio = {}
minotaurVisited = []
companionVisited = []
minotaurspeed = 1000
companionspeed = 500







