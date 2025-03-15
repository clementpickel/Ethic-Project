import matplotlib.pyplot as plt
from menum import GameState

class MoveEvaluation:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_score = 0
        self.player_1_score_history = []
        self.player_2_score = 0
        self.player_2_score_history = []
        self.directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def move_evaluation(self, player, board):
        if player == self.player_1:
            self.player_1_score = 0
        else:
            self.player_2_score = 0

        # all the patterns
        self.open_four(player, board)
        self.semi_open_four(player, board)
        self.open_three(player, board)
        self.semi_open_three(player, board)
        self.open_two(player, board)
        self.semi_open_two(player, board)

        # updating score
        self.add_score(player, 0)

    # four pieces, open on both sides
    def open_four(self, player, board):
        marker = GameState.PLAYER_1 if player == self.player_1 else GameState.PLAYER_2
        size = len(board)
        open_four_count = 0

        for x in range(size):
            for y in range(size):
                for dx, dy in self.directions:
                    if 0 <= y + 5 * dy < size and 0 <= x + 5 * dx < size:
                        if (board[x][y] is None and board[x + dx][y + dy] == marker and board[x + 2 * dx][y + 2 * dy] == marker and board[x + 3 * dx][y + 3 * dy] == marker and
                            board[x + 4 * dx][y + 4 * dy] == marker and board[x + 5 * dx][y + 5 * dy] is None):
                            open_four_count += 1
        score_from_open_four = open_four_count * 20 # biggest score as it's the best move
        if player == self.player_1:
            self.player_1_score += score_from_open_four
        else:
            self.player_2_score += score_from_open_four

    # four pieces, open on one of the sides
    def semi_open_four(self, player, board):
        marker = GameState.PLAYER_1 if player == self.player_1 else GameState.PLAYER_2
        size = len(board)
        semi_open_four_count = 0

        for x in range(size):
            for y in range(size):
                for dx, dy in self.directions:
                    if 0 <= x + 5 * dx < size and 0 <= y + 5 * dy < size:
                        if (board[x][y] is None and
                            board[x + dx][y + dy] == marker and board[x + 2 * dx][y + 2 * dy] == marker and board[x + 3 * dx][y + 3 * dy] == marker and
                            board[x + 4 * dx][y + 4 * dy] == marker and board[x + 5 * dx][y + 5 * dy] is not None):
                            semi_open_four_count += 1
                        elif (board[x][y] is not None and
                              board[x + dx][y + dy] == marker and
                              board[x + 2 * dx][y + 2 * dy] == marker and board[x + 3 * dx][y + 3 * dy] == marker
                              and board[x + 4 * dx][y + 4 * dy] == marker and board[x + 5 * dx][y + 5 * dy] is None):
                            semi_open_four_count += 1
        score_from_semi_open_four = semi_open_four_count * 15 # second best score
        if player == self.player_1:
            self.player_1_score += score_from_semi_open_four
        else:
            self.player_2_score += score_from_semi_open_four

    # three pieces, open on both sides
    def open_three(self, player, board):
        marker = GameState.PLAYER_1 if player == self.player_1 else GameState.PLAYER_2
        size = len(board)
        open_three_count = 0

        for x in range(size):
            for y in range(size):
                for dx, dy in self.directions:
                    if 0 <= x + 4 * dx < size and 0 <= y + 4 * dy < size:
                        if (board[x][y] is None and
                            board[x + dx][y + dy] == marker and board[x + 2 * dx][y + 2 * dy] == marker and
                            board[x + 3 * dx][y + 3 * dy] == marker and board[x + 4 * dx][y + 4 * dy] is None):
                            open_three_count += 1
        score_from_open_three = open_three_count * 10 # third
        if player == self.player_1:
            self.player_1_score += score_from_open_three
        else:
            self.player_2_score += score_from_open_three

    # three pieces, open on one of the sides
    def semi_open_three(self, player, board):
        marker = GameState.PLAYER_1 if player == self.player_1 else GameState.PLAYER_2
        size = len(board)
        semi_open_three_count = 0

        for x in range(size):
            for y in range(size):
                for dx, dy in self.directions:
                    if 0 <= x + 4 * dx < size and 0 <= y + 4 * dy < size:
                        if (board[x][y] is None and
                            board[x + dx][y + dy] == marker and board[x + 2 * dx][y + 2 * dy] == marker and board[x + 3 * dx][y + 3 * dy] == marker and
                            board[x + 4 * dx][y + 4 * dy] is not None):
                            semi_open_three_count += 1
                        elif (board[x][y] is not None and
                              board[x + dx][y + dy] == marker and board[x + 2 * dx][y + 2 * dy] == marker and
                              board[x + 3 * dx][y + 3 * dy] == marker and board[x + 4 * dx][y + 4 * dy] is None):
                            semi_open_three_count += 1
        score_from_semi_open_three = semi_open_three_count * 5 # fourth
        if player == self.player_1:
            self.player_1_score += score_from_semi_open_three
        else:
            self.player_2_score += score_from_semi_open_three

    # two pieces, open on both sides
    def open_two(self, player, board):
        marker = GameState.PLAYER_1 if player == self.player_1 else GameState.PLAYER_2
        size = len(board)
        open_two_count = 0

        for x in range(size):
            for y in range(size):
                for dx, dy in self.directions:
                    if 0 <= x + 3 * dx < size and 0 <= y + 3 * dy < size:
                        if (board[x][y] is None and
                            board[x + dx][y + dy] == marker and
                            board[x + 2 * dx][y + 2 * dy] == marker and board[x + 3 * dx][y + 3 * dy] is None):
                            open_two_count += 1
        score_from_open_two = open_two_count * 2 # 5
        if player == self.player_1:
            self.player_1_score += score_from_open_two
        else:
            self.player_2_score += score_from_open_two

    # two pieces, open on one of the sides
    def semi_open_two(self, player, board):
        marker = GameState.PLAYER_1 if player == self.player_1 else GameState.PLAYER_2
        size = len(board)
        semi_open_two_count = 0

        for x in range(size):
            for y in range(size):
                for dx, dy in self.directions:
                    if 0 <= x + 3 * dx < size and 0 <= y + 3 * dy < size:
                        if (board[x][y] is None and
                            board[x + dx][y + dy] == marker and board[x + 2 * dx][y + 2 * dy] == marker and board[x + 3 * dx][y + 3 * dy] is not None):
                            semi_open_two_count += 1
                        elif (board[x][y] is not None and
                              board[x + dx][y + dy] == marker and board[x + 2 * dx][y + 2 * dy] == marker and board[x + 3 * dx][y + 3 * dy] is None):
                            semi_open_two_count += 1
        score_from_semi_open_two = semi_open_two_count * 1 # 6
        if player == self.player_1:
            self.player_1_score += score_from_semi_open_two
        else:
            self.player_2_score += score_from_semi_open_two

    def add_score(self, player, score):
        if player == self.player_1:
            self.player_1_score_history.append(self.player_1_score)
            print("Player 1 score is ", self.player_1_score)
        else:
            self.player_2_score_history.append(self.player_2_score)
            print("Player 2 score is ", self.player_2_score)

    def plot_score_history(self):

        plt.figure(figsize=(8, 6))
        moves_player1 = list(range(1, len(self.player_1_score_history) + 1))
        moves_player2 = list(range(1, len(self.player_2_score_history) + 1))

        plt.plot(moves_player1, self.player_1_score_history, label='Player 1', marker='o')
        plt.plot(moves_player2, self.player_2_score_history, label='Player 2', marker='o')

        plt.xlabel('move number')
        plt.ylabel('score')
        plt.title('creativity score or "threat score", per move')
        plt.legend()
        plt.grid(True)
        plt.show()
