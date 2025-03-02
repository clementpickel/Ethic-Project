from menum import GameState


class Bot:
    def __init__(self, symbol: GameState, botType):
        self.player = symbol
        # type of bot (minmax, stupid, neural network, regression)
        self.botType = botType
        self.opponent = GameState.PLAYER_1 if symbol == GameState.PLAYER_2 else GameState.PLAYER_2
        pass

    # take the board as input and return the move as a tuple
    def play(self, board: list[list[str]]) -> tuple:
        pass


class StupidBot(Bot):
    def __init__(self, symbol):
        super().__init__(symbol, "Stupid Bot")

    def play(self, board: list[list[str]]) -> tuple:
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell is None:
                    return i, j


class StupidBot2(Bot):
    def __init__(self, symbol):
        super().__init__(symbol, "Stupid Bot")

    def play(self, board: list[list[str]]) -> tuple:
        for i, row in reversed(list(enumerate(board))):
            for j, cell in reversed(list(enumerate(row))):
                if cell is None:
                    return i, j
