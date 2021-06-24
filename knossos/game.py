from knossos.player import Human, Target, Enemy, Sword, Enemy_Sword
from knossos.scoreboard import Level, Score, Highscore, Lives, Cooldown, Ability
from knossos.daedalus import daeda
from knossos.screen import Screen
from knossos.timer import Timer
from knossos.maze import Maze
import knossos.score_data as sd
from knossos.score_data import Levels
from knossos.color import colors as c
import random
import pygame
import pickle


class Game():
    def __init__(self):
        self.screen = Screen()
        # Maze resources---------------------------------
        self.color = random.choice(c.MEDITERRANEAN)
        self.set_maze()
        self.lvl, self.cells = Levels.levels[0]
        self.aMaze = daeda(self.cells)
        self.maze = self.aMaze.mazemap
        self.gate = self.aMaze.andron
        self.wall = self.aMaze.wall
        self.cell = self.aMaze.cell
        self.wall_cell = self.wall + self.cell
        self.solution = self.aMaze.solution
        x, y = self.aMaze.grid[0]
        self.maze_list = []
        self.gate_list = []

        # Scoreboard resources---------------------------------
        self.current_score = 0
        self.timer = Timer()
        self.level = Level(str(self.lvl))
        self.lives = Lives()
        self.cooldown = Cooldown()
        self.ability1 = Ability("Vanish ", 45, 45, 340, 7, 10)
        self.ability2 = Ability("Lightning", 45, 45, 395, 7, 10)
        self.score = Score("Score: " + str(self.current_score))
        self.highscore = Highscore()
        self.lives.lives = 20
        self.cooldown.energy = 20
        self.current_highscore = sd.score_dict[0]["highscore"]
        self.add_score()
        self.save()

        # Player resources----------------------------
        self.player = Human(x, y, self.cell, self.cell)
        self.sword_list = []

        # Target resources-----------------------------------
        fx, fy = self.aMaze.farCell
        self.target = Target(fx, fy, self.cell, self.cell)
        self.set_target_imagex()

       # Enemy resources------------------------
        self.enemy_list = []
        self.enemy_chasing_list = []
        self.enemy_dead = []
        self.enemy_sword_list = []
        self.following = {}
        self.delay = 1000
        self.chase_delay = 500


        self.PAUSED = False
        self.rooms()
        self.gates()
        self.enemies()

    # DATA----------------------------------------------------------------
    def display_score(self):
        self.score.text = "Score: " + str(self.current_score)

    def calc_score(self):
        self.current_score += 20 * (len(self.enemy_dead))
        self.calc_highscore()

    def calc_highscore(self):
        if self.current_score > self.current_highscore:
            self.current_highscore = self.current_score
        self.up_date_highscore()

    def end_round_score(self):
        self.current_score += (1000 + self.timer.width)
        self.up_date_highscore()

    def up_date_highscore(self):
        top_score = 0
        for i in range(self.lvl + 1):
            top_score = top_score + sd.score_dict[i]["score"]
        if top_score > self.current_highscore:
            self.current_highscore = top_score
        self.add_score()
        self.save()


    def save(self):
        f = open(sd.score_dir, "wb")
        pickle.dump(sd.score_dict, f)
        f.close()

    def add_score(self):
        sd.Score_Data(0, 000000, self.current_highscore)
        sd.Score_Data(self.lvl, self.current_score, self.current_highscore)


    # Swords-------------------------------------------------------------------------------
    def swords(self, toward):
        x, y = self.player.x, self.player.y
        #        |    wx / wy        |          x            |         y          |          width          |             hieght       |direction| ix | iy |
        sword = {(x - (self.wall), y): ((x - self.wall_cell),         y          ,(self.cell*2) + self.wall,           self.cell     ,"left"   , -70, -70 ,),
                 (x + (self.cell), y): (       x            ,         y          ,(self.cell*2) + self.wall,           self.cell     ,"right"  ,  0 , -70 ,),
                 (x, y - (self.wall)): (       x            ,(y - self.wall_cell),         self.cell       ,(self.cell*2) + self.wall,"up"     , -35, -100,),
                 (x, y + (self.cell)): (       x            ,         y          ,         self.cell       ,(self.cell*2) + self.wall,"down"   ,   0 ,-105,)}

        for key, value in sword.items():
            wx, wy, = key
            x, y, width, hieght, direction, ix, iy = value
            if direction == toward:
                self.sword = Sword(x, y, width, hieght, ix, iy)
                self.sword_list.append(self.sword)
    

    def swords_done(self):
        self.sword_list.clear()

    def enemy_swords_done(self):
        self.enemy_sword_list.clear()
        self.enemy_strike = False

    # Collisions---------------------------------------------------------
    # Because of the way enemies and swords are creacted it is easier to
    # check collision in three different methods

    def update_sprite_rect(self):
        self.player.RECT.x, self.player.RECT.y = self.player.x, self.player.y
        for sword in self.sword_list:
            sword.RECT.x, sword.RECT.y = sword.x, sword.y
        for sword in self.enemy_sword_list:
            sword.RECT.x, sword.RECT.y = sword.x, sword.y

    def check_sword_collision_patrol(self):
        for sword in self.sword_list:
            for enemy in self.enemy_list:
                if sword.RECT.colliderect(enemy.RECT):
                    self.enemy_dead.append(self.enemy_list.remove(enemy))
                    return True

    def check_sword_collision_chase(self):
        for sword in self.sword_list:
            for enemy in self.enemy_chasing_list:
                if sword.RECT.colliderect(enemy.RECT):
                    self.enemy_dead.append(self.enemy_chasing_list.remove(enemy))
                    return True

    def check_sword_collision_player(self):
        for sword in self.enemy_sword_list:
            if sword.RECT.colliderect(self.player.RECT):
                self.lives.lives -= 2
                return True

    def check_target_collision(self):
        return self.player.x == self.target.x and self.player.y == self.target.y

    # Spawn Enemies----------------------------------------------------------------
    # Makes an enemy at every dead end point in maze

    def enemies(self):
        for value in self.aMaze.enemy_loc:
            x, y = value
            self.enemy = Enemy(x, y, self.cell, self.cell)
            self.enemy_list.append(self.enemy)

    # Partrolling Enemies----------------------------------------------------------
    # Checks if enemy is in a position where the player has been before,
    # self.following is a dictionary of moves the lead to player

    def enemy_check_follow(self, enemy):
        if (enemy.x, enemy.y) in self.following.keys():
            enemy.moves.clear()
            self.enemy_list.remove(enemy)
            self.enemy_chasing_list.append(enemy)
        else:
            self.enemy_path_patrolling(enemy)

    # Partrolling enemies are given ten moves that starting from dead
    # end spawn location leading to first cell of maze
    # once the patrolling enemy reaches the end of those ten steps it
    # will walk back to the dead end by using enemy.move_back

    def enemy_patrolling(self, enemy):
        if len(enemy.move_back) == 0:
            x, y = enemy.x, enemy.y
            try:
                for i in range(10):
                    x, y = self.solution[x, y]
                    enemy.moves.append((x, y))
            except KeyError:
                print("ahhhhhhhhhhh")
        else:
            enemy.moves = list(reversed(enemy.move_back))
            self.enemy_path_patrolling(enemy)

    # Changes enemy x, y using  enemy.moves. Pops enemy_move into
    # move_back to create a patrolling back and forth motion.
    def enemy_path_patrolling(self, enemy):
        if len(enemy.moves) == 0:
            self.enemy_patrolling(enemy)
        else:
            self.stage_moves(enemy)


    def stage_moves(self, enemy):
        x, y = enemy.x, enemy.y
        x1, y1 = enemy.moves[0]
        if enemy.enemy_steps_left > 0:
            self.step_left(enemy)
        elif enemy.enemy_steps_right > 0:
            self.step_right(enemy)
        elif enemy.enemy_steps_up > 0:
            self.step_up(enemy)
        elif enemy.enemy_steps_down > 0:
            self.step_down(enemy)
        else:
            dx, dy = x1 - x, y1 - y
            if dx == -40:
                enemy.enemy_steps_left = 40/enemy.speed
            elif dx == 40:
                enemy.enemy_steps_right = 40/enemy.speed
            elif dy == -40:
                enemy.enemy_steps_up = 40/enemy.speed
            elif dy == 40:
                enemy.enemy_steps_down = 40/enemy.speed
            enemy.move_back.append(enemy.moves.pop(0))
            enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y
            self.enemy_path_patrolling(enemy)
    
    def step_left(self, enemy):
        enemy.x -= enemy.speed
        enemy.y = enemy.y
        enemy.ix, enemy.iy = enemy.enemy_facing_left[0]
        enemy.enemy_facing_left.append(enemy.enemy_facing_left.pop(0))
        enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y
        enemy.enemy_steps_left -= 1
   

    def step_right(self, enemy):
        enemy.x += enemy.speed
        enemy.y = enemy.y
        enemy.ix, enemy.iy = enemy.enemy_facing_right[0]
        enemy.enemy_facing_right.append(enemy.enemy_facing_right.pop(0))
        enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y
        enemy.enemy_steps_right -= 1


    def step_up(self, enemy):
        enemy.x = enemy.x
        enemy.y -= enemy.speed
        enemy.ix, enemy.iy = enemy.enemy_facing_up[0]
        enemy.enemy_facing_up.append(enemy.enemy_facing_up.pop(0))
        enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y
        enemy.enemy_steps_up -= 1


    def step_down(self, enemy):
        enemy.x = enemy.x
        enemy.y += enemy.speed
        enemy.ix, enemy.iy = enemy.enemy_facing_down[0]
        enemy.enemy_facing_down.append(enemy.enemy_facing_down.pop(0))
        enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y
        enemy.enemy_steps_down -= 1


    def enemy_move_chasing(self, enemy):
        x, y = enemy.x, enemy.y
        if (enemy.x, enemy.y) in self.following.keys():
            dx, dy = self.player.x - x, self.player.y -y
            x, y = self.following[enemy.x, enemy.y]
            if dx < -20 or dx > 20 or dy < -20 or dy > 20:
                enemy.x, enemy.y = x, y
            if enemy.stationary != (x, y):
                enemy.stationary = (x, y)
                self.following_animation(enemy, dx, dy)
            self.fighting_animation(enemy, dx, dy)
            enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y
        else:
            self.enemy_chasing_list.remove(enemy)
            
    def following_animation(self, enemy, dx, dy):
            if dx < 0:
                enemy.ix, enemy.iy = enemy.enemy_facing_left[0]
                enemy.enemy_facing_left.append(enemy.enemy_facing_left.pop(0))
            elif dx > 0:
                enemy.ix, enemy.iy = enemy.enemy_facing_right[0]
                enemy.enemy_facing_right.append(enemy.enemy_facing_right.pop(0))
            elif dy < 0:
                enemy.ix, enemy.iy = enemy.enemy_facing_up[0]
                enemy.enemy_facing_up.append(enemy.enemy_facing_up.pop(0))
            elif dy > 0:
                enemy.ix, enemy.iy = enemy.enemy_facing_down[0]
                enemy.enemy_facing_down.append(enemy.enemy_facing_down.pop(0))

    def fighting_animation(self, enemy, dx, dy):
        delay = random.random()
        if delay >= .5:
            #left
            if dx >= -20 and dx <= -10 and dy == 0:
                self.enemy_sword = Enemy_Sword(enemy.x - 35, enemy.y, (self.wall_cell*2), self.cell, -70, -70)
                self.enemy_sword_list.append(self.enemy_sword)
            #right
            if dx <= 20 and dx >= 10 and dy == 0:
                self.enemy_sword = Enemy_Sword(enemy.x, enemy.y, (self.wall_cell*2), self.cell, 0, -70)
                self.enemy_sword_list.append(self.enemy_sword)
            #up
            if dx == 0 and dy >= -20 and dy <= -10:
                self.enemy_sword = Enemy_Sword(enemy.x, enemy.y - 35, self.cell, (self.wall_cell*2), -35, -100)
                self.enemy_sword_list.append(self.enemy_sword)
            #down
            if dx == 0 and dy <= 20 and dy >= 10:
                self.enemy_sword = Enemy_Sword(enemy.x, enemy.y, self.cell, (self.wall_cell*2), 0, -105)
                self.enemy_sword_list.append(self.enemy_sword)

    def enemy_follow_path(self, x, y):
        self.following[(x, y)] = self.player.x, self.player.y

    # Player controls -------------------------------------------------------------
    # This transports player to random location and clears self.following
    # to stop enemies chasing

    def player_vanish(self):
        if self.cooldown.energy >= 6:
            self.player.x, self.player.y = random.choice(self.aMaze.grid)
            self.cooldown.energy -= 6
            self.cooldown.ready = pygame.time.get_ticks()
            self.following.clear()        

    def player_left(self):
        self.player.ix, self.player.iy = self.player.player_facing_left[0]
        for room in self.gate_list:
            if room.RECT.collidepoint((self.player.x+(self.player.width * .5)) - 1,
            self.player.y+(self.player.width * .5)):
                self.player.x -= self.player.speed
                self.player.y = self.player.y
        self.player.player_facing_left.append(self.player.player_facing_left.pop(0))
        self.swords_done()

    def player_right(self):
        self.player.ix, self.player.iy = self.player.player_facing_right[0]
        for room in self.gate_list:
            if room.RECT.collidepoint((self.player.x+(self.player.width * .5)) + 1,
            self.player.y+(self.player.width * .5)):
                self.player.x += self.player.speed
                self.player.y = self.player.y
        self.player.player_facing_right.append(self.player.player_facing_right.pop(0))
        self.swords_done()

    def player_up(self):
        self.player.ix, self.player.iy = self.player.player_facing_up[0]
        for room in self.gate_list:
            if room.RECT.collidepoint(self.player.x+(self.player.width * .5),
            (self.player.y+(self.player.width * .5)) - 1):
                self.player.x = self.player.x
                self.player.y -= self.player.speed
        self.player.player_facing_up.append(self.player.player_facing_up.pop(0))
        self.swords_done()


    def player_down(self):
        self.player.ix, self.player.iy = self.player.player_facing_down[0]
        for room in self.gate_list:
            if room.RECT.collidepoint(self.player.x+(self.player.width * .5),
            (self.player.y+(self.player.width * .5)) + 1):
                self.player.x = self.player.x
                self.player.y += self.player.speed
        self.player.player_facing_down.append(self.player.player_facing_down.pop(0))
        self.swords_done()

    def player_strike(self, towards):
        if towards == "left":
            self.player.ix, self.player.iy = -110, -70
            self.swords_done()
        if towards == "right":
            self.player.ix, self.player.iy = 0, -70
            self.swords_done()
        if towards == "up":
            self.player.ix, self.player.iy = -35, -140
            self.swords_done()
        if towards == "down":
            self.player.ix, self.player.iy = 0, -105
            self.swords_done()

    def player_default(self, towards):
        if towards == "left":
            self.player.ix, self.player.iy = -70, 0
            self.swords_done()
        if towards == "right":
            self.player.ix, self.player.iy = -35, 0
            self.swords_done()
        if towards == "up":
            self.player.ix, self.player.iy = -70, -35
            self.swords_done()
        if towards == "down":
            self.player.ix, self.player.iy = 0, -35
            self.swords_done()
    # Environment----------------------------------------------------------
    # Maze rooms---------------------------------------------------------------------------
    def rooms(self):
        for value in self.maze:
            x, y, width, height = value
            self.room = Maze(x, y, width, height, self.color)
            self.maze_list.append(self.room)

    def gates(self):
        for value in self.gate:
            x, y, width, height = value
            self.door = Maze(x, y, width, height, c.WHITE)
            self.gate_list.append(self.door)

    def move_maze(self):
        for room in self.maze_list:
            room.x += 1

    def set_target_imagex(self):
        x, y = self.target.x, self.target.y
        if (x, y - self.wall) in self.aMaze.andron:
            self.target.ix = -35
    # pops level at index 0 in levels and puts it at the end
    # of the list. this is how looping through levels

    def set_maze(self):
        Levels.levels.append(Levels.levels.pop(0))

    def restart_level(self):
        Levels.levels.insert(0, Levels.levels.pop(-1))

    def check_gameover(self):
        return self.lives.lives <= 0

    def run_down_time(self):
        self.timer.width -= 5

    def check_timer(self):
        if self.timer.width <= 0:
            return True

    def next_level(self):
        self.end_round_score()
        self.up_date_highscore()

    def is_cooldown_ready(self):
        cooldown = 4000
        if self.cooldown.energy < 20:
            now = pygame.time.get_ticks()
            return now - self.cooldown.ready >= cooldown
        else:
            return False

    def mp_cooldown(self):
        cooldown = 500
        if self.is_cooldown_ready():
            now = pygame.time.get_ticks()
            if now - self.cooldown.last >= cooldown:
                self.cooldown.energy += 1
                self.cooldown.last = pygame.time.get_ticks()

        else:
            self.ready = False
    def update_screen(self):
        self.screen.update_screen(self.gate_list, self.maze_list, self.player,
                                  self.target, self.sword_list, self.enemy_sword_list,
                                  self.level, self.score, self.lives, self.cooldown,
                                  self.ability1, self.ability2, self.timer, self.PAUSED,
                                  self.enemy_list, self.enemy_chasing_list)

