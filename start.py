import pygame
import sys
from pygame.locals import *
import knossos.game
import gameover
import level_complete


def main():
    # INIT -------------------------------------------------------------------------------------------------------
    pygame.init()

    SETUP = "SETUP"
    PLAYING = "PLAYING"
    GAMESTATE = PLAYING

    move_left = False
    move_right = False
    move_up = False
    move_down = False
    vanish = False

    # towards dictates which way the sword will stike
    sword_strike = False
    towards = "down"

    PLAYER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(PLAYER_EVENT, 125)

    ENEMY_EVENT_PATROLLING = pygame.USEREVENT + 2
    pygame.time.set_timer(ENEMY_EVENT_PATROLLING, 500)

    ENEMY_EVENT_CHASING = pygame.USEREVENT + 3
    pygame.time.set_timer(ENEMY_EVENT_CHASING, 225)

    TIMER_EVENT = pygame.USEREVENT + 4
    pygame.time.set_timer(TIMER_EVENT, 2000)

    SWORD_EVENT = pygame.USEREVENT + 5
    pygame.time.set_timer(SWORD_EVENT, 500)

    ENEMY_SWORD_EVENT = pygame.USEREVENT + 6
    pygame.time.set_timer(ENEMY_SWORD_EVENT, 600)

    GAME = knossos.game.Game()
    # RUNGAME-----------------------------------------------------------------------------------------------------
    RUNNING = True
    while RUNNING:
        checkForQuit()
        for event in pygame.event.get():
            if GAMESTATE == SETUP:
                GAME = knossos.game.Game()
                GAMESTATE = PLAYING

            if GAMESTATE == PLAYING:
                if event.type == KEYDOWN:

                    # maze control--------------------
                    if event.key == K_RETURN:
                        GAME.PAUSED = not GAME.PAUSED
                    elif event.key == K_LSHIFT:
                        GAMESTATE = SETUP
                    elif event.key == K_RSHIFT:
                        GAME.restart_level()
                        GAMESTATE = SETUP
                    elif event.key == K_TAB:
                        GAME.list_scores()

                    # player control--------------------
                    elif event.key == K_SPACE:
                        sword_strike = True
                    elif event.key == K_a:
                        move_left = True
                    elif event.key == K_d:
                        move_right = True
                    elif event.key == K_w:
                        move_up = True
                    elif event.key == K_s:
                        move_down = True
                    elif event.key == K_r:
                        vanish = True
                    elif event.key == K_LEFT:
                        towards = "left"
                    elif event.key == K_RIGHT:
                        towards = "right"
                    elif event.key == K_UP:
                        towards = "up"
                    elif event.key == K_DOWN:
                        towards = "down"

                # Key up----------------------------------
                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        sword_strike = False
                    elif event.key == K_a:
                        move_left = False
                    elif event.key == K_d:
                        move_right = False
                    elif event.key == K_w:
                        move_up = False
                    elif event.key == K_s:
                        move_down = False
                    elif event.key == K_r:
                        vanish = False

                # game events -------------------------------
            if not GAME.PAUSED:
                if event.type == PLAYER_EVENT:
                    x, y = GAME.player.x, GAME.player.y
                    if sword_strike:
                        GAME.swords(towards)
                    if move_left:
                        towards = "left"
                        GAME.player_left()
                    if move_right:
                        towards = "right"
                        GAME.player_right()
                    if move_up:
                        towards = "up"
                        GAME.player_up()
                    if move_down:
                        towards = "down"
                        GAME.player_down()
                    GAME.enemy_follow_path(x, y)
                    GAME.player_facing(towards)
                    if vanish:
                        GAME.player_vanish()

                if event.type == ENEMY_EVENT_PATROLLING:
                    for enemy in GAME.enemy_list:
                        GAME.enemy_check_follow(enemy)
                        GAME.enemy_move_patrolling(enemy)

                if event.type == ENEMY_EVENT_CHASING:
                    for enemy in GAME.enemy_chasing_list:
                        GAME.enemy_move_chasing(enemy)
                        GAME.enemy_swords(enemy)

                if event.type == TIMER_EVENT:
                    if GAME.check_timer():
                        gameover.main()
                    else:
                        GAME.run_down_time()

                if event.type == SWORD_EVENT:
                    if GAME.check_sword_collision_patrol():
                        GAME.calc_score()
                    if GAME.check_sword_collision_chase():
                        GAME.calc_score()
                    GAME.check_sword_collision_player()
                    GAME.swords_done()

                if GAME.check_gameover():
                    gameover.main()
            GAME.display_score()

            if GAME.check_target_collision():
                GAME.next_level()
                level_complete.main()

        GAME.update_sprite_rect()
        GAME.update_screen()
# QUITGAME--------------------------------------------------------------------------------------------------------


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


if __name__ == '__main__':
    main()
