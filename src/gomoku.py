from bot import Bot
from enum import Enum

class GameState(Enum):
    START = 1
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'
    FINISHED = 4

class TurnResult(Enum):
    VALID = 1
    INVALID = 2
    WIN = 3
    DRAW = 4

class Gomoku:
    def __init__(self, player_1: Bot, player_2: Bot, size=15):
        self.size = size
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.game_state = GameState.START

    def reset(self):
        """Reset the game to its initial state"""
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.game_state = GameState.START
        self.winner = None

    def get_valid_moves(self):
        """Return list of valid moves as (row, col) tuples"""
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] is None]

    def is_valid_move(self, row, col):
        """Check if a move is valid"""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] is None

    def make_move(self, row, col) -> TurnResult:
        """
        Make a move on the board
        Returns True if move was valid, False otherwise
        """
        if not self.is_valid_move(row, col):
            return TurnResult.INVALID

        # Place the stone
        self.board[row][col] = self.game_state.value

        # Check for win
        if self.check_win(row, col):
            return TurnResult.WIN
        elif self.is_draw():
            return TurnResult.DRAW
        
        return TurnResult.VALID

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
    
    def game_turn(self):
        if self.game_state == GameState.START:
            self.game_state = GameState.PLAYER_1

        elif self.game_state == GameState.PLAYER_1:
            row, col = self.player_1.play(self.board)
            res = self.make_move(row, col)
            if res == TurnResult.WIN or res == TurnResult.DRAW:
                self.game_state = GameState.FINISHED
                if res == TurnResult.WIN:
                    self.winner = GameState.PLAYER_1
            else:
                self.game_state = GameState.PLAYER_2

        elif self.game_state == GameState.PLAYER_2:
            row, col = self.player_2.play(self.board)
            res = self.make_move(row, col)
            if res == TurnResult.WIN or res == TurnResult.DRAW:
                self.game_state = GameState.FINISHED
                if res == TurnResult.WIN:
                    self.winner = GameState.PLAYER_2
            else:
                self.game_state = GameState.PLAYER_1

    def game_loop(self, number_of_moves=100):
        move_counter = 0
        while self.game_state != GameState.FINISHED and move_counter < number_of_moves:
            self.game_turn()
            move_counter += 1

    def print_board(self):
        """Print the current board state with row/col labels"""
        print('   ' + ' '.join(f"{c:2}" for c in range(self.size)))
        
        for r in range(self.size):
            print(f"{r:2} ", end='')
            print(' '.join(f"{' ' if cell is None else cell:2}" for cell in self.board[r]))
        print()
