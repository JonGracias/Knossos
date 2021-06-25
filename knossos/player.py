import pygame
from knossos.color import colors as c


class Player():
    def __init__(self, x, y, width, hieght, ix=0, iy=0, color=c.LIMEGREEN):
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



class Human(Player):
    def __init__(self, x, y, width, hieght):
        super().__init__(x, y, width, hieght, color=c.LIMEGREEN)
        self.image = pygame.image.load('knossos/res/player.png')
        self.x, self.y = x, y
        self.player_facing_left = [(-70, 0), (-105, 0)]
        self.player_facing_right = [(0, 0),  (-35, 0)]
        self.player_facing_up = [(-70, -35),  (-105, -35)]
        self.player_facing_down = [(0, -35),  (-35, -35)]
        self.speed = 10
        self.pose = True

class Target(Player):
    def __init__(self, x, y, width, hieght):
        super().__init__(x, y, width, hieght, color=c.SILVER)
        self.image = pygame.image.load('knossos/res/exit.png')


class Sword(Player):
    def __init__(self, x, y, width, hieght, ix, iy):
        super().__init__(x, y, width, hieght, ix, iy, color=c.SILVER)
        self.image = pygame.image.load('knossos/res/player.png')


class Enemy_Sword(Player):
    def __init__(self, x, y, width, hieght, ix, iy):
        super().__init__(x, y, width, hieght, ix, iy, color=c.SILVER)
        self.image = pygame.image.load('knossos/res/enemy.png')


class Enemy(Player):
    def __init__(self, x, y, width, hieght):
        super().__init__(x, y, width, hieght, color=c.RED)
        self.image = pygame.image.load('knossos/res/enemy.png')
        self.health = 5
        self.moves = []
        self.move_back = []
        self.stationary = []
        self.enemy_pose = [0, 1]
        self.enemy_steps_left = 0
        self.enemy_steps_right = 0
        self.enemy_steps_up = 0
        self.enemy_steps_down = 0
        self.enemy_facing_left = [(-70, 0), (-105, 0)]
        self.enemy_facing_right = [(0, 0),  (-35, 0)]
        self.enemy_facing_up = [(-70, -35),  (-105, -35)]
        self.enemy_facing_down = [(0, -35),  (-35, -35)]
        self.speed = 5
