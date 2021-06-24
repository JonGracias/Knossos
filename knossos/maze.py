import pygame

class Maze():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.RECT = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color

    def draw_rooms(self, screen):
        CELL_SURF = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        CELL_SURF.fill(self.color)
        screen.blit(CELL_SURF, [self.x, self.y])
