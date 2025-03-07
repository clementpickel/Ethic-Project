from menum import GameState
from gomoku import Gomoku
from bot import StupidBot, StupidBot2
from minmax import MinMaxBot

class GameManager:
    def __init__(self):
        self.game = None

    def define_bots(self, bot1_name, bot2_name):
        bot_map = {
            "Stupid bot 1": StupidBot,
            "Stupid bot 2": StupidBot2,
            "MinMax": MinMaxBot
        }

        bot1 = bot_map.get(bot1_name, StupidBot)(symbol=GameState.PLAYER_1)
        bot2 = bot_map.get(bot2_name, StupidBot)(symbol=GameState.PLAYER_2)

        return bot1, bot2

    def launch_game(self, bot1_name, bot2_name):
        print("Launching game with:", bot1_name, "and", bot2_name)

        bot1, bot2 = self.define_bots(bot1_name, bot2_name)
        self.game = Gomoku(bot1, bot2)
        return self.game
