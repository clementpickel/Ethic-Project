from menum import GameState

class Bot:
    def __init__(self, symbol: GameState, botType):
        self.player = symbol
        self.botType = botType
        self.opponent = GameState.PLAYER_1 if symbol == GameState.PLAYER_2 else GameState.PLAYER_2

    def play(self, board: list[list[str]]) -> tuple:
        raise NotImplementedError("This method should be overridden by subclasses")

class StupidBot(Bot):
    def __init__(self, symbol):
        super().__init__(symbol, "Stupid Bot")

    def play(self, board):
        # Returns the first empty cell (row-wise)
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell is None:
                    return i, j
