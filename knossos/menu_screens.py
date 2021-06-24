from knossos.game import Levels
from knossos.maze import Maze
from knossos.daedalus import daeda
from knossos.screen import Screen
from knossos.color import colors as c
from knossos.menu_objects import Gameover, Won, Start
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
        self.color = c.BLUE
        self.highscore = sd.score_dict[0]["highscore"]
        #           fontsize |  text |   x   |   y   |  width |  height  | fontx | fonty
        self.background = Start(75, "",
                         10,     5,      595,     595,      85,     65)
        self.welcome = Start(75, "WELCOME",
                         105,     20,      405,     80,      0,     0)
        self.to = Start(55, "T0",
                         255,     105,      95,     60,      10,     0)
        self.knossos = Start(75, "KNOSSOS",
                         105,     170,      405,     80,      10,     0)

        self.timetrial = Start(40, "Time Trial",
                          180,    290,     250,      70,      10,     10)
        self.adventure = Start(40, "Adventure",
                          180,    365,     250,      70,      10,     10)
        self.dark = Start(40, "Pitch Black",
                          180,    440,     250,      70,      10,     10)

        self.highscore = Start(40, "HighScore   " + str(self.highscore),
                          115,    525,     380,      70,      10,     10)

        self.aMaze = daeda(15)
        self.maze = self.aMaze.mazemap
        self.maze_list = []
        
        self.time_button = self.timetrial.RECT
        self.adv_button = self.adventure.RECT
        self.dark_button = self.dark.RECT

        self.rooms()

    def menu_update_screen(self):
        self.screen.menu_update_screen(
            self.maze_list, self.welcome, self.to, self.knossos,
             self.timetrial, self.adventure, self.dark, self.highscore)

    # Reset level list
    def gamestart(self):
        Levels.levels = [(10, 15), (1, 15), (2, 15), (3, 15), (4, 15),
                        (5, 15), (6, 15), (7, 15), (8, 15), (9, 15)]

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

    def rooms(self):
        for value in self.maze:
            x, y, width, height = value
            self.room = Maze(x, y, width, height, self.color)
            self.maze_list.append(self.room)

    def set_retry(self):
        Levels.levels.insert(0, Levels.levels.pop(-1))


# Game Over Screen------------------------------------------------------
class GameOver(Menu):
    def __init__(self):
        super().__init__()
        self.screen = Screen()
        self.level = list(sd.score_dict.keys())[-1]
        self.highscore = sd.score_dict[0]["highscore"]
        self.current_score = sd.score_dict[self.level]["score"]
        #           fontsize |  text |   x   |   y   |  width |  height  | fontx | fonty
        self.lost = Gameover(75, "GAMEOVER",
                        5,     5,      595,     595,      65,     65)
        self.highscore = Gameover(40, "HighScore   " + str(self.highscore),
                        110,    210,     400,      70,      10,     10)
        self.score = Gameover(40, "Score           " + str(self.current_score),
                        110,    280,     400,      70,      10,     10)
        self.retry = Gameover(40, "Retry",
                        110,    365,     400,      70,      10,     10)
        self.main_menu = Gameover(40, "Quit",
                        110,    435,     400,      70,      10,     10)
        self.color = c.RED
        self.aMaze = daeda(15)
        self.maze = self.aMaze.mazemap
        self.maze_list = []

        self.retry_button = self.retry.RECT
        self.main_menu_button = self.main_menu.RECT

        self.rooms()

    def GameOver_update_screen(self):
        self.screen.gameover_update_screen(
            self.maze_list, self.lost, self.highscore, self.score, self.retry, self.main_menu)

# Level Complete Screen------------------------------------------------------
class Win(Menu):
    def __init__(self):
        super().__init__()
        self.screen = Screen()
        self.level = list(sd.score_dict.keys())[-1]
        self.highscore = sd.score_dict[0]["highscore"]
        self.current_score = sd.score_dict[self.level]["score"]
        #           fontsize |  text |   x   |   y   |  width |  height  | fontx | fonty
        self.won = Won(75, "WINNER",
                        5,     5,      595,     595,      135,     65)
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
        self.color = c.GREEN
        self.aMaze = daeda(15)
        self.maze = self.aMaze.mazemap
        self.maze_list = []

        self.continue_button = self.next_level.RECT
        self.retry_button = self.retry.RECT
        self.main_menu_button = self.main_menu.RECT

        self.rooms()

    def win_update_screen(self):
        self.screen.win_update_screen(
            self.maze_list, self.won, self.highscore, self.score, self.next_level, self.retry, self.main_menu)

