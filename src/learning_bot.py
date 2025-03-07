# learning_bot.py
from bot import Bot
import random
import json

class LearningBot(Bot):
    def __init__(self, symbol, exploration_rate=0.3, learning_rate=0.1):
        super().__init__(symbol, "Learning Bot")
        self.q_table = {}
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.last_state = None
        self.last_action = None

    def _get_valid_moves(self, board):
        valid = []
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for row in range(15):
            for col in range(15):
                if board[row][col] is None:
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        if 0 <= r < 15 and 0 <= c < 15 and board[r][c] is not None:
                            valid.append((row, col))
                            break
        return valid if valid else [(7, 7)]

    def play(self, board):
        state = hash(tuple(tuple(row) for row in board))
        valid_moves = self._get_valid_moves(board)
        if random.random() < self.exploration_rate:
            action = random.choice(valid_moves)
        else:
            q_values = [self.q_table.get((state, move), 0) for move in valid_moves]
            max_q = max(q_values)
            action = valid_moves[q_values.index(max_q)]
        self.last_state = state
        self.last_action = action
        return action

    def learn(self, reward):
        if self.last_state is not None and self.last_action is not None:
            old_value = self.q_table.get((self.last_state, self.last_action), 0)
            self.q_table[(self.last_state, self.last_action)] = old_value + self.learning_rate * (reward - old_value)

    def save_q_table(self, filename):
        with open(filename, 'w') as f:
            json.dump({str(k): v for k, v in self.q_table.items()}, f)

    def load_q_table(self, filename):
        try:
            with open(filename) as f:
                self.q_table = {eval(k): v for k, v in json.load(f).items()}
        except FileNotFoundError:
            pass
