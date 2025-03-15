# ui.py
import tkinter as tk
from tkinter import ttk
from menum import GameState, TurnResult
from game_manager import GameManager
from human_bot import HumanPlayer
from training import TrainingManager
from learning_bot import LearningBot
from bot import StupidBot, StupidBot2
from gomoku import Gomoku
from move_evaluation import MoveEvaluation

CELL_SIZE = 40

class BaseGomokuGUI:
    """
    base class to not have redondant functions
    """
    whiteTurn= True
    def __init__(self, root, game: Gomoku, size=15, cell_size=CELL_SIZE, move_delay=500):
        self.root = root
        self.game: Gomoku = game
        self.size = size
        self.cell_size = cell_size
        self.move_delay = move_delay

        self.canvas = tk.Canvas(self.root,
                                width  = self.size * self.cell_size,
                                height = self.size * self.cell_size)
        self.canvas.pack()
        self.draw_board()
        self.update_board()
        self.schedule_next_move()

    def draw_board(self):
        for i in range(self.size):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.size * self.cell_size)
            self.canvas.create_line(0, i * self.cell_size, self.size * self.cell_size, i * self.cell_size)

    def update_board(self):
        self.canvas.delete("pieces")
        for row in range(self.size):
            for col in range(self.size):
                piece = self.game.board[row][col]
                if piece is not None:
                    x = col * self.cell_size + (self.cell_size // 2)
                    y = row * self.cell_size + (self.cell_size // 2)
                    color = "white" if piece == GameState.PLAYER_1 else "black"
                    self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color, tags="pieces")

    def schedule_next_move(self):
        self.root.after(self.move_delay, self.game_step)

    def game_step(self):
        if self.game.game_state != GameState.FINISHED:
            self.game.game_turn()
            self.update_board()
            self.schedule_next_move()
        else:
            self.on_game_over()

    def on_game_over(self):

        winner = self.game.winner
        winner_string = "Draw"

        if winner == GameState.PLAYER_1:
            winner = self.game.player_1.botType
            winner_string = "Player 1"
        elif winner == GameState.PLAYER_2:
            winner = self.game.player_2.botType
            winner_string = "Player 2"
        else:
            winner = "Draw"

        canvas_width = self.size * self.cell_size
        canvas_height = self.size * self.cell_size
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        bg_id = self.canvas.create_rectangle(
            center_x - 200, center_y - 50,
            center_x + 200, center_y + 50,
            fill="white", outline="black", width=3
        )

        text_id = self.canvas.create_text(
            center_x, center_y,
            text=f"GAME OVER!\n{winner_string} ({winner}) wins!",
            font=("Arial", 18, "bold"),
            fill="black",
            justify="center"
        )

        self.canvas.tag_raise(text_id, bg_id)

        # Add a button to restart
        restart_btn = tk.Button(
            self.canvas,
            text="Play Again",
            command=self.restart_game,
            font=("Arial", 14)
        )
        self.canvas.create_window(
            center_x, center_y + 80,
            window=restart_btn
        )

        self.game.move_evaluation.plot_score_history()

    def restart_game(self):
        """Optional method to reset the game"""
        self.game.reset()
        self.canvas.delete("all")
        self.draw_board()
        self.update_board()
        self.schedule_next_move()

class GomokuBotVsBotGUI(BaseGomokuGUI):
    """
    bot vs bot, inherits from BaseGomokuGUI.
    """
    def __init__(self, root, game, size=15):
        super().__init__(root, game, size=size, cell_size=CELL_SIZE, move_delay=500)
        # No additional setup required. No user clicks needed.

    # def on_game_over(self):
    #     if self.game.winner == GameState.PLAYER_1:
    #         print("Player 1 wins!")
    #     elif self.game.winner == GameState.PLAYER_2:
    #         print("Player 2 wins!")
    #     else:
    #         print("It's a draw!")

class TrainingGUI(BaseGomokuGUI):
    """training gui,  inherits from BaseGomokuGU"""
    def __init__(self, root, game, training_games=5000, delay=500, size=15, cell_size=CELL_SIZE):
        # Training-specific attributes
        self.training_games = training_games
        self.delay = delay
        self.games_played = 0
        self.stats = {"bot1": 0, "bot2": 0, "draw": 0}

        # Create an info label to show training progress
        self.info_label = tk.Label(root, text=f"Training Game: {self.games_played}/{self.training_games}")
        self.info_label.pack()

        # Initialize the BaseGomokuGUI which creates the canvas, draws the board,
        # and schedules the first move.
        super().__init__(root, game, size=size, cell_size=cell_size, move_delay=delay)

    def game_step(self):
        if self.game.game_state != GameState.FINISHED:
            self.game.game_turn()
            self.update_board()
            self.schedule_next_move()
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
                self.root.after(self.delay, self.game_step)
            else:
                learning_bot.save_q_table("bot2_q.json")
                print("Training complete. Model saved to 'bot2_q.json'.")
                print("Final Stats:", self.stats)
                self.info_label.config(text=f"Training complete. Stats:\nBot1 wins: {self.stats['bot1']} | Bot2 wins: {self.stats['bot2']} | Draws: {self.stats['draw']}")

class HumanVsBotGUI(BaseGomokuGUI):
    """
    human vs bot, inherits from BaseGomokuGUI.
    """
    def __init__(self, root, game, size=15):
        super().__init__(root, game, size=size, move_delay=500)
        # handle click
        self.canvas.bind("<Button-1>", self.on_click)
        self.info_label = tk.Label(root, text="Your turn (Human = Player 1)")
        self.info_label.pack()

    def on_click(self, event):
        if self.game.game_state == GameState.PLAYER_1:
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            if self.game.is_valid_move(row, col):
                self.game.player_1.selected_move = (row, col)

    # def on_game_over(self):
    #     if self.game.winner == GameState.PLAYER_1:
    #         self.info_label.config(text="Human wins")
    #     elif self.game.winner == GameState.PLAYER_2:
    #         self.info_label.config(text="Bot wins")
    #     else:
    #         self.info_label.config(text="Draw!")
