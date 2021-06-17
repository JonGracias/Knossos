import pygame
from knossos.color import colors as c

class Maze():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.RECT = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_rooms(self, screen):
        CELL_SURF = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        CELL_SURF.fill(c.WHITE)
        screen.blit(CELL_SURF, [self.x, self.y])