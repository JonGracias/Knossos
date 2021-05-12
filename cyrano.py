import cfg
import pygame

# write text-------------------------------------------------------------------------------------------------------------
class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
    
        self.font = pygame.font.Font('freesansbold.ttf', cfg.BASICFONTSIZE)
        self.textSurf = self.font.render(text, True, color, cfg.RED)
        self.image = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [0, 0])
        self.rect = pygame.rect.Rect(x, y, width, height)
    

# Create window----------------------------------------------------------------------------------------------------------
class Window(pygame.sprite.Sprite):
    def __init__(self, color, x, y,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([cfg.BGSIZE,height])
        self.image.fill(color)
 
        pygame.draw.rect(self.image, color, [0, 0, cfg.BGSIZE, height])
        
        # If I want to add pic
        # self.image = pygame.image.load("car.png").convert_alpha()
 
        self.rect = pygame.rect.Rect(x, y, cfg.BGSIZE, height)