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
        # Set a fixed window size
        self.root.geometry("400x400")
        self.game_manager = GameManager()
        self.game_happening = False

        self.draw_menu()

    def draw_menu(self):
        # Destroy previous menu_frame if exists
        if hasattr(self, 'menu_frame'):
            self.menu_frame.destroy()

        self.menu_frame = tk.Frame(self.root, width=280, height=230)
        self.menu_frame.pack(expand=True)
        self.menu_frame.pack_propagate(False)

        values = ["Stupid bot 1", "Stupid bot 2", "MinMax bot", "Learning Bot", "You play"]
        values_mode = ["Human vs Bot", "Bot vs bot", "Train without GUI", "Train with GUI"]

        dropdown_mode= ttk.Combobox(self.menu_frame, state="readonly", values=values_mode)
        dropdown_mode.current(3)

        dropdown_selection_player_one = ttk.Combobox(self.menu_frame, state="readonly", values=values)
        dropdown_selection_player_one.current(0)

        dropdown_selection_player_two = ttk.Combobox(self.menu_frame, state="readonly", values=values)
        dropdown_selection_player_two.current(1)

        play_btn = tk.Button(self.menu_frame, text="play!", command=lambda: self.start_game(dropdown_selection_player_one.get(), dropdown_selection_player_two.get(), dropdown_mode.get()))
        quit_btn = tk.Button(self.menu_frame, text="quit")

        if self.game_happening:
            quit_btn = tk.Button(self.menu_frame, text="quit", command=self.root.destroy)
            quit_btn.place(x=60, y=140)
        else:
            # Labels
            tk.Label(self.menu_frame, text="Select mode").place(x=10, y=10)
            tk.Label(self.menu_frame, text="Player one").place(x=10, y=50)
            tk.Label(self.menu_frame, text="Player two").place(x=10, y=90)

            # Dropdowns and Button
            dropdown_mode.place(x=110, y=10)
            dropdown_selection_player_one.place(x=110, y=50)
            dropdown_selection_player_two.place(x=110, y=90)
            play_btn.place(x=60, y=130)

    def start_game(self, bot1_name, bot2_name, mode_name):
        self.game_happening = True
        self.launch_game(bot1_name, bot2_name, mode_name)
        #self.draw_board()
        #self.update_board()
        #self.side_panel()
        #self.draw_menu()
        #self.root.after(500, self.play_game)

    def launch_game(self, bot1_name, bot2_name, mode_name):
        values_mode = ["Human vs Bot", "Bot vs bot", "Train without GUI", "Train with GUI"]
        print(f"Launching {mode_name} game with: {bot1_name} and {bot2_name}")

        #bot1, bot2 = self.game_manager.define_bots(bot1_name, bot2_name)

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
        elif mode_name == "Human vs Bot":
            print("play human")
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
            HumanVsBotGUI(root, game)
            root.mainloop()
        else:  # play_bot mode (default)
            print("play bot mode")
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
            GomokuBotVsBotGUI(root, game)
            root.mainloop()

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
