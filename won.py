import pygame
import sys
from pygame.locals import *
from knossos.menu_screens import Win
import start as s
import main as m


def main():
    # INIT -------------------------------------------------------------------------------------------------------
    pygame.init()
    win = Win()

    # RUNGAME-----------------------------------------------------------------------------------------------------
    RUNNING = True
    while RUNNING:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    s.main()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if win.continue_button.collidepoint(pos):
                    s.main()
                if win.retry_button.collidepoint(pos):
                    print("this")
                    win.set_retry()
                    s.main()
                if win.main_menu_button.collidepoint(pos):
                    m.main()

        win.win_update_screen()

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
