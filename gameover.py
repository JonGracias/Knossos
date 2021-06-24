import pygame
import sys
from pygame.locals import *
from knossos.menu_screens import GameOver
import main as m
import start


def main():
    # INIT -------------------------------------------------------------------------------------------------------
    pygame.init()
    gameover = GameOver()

    # RUNGAME-----------------------------------------------------------------------------------------------------
    RUNNING = True
    while RUNNING:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    m.main()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if gameover.retry_button.collidepoint(pos):
                    gameover.set_retry()
                    start.main()
                if gameover.main_menu_button.collidepoint(pos):
                    m.main()

        gameover.GameOver_update_screen()

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
