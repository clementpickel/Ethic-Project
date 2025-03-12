from menum import GameState
from bot import StupidBot, StupidBot2
from minmax import MinMaxBot
from learning_bot import LearningBot
from human_bot import HumanPlayer
from heuribot_bot import HeuribotBot

class GameManager:
    def __init__(self):
        self.game = None

    def define_bots(self, bot1_name, bot2_name):
        bot_map = {
            "Stupid bot 1": StupidBot,
            "Stupid bot 2": StupidBot2,
            "MinMax bot": MinMaxBot,
            "Learning Bot": LearningBot,
            "Heuristic bot": HeuribotBot,
            "You play" : HumanPlayer
        }

        bot1 = bot_map.get(bot1_name, StupidBot)(symbol=GameState.PLAYER_1)
        bot2 = bot_map.get(bot2_name, StupidBot)(symbol=GameState.PLAYER_2)

        return bot1, bot2

        #self.game = Gomoku(bot1, bot2)
        #return self.game
