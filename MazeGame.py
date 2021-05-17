# CMIS226 - Assgignment 1
# Name: Jonatan Gracias
# Project Title: Maze Game
# Project Desciption: Find way to target in a randomly generated maze.
# work in progess
# basic setup for pygame

import pygame
import sys
from pygame.locals import *
import daeda
import cfg
from theseus import Theseus
from cyrano import *
import time
import random
import pickle


# start main-------------------------------------------------------------------------------------------------------
def main():
    # INIT --------------------------------------------------------------------------------------------------------
    pygame.init()
    cfg.FPSCLOCK = pygame.time.Clock()

    # Window---------------------------------------------------------------------------------------------------------
    DISPLAYSURF = pygame.display.set_mode((cfg.WINDOWX, cfg.WINDOW))
    DISPLAYSURF.fill(cfg.BLACK)
    pygame.display.set_caption('MAZE GAME')

    # splashscreen-------------------------------------------------------------------------------------------------------
    # set display fonts - NOTE: print(pygame.font.get_fonts()) will print the fonts on the system
    # describe your project
    description_list = pygame.sprite.Group()
    BLACKBG = Text("", cfg.RED, cfg.BLACK, cfg.LOC + 10,
                   cfg.LOC + 50, cfg.BGSIZE - 20, 165)
    WHITEBG = Text("", cfg.RED, cfg.WHITE, cfg.LOC + 15,
                   cfg.LOC + 55, cfg.BGSIZE - 30, 155)
    COURSE = Text("CMIS226 Assignment 1", cfg.RED, cfg.WHITE,
                  cfg.LOC + 20, cfg.LOC + 60, cfg.BGSIZE - 40, 20)
    REDLINE = Text("", cfg.RED, cfg.RED, cfg.LOC + 20,
                   cfg.LOC + 80, cfg.BGSIZE - 40, 5)
    NAME = Text("Jonathan Gracias", cfg.BLUE, cfg.WHITE,
                cfg.LOC + 20, cfg.LOC + 85, cfg.BGSIZE - 40, 20)
    TITLE = Text("MAZE GAME", cfg.BLUE, cfg.WHITE, cfg.LOC +
                 20, cfg.LOC + 105, cfg.BGSIZE - 40, 20)
    DESC1 = Text("A labyrinth game that features Theseus, Ariadne and the Minotaur.",
                 cfg.GREEN, cfg.WHITE, cfg.LOC + 20, cfg.LOC + 125, cfg.BGSIZE - 40, 20)
    DESC2 = Text("Rescue Ariadne and defeat the Minotaur together.", cfg.GREEN,
                 cfg.WHITE, cfg.LOC + 20, cfg.LOC + 145, cfg.BGSIZE - 40, 20)
    DESC3 = Text("Uses Filo approach to create a maze.", cfg.GREEN,
                 cfg.WHITE, cfg.LOC + 20, cfg.LOC + 165, cfg.BGSIZE - 40, 20)
    DESC4 = Text("Push spacebar to start", cfg.GREEN, cfg.WHITE,
                 cfg.LOC + 20, cfg.LOC + 185, cfg.BGSIZE - 40, 20)
    description_list.add(BLACKBG, WHITEBG, COURSE, REDLINE,
                         NAME, TITLE, DESC1, DESC2, DESC3, DESC4)

    # Pause menu----------------------------------------------------------------------------------------------------
    pause_menu_list = pygame.sprite.Group()
    INGAME = Pause("IN GAME COMMANDS", cfg.WHITE, cfg.RED, 770, 5, 395, 30)
    SPACE = Pause("START/PAUSE         SPACEBAR",
                  cfg.WHITE, cfg.BLACK, 770, 35, 395, 30)
    UP = Pause("UP                           W",
               cfg.WHITE, cfg.BLACK, 770, 65, 395, 30)
    DOWN = Pause("DOWN                     S",
                 cfg.WHITE, cfg.BLACK, 770, 95, 395, 30)
    LEFT = Pause("LEFT                       A",
                 cfg.WHITE, cfg.BLACK, 770, 125, 395, 30)
    RIGHT = Pause("RIGHT                     D",
                  cfg.WHITE, cfg.BLACK, 770, 155, 395, 30)
    PAUSEMENU = Pause("PAUSE MENU COMMANDS", cfg.WHITE,
                      cfg.RED, 770, 190, 395, 30)
    NEW = Pause("NEW GAME                   1",
                cfg.WHITE, cfg.BLACK, 770, 220, 395, 30)
    RESTART = Pause("RESTART                       2",
                    cfg.WHITE, cfg.BLACK, 770, 250, 395, 30)
    CRUMBS = Pause("BREAD CRUMBS           3", cfg.WHITE,
                   cfg.BLACK, 770, 280, 395, 30)
    FOLLOWERS = Pause("FOLLOWERS", cfg.WHITE, cfg.RED, 770, 315, 395, 30)
    FOLLOWERS_LIST = Pause(" ", cfg.WHITE, cfg.BLACK, 770, 345, 395, 125)
    RESCUED = Pause("RESCUED", cfg.WHITE, cfg.RED, 770, 475, 395, 30)
    RESCUED_LIST = Pause(" ", cfg.WHITE, cfg.BLACK, 770, 505, 395, 130)
    GRAVEYARD = Pause("GRAVEYARD", cfg.WHITE, cfg.RED, 770, 640, 395, 30)
    GRAVEYARD_LIST = Pause(" ", cfg.WHITE, cfg.BLACK, 770, 670, 395, 125)
    pause_menu_list.add(SPACE, UP, DOWN, LEFT, RIGHT, NEW, RESTART, CRUMBS, INGAME, PAUSEMENU,
                        FOLLOWERS, FOLLOWERS_LIST, RESCUED, RESCUED_LIST, GRAVEYARD, GRAVEYARD_LIST)
    pause_menu_list.draw(DISPLAYSURF)

    # game 0ver-----------------------------------------------------------------------------------------------------

    lost_list = pygame.sprite.Group()
    TITLE = Text("               YOU HAVE DIED!! Better luck next time...",
                 cfg.BLACK, cfg.WHITE, cfg.LOC + 20, cfg.LOC + 105, cfg.BGSIZE - 40, 20)
    lost_list.add(BLACKBG, WHITEBG, TITLE)

    won_list = pygame.sprite.Group()
    TITLE = Text("               YOU HAVE WON!!", cfg.BLACK,
                 cfg.WHITE, cfg.LOC + 20, cfg.LOC + 105, cfg.BGSIZE - 40, 20)
    won_list.add(BLACKBG, WHITEBG, TITLE)

    # Game board------------------------------------------------------------------------------------------------------
    all_windows_list = pygame.sprite.Group()
    BORDER = Window(cfg.WHITE, 30, 0, cfg.WINDOWX - 60, cfg.WINDOW)
    BACKGROUND = Window(cfg.BLACK, 35, 5, cfg.BGSIZE + 10, cfg.BGSIZE + 70)
    INFO = Window(cfg.RED, cfg.LOC, 10, cfg.BGSIZE, 25)
    INFOMENU = Window(cfg.RED, cfg.LOC, cfg.BGSIZE + 45, cfg.BGSIZE, 25)
    MAZE = Window(cfg.WHITE, cfg.LOC, cfg.LOC, cfg.BGSIZE, cfg.BGSIZE)
    all_windows_list.add(BORDER, BACKGROUND, INFO, INFOMENU, MAZE)
    all_windows_list.draw(DISPLAYSURF)

    all_options_list = pygame.sprite.Group()
    # Store time, level score, and high score---------------------------------------------------------------------
    lvl = 1
    TIME = Text('Time: ', cfg.WHITE, cfg.RED, cfg.LOC + 105, 15, 60, 20)
    LEVEL = Text('Level: ' + str(lvl), cfg.WHITE, cfg.RED, cfg.LOC, 15, 75, 20)
    SCORE = Text('Score: ' + str(cfg.score), cfg.WHITE,
                 cfg.RED, cfg.LOC + 380, 15, 200, 20)
    HIGHSCORE = Text('High Score: ' + str(cfg.high_score),
                     cfg.WHITE, cfg.RED, cfg.LOC + 525, 15, 200, 20)
    all_options_list.add(SPACE, TIME, LEVEL, SCORE, HIGHSCORE)
    all_options_list.draw(DISPLAYSURF)

    # Timer-------------------------------------------------------------------------------------------------------
    font = pygame.font.Font('freesansbold.ttf', cfg.BASICFONTSIZE)
    te = cfg.chrono
    time_surf = pygame.Surface((54, 20))
    time_surf.fill(cfg.YELLOW)

    # Gamestate---------------------------------------------------------------------------------------------------
    cfg.gamestate = cfg.MAIN

    # Game variables-----------------------------------------------------------------------------------------------
    daeda.createGrid()

    # Create Grid---------------------------------------------------------------------------------------------------
    daeda.renderGrid(DISPLAYSURF)

    # Create Player-------------------------------------------------------------------------------------------------
    sprites = pygame.sprite.Group()
    tStartcell = Theseus('StartCell', cfg.WHITE)
    tplayer = Theseus('Theseus', cfg.player_color)
    tcompanion1 = Theseus('Companion', cfg.companion_color)
    tminotaur = Theseus('Minotaur', cfg.minotaur_color)
    sprites.add(tminotaur, tcompanion1, tStartcell, tplayer)

    #  Passes Startcell x, y and EndCell x, y to daeda.py (The game actually starts at the Endcell
    # and ends at Startcell)
    cfg.xs, cfg.ys = tStartcell.rect.x, tStartcell.rect.y
    tplayer.rect.x, tplayer.rect.y = cfg.xs, cfg.ys
    cfg.xe, cfg.ye = tplayer.rect.x, tplayer.rect.y

    # User Events--------------------------------------------------------------------------------------------------
    time_event = pygame.USEREVENT + 1
    minotaur_move_event = pygame.USEREVENT + 2

    pygame.time.set_timer(minotaur_move_event, cfg.minotaurspeed)
    pygame.time.set_timer(time_event, 1000)

    # Run Game------------------------------------------------------------------------------------------------------
    running = True
    while running:
        checkForQuit()
        for event in pygame.event.get():
            # Main menu---------------------------------
            if cfg.gamestate == cfg.MAIN:
                # display the intro splash page
                description_list.update()
                pause_menu_list.update()
                description_list.draw(DISPLAYSURF)
                pause_menu_list.draw(DISPLAYSURF)
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        cfg.gamestate = cfg.SETUP
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()
            # Setp----------------------------------------
            elif cfg.gamestate == cfg.SETUP:
                DISPLAYSURF.fill(cfg.BLACK)
                all_windows_list.draw(DISPLAYSURF)
                all_options_list.draw(DISPLAYSURF)
                pause_menu_list.draw(DISPLAYSURF)
                daeda.renderGrid(DISPLAYSURF)
                daeda.daedalus(DISPLAYSURF)
                cfg.score = 0
                if cfg.cellNum >= 10:
                    cfg.score += 100
                if cfg.cellNum >= 20:
                    cfg.score += 200
                file = open(cfg.scoreFile, 'rb')
                cfg.high_score = pickle.load(file)
                file.close()
                cfg.gamestate = cfg.PLAYING
            # paused-------------------------------------------    
            elif cfg.gamestate == cfg.PAUSED:
                pause_menu_list.draw(DISPLAYSURF)
                pause_menu_list.draw(DISPLAYSURF)
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        cfg.gamestate = cfg.PLAYING
                        te = te
                    elif event.key == K_3:
                        daeda.goal(DISPLAYSURF)
                    elif event.key == K_1:
                        new()
                    elif event.key == K_2:
                        tplayer.rect.x = cfg.xs
                        tplayer.rect.y = cfg.ys
                        cfg.clio.clear()
                        te = cfg.chrono
                        pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                                         (tcompanion1.rect.x, tcompanion1.rect.y, cfg.cellSize, cfg.cellSize), 0)
                        tcompanion1.rect.x, tcompanion1.rect.y = random.choice(
                            cfg.grid)
            # Game over---------------------------------------
            elif cfg.gamestate == cfg.GAMEOVER:
                daeda.renderGrid(DISPLAYSURF)
                pause_menu_list.update()
                pause_menu_list.draw(DISPLAYSURF)
                if cfg.score > cfg.high_score:
                    file = open(cfg.scoreFile, 'wb')
                    pickle.dump(cfg.score, file)
                    file.close()
                if cfg.LOST:
                    lost_list.draw(DISPLAYSURF)
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            cfg.gamestate = cfg.MAIN
                            new()
                elif not cfg.LOST:
                    won_list.draw(DISPLAYSURF)
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            cfg.gamestate = cfg.MAIN
                            new()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        cfg.gamestate = cfg.MAIN
                        new()
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()
            # Playing-------------------------------------------
            elif cfg.gamestate == cfg.PLAYING:
                sprites.draw(DISPLAYSURF)
                all_options_list.update()
                all_options_list.draw(DISPLAYSURF)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # minotaur move----------------------------------
                elif event.type == minotaur_move_event:
                    pygame.time.set_timer(
                        minotaur_move_event, cfg.minotaurspeed)
                    tminotaur.minotaurMovement(DISPLAYSURF)  # enemy
                    sprites.update()
                # timer---------------------------------------------
                elif event.type == time_event:
                    te -= 1
                    text_Surf = font.render(time.strftime(
                        '%M:%S', time.gmtime(te)), True, cfg.WHITE, cfg.RED)
                    time_surf.blit(text_Surf, [0, 0])
                    DISPLAYSURF.blit(time_surf, [cfg.LOC + 165, 14])
                    # time ends------------------------------------------
                    if te == 0:  # if more than 60 seconds end round
                        te = cfg.chrono
                        tplayer.rect.x, tplayer.rect.y = cfg.xs, cfg.ys
                        cfg.clio.clear()
                        tminotaur.timeout()
                        tcompanion1.timeout()
                        cfg.gamestate = cfg.PAUSED
                    sprites.update()
                # player input ------------------------------------------
                elif event.type == KEYDOWN:
                    # player movement
                    if event.key in (K_LEFT, K_a):
                        tcompanion1.compMovement(DISPLAYSURF)  # companion
                        tplayer.moveLeft(DISPLAYSURF)
                        sprites.update()
                    elif event.key in (K_RIGHT, K_d):
                        tcompanion1.compMovement(DISPLAYSURF)  # companion
                        tplayer.moveRight(DISPLAYSURF)
                        sprites.update()
                    elif event.key in (K_UP, K_w):
                        tcompanion1.compMovement(DISPLAYSURF)  # companion
                        tplayer.moveUp(DISPLAYSURF)
                        sprites.update()
                    elif event.key in (K_DOWN, K_s):
                        tcompanion1.compMovement(DISPLAYSURF)  # companion
                        tplayer.moveDown(DISPLAYSURF)
                        sprites.update()
                    # show answer
                    elif event.key == K_SPACE:  # start level
                        cfg.gamestate = cfg.PAUSED

        # check if alive
        Theseus.check_alive(DISPLAYSURF)
        pygame.display.update()
        cfg.FPSCLOCK.tick(cfg.FPS)

    pygame.quit()
    sys.exit()
# End main-------------------------------------------------------------------------------------------------------------


# Quit functions-------------------------------------------------------------------------------------------------------
def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back

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


if __name__ == '__main__':
    main()
