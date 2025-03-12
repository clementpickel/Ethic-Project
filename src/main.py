import tkinter as tk
import sys
from gomoku import Gomoku
from bot import StupidBot
# from minmax import MinMaxBot
from menum import GameState
from ui import GomokuBotVsBotGUI, TrainingGUI, HumanVsBotGUI, MenuGUI
from human_bot import HumanPlayer
from training import TrainingManager
from learning_bot import LearningBot
from heuribot_bot import HeuribotBot

def main():
    root = tk.Tk()
    root.title("Gomoku Game")
    # gui = GomokuGUI(root, game)
    gui = MenuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
