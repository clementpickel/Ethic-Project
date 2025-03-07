# human_bot.py
from bot import Bot
from menum import GameState

class HumanPlayer(Bot):
    def __init__(self, symbol):
        super().__init__(symbol, "Human Player")
        self.selected_move = None

    def play(self, board):
        # Return the selected move and then reset it to None.
        move = self.selected_move
        self.selected_move = None
        return move
