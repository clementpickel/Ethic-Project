import tkinter as tk
import sys
from gomoku import Gomoku
from bot import StupidBot
# from minmax import MinMaxBot
from menum import GameState
from ui import GomokuGUI, TrainingGUI, HumanGUI
from human_bot import HumanPlayer
from training import TrainingManager
from learning_bot import LearningBot


def main():
    mode = "play_bot"  # default GUI bot-vs-bot play
    if len(sys.argv) > 1:
        if sys.argv[1] == "train":
            mode = "train"       # headless training
        elif sys.argv[1] == "train_gui":
            mode = "train_gui"   # training with GUI
        elif sys.argv[1] == "play_human":
            mode = "play_human"  # human vs. LearningBot in GUI
        elif sys.argv[1] == "play_bot":
            mode = "play_bot"    # bot vs. bot GUI play

    if mode == "train":
        print("Starting headless training...")
        bot1 = LearningBot(GameState.PLAYER_1)
        bot2 = LearningBot(GameState.PLAYER_2)
        bot1.load_q_table("bot1_q.json")
        bot2.load_q_table("bot2_q.json")
        trainer = TrainingManager(bot1, bot2, num_games=5000)
        trainer.run_training_session()
        bot1.save_q_table("bot1_q.json")
        bot2.save_q_table("bot2_q.json")
    elif mode == "train_gui":
        # GUI training: show each game with delay and running stats.
        bot1 = StupidBot(GameState.PLAYER_1)
        bot2 = LearningBot(GameState.PLAYER_2)
        try:
            bot2.load_q_table("bot2_q.json")
            print("Loaded trained model for LearningBot.")
        except Exception as e:
            print("No trained model found; starting with untrained LearningBot.")
        game = Gomoku(bot1, bot2)
        root = tk.Tk()
        root.title("Gomoku Training Mode (GUI)")
        TrainingGUI(root, game, training_games=5000, delay=500)
        root.mainloop()
    elif mode == "play_human":
        # Human vs. LearningBot GUI play. Human is Player 1.
        human = HumanPlayer(GameState.PLAYER_1)
        bot = LearningBot(GameState.PLAYER_2)
        try:
            bot.load_q_table("bot2_q.json")
            print("Loaded trained model for LearningBot.")
        except Exception as e:
            print("No trained model found; using untrained LearningBot.")
        game = Gomoku(human, bot)
        root = tk.Tk()
        root.title("Gomoku: Human vs. LearningBot")
        HumanGUI(root, game)
        root.mainloop()
    else:  # play_bot mode (default)
        bot1 = StupidBot(GameState.PLAYER_1)
        bot2 = LearningBot(GameState.PLAYER_2)
        try:
            bot2.load_q_table("bot2_q.json")
            print("Loaded trained model for LearningBot.")
        except Exception as e:
            print("No trained model found; using untrained LearningBot.")
        game = Gomoku(bot1, bot2)
        root = tk.Tk()
        root.title("Gomoku: Bot vs. Bot")
        GomokuGUI(root, game)
        root.mainloop()

if __name__ == "__main__":
    main()
