class Gomoku:
    def __init__(self, size=15):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'  # Player 'X' starts
        self.game_over = False
        self.winner = None

    def reset(self):
        """Reset the game to its initial state"""
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def get_valid_moves(self):
        """Return list of valid moves as (row, col) tuples"""
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] is None]

    def is_valid_move(self, row, col):
        """Check if a move is valid"""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] is None

    def make_move(self, row, col):
        """
        Make a move on the board
        Returns True if move was valid, False otherwise
        """
        if self.game_over or not self.is_valid_move(row, col):
            return False

        # Place the stone
        self.board[row][col] = self.current_player

        # Check for win
        if self.check_win(row, col):
            self.winner = self.current_player
            self.game_over = True
        elif self.is_draw():
            self.game_over = True
        else:
            # Switch players if game continues
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True

    def check_win(self, row, col):
        """Check if the last move resulted in a win"""
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, two diagonals

        for dr, dc in directions:
            count = 1
            # Check in positive direction
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            # Check in negative direction
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False

    def is_draw(self):
        """Check if the game is a draw"""
        return all(cell is not None for row in self.board for cell in row)

    def print_board(self):
        """Print the current board state with row/col labels"""
        # Column headers
        print('   ' + ' '.join(f"{c:2}" for c in range(self.size)))
        
        for r in range(self.size):
            # Row number with padding
            print(f"{r:2} ", end='')
            # Board cells
            print(' '.join(f"{' ' if cell is None else cell:2}" for cell in self.board[r]))
        print()

# Example usage:
if __name__ == "__main__":
    game = Gomoku()
    
    # Example game sequence
    moves = [(7,7), (7,8), (8,8), (8,7), (9,9), (9,8), (10,10)]
    
    for move in moves:
        if not game.game_over:
            row, col = move
            game.make_move(row, col)
            game.print_board()
    
    if game.winner:
        print(f"Player {game.winner} wins!")
    else:
        print("It's a draw!")