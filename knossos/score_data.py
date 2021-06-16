score_dict = {0: {"score": 0, "highscore": 0}}
score_dir = "score_dir.data"

class Score_Data():  
    def __init__(self, lvl = 1, score=00000, highscore=20):
        score_dict[lvl] = {"score": score, "highscore": highscore}

class Levels():
    levels = [(10, 15), (1, 15), (2, 15), (3, 15), (4, 15),
              (5, 15), (6, 15), (7, 15), (8, 15), (9, 15)]


