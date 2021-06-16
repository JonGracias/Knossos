import pygame
import sys
from pygame.locals import *
from knossos.menus import Menu
import start


def main():
    # INIT -------------------------------------------------------------------------------------------------------
    pygame.init()
    menu = Menu()

    # RUNGAME-----------------------------------------------------------------------------------------------------
    RUNNING = True
    while RUNNING:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    start.main()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if menu.time_button.collidepoint(pos):
                    print("time")
                if menu.adv_button.collidepoint(pos):
                    start.main()
                if menu.dark_button.collidepoint(pos):
                    print("dark")

        menu.menu_update_screen()

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
