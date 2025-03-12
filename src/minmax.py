from bot import Bot


class MinMaxBot(Bot):
    def __init__(self, symbol, depth=2):
        super().__init__(symbol, "Min Max Bot")
        self.depth = depth  # Search depth (higher = stronger but slower)

    def play(self, board: list[list[str]]) -> tuple:
        # Get list of valid moves (empty cells adjacent to existing pieces)
        valid_moves = self._get_valid_moves(board)

        # MiniMax with Alpha-Beta pruning
        best_score = -float('inf')
        best_move = valid_moves[0]
        # print(best_move)

        for move in valid_moves:
            row, col = move
            board[row][col] = self.player
            score = self._minimax(board, self.depth, -
                                  float('inf'), float('inf'), False)
            board[row][col] = None  # Undo move

            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        # Check for terminal states
        if self._check_win(board, self.player):
            return 1000
        if self._check_win(board, self.opponent):
            return -1000
        if depth == 0:
            return self._evaluate(board)

        valid_moves = self._get_valid_moves(board)

        if is_maximizing:
            max_score = -float('inf')
            for move in valid_moves:
                row, col = move
                board[row][col] = self.player
                score = self._minimax(board, depth-1, alpha, beta, False)
                board[row][col] = None
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for move in valid_moves:
                row, col = move
                board[row][col] = self.opponent
                score = self._minimax(board, depth-1, alpha, beta, True)
                board[row][col] = None
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score

    def _evaluate(self, board):
        """Simple heuristic: count potential winning lines"""
        score = 0

        # Check all possible 5-length sequences
        for row in range(15):
            for col in range(15):
                # Horizontal
                if col <= 10:
                    window = [board[row][col+i] for i in range(5)]
                    score += self._score_window(window)
                # Vertical
                if row <= 10:
                    window = [board[row+i][col] for i in range(5)]
                    score += self._score_window(window)
                # Diagonal down-right
                if row <= 10 and col <= 10:
                    window = [board[row+i][col+i] for i in range(5)]
                    score += self._score_window(window)
                # Diagonal down-left
                if row <= 10 and col >= 4:
                    window = [board[row+i][col-i] for i in range(5)]
                    score += self._score_window(window)
        return score

    def _score_window(self, window):
        """Score a 5-cell window"""
        player_count = window.count(self.player)
        opponent_count = window.count(self.opponent)

        if opponent_count == 0:
            return player_count ** 2
        elif player_count == 0:
            return -opponent_count ** 2
        return 0  # Mixed window has no value

    def _get_valid_moves(self, board):
        """Get empty cells adjacent to existing pieces"""
        valid = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]

        for row in range(15):
            for col in range(15):
                if board[row][col] != None:
                    continue
                # Check adjacent cells
                for dr, dc in directions:
                    r, c = row+dr, col+dc
                    if 0 <= r < 15 and 0 <= c < 15 and board[r][c] != None:
                        valid.append((row, col))
                        break
        return valid if valid else [(7, 7)]  # Center if empty board

    def _check_win(self, board, symbol):
        """Check if specified symbol has won"""
        # Check all directions for 5 in a row
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(15):
            for col in range(15):
                if board[row][col] != symbol:
                    continue
                for dr, dc in directions:
                    if all(0 <= row+i*dr < 15 and 0 <= col+i*dc < 15 and
                           board[row+i*dr][col+i*dc] == symbol for i in range(5)):
                        return True
        return False
