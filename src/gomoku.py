# gomoku.py
import copy
from menum import GameState, TurnResult
from bot import Bot

class Gomoku:
    def __init__(self, player_1: Bot, player_2: Bot, size=15):
        self.size = size
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.game_state = GameState.START
        # print(f"Game begin. Player one is a {player_1.botType} and player 2 is a {player_2.botType}")

    def reset(self):
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.game_state = GameState.START
        self.winner = None

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] is None

    def make_move(self, row, col) -> TurnResult:
        if not self.is_valid_move(row, col):
            return TurnResult.INVALID
        # Place the stone based on whose turn it is.
        current_symbol = self.game_state.PLAYER_1 if self.game_state == GameState.PLAYER_1 else self.game_state.PLAYER_2
        self.board[row][col] = current_symbol
        if self.check_win(row, col):
            return TurnResult.WIN
        elif self.is_draw():
            return TurnResult.DRAW
        return TurnResult.VALID

    def check_win(self, row, col):
        player = self.board[row][col]
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False

    def is_draw(self):
        return all(cell is not None for row in self.board for cell in row)

    def game_turn(self):
        if self.game_state == GameState.START:
            self.game_state = GameState.PLAYER_1
        elif self.game_state == GameState.PLAYER_1:
            move = self.player_1.play(copy.deepcopy(self.board))
            if move is None:
                return  # For human player waiting for input
            row, col = move
            result = self.make_move(row, col)
            # print(f"Player 1 ({self.player_1.botType}) move {(row, col)} result: {result}")
            if result == TurnResult.WIN or result == TurnResult.DRAW:
                self.game_state = GameState.FINISHED
                if result == TurnResult.WIN:
                    self.winner = self.player_1.player
            else:
                self.game_state = GameState.PLAYER_2
        elif self.game_state == GameState.PLAYER_2:
            move = self.player_2.play(copy.deepcopy(self.board))
            if move is None:
                return
            row, col = move
            result = self.make_move(row, col)
            # print(f"Player 2 ({self.player_2.botType}) move {(row, col)} result: {result}")
            if result == TurnResult.WIN or result == TurnResult.DRAW:
                self.game_state = GameState.FINISHED
                if result == TurnResult.WIN:
                    self.winner = self.player_2.player
            else:
                self.game_state = GameState.PLAYER_1
