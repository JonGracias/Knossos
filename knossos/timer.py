import pygame
from knossos.color import colors as c


class Timer():
    def __init__(self, x=5, y=0, width=595):
        self.x = x
        self.y = y
        self.width = width
        self.w = 595

    def draw(self, screen):
        TIMER_SURF = pygame.Surface((self.width, 15), pygame.SRCALPHA)
        TIMER_SURF.fill(c.LIGHTRED)
        TIMER_DISPLAY_BAR = pygame.draw.rect(
            screen, c.SILVER, [self.x, 650, 605, 25])
        TIMER_BACKGROUND = pygame.draw.rect(
            screen, c.BLUE, [10, 655, self.w, 15])
        screen.blit(TIMER_SURF, (10, 655))
