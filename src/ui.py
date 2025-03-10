# ui.py
import tkinter as tk
from tkinter import ttk
from menum import GameState, TurnResult
from game_manager import GameManager
from menum import GameState
from human_bot import HumanPlayer
from training import TrainingManager
from learning_bot import LearningBot
from bot import StupidBot, StupidBot2
from gomoku import Gomoku

CELL_SIZE = 40

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
        self.selected_mode = "Train with GUI"
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
        quit_btn = tk.Button(self.menu_frame, text="quit")

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
        self.game_happening = True
        self.launch_game(bot1_name, bot2_name, mode_name)

    def launch_game(self, bot1_name, bot2_name, mode_name):
        print(f"bot1 : {bot1_name}, bot2 {bot2_name}")
        values_mode = ["Human vs Bot", "Bot vs bot", "Train without GUI", "Train with GUI"]

        if mode_name == "Train without GUI":
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

        elif mode_name == "Train with GUI":
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

        elif mode_name == "Human vs Bot":
            print(f"Launching {mode_name} game with: human and {bot2_name}")
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

        else:  # Bot vs bot. #TODO: Need to implement heuristic handling bot here !
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

#TODO: better classes. some function are redundant

class GomokuBotVsBotGUI:
    """GUI for a single game (bot vs. bot)."""
    def __init__(self, root, game, size=15):
        self.root = root
        self.game = game
        self.size = size
        self.canvas = tk.Canvas(root, width=size * CELL_SIZE, height=size * CELL_SIZE)
        self.canvas.pack()
        self.draw_board()
        self.update_board()
        self.root.after(500, self.play_game)

    def draw_board(self):
        for i in range(self.size):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, self.size * CELL_SIZE)
            self.canvas.create_line(0, i * CELL_SIZE, self.size * CELL_SIZE, i * CELL_SIZE)

    def update_board(self):
        self.canvas.delete("pieces")
        for row in range(self.size):
            for col in range(self.size):
                piece = self.game.board[row][col]
                if piece is not None:
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    color = "white" if piece == GameState.PLAYER_1 else "black"
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, tags="pieces")

    def play_game(self):
        if self.game.game_state != GameState.FINISHED:
            self.game.game_turn()
            self.update_board()
            self.root.after(500, self.play_game)
        else:
            if self.game.winner == GameState.PLAYER_1:
                print("Player 1 wins!")
            elif self.game.winner == GameState.PLAYER_2:
                print("Player 2 wins!")
            else:
                print("Draw!")

class TrainingGUI:
    """GUI training: plays each game with delay, resets, and shows running stats."""
    def __init__(self, root, game, training_games=5000, delay=500):
        self.root = root
        self.game = game
        self.training_games = training_games
        self.delay = delay
        self.games_played = 0
        self.stats = {"bot1": 0, "bot2": 0, "draw": 0}
        self.canvas = tk.Canvas(root, width=game.size * CELL_SIZE, height=game.size * CELL_SIZE)
        self.canvas.pack()
        self.draw_board()
        self.update_board()
        self.info_label = tk.Label(root, text=f"Training Game: {self.games_played}/{self.training_games}")
        self.info_label.pack()
        self.root.after(self.delay, self.training_step)

    def draw_board(self):
        for i in range(self.game.size):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, self.game.size * CELL_SIZE)
            self.canvas.create_line(0, i * CELL_SIZE, self.game.size * CELL_SIZE, i * CELL_SIZE)

    def update_board(self):
        self.canvas.delete("pieces")
        for row in range(self.game.size):
            for col in range(self.game.size):
                piece = self.game.board[row][col]
                if piece is not None:
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    color = "white" if piece == GameState.PLAYER_1 else "black"
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, tags="pieces")

    def training_step(self):
        if self.game.game_state != GameState.FINISHED:
            self.game.game_turn()
            self.update_board()
            self.root.after(self.delay, self.training_step)
        else:
            # Update stats based on outcome.
            if self.game.winner == self.game.player_1:
                self.stats["bot1"] += 1
            elif self.game.winner == self.game.player_2:
                self.stats["bot2"] += 1
            else:
                self.stats["draw"] += 1

            # Let LearningBot learn (assumed to be player 2)
            learning_bot = self.game.player_2
            reward = 1 if self.game.winner == learning_bot.player else (-1 if self.game.winner else 0)
            learning_bot.learn(reward)

            self.games_played += 1
            self.info_label.config(text=f"Training Game: {self.games_played}/{self.training_games}")
            print(f"Game {self.games_played} finished. Reward: {reward}")
            self.game.reset()
            if self.games_played < self.training_games:
                self.root.after(self.delay, self.training_step)
            else:
                learning_bot.save_q_table("bot2_q.json")
                print("Training complete. Model saved to 'bot2_q.json'.")
                print("Final Stats:", self.stats)
                self.info_label.config(text=f"Training complete. Stats:\nBot1 wins: {self.stats['bot1']} | Bot2 wins: {self.stats['bot2']} | Draws: {self.stats['draw']}")

class HumanVsBotGUI:
    """GUI for human vs. LearningBot. Human is Player 1."""
    def __init__(self, root, game, size=15):
        self.root = root
        self.game = game
        self.size = size
        self.canvas = tk.Canvas(root, width=size * CELL_SIZE, height=size * CELL_SIZE)
        self.canvas.pack()
        self.draw_board()
        self.update_board()
        # Bind mouse click to board click handler.
        self.canvas.bind("<Button-1>", self.on_click)
        self.info_label = tk.Label(root, text="Your turn (Human is Player 1)")
        self.info_label.pack()
        self.root.after(500, self.play_game)

    def draw_board(self):
        for i in range(self.size):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, self.size * CELL_SIZE)
            self.canvas.create_line(0, i * CELL_SIZE, self.size * CELL_SIZE, i * CELL_SIZE)

    def update_board(self):
        self.canvas.delete("pieces")
        for row in range(self.size):
            for col in range(self.size):
                piece = self.game.board[row][col]
                if piece is not None:
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    color = "white" if piece == GameState.PLAYER_1 else "black"
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, tags="pieces")

    def on_click(self, event):
        # Only process click if it is HumanPlayer's turn.
        if self.game.game_state == GameState.PLAYER_1:
            col = event.x // CELL_SIZE
            row = event.y // CELL_SIZE
            if self.game.is_valid_move(row, col):
                # Set the human player's move.
                self.game.player_1.selected_move = (row, col)
        # For other turns, ignore clicks.

    def play_game(self):
        if self.game.game_state != GameState.FINISHED:
            # For Human turn, wait if no move has been selected.
            if self.game.game_state == GameState.PLAYER_1:
                if self.game.player_1.selected_move is None:
                    self.root.after(100, self.play_game)
                    return
            self.game.game_turn()
            self.update_board()
            self.root.after(500, self.play_game)
        else:
            if self.game.winner == GameState.PLAYER_1:
                self.info_label.config(text="Human wins!")
            elif self.game.winner == GameState.PLAYER_2:
                self.info_label.config(text="LearningBot wins!")
            else:
                self.info_label.config(text="Draw!")
