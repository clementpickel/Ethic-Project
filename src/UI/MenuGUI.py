import tkinter as tk
from tkinter import ttk
from menum import GameState, TurnResult
from game_manager import GameManager
from human_bot import HumanPlayer
from training import TrainingManager
from learning_bot import LearningBot
from bot import StupidBot, StupidBot2
from gomoku import Gomoku
from UI.ui import TrainingGUI, HumanVsBotGUI, GomokuBotVsBotGUI

class MenuGUI:
    def __init__(self, root):
        self.root = root
        #self.root.geometry("400x350")

        # window size and setting to make the window appear at the center of the screen
        win_width  = 400
        win_height = 350

        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_offset = (screen_width  - win_width)  // 2
        y_offset = (screen_height - win_height) // 2

        self.root.geometry(f"{win_width}x{win_height}+{x_offset}+{y_offset}")

        # default mode
        self.selected_mode = "Human vs Bot"
        self.game_manager = GameManager()
        self.game_happening = False
        self.draw_menu()

    def draw_menu(self):
        # destroying previous menu_frame if exists
        if hasattr(self, 'menu_frame'):
            self.menu_frame.destroy()

        self.menu_frame = tk.Frame(self.root, width=320, height=200)
        self.menu_frame.pack(expand=True)
        self.menu_frame.pack_propagate(False)

        values = ["Stupid bot 1", "Stupid bot 2", "MinMax bot", "Learning Bot", "Heuristic bot"]
        values_mode = ["Human vs Bot", "Bot vs bot", "Train without GUI", "Train with GUI"]

        dropdown_mode = ttk.Combobox(self.menu_frame, state="readonly", values=values_mode)
        dropdown_mode.set(self.selected_mode)  # set the combobox text to the stored mode
        dropdown_mode.bind("<<ComboboxSelected>>", self.on_mode_selected)

        dropdown_selection_player_one = ttk.Combobox(self.menu_frame, state="readonly", values=values)
        dropdown_selection_player_one.current(0)

        dropdown_selection_player_two = ttk.Combobox(self.menu_frame, state="readonly", values=values)
        dropdown_selection_player_two.current(1)

        play_btn = tk.Button(self.menu_frame, text="play", command=lambda: self.start_game(dropdown_selection_player_one.get(), dropdown_selection_player_two.get(), dropdown_mode.get()))

        """
        if train without gui : don't show the bot choice
        if train with gui : don't show the bot choice
        if it's human vs bot : choose between all the bots for player 2
        if it's bot vs bot : choose between all the bots for both players
        """

        # handling which dropdowns are showed in function of the mode selected
        if self.game_happening:
            quit_btn = tk.Button(self.menu_frame, text="quit", command=self.root.destroy)
            quit_btn.place(x=60, y=140)
        else:
            tk.Label(self.menu_frame, text="Select mode").place(x=10, y=10)
            dropdown_mode.place(x=110, y=10)

            if dropdown_mode.get() == "Bot vs bot":
                tk.Label(self.menu_frame, text="Player one").place(x=10, y=50)
                tk.Label(self.menu_frame, text="Player two").place(x=10, y=90)
                dropdown_selection_player_one.place(x=110, y=50)
                dropdown_selection_player_two.place(x=110, y=90)

            elif dropdown_mode.get() == "Human vs Bot":
                tk.Label(self.menu_frame, text="Player two (bot)").place(x=10, y=90)
                dropdown_selection_player_two.place(x=110, y=90)

            play_btn.place(x=60, y=130)

    def on_mode_selected(self, event):
        self.selected_mode = event.widget.get()  # store whatever the user picked
        self.draw_menu()

    def start_game(self, bot1_name, bot2_name, mode_name):
        self.launch_game(bot1_name, bot2_name, mode_name)

    def launch_game(self, bot1_name, bot2_name, mode_name):
        self.game_happening = True
        self.draw_menu() #update menu
        print(f"bot1 : {bot1_name}, bot2 {bot2_name}")

        mode_dispatch = {
            "Train without GUI": self.launch_train_without_gui,
            "Train with GUI": self.launch_train_with_gui,
            "Human vs Bot": self.launch_human_vs_bot,
            "Bot vs bot": self.launch_bot_vs_bot
        }

        if mode_name in mode_dispatch:
            mode_dispatch[mode_name](bot1_name, bot2_name)
        else:
            print(f"{mode_name} does not exist")

    def launch_train_without_gui(self, bot1_name, bot2_name):
            print("Train without GUI")
            print("Starting headless training...")
            bot1 = LearningBot(GameState.PLAYER_1)
            bot2 = LearningBot(GameState.PLAYER_2)
            bot1.load_q_table("bot1_q.json")
            bot2.load_q_table("bot2_q.json")
            trainer = TrainingManager(bot1, bot2, num_games=5000)
            trainer.run_training_session()
            bot1.save_q_table("bot1_q.json")
            bot2.save_q_table("bot2_q.json")

    def launch_train_with_gui(self, bot1_name, bot2_name):
            print("Train with GUI")
            bot1 = StupidBot(GameState.PLAYER_1)
            bot2 = LearningBot(GameState.PLAYER_2)
            try:
                bot2.load_q_table("bot2_q.json")
                print("Loaded trained model for LearningBot.")
            except Exception as e:
                print("No trained model found; starting with untrained LearningBot.")
            game = Gomoku(bot1, bot2)
            game_window = tk.Toplevel(self.root)
            game_window.title("Gomoku Training Mode (GUI)")
            TrainingGUI(game_window, game, training_games=5000, delay=500)

    def launch_human_vs_bot(self, bot1_name, bot2_name):
            print("play human")

            # only defining bot2 as bot1 is the human
            _, bot2 = self.game_manager.define_bots("Dummy", bot2_name)

            try:
                bot2.load_q_table("bot2_q.json")
                print("Loaded trained model for LearningBot.")
            except Exception as e:
                print("No trained model found; using untrained LearningBot.")

            human = HumanPlayer(GameState.PLAYER_1)
            game = Gomoku(human, bot2)
            game_window = tk.Toplevel(self.root)
            game_window.title("Gomoku: Human vs. LearningBot")
            HumanVsBotGUI(game_window, game)

    def launch_bot_vs_bot(self, bot1_name, bot2_name):
            print("play bot mode")
            bot1, bot2 = self.game_manager.define_bots(bot1_name, bot2_name)
            try:
                bot2.load_q_table("bot2_q.json")
                print("Loaded trained model for LearningBot.")
            except Exception as e:
                print("No trained model found; using untrained LearningBot.")
            game = Gomoku(bot1, bot2)
            game_window = tk.Toplevel(self.root)
            game_window.title("Gomoku: Bot vs. Bot")
            GomokuBotVsBotGUI(game_window, game)
