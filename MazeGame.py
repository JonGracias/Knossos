# CMIS226 - Assgignment 1
# Name: Jonatan Gracias
# Project Title: Maze Game
# Project Desciption: Find way to target in a randomly generated maze.
# work in progess
# basic setup for pygame

import pygame, sys
from pygame.locals import *
import daeda
import cfg
from theseus import Theseus
from cyrano import *
import time 



# start main------------------------------------------------------------------------------------------------------- 
def main():
    # INIT --------------------------------------------------------------------------------------------------------
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    #Window---------------------------------------------------------------------------------------------------------
    DISPLAYSURF = pygame.display.set_mode((cfg.WINDOWX, cfg.WINDOW))
    DISPLAYSURF.fill(cfg.BLACK)
    pygame.display.set_caption('MAZE GAME')

    #Game board------------------------------------------------------------------------------------------------------
    all_windows_list = pygame.sprite.Group()
    # info bar
    INFO = Window(cfg.RED, cfg.LOC, 10, 25)
    INFOMENU = Window(cfg.RED, cfg.LOC, cfg.BGSIZE + 50, 25)
    # maze
    MAZE = Window(cfg.WHITE, cfg.LOC, cfg.LOC, cfg.BGSIZE)
    all_windows_list.add(INFO, MAZE, INFOMENU)
    all_windows_list.draw(DISPLAYSURF)

    # Store the option buttons and their rectangles in OPTIONS----------------------------------------------------
    all_options_list = pygame.sprite.Group()
    RESET= Text('2:Reset',cfg.WHITE, cfg.BGSIZE - 295, cfg.BGSIZE + 50, 70, 20)
    SHOW = Text('3:Show Answer',cfg.WHITE, cfg.BGSIZE - 117, cfg.BGSIZE + 50, 153, 20)
    NEW= Text('1:New Game',cfg.WHITE, cfg.LOC + 150, cfg.BGSIZE + 50, 123, 20)
    SETTINGS = Text('0:Settings',cfg.WHITE, cfg.LOC, cfg.BGSIZE + 50, 100, 20)

    # Store time, level score, and high score---------------------------------------------------------------------
    lvl = 1
    TIME = Text('Time: ', cfg.WHITE, cfg.LOC + 105, 15, 60, 20)
    LEVEL = Text('Level: ' + str(lvl) , cfg.WHITE, cfg.LOC, 15, 75, 20)
    SCORE = Text('Score: ', cfg.WHITE, cfg.LOC + 380, 15, 65, 20)
    HIGHSCORE = Text('High Score: ', cfg.WHITE, cfg.LOC + 525, 15, 115, 20)
    all_options_list.add(RESET, SHOW, NEW, SETTINGS, TIME, LEVEL, SCORE, HIGHSCORE)
    all_options_list.draw(DISPLAYSURF)

    # Timer------------------------------------------------------------------------------------
    start_ticks=pygame.time.get_ticks() #starter tick
    font = pygame.font.Font('freesansbold.ttf', cfg.BASICFONTSIZE)
    te = 0
    time_surf = pygame.Surface((54, 20))
    time_surf.fill(cfg.YELLOW)
    run = False

    # Game variables-----------------------------------------------------------------------------------------------
    daeda.createGrid()

    # Create Grid---------------------------------------------------------------------------------------------------
    daeda.renderGrid(DISPLAYSURF)
    bg = True

    # Create Player-------------------------------------------------------------------------------------------------
    sprites = pygame.sprite.Group()
    tStartcell =  Theseus('StartCell', cfg.WHITE)
    tplayer = Theseus('Theseus', cfg.LIMEGREEN)
    tEndcell =  Theseus('EndCell', cfg.WHITE)
    tcompanion1 = Theseus('Companion',cfg.BLUE)
    tminotaur = Theseus('Minotaur',cfg.RED)
    sprites.add(tminotaur, tcompanion1, tStartcell, tEndcell, tplayer)

    #  Passes Startcell x, y and EndCell x, y to daeda.py (The game actually starts at the Endcell 
    # and ends at Startcell)
    cfg.xs, cfg.ys = tStartcell.rect.x, tStartcell.rect.y
    cfg.xe, cfg.ye = tEndcell.rect.x, tEndcell.rect.y

    # Player starting location which is at Endcell
    tplayer.rect.x, tplayer.rect.y = cfg.xe, cfg.ye

    # User Events--------------------------------------------------------------------------------------------------
    minotaur_move_event = pygame.USEREVENT + 1
    companion_move_event = pygame.USEREVENT + 2
    pygame.time.set_timer(minotaur_move_event, cfg.minotaurspeed)
    pygame.time.set_timer(companion_move_event, cfg.companionspeed)

    # Run Game------------------------------------------------------------------------------------------------------
    running = True
    while running:
        checkForQuit()
        # draw the maze 1 time
        if bg == True:
            daeda.daedalus(DISPLAYSURF)
            bg = False
        
        # start the level
        if run == True:
            sprites.update()
            sprites.draw(DISPLAYSURF)

            #timer (Issue time is longer than 60secs)
            seconds=(pygame.time.get_ticks()-start_ticks)/1000   #calculate how many seconds
            te -= 1
            text_Surf = font.render(time.strftime('%M:%S', time.gmtime(te)), True, cfg.WHITE, cfg.RED)
            time_surf.blit(text_Surf, [0, 0])
            DISPLAYSURF.blit(time_surf, [cfg.LOC + 165, 14])

            if seconds>cfg.chrono: # if more than 60 seconds end round
                run = False
                start_ticks=pygame.time.get_ticks() #starter tick
                lives += 1

            #  movement and key events
            for event in pygame.event.get():
                pygame.time.set_timer(minotaur_move_event, cfg.minotaurspeed)
                if pygame.event.get(pygame.QUIT): break
                # NPC movement (Issue---NPCs do not move while player is moving and being drawn)
                if event.type == minotaur_move_event:
                    tminotaur.minotaurMovement(DISPLAYSURF)# enemy
                if event.type == minotaur_move_event:
                    tcompanion1.compMovement(DISPLAYSURF)# companion
                elif event.type == KEYDOWN:
                    # player movement
                    if event.key in (K_LEFT, K_a):
                        tplayer.moveLeft(DISPLAYSURF)
                    elif event.key in (K_RIGHT, K_d):
                        tplayer.moveRight(DISPLAYSURF)                
                    elif event.key in (K_UP, K_w):
                        tplayer.moveUp(DISPLAYSURF)
                    elif event.key in (K_DOWN, K_s):
                        tplayer.moveDown(DISPLAYSURF)
                    # restart    
                    elif event.key == K_SPACE:
                        tplayer.rect.x = cfg.xe
                        tplayer.rect.y = cfg.ye
                        lives = 0
                        cfg.clio.clear()
                    # show answer
                    elif event.key == K_3: 
                        daeda.goal(DISPLAYSURF)

         
        # menu
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_0:# settings
                    pass
                elif event.key == K_1:# new level
                    new()
                elif event.key == K_2: # restart
                    tplayer.rect.x = cfg.xe
                    tplayer.rect.y = cfg.ye
                    lives = 0
                    cfg.clio.clear()
                elif event.key == K_3:# show asnwer
                    daeda.goal(DISPLAYSURF)
                elif event.key == K_SPACE:# start level
                    run = True
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        # check if alive
        Theseus.check_alive()
        pygame.display.update()
        cfg.FPSCLOCK.tick(cfg.FPS)
# End main-------------------------------------------------------------------------------------------------------------
 

# Quit functions-------------------------------------------------------------------------------------------------------      
def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

# options menu------------------------------------------------------------------------------------------------------------

def new():
    cfg.solution.clear()
    cfg.andron.clear()
    cfg.stack.clear()
    cfg.visited.clear()
    cfg.clio.clear()
    cfg.minotaurVisited.clear()
    time.sleep(1)

    main()

def settings():
    pass


if __name__ == '__main__':
    main()