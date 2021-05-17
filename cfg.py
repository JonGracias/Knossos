
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

COLOR_LIST = [BLUE, GREEN, RED, YELLOW, LIMEGREEN, LIGHTRED, DARKBLUE]

# DISPLAYSURF size, Background size and location, grid location--------------------------------------------------------------------------------------------
WINDOW = 800
WINDOWX = 1200
WALLSIZE = int(WINDOW / 200)
BGSIZE = int((WINDOW * .9))
LOC = int(WINDOW * .05)
GRIDLOC = int(LOC + 2)
BASICFONTSIZE = 20

# Game time------------------------------------------------------------------------------------------------------------
FPS = 30
FPSCLOCK = pygame.time.Clock()

# Grid information----------------------------------------------------------------------------------------------
cellNum = 10
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
minotaurspeed = 1500

player_color = GREEN
minotaur_color = RED
companion_color = BLUE

LOST = False
MAIN = 'main'
SETUP = 'setup'
PLAYING = 'playing'
PAUSED = 'paused'
GAMEOVER = 'gameover'

gamestate = MAIN

scoreFile = 'score.data'
score = 0
high_score = None





