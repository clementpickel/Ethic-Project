import tkinter as tk
from gomoku import Gomoku
from bot import StupidBot, StupidBot2
from minmax import MinMaxBot
from menum import GameState
from ui import GomokuGUI

# Define board size

# Main program
if __name__ == "__main__":
    bot1 = StupidBot(symbol=GameState.PLAYER_1)
    bot2 = StupidBot2(symbol=GameState.PLAYER_2)
    game = Gomoku(bot1, bot2)

    root = tk.Tk()
    root.title("Gomoku Game")
    gui = GomokuGUI(root, game)
    root.mainloop()
