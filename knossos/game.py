from knossos.player import Human, Target, Enemy, Sword, Enemy_Sword
from knossos.scoreboard import Level, Score, HighScore, Lives
from knossos.daedalus import daeda
from knossos.screen import Screen
from knossos.timer import Timer
from knossos.maze import Maze
import knossos.score_data as sd
from knossos.score_data import Levels
import random
import pickle


class Game():
    def __init__(self):
        self.screen = Screen()

        # Maze resources---------------------------------
        
        self.set_maze()
        self.lvl, self.cells = Levels.levels[0]
        self.aMaze = daeda(self.cells)
        self.maze = self.aMaze.mazemap
        self.wall = self.aMaze.wall
        self.cell = self.aMaze.cell
        x, y = self.aMaze.grid[0]
        self.maze_list = []

        # Scoreboard resources---------------------------------
        self.timer = Timer()
        self.level = Level()
        self.score = Score()
        self.lives = Lives()
        self.highscore = HighScore()
        self.lives.lives = 20
        self.current_score = 0
        self.current_highscore = sd.score_dict[0]["highscore"]
        self.add_score()
        self.save()

        # Player/target resources----------------------------
        self.player = Human(x, y, self.cell, self.cell)
        tx, ty = self.aMaze.farCell
        self.solution = self.aMaze.solution
        self.target = Target(tx, ty, self.cell, self.cell)
        self.set_target_imagex()
        self.sword_list = []
        self.wall_cell = self.wall + self.cell
        self.pose = True
        self.player_strike = False
        self.player_facing_left = [(-70, 0), (-105, 0)]

       # Enemy resources------------------------
        self.enemy_list = []
        self.enemy_sword_list = []
        self.enemy_chasing_list = []
        self.enemy_dead = []
        self.following = {}
        self.patroling_enemy = 1000
        self.delay = self.patroling_enemy
        self.chasing_enemy = 500
        self.chase_delay = self.chasing_enemy
        self.moves = []
        self.move_back = []
        self.enemy_strike = False

        self.PAUSED = False
        self.rooms()
        self.enemies()
        self.display_level()
    # DATA----------------------------------------------------------------
         

    def display_level(self):
        self.level.text = "Level: " + str(self.lvl)

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

    # Maze rooms---------------------------------------------------------------------------
    def rooms(self):
        for value in self.maze:
            x, y, width, height = value
            self.room = Maze(x, y, width, height)
            self.maze_list.append(self.room)

    def move_maze(self):
        for room in self.maze_list:
            room.x += 1

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
                self.player_strike = True


    def enemy_swords(self, enemy):
        x, y = enemy.x, enemy.y
        #        |                  dx / dy                  | ix |  iy |        wx      |        wy      |          x          |           y         |           width            |              hieght          |
        sword = {(x - (self.wall_cell), y)                   :(-70, -70 , (x - self.wall),  y             , (x - self.wall_cell),  y                  , ((self.cell*2) + self.wall),  self.cell)                 ,
                 (x + (self.wall_cell), y)                   :( 0 , -70 , (x + self.cell),  y             ,  x                  ,  y                  , ((self.cell*2) + self.wall),  self.cell)                 ,
                 (x,                    y - (self.wall_cell)):(-35, -100,  x             , (y - self.wall),  x                  , (y - self.wall_cell),   self.cell                , ((self.cell*2) + self.wall)),
                 (x,                    y + (self.wall_cell)):( 0 , -105,  x             , (y + self.cell),  x                  ,  y                  ,   self.cell                , ((self.cell*2) + self.wall))}

        for key, value in sword.items():
            dx, dy, = key
            ix, iy, wx, wy, x, y, width, hieght = value
            if (dx, dy) == (self.player.x, self.player.y) and (wx, wy) in self.aMaze.andron:
                self.enemy_sword = Enemy_Sword(x, y, width, hieght, ix, iy)
                self.enemy_sword_list.append(self.enemy_sword)
                self.enemy_strike = True

    # Clears swords list to stop rendering Sword

    def swords_done(self):
        self.sword_list.clear()
        self.player_strike = False
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
                if sword.RECT.contains(enemy.RECT):
                    self.enemy_dead.append(self.enemy_list.remove(enemy))
                    return True

    def check_sword_collision_chase(self):
        for sword in self.sword_list:
            for enemy in self.enemy_chasing_list:
                if sword.RECT.contains(enemy.RECT):
                    self.enemy_dead.append(self.enemy_chasing_list.remove(enemy))
                    return True

    def check_sword_collision_player(self):
        for sword in self.enemy_sword_list:
            if sword.RECT.contains(self.player.RECT):
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
            #self.enemy_list.append(self.enemy)

    # Partrolling Enemies----------------------------------------------------------
    # Checks if enemy is in a position where the player has been before,
    # self.following is a dictionary of moves the lead to player

    def enemy_check_follow(self, enemy):
        if (enemy.x, enemy.y) in self.following.keys():
            self.enemy_list.remove(enemy)
            self.enemy_chasing_list.append(enemy)

    # Partrolling enemies are given ten moves that starting from dead
    # end spawn location leading to first cell of maze
    # once the patrolling enemy reaches the end of those ten steps it
    # will walk back to the dead end by using enemy.move_back

    def enemy_moves(self, enemy):
        if len(enemy.move_back) == 0:
            x, y = enemy.x, enemy.y
            enemy.moves.append((x, y))
            try:
                for i in range(10):
                    x, y = self.solution[x, y]
                    enemy.moves.append((x, y))
            except KeyError:
                pass
        else:
            enemy.moves = list(reversed(enemy.move_back))

    # Changes enemy x, y using  enemy.moves. Pops enemy_move into
    # move_back to create a patrolling back and forth motion.

    def enemy_move_patrolling(self, enemy):

        x, y = enemy.x, enemy.y
        if len(enemy.moves) == 0:
            self.enemy_moves(enemy)
        else:
            enemy.x, enemy.y = enemy.moves[0]
            enemy.move_back.append(enemy.moves.pop(0))
            self.enemy_focus(x, y, enemy)
            enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y


    def enemy_move_chasing(self, enemy):
        x, y = enemy.x, enemy.y
        x1, y1 = enemy.x, enemy.y
        if (enemy.x, enemy.y) in self.following.keys():
            x, y = self.following[enemy.x, enemy.y]
            if (x, y) != (self.player.x, self.player.y):
                enemy.x, enemy.y = x, y
                enemy.move_back.append((enemy.x, enemy.y))
                self.enemy_focus(x1, y1, enemy)
                enemy.RECT.x, enemy.RECT.y = enemy.x, enemy.y

        else:
            self.enemy_chasing_list.remove(enemy)
            self.enemy_list.append(enemy)

    def enemy_focus(self, x, y, enemy):
        left = (x - self.wall_cell, y)
        right = (x + self.wall_cell, y)
        up = (x, y - self.wall_cell)
        down = (x, y + self.wall_cell)

        if left == (enemy.x, enemy.y) or left == (self.player.x, self.player.y):
            self.enemy_facing("left", enemy)
        elif right == (enemy.x, enemy.y) or right == (self.player.x, self.player.y):
            self.enemy_facing("right", enemy)
        elif up == (enemy.x, enemy.y) or up == (self.player.x, self.player.y):
            self.enemy_facing("up", enemy)
        elif down == (enemy.x, enemy.y) or down == (self.player.x, self.player.y):
            self.enemy_facing("down", enemy)

    def enemy_facing(self, towards, enemy):
        facing = {"left": [(-70, 0), (-105, 0)],
                  "right": [(0, 0),  (-35, 0)],
                  "up": [(-70, -35),  (-105, -35)],
                  "down": [(0, -35),  (-35, -35)],
                  "attack_left": [(-110,-70,)],
                  "attack_right": [(0,-70)],
                  "attack_up": [(-35,-140)],
                  "attack_down": [(0,-105)]}

        if not self.enemy_strike:
            if towards == "left":
                enemy.ix, enemy.iy = facing["left"][enemy.enemy_pose[0]]
            elif towards == "right":
                enemy.ix, enemy.iy = facing["right"][enemy.enemy_pose[0]]
            elif towards == "up":
                enemy.ix, enemy.iy = facing["up"][enemy.enemy_pose[0]]
            elif towards == "down":
                enemy.ix, enemy.iy = facing["down"][enemy.enemy_pose[0]]

        if self.enemy_strike:
            if towards == "left":
                enemy.ix, enemy.iy = facing["attack_left"][0]
            elif towards == "left":
                enemy.ix, enemy.iy = facing["attack_right"][0]
            elif towards == "up":
                enemy.ix, enemy.iy = facing["attack_up"][0]
            elif towards == "down":
                enemy.ix, enemy.iy = facing["attack_down"][0]

        enemy.enemy_pose.append(enemy.enemy_pose.pop(0))

    def enemy_follow_path(self, x, y):
        self.following[(x, y)] = self.player.x, self.player.y

    # Player controls -------------------------------------------------------------
    # This transports player to random location and clears self.following
    # to stop enemies chasing

    def player_vanish(self):
        self.player.x, self.player.y = random.choice(self.aMaze.grid)
        self.following.clear()

    def player_facing(self, towards):
        if self.pose:
            l = 0
        else:
            l = 1
        facing = {"left": [(-70, 0), (-105, 0)],
                  "right": [(0, 0),  (-35, 0)],
                  "up": [(-70, -35),  (-105, -35)],
                  "down": [(0, -35),  (-35, -35)],
                  "attack_left": [(-110,-70,)],
                  "attack_right": [(0,-70)],
                  "attack_up": [(-35,-140)],
                  "attack_down": [(0,-105)]}


        if towards == "left":
            self.player.ix, self.player.iy = facing["left"][l]
        if towards == "right":
            self.player.ix, self.player.iy = facing["right"][l]
        if towards == "up":
            self.player.ix, self.player.iy = facing["up"][l]
        if towards == "down":
            self.player.ix, self.player.iy = facing["down"][l]
        
        if self.player_strike:
            if towards == "left":
                self.player.ix, self.player.iy = facing["attack_left"][0]
            if towards == "right":
                self.player.ix, self.player.iy = facing["attack_right"][0]
            if towards == "up":
                self.player.ix, self.player.iy = facing["attack_up"][0]
            if towards == "down":
                self.player.ix, self.player.iy = facing["attack_down"][0]

    def player_left(self):
        for room in self.maze_list:
            if room.RECT.collidepoint(self.player.x - 5, self.player.y):
                self.player.x -= 5
                self.player.y = self.player.y
        self.player.ix, self.player.iy = self.player_facing_left[0]
        self.player_facing_left.append(self.player_facing_left.pop(0))
        
    def player_right(self):
        if (self.player.x + self.cell, self.player.y) in self.aMaze.andron:
            self.player.x = self.player.x + (self.wall_cell)
            self.player.y = self.player.y
            self.pose = not self.pose

    def player_up(self):
        if (self.player.x, self.player.y - self.wall) in self.aMaze.andron:
            self.player.x = self.player.x
            self.player.y = self.player.y - (self.wall_cell)
            self.pose = not self.pose

    def player_down(self):
        if (self.player.x, self.player.y + self.cell) in self.aMaze.andron:
            self.player.x = self.player.x
            self.player.y = self.player.y + (self.wall_cell)
            self.pose = not self.pose

    # Environment----------------------------------------------------------
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

    def update_screen(self):
        self.screen.update_screen(self.maze_list, self.player,
                                  self.target, self.sword_list, self.enemy_sword_list,
                                  self.level, self.score, self.lives, self.timer, self.PAUSED,
                                  self.enemy_list, self.enemy_chasing_list)

