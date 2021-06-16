import pygame
from knossos.color import colors as c
from random import choice


class daeda():
    def __init__(self, num):
        self.cellNum = num
        self.wall = 5
        self.cell = 35
        self.wall_cell = self.wall + self.cell

        self.grid = []
        self.solution = {}

        self.mazemap = []
        self.deadend = []
        self.enemy_loc = []
        self.farCell = []
        self.andron = [(int(self.wall),
                        int(self.wall))]
        self.flag = 0
        self.font = pygame.font.Font("freesansbold.ttf", int(self.cell * .28))
        self.color = choice(c.MEDITERRANEAN)

        self.map_size = 605

        self.BACKGROUND = pygame.Surface((self.map_size, self.map_size), pygame.SRCALPHA)
        self.BACKGROUND.fill(c.BLACK)
        self.MAP = pygame.Surface((self.map_size, self.map_size), pygame.SRCALPHA)
        self.MAP.fill(c.BLACK)
        self.CELL_SURF = pygame.Surface((self.map_size, self.map_size), pygame.SRCALPHA)
        self.CELL_SURF.fill(self.color)

        self.createGrid()
        self.daedalus()
        self.endLoc()
        
        

    # Draw the maze-------------------------------------------------------------------------------------------------------
    def renderGrid(self, surface, color=choice(c.MEDITERRANEAN)):
        
        for value in (self.mazemap):
            x, y, width, height = value
            self.CELL_SURF = pygame.Surface((width, height), pygame.SRCALPHA)
            self.CELL_SURF.fill(color)

            self.MAP.blit(self.CELL_SURF, (x, y))
        self.BACKGROUND.blit(self.MAP,(0,0))
        surface.blit(self.BACKGROUND, (5, 30))

    def debugGrid(self, screen):
        for value in (self.grid):
            x, y = value[0], value[1]
    
            s = str(x)
            b = str(y)
            sb = s + ", " + b
            GRID_SURF = self.font.render(sb, True, c.WHITE)
            screen.blit(GRID_SURF, [x, y])

    # Grid---------------------------------------------------------

    def createGrid(self):
        for i in range(self.cellNum):
            x = (self.cell * i) + (self.wall * i) + 5
            for j in range(self.cellNum):
                y = (self.cell * j) + (self.wall * j) + 5
                self.grid.append((x, y))

    # Carves the maze-----------------------------------------------------------------------------------------------------

    def daedalus(self):
        x, y = self.grid[0]
        visited = []
        stack = []
        visited.append((x, y))
        stack.append((x, y))
        while len(stack) > 0:
            cell = []
            if (x + self.cell + self.wall, y
                ) not in visited and (
                    x + self.cell + self.wall, y) in self.grid:
                cell.append("right")
            if (x - self.cell - self.wall, y) \
                    not in visited and \
                    (x - self.cell - self.wall, y) in self.grid:
                cell.append("left")
            if (x, y + self.cell + self.wall) \
                    not in visited and \
                    (x, y + self.cell + self.wall) in self.grid:
                cell.append("down")
            if (x, y - self.cell - self.wall) \
                    not in visited and \
                    (x, y - self.cell - self.wall) in self.grid:
                self.flag = 0
                cell.append("up")

            if len(cell) > 0:
                cell_chosen = (choice(cell))
                if cell_chosen == "right":
                    self.push_right(x, y)
                    self.solution[(x + self.cell + self.wall, y)] = x, y
                    x = x + self.cell + self.wall
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "left":
                    self.push_left(x, y)
                    self.solution[(x - self.cell - self.wall, y)] = x, y
                    x = x - self.cell - self.wall
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "down":
                    self.push_down(x, y)
                    self.solution[(x, y + self.cell + self.wall)] = x, y
                    y = y + self.cell + self.wall
                    visited.append((x, y))
                    stack.append((x, y))

                elif cell_chosen == "up":
                    self.push_up(x, y)
                    self.solution[(x, y - self.cell - self.wall)] = x, y
                    y = y - self.cell - self.wall
                    visited.append((x, y))
                    stack.append((x, y))
            else:
                if self.flag == 0:
                    self.flag = 1
                    self.enemy_loc.append((x, y))
                x, y = stack.pop()
                self.backtracking(x, y)

    # Draw the path and create dictionary of acceptable moves--------------------------------------------------------------

    def push_left(self, x, y):
        x, y = (x - self.wall, y)
        self.mazemap.append((x, y,
                             self.wall_cell, self.cell))
        self.andron.append((x, y))

    def push_right(self, x, y):
        self.mazemap.append((x, y,
                             self.wall_cell, self.cell))
        self.andron.append((x + self.cell, y))

    def push_up(self, x, y):
        x, y = (x, y - self.wall)
        self.mazemap.append((x, y,
                             self.cell, self.cell + self.wall))
        self.andron.append((x, y))

    def push_down(self, x, y):
        self.mazemap.append((x, y,
                             self.cell, self.cell + self.wall))
        self.andron.append((x, y + self.cell))

    def backtracking(self, x, y):
        self.mazemap.append((x, y,
                             self.cell, self.cell))
        self.deadend.append((x, y))
        self.andron.append((x, y))

    # End location---------------------------------------------------------------------------------------------------------

    def endLoc(self):
        count = 0
        final = 0
        longPath = []
        xs, ys = self.grid[0]

        for value in (self.deadend):
            x, y = value
            count = 0
            while (x, y) != (xs, ys):
                longPath.append((x, y))
                x, y = self.solution[x, y]
                count += 1
            if count > final:
                final = count
                self.farCell = longPath[0]
            else:
                longPath.clear()

    # Debugging-------------------------------------------------------------------------------------------------------------
    def renderAndron(self, surface):
        for value in self.andron:
            x, y = value
            pygame.draw.rect(self.PLAYER_SURF, c.BLACK,
                             pygame.Rect(x, y, 10, 10))
