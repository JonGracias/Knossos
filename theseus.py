import pygame
import cfg
import random

# The char statues dictionary--------------------------------------------------------------------------------
char = {'name':{'xy':(0,0), 'Theseus': False}}


# The player---------------------------------------------------------------------------------------------------
class Theseus(pygame.sprite.Sprite):
    
    def __init__(self, name, color):                                                # Basic sprite __init__ method
        pygame.sprite.Sprite.__init__(self)                                         # it creates a sprite
        x, y = random.choice(cfg.grid)                                              # and then creates a dictionary with
        # character surface                                                         # character information
        self.image = pygame.Surface([cfg.cellSize, cfg.cellSize])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, [0, 0, cfg.cellSize, cfg.cellSize])

        # If I want to add pic
        # self.image = pygame.image.load("car.png").convert_alpha()

        # character statues dictionary 
        self.rect.x, self.rect.y = x, y
        self.name = name
        location = (self.rect.x, self.rect.y)
        char[name] = {'xy':location, 'Theseus': False}
     


# Player movement-----------------------------------------------------------------------------------------------------------
    def moveLeft(self, DISPLAYSURF):                        # Defines player movement
        x, y = self.rect.x, self.rect.y                     # by taking rect location 
        if (x - cfg.WALLSIZE, y) in cfg.andron.keys():      # And checking if it is in moves dict
            self.char_draw(DISPLAYSURF, "left")             # sends information to char_draw()
            cfg.clio[(x, y)] = self.rect.x, self.rect.y     # and adds move to clio dict
        
    def moveRight(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x + cfg.cellSize, y) in cfg.andron.keys():
            self.char_draw(DISPLAYSURF, "right")
            cfg.clio[(x, y)] = self.rect.x, self.rect.y

    def moveUp(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x, y - cfg.WALLSIZE) in cfg.andron.keys():
            self.char_draw(DISPLAYSURF, "up")
            cfg.clio[(x, y)] = self.rect.x, self.rect.y

    def moveDown(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x, y + cfg.cellSize) in cfg.andron.keys():
            self.char_draw(DISPLAYSURF, "down")
            cfg.clio[(x, y)] = self.rect.x, self.rect.y


# Companion Movement---------------------------------------------------------------------------------------        
    def compMovement(self, DISPLAYSURF):                                # Companions do not move
        x, y = self.rect.x, self.rect.y
        alive = True
        if alive:
            if ((x, y) not in cfg.clio.keys()):                         # until a player comes and then 
                char[self.name]['xy'] = self.rect.x, self.rect.y        # they follow player
            else:
                self.follow(DISPLAYSURF)


    # Minotaur Movement-------------------------------------------------------------------------------------
    def minotaurMovement(self, DISPLAYSURF):                            # Works muchs like daedalus method
        x, y = self.rect.x, self.rect.y                                 # it checks if move is possible
        alive = True                                                    # and then if it is in minotaurVisited dict
        if alive:                                                       # if not it makes the move and records it in
            if ((x, y) not in cfg.clio.keys()):                         # minotaurdict unless it crosses the player
                # move left                                             # path then Minotaur chases player
                if ((x - cfg.WALLSIZE, y) in cfg.andron.keys()
                    ) and ((x - (cfg.WALLSIZE + cfg.cellSize), y
                    ) not in cfg.minotaurVisited):
                        self.char_draw(DISPLAYSURF, "left")
                        cfg.minotaurVisited.append((x, y))
                # move right
                elif((x + cfg.cellSize, y) in cfg.andron.keys()
                    ) and ((x + (cfg.WALLSIZE + cfg.cellSize), y
                    )not in cfg.minotaurVisited):
                        self.char_draw(DISPLAYSURF, "right")
                        cfg.minotaurVisited.append((x, y))
                # move up
                elif((x, y - cfg.WALLSIZE) in cfg.andron.keys()
                    ) and ((x, y - (cfg.WALLSIZE + cfg.cellSize)
                    ) not in cfg.minotaurVisited):
                        self.char_draw(DISPLAYSURF, "up")
                        cfg.minotaurVisited.append((x, y))
                # move down
                elif((x, y + cfg.cellSize) in cfg.andron.keys()
                    ) and ((x, y + (cfg.WALLSIZE + cfg.cellSize)
                    ) not in cfg.minotaurVisited):
                        self.char_draw(DISPLAYSURF, "down")
                        cfg.minotaurVisited.append((x, y))
                # no move available 
                else:
                    cfg.minotaurVisited.clear() # clears dict if there is no other move left

            else:
                self.follow(DISPLAYSURF) # chase player


    # Follow function for npc to follow player--------------------------------------------------------------------------------
    def follow(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x, y) != (char['Theseus']['xy']):                                               # while not at player location
                    pygame.draw.rect(DISPLAYSURF, cfg.BLACK,                                # follows clio dict to player
                    pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))      # records location and that it is following
                    self.rect.x, self.rect.y = cfg.clio[x, y]                               # player in char dict
                    char[self.name] = {'xy':(self.rect.x, self.rect.y), 'Theseus': True}
                    if self.name == 'Minotaur':                                             # if the minotaur is following player
                        cfg.minotaurspeed = 500                                             # NPC speed increases (Issue player lags NPCs)
                        cfg.companionspeed = 250
                    pygame.display.update()


    # Redraw characters as they move------------------------------------------------------------------------------------------
    def char_draw(self, DISPLAYSURF, direction):                                        # draws a black square 
        if direction == "left":                                                         # and then changes sprite loc
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x - (cfg.WALLSIZE + cfg.cellSize)
            self.rect.y = self.rect.y
            char[self.name]['xy'] = self.rect.x, self.rect.y
            pygame.display.update()
        elif direction == "right":
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x + (cfg.WALLSIZE + cfg.cellSize)
            self.rect.y = self.rect.y
            char[self.name]['xy'] = self.rect.x, self.rect.y
            pygame.display.update()
        elif direction == "up":
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x 
            self.rect.y = self.rect.y - (cfg.WALLSIZE + cfg.cellSize)
            char[self.name]['xy'] = self.rect.x, self.rect.y
            pygame.display.update()
        elif direction == "down":
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x 
            self.rect.y = self.rect.y + (cfg.WALLSIZE + cfg.cellSize)
            char[self.name]['xy'] = self.rect.x, self.rect.y
            pygame.display.update()


    # Timeout---------------------------------------------------------------------------------------------------------
    def timeout(self):
        char[self.name] = {'xy':(self.rect.x, self.rect.y), 'Theseus': False}
    # Check if character is alive-------------------------------------------------------------------------------------
    def check_alive():                                              # not finished but basically will track what player has
        if char['Minotaur']['xy'] == char['Theseus']['xy']:         # if player is at minotaur
            if char['Companion']['Theseus'] == True:                        # if player is with companion
                print('Minotaur is dead')                           # minotaur dies
            else:
                print('you are dead')                               # else player dies

                    
                        
       
    