import pygame
from knossos.color import colors as c


class Effect():
    def __init__(self, x, y, width, hieght, ix=0, iy=0, color=c.YELLOW):
        self.x = x
        self.y = y
        self.ix = ix
        self.iy = iy
        self.color = color
        self.width = width
        self.hieght = hieght
        self.RECT = pygame.Rect(self.x, self.y, self.width, self.hieght)
        self.LEFT_RECT = pygame.Rect ( self.x,               self.y+self.width*.4,   self.width*.2, self.hieght*.4)
        self.RIGHT_RECT = pygame.Rect( self.x+self.width,    self.y+self.width*.4,   self.width*.2, self.hieght*.4)
        self.UP_RECT = pygame.Rect   ( self.x+self.width*.4, self.y,                 self.width*.4, self.hieght*.2)
        self.DOWN_RECT = pygame.Rect ( self.x+self.width*.4, self.y+self.hieght,     self.width*.4, self.hieght*.2)

    def draw_sprite(self, screen):
        IMAGE_SURF = pygame.Surface((self.width, self.hieght), pygame.SRCALPHA)
        IMAGE_SURF.fill(c.transparent)

        IMAGE_SURF.blit(self.image, [self.ix, self.iy])
        screen.blit(IMAGE_SURF, [self.x, self.y])

    def update_rects(self):
        self.RECT = pygame.Rect(self.x, self.y, self.width, self.hieght)
        self.LEFT_RECT = pygame.Rect ( self.x,               self.y+self.width*.4,   self.width*.2, self.hieght*.4)
        self.RIGHT_RECT = pygame.Rect( self.x+self.width,    self.y+self.width*.4,   self.width*.2, self.hieght*.4)
        self.UP_RECT = pygame.Rect   ( self.x+self.width*.4, self.y,                 self.width*.4, self.hieght*.2)
        self.DOWN_RECT = pygame.Rect ( self.x+self.width*.4, self.y+self.hieght,     self.width*.4, self.hieght*.2)

    def drawrects(self, screen):
        pygame.draw.rect(screen, c.wall, self.RECT)
        pygame.draw.rect(screen, c.PURPLE, self.LEFT_RECT)
        pygame.draw.rect(screen, c.PURPLE, self.RIGHT_RECT)
        pygame.draw.rect(screen, c.PURPLE, self.UP_RECT)
        pygame.draw.rect(screen, c.PURPLE, self.DOWN_RECT)

class Vanish(Effect):
    def __init__(self, x, y, width, hieght, ix=0, iy=-35, color=c.YELLOW):
        super().__init__(x, y, width, hieght, ix, iy, color)
        self.image = pygame.image.load('knossos/res/effects.png')
        self.animate = 0


class Lightning(Effect):
    def __init__(self, x, y, width, hieght, ix=0, iy=0, color=c.YELLOW):
        super().__init__(x, y, width, hieght, ix, iy, color)
        self.image = pygame.image.load('knossos/res/effects.png')
        self.alive = 10
        self.speed = 10
        self.animate = " "