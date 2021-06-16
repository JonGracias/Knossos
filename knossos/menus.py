from knossos.game import Levels
from knossos.daedalus import daeda
from knossos.screen import Screen
from knossos.color import colors
from knossos.endgame import Lost, Won, Start
import knossos.score_data as sd
from knossos.score_data import Levels
import os
import pickle


class Menu():
    def __init__(self):
        self.gamestart()
        self.load()
        print(sd.score_dict.items())
        self.prepare_score_dict()
        self.save()
        self.screen = Screen()
        self.highscore = sd.score_dict[0]["highscore"]
        #           fontsize |  text |   x   |   y   |  width |  height  | fontx | fonty
        self.background = Start(75, "",
                         10,     35,      595,     595,      85,     65)
        self.welcome = Start(75, "WELCOME",
                         105,     50,      405,     80,      0,     0)
        self.to = Start(55, "T0",
                         255,     135,      95,     60,      10,     0)
        self.knossos = Start(75, "KNOSSOS",
                         105,     200,      405,     80,      10,     0)

        self.timetrial = Start(40, "Time Trial",
                          180,    320,     250,      70,      10,     10)
        self.adventure = Start(40, "Adventure",
                          180,    395,     250,      70,      10,     10)
        self.dark = Start(40, "Pitch Black",
                          180,    470,     250,      70,      10,     10)

        self.highscore = Start(40, "HighScore   " + str(self.highscore),
                          115,    555,     380,      70,      10,     10)

        self.color = colors.BLACK
        self.maze = daeda(20)
        self.time_button = self.timetrial.RECT
        self.adv_button = self.adventure.RECT
        self.dark_button = self.dark.RECT

    def menu_update_screen(self):
        self.screen.menu_update_screen(
            self.maze, self.color, self.welcome, self.to, self.knossos,
             self.timetrial, self.adventure, self.dark, self.highscore)

    # Reset level list
    def gamestart(self):
        Levels.levels = [(10, 40), (1, 15), (2, 15), (3, 15), (4, 25),
                         (5, 25), (6, 25), (7, 30), (8, 30), (9, 40)]

    def load(self):
        if os.path.exists(sd.score_dir):
            f = open(sd.score_dir, "rb")
            sd.score_dict = pickle.load(f)
        else:
            f = open(sd.score_dir, "wb")
            pickle.dump(sd.score_dict, f)
            f.close()

    def prepare_score_dict(self):
        rem_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        sd.score_dict = dict([(key, val) for key, val in 
            sd.score_dict.items() if key not in rem_list])

    def save(self):
        f = open(sd.score_dir, "wb")
        pickle.dump(sd.score_dict, f)
        f.close()



# Game Over Screen------------------------------------------------------
class GameOver():
    def __init__(self):
        self.screen = Screen()
        self.level = list(sd.score_dict.keys())[-1]
        self.highscore = sd.score_dict[0]["highscore"]
        self.current_score = sd.score_dict[self.level]["score"]
        #           fontsize |  text |   x   |   y   |  width |  height  | fontx | fonty
        self.lost = Lost(75, "GAMEOVER",
                         10,     35,      595,     595,      65,     65)
        self.highscore = Lost(40, "HighScore   " + str(self.highscore),
                              110,    210,     400,      70,      10,     10)
        self.score = Lost(40, "Score           " + str(self.current_score),
                          110,    280,     400,      70,      10,     10)

        self.retry = Lost(40, "Retry",
                              110,    435,     400,      70,      10,     10)
        self.main_menu = Lost(40, "Quit",
                          110,    505,     400,      70,      10,     10)
        self.color = colors.RED
        self.maze = daeda(20)

        self.retry_button = self.retry.RECT
        self.main_menu_button = self.main_menu.RECT

    def GameOver_update_screen(self):
        self.screen.gameover_update_screen(
            self.maze, self.color, self.lost, self.highscore, self.score, self.retry, self.main_menu)

    def set_retry(self):
        Levels.levels.insert(0, Levels.levels.pop(-1))



# Level Complete Screen------------------------------------------------------
class Win():
    def __init__(self):
        self.screen = Screen()
        self.level = list(sd.score_dict.keys())[-1]
        self.highscore = sd.score_dict[0]["highscore"]
        self.current_score = sd.score_dict[self.level]["score"]
        #           fontsize |  text |   x   |   y   |  width |  height  | fontx | fonty
        self.won = Won(75, "WINNER",
                       10,     35,      595,     595,      135,     65)
        self.highscore = Won(40, "HighScore   " + str(self.highscore),
                              110,    210,     400,      70,      10,     10)
        self.score = Won(40, "Score           " + str(self.current_score),
                          110,    280,     400,      70,      10,     10)

        self.next_level = Won(40, "Continue",
                              110,    365,     400,      70,      10,     10)
        self.retry = Won(40, "Retry",
                              110,    435,     400,      70,      10,     10)
        self.main_menu = Won(40, "Quit",
                          110,    505,     400,      70,      10,     10)
        self.color = colors.RED
        self.maze = daeda(20)

        self.continue_button = self.next_level.RECT
        self.retry_button = self.retry.RECT
        self.main_menu_button = self.main_menu.RECT

    def win_update_screen(self):
        self.screen.win_update_screen(
            self.maze, self.color, self.won, self.highscore, self.score, self.next_level, self.retry, self.main_menu)

    def set_retry(self):
        Levels.levels.insert(0, Levels.levels.pop(-1))