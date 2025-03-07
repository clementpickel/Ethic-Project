from tkinter import ttk
import tkinter as tk
from gameManager import GameManager
from menum import GameState

CELL_SIZE = 40

class GomokuGUI:
    def __init__(self, root, size=15):
        self.root = root
        self.size = size
        self.game_manager = GameManager()
        self.game_happening = False

        # side panel
        self.canvas = tk.Canvas(root, width=size * CELL_SIZE, height=size * CELL_SIZE)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.draw_menu()

    def draw_menu(self):
        if hasattr(self, 'menu_frame'):
            self.menu_frame.destroy()
        self.menu_frame = tk.Frame(self.root, width=200, height=200)
        self.menu_frame.pack(side="right", fill="both")
        self.menu_frame.pack_propagate(False)

        values = ["Stupid bot 1", "Stupid bot 2", "MinMax"]

        dropdown_selection_player_one = ttk.Combobox(self.menu_frame, state="readonly", values=values)
        dropdown_selection_player_one.current(0)

        dropdown_selection_player_two = ttk.Combobox(self.menu_frame, state="readonly", values=values)
        dropdown_selection_player_two.current(1)

        play_btn = tk.Button(self.menu_frame, text="play!", command=lambda: self.start_game(dropdown_selection_player_one.get(), dropdown_selection_player_two.get()))
        quit_btn = tk.Button(self.menu_frame, text="quit")

        if self.game_happening:
            quit_btn = tk.Button(self.menu_frame, text="quit", command=self.root.destroy)
            quit_btn.place(x=60, y=140)
        else:
            dropdown_selection_player_one.place(x=110, y=50)
            dropdown_selection_player_two.place(x=110, y=90)
            play_btn.place(x=60, y=130)
            tk.Label(self.menu_frame, text="Choose which bots to use").place(x=10, y=10)
            tk.Label(self.menu_frame, text="Player one").place(x=10, y=50)
            tk.Label(self.menu_frame, text="Player two").place(x=10, y=90)

    def start_game(self, bot1_name, bot2_name):
        self.game_happening = True
        self.game_manager.launch_game(bot1_name, bot2_name)
        self.draw_board()
        self.update_board()
        self.side_panel()
        self.draw_menu()
        self.root.after(500, self.play_game)

    def side_panel(self):
        """side panel config"""
        self.side_frame = tk.Frame(self.root)
        self.side_frame.pack(side="right", fill="y")

        self.player_one_label = tk.Label(self.side_frame, text="player one is playing in white")
        self.player_two_label = tk.Label(self.side_frame, text="player two is playing in black")
        self.player_one_label.pack(padx=10, pady=10)
        self.player_two_label.pack(padx=10, pady=10)

        self.current_player_label = tk.Label(self.side_frame, text="", fg="blue")
        self.current_player_label.pack(padx=10, pady=10)

    def draw_board(self):
        """Draws the initial board grid."""
        for i in range(self.size):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, self.size * CELL_SIZE)
            self.canvas.create_line(0, i * CELL_SIZE, self.size * CELL_SIZE, i * CELL_SIZE)

    def update_board(self):
        """Updates the board UI based on the current game state."""
        self.canvas.delete("pieces")  # Clear previous pieces
        for row in range(self.size):
            for col in range(self.size):
                piece = self.game_manager.game.board[row][col]
                if piece is not None:
                    x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2
                    color = "white" if piece == GameState.PLAYER_1.value else "black"
                    self.canvas.create_oval(
                        x - 15, y - 15, x + 15, y + 15,
                        fill=color, tags="pieces"
                    )

    def play_game(self):
        """Runs the game loop and updates the board after each move."""
        if not self.game_manager.game.winner:
            self.game_manager.game.game_loop(number_of_moves=1)  # Make one move
            self.update_board()
            self.root.after(500, self.play_game)
        else:
            if self.game_manager.game.winner.value == 'X':
                self.current_player_label.config(text="Winner is Player 1")
            else:
                self.current_player_label.config(text="Winner is Player 2")
