import pygame
from knossos.color import colors as c


class Scoreboard():
    def __init__(self, text=str(0), width=200, height=20, x=10, y=7, fontsize=18):
        self.text = text
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.fontx = 2
        self.fonty = 2
        self.score = 0

        self.font = pygame.font.Font("freesansbold.ttf", fontsize)

    def draw(self, screen):
        SCORE_SURF = self.font.render(self.text, True, c.WHITE)
        SCORE_BOARD = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        SCORE_BOARD.fill(c.BLACK)
        SCORE_BOARD.blit(SCORE_SURF, [self.fontx, self.fonty])
        screen.blit(SCORE_BOARD, [self.x, self.y])


class Level(Scoreboard):
    def __init__(self, text=str(0), width=45, height=45, x=10, y=7):
        super().__init__(text, width, height, x, y)
        self.text = text
        self.font = pygame.font.Font("freesansbold.ttf", 30)
        self.fontx = (width*.5)-(len(self.text) * 9)
        self.fonty = 7

class Ability(Scoreboard):
    def __init__(self, text="ability", width=45, height=45, x=400, y=7, fontsize=18):
        super().__init__(text, width, height, x, y, fontsize)
        self.text = text
        self.font = pygame.font.Font("freesansbold.ttf", fontsize)
        self.fontx = (width*.5)-(len(self.text) * 2.5)
        self.fonty = 7

class Score(Scoreboard):
    def __init__(self, text="Score: ", width=155, height=20, x=450, y=7):
        super().__init__(text, width, height, x, y)
        self.text = text
        self.font = pygame.font.Font("freesansbold.ttf", 18)
        self.fontx = (width*.5)-(len(self.text) * 9)
        self.fonty = 2

class Highscore(Scoreboard):
    def __init__(self, text="Highscore: " + str(0), width=200, x=405, y=32):
        super().__init__(text, width, x, y)


class Lives(Scoreboard):
    def __init__(self, text="HP: ", width=265, height=20, x=65, y=7):
        super().__init__(text, width, height, x, y)
        self.lives = 3

    def draw_lives(self, screen):
        for i in range(self.lives):
            x = 105 + ((1 * i) + (10 * i))
            pygame.draw.rect(screen, c.LIMEGREEN, [x, 13, 10, 10])

class Cooldown(Scoreboard):
    def __init__(self, text="MP: ", width=265, height=20, x=65, y=32):
        super().__init__(text, width, height, x, y)
        self.energy = 3
        self.last = pygame.time.get_ticks()
        self.ready = pygame.time.get_ticks()

    def draw_cooldown(self, screen):
        for i in range(self.energy):
            x = 105 + ((1 * i) + (10 * i))
            pygame.draw.rect(screen, c.MORANGE, [x, 37, 10, 10])
