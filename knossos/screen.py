import pygame
from pygame.locals import *
from knossos.color import colors as c


class Screen():
    def __init__(self, width=615, height=667, background_color=c.MNAVY,
                 font_type="freesansbold.ttf", font_size=20, clock_tick=60):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('KNOSSOS')
        self.maze_screen = pygame.Surface((605, 605), pygame.SRCALPHA)
        self.font = pygame.font.Font(font_type, font_size)
        self.clock = pygame.time.Clock()
        self.clock_tick = clock_tick

    def refresh_background(self):
        self.screen.fill(self.background_color)
    
    def draw_maze(self, rooms):
        for room in rooms:
            room.draw_rooms(self.maze_screen)

    def draw_swords(self, swords):
        for sword in swords:
            sword.draw_sprite(self.maze_screen)

    def draw_enemies(self, enemies):
        for enemy in enemies:
            enemy.draw_sprite(self.maze_screen)

    def draw_player(self, player):
        player.draw_sprite(self.maze_screen)

    def refresh_maze_screen(self):
        self.screen.blit(self.maze_screen, (5, 30))
        self.maze_screen.fill(c.BLACK)


    def draw_level(self, level):
        pygame.draw.rect(self.screen, c.SILVER, [5, 0, 605, 28])
        level.draw(self.screen)

    def draw_score(self, score):
        score.draw(self.screen)

    def draw_lives(self, lives):
        lives.draw(self.screen)
        lives.draw_lives(self.screen)

    def draw_timer(self, timer):
        timer.draw(self.screen)

    def draw_paused(self, pause):
        if pause == True:
            PAUSED_SURF = self.font.render("Paused", True, c.PURPLE)
            s = pygame.Surface((595, 595), pygame.SRCALPHA)
            s.fill(c.PAUSED)
            self.screen.blit(s, (10, 35))
            self.screen.blit(PAUSED_SURF, [267, 320])

    def update_screen(self, maze, player, target, swords, enemy_swords,
                      level, score, lives, timer, pause, enemies, chasing_enemies):
        self.refresh_background()
        self.draw_maze(maze)
        self.draw_enemies(enemies)
        self.draw_enemies(chasing_enemies)
        self.draw_player(player)
        self.draw_swords(swords)
        self.draw_swords(enemy_swords)
        self.draw_player(target)
        self.refresh_maze_screen()
        self.draw_level(level)
        self.draw_score(score)
        self.draw_lives(lives)
        self.draw_timer(timer)
        self.draw_paused(pause)
        self.clock.tick(self.clock_tick)
        pygame.display.update()

    # Start Menu--------------------------------------------------------
    def draw_start_screen(self, start):
        start.draw(self.screen)

    def menu_update_screen(self, maze, color, welcome, to, knossos,
             timetrial, adventure, dark, highscore):
        self.refresh_background()
        maze.renderGrid(self.screen, color)
        self.draw_gameover(welcome)
        self.draw_gameover(to)
        self.draw_gameover(knossos)
        self.draw_gameover(timetrial)
        self.draw_gameover(adventure)
        self.draw_gameover(dark)
        self.draw_gameover(highscore)
        pygame.display.update()

    # Gameover screen----------------------------------------------------
    def draw_gameover(self, lost):
        lost.draw(self.screen)

    def gameover_update_screen(self, maze, color, lost, highscore, score, retry, quit):
        self.refresh_background()
        maze.renderGrid(self.screen, color)
        self.draw_gameover(lost)
        self.draw_gameover(highscore)
        self.draw_gameover(score)
        self.draw_gameover(retry)
        self.draw_gameover(quit)
        self.clock.tick(self.clock_tick)
        pygame.display.update()

    # Level win screen-----------------------------------------------------------
    def draw_winner(self, won):
        won.draw(self.screen)

    def win_update_screen(self, maze, color, won, highscore, score, next_level, retry, quit):
        self.refresh_background()
        maze.renderGrid(self.screen, color)
        self.draw_winner(won)
        self.draw_winner(highscore)
        self.draw_winner(score)
        self.draw_winner(next_level)
        self.draw_winner(retry)
        self.draw_winner(quit)
        self.clock.tick(self.clock_tick)
        pygame.display.update()
