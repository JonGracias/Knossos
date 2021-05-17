import pygame
import cfg
import random

# The char statues dictionary--------------------------------------------------------------------------------
char = {'name':{'xy':(0,0), 'Theseus': False, 'color': cfg.BLACK, 'alive': True }}


# The player---------------------------------------------------------------------------------------------------
class Theseus(pygame.sprite.Sprite):
    
    def __init__(self, name, color):                                                # Basic sprite __init__ method
        pygame.sprite.Sprite.__init__(self)                                         # it creates a sprite
        # character statues dictionary 
        x, y = random.choice(cfg.grid)
        self.color = color
        self.name = name
        location = (x, y)
        char[name] = {'xy':location, 'Theseus': False, 'color': color, 'alive': True}
                                                    
        # character surface                                   
        self.image = pygame.Surface([cfg.cellSize, cfg.cellSize])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = char[name]['xy']

        self.following = False
        pygame.draw.rect(self.image, char[name]['color'], [0, 0, cfg.cellSize, cfg.cellSize])

        # If I want to add pic
        # self.image = pygame.image.load("car.png").convert_alpha()

     


# Player movement-----------------------------------------------------------------------------------------------------------
    def moveLeft(self, DISPLAYSURF):                                            # Defines player movement
        x, y = self.rect.x, self.rect.y                                         # by taking rect location 
        if (x - cfg.WALLSIZE, y) in cfg.andron.keys():                          # And checking if it is in moves dict
            self.char_draw(DISPLAYSURF, "left")                                 # sends information to char_draw()
            cfg.xe, cfg.ye = self.rect.x, self.rect.y
            cfg.clio[(x, y)] = self.rect.x, self.rect.y                         # and adds move to clio dict
            if (self.rect.x, self.rect.y) not in cfg.solution:
                cfg.solution[(self.rect.x, self.rect.y)] = x, y
    def moveRight(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x + cfg.cellSize, y) in cfg.andron.keys():
            self.char_draw(DISPLAYSURF, "right")
            cfg.xe, cfg.ye = self.rect.x, self.rect.y
            cfg.clio[(x, y)] = self.rect.x, self.rect.y
            if (self.rect.x, self.rect.y) not in cfg.solution:
                cfg.solution[(self.rect.x, self.rect.y)] = x, y
    def moveUp(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x, y - cfg.WALLSIZE) in cfg.andron.keys():
            self.char_draw(DISPLAYSURF, "up")
            cfg.xe, cfg.ye = self.rect.x, self.rect.y
            cfg.clio[(x, y)] = self.rect.x, self.rect.y
            if (self.rect.x, self.rect.y) not in cfg.solution:
                cfg.solution[(self.rect.x, self.rect.y)] = x, y
    def moveDown(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x, y + cfg.cellSize) in cfg.andron.keys():
            self.char_draw(DISPLAYSURF, "down")
            cfg.xe, cfg.ye = self.rect.x, self.rect.y
            cfg.clio[(x, y)] = self.rect.x, self.rect.y
            if (self.rect.x, self.rect.y) not in cfg.solution:
                cfg.solution[(self.rect.x, self.rect.y)] = x, y


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
                                                                           # and then if it is in minotaurVisited dict
        if char[self.name]['alive']:                                       # if not it makes the move and records it 
            if ((x, y) not in cfg.clio.keys()):
                char[self.name] = {'xy':(x, y), 'Theseus': False, 'color': self.color, 'alive': True}                        
                # move left                                             
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
        else:
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,                              
                    pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            pygame.draw.rect(DISPLAYSURF, cfg.RED,
            pygame.Rect(780, 680, cfg.cellSize, cfg.cellSize))


    # Follow function for npc to follow player--------------------------------------------------------------------------------
    def follow(self, DISPLAYSURF):
        x, y = self.rect.x, self.rect.y
        if (x, y) != (char['Theseus']['xy']):                                               # while not at player location
                    pygame.draw.rect(DISPLAYSURF, cfg.BLACK,                                # follows clio dict to player
                    pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))      # records location and that it is following
                    self.rect.x, self.rect.y = cfg.clio[x, y]                               # player in char dict
                    char[self.name] = {'xy':(x, y), 'Theseus': True, 'color': self.color, 'alive': True}  
                    if self.name == "Companion":
                        pygame.draw.rect(DISPLAYSURF, cfg.BLUE,
                        pygame.Rect(780, 355, cfg.cellSize, cfg.cellSize))


    # Redraw characters as they move------------------------------------------------------------------------------------------
    def char_draw(self, DISPLAYSURF, direction):                                        # draws a black square 
        if direction == "left":                                                         # and then changes sprite loc
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x - (cfg.WALLSIZE + cfg.cellSize)
            self.rect.y = self.rect.y
            char[self.name]['xy'] = self.rect.x, self.rect.y
            
        elif direction == "right":
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x + (cfg.WALLSIZE + cfg.cellSize)
            self.rect.y = self.rect.y
            char[self.name]['xy'] = self.rect.x, self.rect.y
            
        elif direction == "up":
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x 
            self.rect.y = self.rect.y - (cfg.WALLSIZE + cfg.cellSize)
            char[self.name]['xy'] = self.rect.x, self.rect.y
            
        elif direction == "down":
            pygame.draw.rect(DISPLAYSURF, cfg.BLACK,
                pygame.Rect(self.rect.x, self.rect.y, cfg.cellSize, cfg.cellSize))
            self.rect.x = self.rect.x 
            self.rect.y = self.rect.y + (cfg.WALLSIZE + cfg.cellSize)
            char[self.name]['xy'] = self.rect.x, self.rect.y
            


    # Timeout---------------------------------------------------------------------------------------------------------
    def timeout(self):
        if char['Theseus']:
            char[self.name] = {'xy':(cfg.xs, cfg.ys), 'Theseus': False, 'color': self.color, 'alive':True}
        else:
            char[self.name] = {'xy':(self.rect.x, self.rect.y), 'Theseus': False, 'color': self.color, 'alive':True}
        cfg.score -= 20
    # Check if character is alive-------------------------------------------------------------------------------------
    def check_alive(DISPLAYSURF):                                             
        if char['Minotaur']['xy'] == char['Theseus']['xy']:        
            if char['Companion']['Theseus'] == True:                    
                print('Minotaur is dead')                                
                char['Minotaur'] = {'xy':(0, 0), 'Theseus': False, 'color': cfg.BLACK, 'alive':False}
                cfg.score += 200
            else:
                print('you are dead')
                cfg.gamestate = cfg.GAMEOVER
                cfg.LOST = True
                cfg.score = 0
        elif char['Minotaur']['Theseus']:                                             
            cfg.minotaurspeed = 500
        else:
            cfg.minotaurspeed = 1000
        if char['StartCell']['xy'] == char['Theseus']['xy']:        
            if char['Companion']['Theseus'] == True:
                pygame.draw.rect(DISPLAYSURF, cfg.BLUE,
                pygame.Rect(780, 515, cfg.cellSize, cfg.cellSize))
                cfg.score += 200
                cfg.gamestate = cfg.GAMEOVER
                cfg.LOST = False
        
        if char['Companion']['xy'] == char['Theseus']['xy']:
            cfg.score += 50
      
                        
       
    