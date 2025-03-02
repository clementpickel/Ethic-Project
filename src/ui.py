import tkinter as tk
from menum import GameState

CELL_SIZE = 40

class GomokuGUI:
    def __init__(self, root, game, size=15):
        self.root = root
        self.game = game
        self.size = size
        self.canvas = tk.Canvas(root, width=size * CELL_SIZE, height=size * CELL_SIZE)
        self.canvas.pack()
        self.draw_board()
        self.update_board()

        # Start game loop in the background
        self.root.after(500, self.play_game)

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
                piece = self.game.board[row][col]
                if piece is not None:
                    x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2
                    color = "white" if piece == GameState.PLAYER_1.value else "black"
                    self.canvas.create_oval(
                        x - 15, y - 15, x + 15, y + 15,
                        fill=color, tags="pieces"
                    )

    def play_game(self):
        """Runs the game loop and updates the board after each move."""
        if not self.game.winner:
            self.game.game_loop(number_of_moves=1)  # Make one move
            self.update_board()
            self.root.after(500, self.play_game)  # Schedule next move
        else:
            print("Winner:", self.game.winner.value)  # Print winner in terminal
