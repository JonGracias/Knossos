import pygame
from knossos.color import colors as c
from random import choice


class daeda():
    def __init__(self, num):
        self.cellNum = num
        self.wall = 5
        self.cell = 35
        self.map_size = 605
        self.wall_cell = self.wall + self.cell

        self.grid = []
        self.solution = {}
        self.mazemap = []
        self.deadend = []
        self.enemy_loc = []
        self.farCell = []
        self.andron = [(5+(self.cell * .5),  5+(self.cell * .5), 1, 1)]
        self.flag = 0

        self.create_grid()
        self.daedalus()
        self.endLoc()

    # Grid---------------------------------------------------------
    def create_grid(self):
        for i in range(self.cellNum):
            x = (self.cell * i) + (self.wall * i) + 5
            for j in range(self.cellNum):
                y = (self.cell * j) + (self.wall * j) + 5
                self.grid.append((x, y))

    # Carve the maze-----------------------------------------------------------------------------------------------------
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
        self.mazemap.append((x, y, self.wall_cell, self.cell))
        self.andron.append(((x+(self.cell * .5))-self.cell, y+(self.cell * .5), self.wall_cell, 1))

    def push_right(self, x, y):
        self.mazemap.append((x, y, self.wall_cell, self.cell))
        self.andron.append((x+(self.cell * .5), y+(self.cell * .5), self.wall_cell, 1))

    def push_up(self, x, y):
        x, y = (x, y - self.wall)
        self.mazemap.append((x, y, self.cell, self.cell + self.wall))
        self.andron.append((x+(self.cell * .5), (y+(self.cell * .5))-self.cell, 1, self.wall_cell))

    def push_down(self, x, y):
        self.mazemap.append((x, y, self.cell, self.cell + self.wall))
        self.andron.append((x+(self.cell * .5), y+(self.cell * .5), 1, self.wall_cell))

    def backtracking(self, x, y):
        self.mazemap.append((x, y, self.cell, self.cell))
        self.deadend.append((x, y))
        self.andron.append((x+(self.cell * .5), y+(self.cell * .5), 1, 1))

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
