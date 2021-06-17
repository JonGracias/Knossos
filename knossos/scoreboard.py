import pygame
from knossos.color import colors as c


class Scoreboard():
    def __init__(self, text="Level: " + str(0), width=200, x=10, y=7):
        self.text = text
        self.x = x
        self.y = y

        self.width = width
        self.height = 20
        self.fontx = x + 5
        self.fonty = y + 2
        self.score = 0

        self.font = pygame.font.Font("freesansbold.ttf", 18)

    def draw(self, screen):
        SCORE_SURF = self.font.render(self.text, True, c.WHITE)
        SCORE_BOARD = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        SCORE_BOARD.fill(c.BLACK)
        SCORE_BOARD.blit(SCORE_SURF, [2, 2])
        screen.blit(SCORE_BOARD, [self.x, self.y])


class Level(Scoreboard):
    def __init__(self, text="Level: " + str(1), width=90, x=10, y=7):
        super().__init__(text, width, x, y)


class Score(Scoreboard):
    def __init__(self, text="Score: " + str(0), width=200, x=405, y=7):
        super().__init__(text, width, x, y)


class HighScore(Scoreboard):
    def __init__(self, text="Score: " + str(0), width=200, x=405, y=7):
        super().__init__(text, width, x, y)


class Lives(Scoreboard):
    def __init__(self, text="Lives: ", width=295, x=105, y=7):
        super().__init__(text, width, x, y)
        self.lives = 3

    def draw_lives(self, screen):
        for i in range(self.lives):
            x = 170 + ((1 * i) + (10 * i))
            pygame.draw.rect(screen, c.LIMEGREEN, [x, 13, 10, 10])
