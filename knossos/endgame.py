import pygame
from knossos.color import colors as c


class EndGame():
    def __init__(self, fontsize=18, text="Level: " + str(0), surfx=0, surfy=0, width=100, height=100,
                 fontx=0, fonty=0, fcolor=c.frame, bcolor=c.background):
        self.text = text
        self.x = surfx
        self.y = surfy
        self.backx = 5
        self.backy = 5

        self.width = width
        self.height = height
        self.backwidth = self.width - 10
        self.backheight = self.height - 10

        self.fontx = fontx
        self.fonty = fonty
        self.fontsize = fontsize

        self.frame_color = fcolor
        self.background_color = bcolor

        self.font = pygame.font.Font("freesansbold.ttf", self.fontsize)

        self.RECT = pygame.Rect(surfx, surfy, width, height)

    def draw(self, screen):
        FRAME_SURF = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        FRAME_SURF.fill(self.frame_color)

        BACKGROUND_SURF = pygame.Surface(
            (self.backwidth, self.backheight), pygame.SRCALPHA)
        BACKGROUND_SURF.fill(self.background_color)

        TEXT_SURF = self.font.render(self.text, True, c.WHITE)

        BACKGROUND_SURF.blit(TEXT_SURF, [self.fontx, self.fonty])
        FRAME_SURF.blit(BACKGROUND_SURF, [self.backx, self.backy])
        screen.blit(FRAME_SURF, [self.x, self.y])


class Lost(EndGame):
    def __init__(self, fontsize=18, text="Level: " + str(0), surfx=0, surfy=0, width=100, height=100,
                 fontx=0, fonty=0, fcolor=c.redframe, bcolor=c.background):
        super().__init__(fontsize, text, surfx, surfy,
                         width, height, fontx, fonty, fcolor, bcolor)


class Won(EndGame):
    def __init__(self, fontsize=18, text="Level: " + str(0), surfx=0, surfy=0, width=100,
                 height=100, fontx=0, fonty=0, fcolor=c.greenframe, bcolor=c.background):
        super().__init__(fontsize, text, surfx, surfy,
                         width, height, fontx, fonty, fcolor, bcolor)

class Start(EndGame):
    def __init__(self, fontsize=18, text="Welcome", surfx=0, surfy=0, width=100,
                 height=100, fontx=0, fonty=0, fcolor=c.greenframe, bcolor=c.background):
        super().__init__(fontsize, text, surfx, surfy,
                         width, height, fontx, fonty, fcolor, bcolor)