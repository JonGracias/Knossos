# CMIS226 - Assgignment 1
# Name: Jonatan Gracias
# Project Title: Maze Game
# Project Desciption: simple game of getting out of a maze with randomly generated mazes


import pygame, sys
from pygame.locals import *

pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Game Scripting Assignment 1')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (0, 100, 0)
BLUE  = (  0,   0, 255)

# draw on the surface object
DISPLAYSURF.fill(WHITE)

# set display fonts - NOTE: print(pygame.font.get_fonts()) will print the fonts on the system
font = pygame.font.SysFont('arialblack', 24)
font2 = pygame.font.SysFont('couriernew', 16)

# describe your project
course = font.render("CMIS226 Assignment 1", True, RED)
name = font.render("Jonatan Gracias", True, BLUE)
title = font.render("Maze Game", True, GREEN)
desc1 = font2.render("Player is a mouse in a maze.", True, BLACK)
desc2 = font2.render("Player must reach goal of randomly ", True, BLACK)
desc3 = font2.render("generated maze with in time limit", True, BLACK)
desc4 = font2.render("Every level time limit will decrease ", True, BLACK)
desc5 = font2.render("and play velocity will increase.", True, BLACK)

# display the intro splash page
DISPLAYSURF.blit(course, (20,20))
pygame.draw.line(DISPLAYSURF, RED, (20, 55), (325, 55), 4)
DISPLAYSURF.blit(name, (20,70))
DISPLAYSURF.blit(title, (20,110))
DISPLAYSURF.blit(desc1, (20,150))
DISPLAYSURF.blit(desc2, (20,170))
DISPLAYSURF.blit(desc3, (20,190))
DISPLAYSURF.blit(desc4, (20,210))
DISPLAYSURF.blit(desc5, (20,230))

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
