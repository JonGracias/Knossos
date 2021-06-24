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
        self.RECT = pygame.Rect(x, y, self.width, self.hieght)

    def draw_sprite(self, screen):
        IMAGE_SURF = pygame.Surface((self.width, self.hieght), pygame.SRCALPHA)
        IMAGE_SURF.fill(c.transparent)

        IMAGE_SURF.blit(self.image, [self.ix, self.iy])
        screen.blit(IMAGE_SURF, [self.x, self.y])



class Human(Player):
    def __init__(self, x, y, width, hieght):
        super().__init__(x, y, width, hieght, color=c.LIMEGREEN)
        self.image = pygame.image.load('knossos/res/player.png')
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
