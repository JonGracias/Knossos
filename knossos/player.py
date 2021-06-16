import pygame
from knossos.color import colors as c


class Player():
    def __init__(self, x, y, sizex, sizey, ix=0, iy=0, color=c.LIMEGREEN):
        self.x = x
        self.y = y
        self.ix = ix
        self.iy = iy
        self.color = color
        self.sizex = sizex
        self.sizey = sizey
        self.RECT = pygame.Rect(x, y, self.sizex, self.sizey)

    def draw_sprite(self, screen):
        IMAGE_SURF = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        IMAGE_SURF.fill(c.transparent)

        IMAGE_SURF.blit(self.image, [self.ix, self.iy])
        screen.blit(IMAGE_SURF, [self.x + 10, self.y + 30])



class Human(Player):
    def __init__(self, x, y, sizex, sizey):
        super().__init__(x, y, sizex, sizey, color=c.LIMEGREEN)
        self.image = pygame.image.load('knossos/res/player.png')


class Target(Player):
    def __init__(self, x, y, sizex, sizey):
        super().__init__(x, y, sizex, sizey, color=c.SILVER)
        self.image = pygame.image.load('knossos/res/exit.png')


class Sword(Player):
    def __init__(self, x, y, sizex, sizey, ix, iy):
        super().__init__(x, y, sizex, sizey, ix, iy, color=c.SILVER)
        self.image = pygame.image.load('knossos/res/player.png')


class Enemy_Sword(Player):
    def __init__(self, x, y, sizex, sizey, ix, iy):
        super().__init__(x, y, sizex, sizey, ix, iy, color=c.SILVER)
        self.image = pygame.image.load('knossos/res/enemy.png')


class Enemy(Player):
    def __init__(self, x, y, sizex, sizey):
        super().__init__(x, y, sizex, sizey, color=c.RED)
        self.image = pygame.image.load('knossos/res/enemy.png')
        self.moves = []
        self.move_back = []
        self.enemy_pose = [0, 1]
