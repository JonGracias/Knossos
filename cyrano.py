import cfg
import pygame

# write text-------------------------------------------------------------------------------------------------------------
class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, bgcolor, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
    
        self.font = pygame.font.Font('freesansbold.ttf', cfg.BASICFONTSIZE)
        self.textSurf = self.font.render(text, True, color, bgcolor)
        self.image = pygame.Surface((width, height))
        self.image.fill(bgcolor)
        self.image.blit(self.textSurf, [0, 0])
        self.rect = pygame.rect.Rect(x, y, width, height)


#PAUSE----------------------------------------------------------------------------------------------------------------
class Pause(pygame.sprite.Sprite):
    def __init__(self, text, color, bgcolor, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
    
        self.font = pygame.font.Font('freesansbold.ttf', cfg.BASICFONTSIZE)
        self.textSurf = self.font.render(text, True, color, bgcolor)
        self.image = pygame.Surface((width, height))
        self.image.fill(bgcolor)
        self.image.blit(self.textSurf, [10, 10])
        self.rect = pygame.rect.Rect(x, y, width, height)


# Create window----------------------------------------------------------------------------------------------------------
class Window(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # If I want to add pic
        # self.image = pygame.image.load("car.png").convert_alpha()
 
        self.rect = pygame.rect.Rect(x, y, cfg.BGSIZE, height)